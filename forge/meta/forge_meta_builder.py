#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
AUTOMATION_DIR = ROOT / "forge" / "automation"
RUNTIME_ATLAS_DIR = ROOT / "runtime" / "atlas"
RUNTIME_META_DIR = ROOT / "runtime" / "meta"


@dataclass(frozen=True)
class ModuleSpec:
    module_id: int
    slug: str
    title: str
    status: str

    @property
    def module_code(self) -> str:
        return f"FORGE-KNOWLEDGE-{self.module_id:03d}"

    @property
    def script_name(self) -> str:
        return f"forge_knowledge_{self.module_id:03d}_atlas_{self.slug}_engine.py"


def load_catalog(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"CATALOG_NOT_FOUND: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"CATALOG_INVALID_JSON: {exc}") from exc

    required = {"family", "template", "modules"}
    missing = required - data.keys()
    if missing:
        raise SystemExit(f"CATALOG_MISSING_FIELDS: {sorted(missing)}")

    if not isinstance(data["modules"], list) or not data["modules"]:
        raise SystemExit("CATALOG_MODULES_EMPTY")

    return data


def parse_modules(data: dict[str, Any]) -> list[ModuleSpec]:
    modules: list[ModuleSpec] = []
    seen_ids: set[int] = set()
    seen_slugs: set[str] = set()

    for raw in data["modules"]:
        spec = ModuleSpec(
            module_id=int(raw["id"]),
            slug=str(raw["slug"]).strip(),
            title=str(raw["title"]).strip(),
            status=str(raw["status"]).strip(),
        )

        if spec.module_id in seen_ids:
            raise SystemExit(f"DUPLICATE_MODULE_ID: {spec.module_id}")
        if spec.slug in seen_slugs:
            raise SystemExit(f"DUPLICATE_MODULE_SLUG: {spec.slug}")
        if not spec.slug.replace("_", "").isalnum():
            raise SystemExit(f"INVALID_MODULE_SLUG: {spec.slug}")

        seen_ids.add(spec.module_id)
        seen_slugs.add(spec.slug)
        modules.append(spec)

    modules.sort(key=lambda item: item.module_id)

    for previous, current in zip(modules, modules[1:]):
        if current.module_id != previous.module_id + 1:
            raise SystemExit(
                f"NON_CONTIGUOUS_IDS: {previous.module_id} -> {current.module_id}"
            )

    return modules


def replace_template(
    template_text: str,
    template_id: int,
    template_slug: str,
    template_title: str,
    template_status: str,
    spec: ModuleSpec,
) -> str:
    replacements = [
        (
            f"FORGE-KNOWLEDGE-{template_id:03d}",
            spec.module_code,
        ),
        (
            template_status,
            spec.status,
        ),
        (
            template_title,
            spec.title,
        ),
        (
            template_title.lower(),
            spec.title.lower(),
        ),
        (
            template_slug,
            spec.slug,
        ),
        (
            f"_{template_id:03d}",
            f"_{spec.module_id:03d}",
        ),
    ]

    text = template_text
    for old, new in replacements:
        text = text.replace(old, new)

    return text


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(command: list[str]) -> None:
    process = subprocess.run(command, cwd=ROOT, text=True)
    if process.returncode != 0:
        raise SystemExit(
            f"COMMAND_FAILED[{process.returncode}]: {' '.join(command)}"
        )


def build_family(
    catalog_path: Path,
    dry_run: bool,
    execute: bool,
    overwrite: bool,
) -> dict[str, Any]:
    data = load_catalog(catalog_path)
    modules = parse_modules(data)

    template = data["template"]
    template_id = int(template["id"])
    template_slug = str(template["slug"])
    template_title = str(template["title"])
    template_status = str(template["status"])

    template_path = AUTOMATION_DIR / str(template["script"])
    if not template_path.is_file():
        raise SystemExit(f"TEMPLATE_NOT_FOUND: {template_path}")

    template_text = template_path.read_text(encoding="utf-8")
    generated_scripts: list[str] = []
    executed_modules: list[str] = []

    for spec in modules:
        destination = AUTOMATION_DIR / spec.script_name

        if destination.exists() and not overwrite:
            raise SystemExit(f"DESTINATION_EXISTS: {destination}")

        rendered = replace_template(
            template_text=template_text,
            template_id=template_id,
            template_slug=template_slug,
            template_title=template_title,
            template_status=template_status,
            spec=spec,
        )

        expected_tokens = [
            spec.module_code,
            spec.status,
            spec.slug,
            f"_{spec.module_id:03d}",
        ]
        missing_tokens = [token for token in expected_tokens if token not in rendered]
        if missing_tokens:
            raise SystemExit(
                f"RENDER_VALIDATION_FAILED[{spec.module_code}]: {missing_tokens}"
            )

        generated_scripts.append(str(destination.relative_to(ROOT)))

        if not dry_run:
            destination.write_text(rendered, encoding="utf-8")
            destination.chmod(0o755)

            if execute:
                run_command(["python3", str(destination.relative_to(ROOT))])

                expected_artifacts = [
                    RUNTIME_ATLAS_DIR / f"{spec.slug}_{spec.module_id:03d}.json",
                    RUNTIME_ATLAS_DIR / f"{spec.slug}_{spec.module_id:03d}_hash.json",
                    RUNTIME_ATLAS_DIR / f"{spec.slug}_{spec.module_id:03d}_ledger.jsonl",
                ]

                missing_artifacts = [
                    str(path.relative_to(ROOT))
                    for path in expected_artifacts
                    if not path.is_file()
                ]
                if missing_artifacts:
                    raise SystemExit(
                        f"ARTIFACT_VALIDATION_FAILED[{spec.module_code}]: "
                        f"{missing_artifacts}"
                    )

                executed_modules.append(spec.module_code)

    result = {
        "builder": "FORGE_META_BUILDER",
        "status": "FORGE_META_BUILDER_VALIDATION_READY"
        if dry_run
        else "FORGE_META_BUILDER_EXECUTION_READY",
        "family": data["family"],
        "catalog": str(catalog_path.relative_to(ROOT)),
        "template": str(template_path.relative_to(ROOT)),
        "module_count": len(modules),
        "first_module": modules[0].module_code,
        "last_module": modules[-1].module_code,
        "generated_scripts": generated_scripts,
        "executed_modules": executed_modules,
        "dry_run": dry_run,
        "execute": execute,
        "runtime_mode": "SHADOW_ONLY_READ_ONLY",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["hash"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    return result


def write_report(result: dict[str, Any]) -> None:
    RUNTIME_META_DIR.mkdir(parents=True, exist_ok=True)

    report_path = RUNTIME_META_DIR / "forge_meta_builder_report.json"
    hash_path = RUNTIME_META_DIR / "forge_meta_builder_report_hash.json"
    ledger_path = RUNTIME_META_DIR / "forge_meta_builder_ledger.jsonl"

    report_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    hash_path.write_text(
        json.dumps(
            {
                "artifact": str(report_path.relative_to(ROOT)),
                "sha256": sha256_file(report_path),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    with ledger_path.open("a", encoding="utf-8") as ledger:
        ledger.write(json.dumps(result, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera familias completas de motores Atlas."
    )
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    catalog_path = args.catalog
    if not catalog_path.is_absolute():
        catalog_path = ROOT / catalog_path

    result = build_family(
        catalog_path=catalog_path,
        dry_run=args.dry_run,
        execute=args.execute,
        overwrite=args.overwrite,
    )
    write_report(result)

    print("FORGE-META-BUILDER-001")
    print(result["status"])
    print(f"family = {result['family']}")
    print(f"module_count = {result['module_count']}")
    print(f"range = {result['first_module']}..{result['last_module']}")
    print(f"hash = {result['hash']}")
    print(f"runtime_mode = {result['runtime_mode']}")


if __name__ == "__main__":
    main()
