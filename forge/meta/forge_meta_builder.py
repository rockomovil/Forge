#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
AUTOMATION = ROOT / "forge" / "automation"
RUNTIME = ROOT / "runtime" / "atlas"
RUNTIME_META = ROOT / "runtime" / "meta"
TEMPLATES = ROOT / "forge" / "meta" / "templates"


@dataclass(frozen=True)
class Module:
    module_id: int
    slug: str
    title: str
    status: str

    @property
    def module_code(self) -> str:
        return f"FORGE-KNOWLEDGE-{self.module_id:03d}"

    @property
    def script_path(self) -> Path:
        return AUTOMATION / (
            f"forge_knowledge_{self.module_id:03d}_atlas_"
            f"{self.slug}_engine.py"
        )

    @property
    def runtime_paths(self) -> tuple[Path, Path, Path]:
        base = RUNTIME / f"{self.slug}_{self.module_id:03d}"
        return (
            base.with_suffix(".json"),
            RUNTIME / f"{self.slug}_{self.module_id:03d}_hash.json",
            RUNTIME / f"{self.slug}_{self.module_id:03d}_ledger.jsonl",
        )


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"FILE_NOT_FOUND: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"INVALID_JSON[{path}]: {exc}") from exc


def load_catalog(path: Path) -> tuple[dict[str, Any], list[Module]]:
    catalog = load_json(path)

    if "family" not in catalog or "modules" not in catalog:
        raise SystemExit("CATALOG_MISSING_REQUIRED_FIELDS")

    modules = [
        Module(
            module_id=int(item["id"]),
            slug=str(item["slug"]).strip(),
            title=str(item["title"]).strip(),
            status=str(item["status"]).strip(),
        )
        for item in catalog["modules"]
    ]

    modules.sort(key=lambda item: item.module_id)

    ids = [item.module_id for item in modules]
    if len(ids) != len(set(ids)):
        raise SystemExit("CATALOG_DUPLICATE_MODULE_IDS")

    slugs = [item.slug for item in modules]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("CATALOG_DUPLICATE_MODULE_SLUGS")

    for module in modules:
        if not module.slug.replace("_", "").isalnum():
            raise SystemExit(f"INVALID_SLUG: {module.slug}")

    return catalog, modules


def scan_module(module: Module) -> str:
    script_exists = module.script_path.is_file()
    runtime_exists = [
        path.is_file()
        for path in module.runtime_paths
    ]

    if script_exists and all(runtime_exists):
        return "COMPLETE"

    if script_exists and any(runtime_exists):
        return "PARTIAL"

    if script_exists:
        return "SCRIPT_ONLY"

    if any(runtime_exists):
        return "RUNTIME_ONLY"

    return "MISSING"


def render_template(template_text: str, module: Module) -> str:
    values = {
        "module_code": module.module_code,
        "module_id": module.module_id,
        "slug": module.slug,
        "title": module.title,
        "status": module.status,
    }

    try:
        rendered = template_text.format(**values)
    except KeyError as exc:
        raise SystemExit(
            f"TEMPLATE_UNKNOWN_PLACEHOLDER: {exc}"
        ) from exc

    required = (
        module.module_code,
        module.status,
        module.slug,
        str(module.module_id),
    )

    missing = [
        token
        for token in required
        if token not in rendered
    ]

    if missing:
        raise SystemExit(
            f"TEMPLATE_RENDER_VALIDATION_FAILED"
            f"[{module.module_code}]: {missing}"
        )

    return rendered


def generate_script(
    module: Module,
    template_text: str,
    overwrite: bool,
) -> None:
    if module.script_path.exists() and not overwrite:
        raise SystemExit(
            f"DESTINATION_EXISTS: {module.script_path}"
        )

    module.script_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    rendered = render_template(template_text, module)

    module.script_path.write_text(
        rendered,
        encoding="utf-8"
    )
    module.script_path.chmod(0o755)


def execute_module(module: Module) -> None:
    subprocess.run(
        ["python3", str(module.script_path)],
        cwd=ROOT,
        check=True,
    )


def validate_module(module: Module) -> None:
    missing = [
        str(path.relative_to(ROOT))
        for path in module.runtime_paths
        if not path.is_file()
    ]

    if missing:
        raise SystemExit(
            f"RUNTIME_VALIDATION_FAILED"
            f"[{module.module_code}]: {missing}"
        )

    runtime_payload = load_json(module.runtime_paths[0])

    if runtime_payload.get("module") != module.module_code:
        raise SystemExit(
            f"MODULE_CODE_MISMATCH[{module.module_code}]"
        )

    if runtime_payload.get("status") != module.status:
        raise SystemExit(
            f"STATUS_MISMATCH[{module.module_code}]"
        )

    if runtime_payload.get("result") != "PASS":
        raise SystemExit(
            f"RESULT_NOT_PASS[{module.module_code}]"
        )

    runtime_mode = (
        runtime_payload
        .get("runtime", {})
        .get("runtime_mode")
    )

    if runtime_mode != "SHADOW_ONLY_READ_ONLY":
        raise SystemExit(
            f"UNSAFE_RUNTIME_MODE[{module.module_code}]: "
            f"{runtime_mode}"
        )


def write_report(report: dict[str, Any]) -> str:
    RUNTIME_META.mkdir(parents=True, exist_ok=True)

    report_path = (
        RUNTIME_META /
        "forge_meta_builder_006_report.json"
    )
    hash_path = (
        RUNTIME_META /
        "forge_meta_builder_006_report_hash.json"
    )
    ledger_path = (
        RUNTIME_META /
        "forge_meta_builder_006_ledger.jsonl"
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False
        ) + "\n",
        encoding="utf-8"
    )

    digest = hashlib.sha256(
        report_path.read_bytes()
    ).hexdigest()

    hash_path.write_text(
        json.dumps(
            {
                "artifact": str(
                    report_path.relative_to(ROOT)
                ),
                "sha256": digest
            },
            indent=2
        ) + "\n",
        encoding="utf-8"
    )

    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                report,
                ensure_ascii=False
            ) + "\n"
        )

    return digest


def git_batch(message: str, push: bool) -> None:
    subprocess.run(
        ["git", "add", "forge/meta", "forge/automation", "runtime"],
        cwd=ROOT,
        check=True
    )

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True
    )

    if not status.stdout.strip():
        print("GIT_BATCH = NO_CHANGES")
        return

    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=ROOT,
        check=True
    )

    if push:
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=ROOT,
            check=True
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Forge Meta Builder Template Engine"
    )

    parser.add_argument("--catalog", required=True)
    parser.add_argument(
        "--template",
        default="forge/meta/templates/"
                "atlas_knowledge_engine.py.tpl"
    )
    parser.add_argument("--scan", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--git-batch", action="store_true")
    parser.add_argument("--push", action="store_true")

    args = parser.parse_args()

    catalog_path = ROOT / args.catalog
    template_path = ROOT / args.template

    catalog, modules = load_catalog(catalog_path)

    try:
        template_text = template_path.read_text(
            encoding="utf-8"
        )
    except FileNotFoundError as exc:
        raise SystemExit(
            f"TEMPLATE_NOT_FOUND: {template_path}"
        ) from exc

    states = {
        module.module_id: scan_module(module)
        for module in modules
    }

    counts = {
        state: list(states.values()).count(state)
        for state in (
            "COMPLETE",
            "PARTIAL",
            "SCRIPT_ONLY",
            "RUNTIME_ONLY",
            "MISSING",
        )
    }

    print("FORGE-META-BUILDER-006")
    print("ATLAS_TEMPLATE_ENGINE_READY")
    print(f"family = {catalog['family']}")
    print(f"modules = {len(modules)}")
    print(f"complete = {counts['COMPLETE']}")
    print(f"partial = {counts['PARTIAL']}")
    print(f"script_only = {counts['SCRIPT_ONLY']}")
    print(f"runtime_only = {counts['RUNTIME_ONLY']}")
    print(f"missing = {counts['MISSING']}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")

    if args.scan:
        return

    generated: list[str] = []
    skipped: list[str] = []
    validated: list[str] = []

    for module in modules:
        state = states[module.module_id]

        if state == "COMPLETE" and args.resume:
            skipped.append(module.module_code)
            continue

        if state != "MISSING" and not args.overwrite:
            raise SystemExit(
                f"MODULE_NOT_MISSING[{module.module_code}]: "
                f"{state}; use --resume or --overwrite"
            )

        generate_script(
            module=module,
            template_text=template_text,
            overwrite=args.overwrite
        )

        generated.append(module.module_code)

        if args.execute:
            execute_module(module)
            validate_module(module)
            validated.append(module.module_code)

    report = {
        "builder": "FORGE-META-BUILDER-006",
        "status": "ATLAS_TEMPLATE_ENGINE_READY",
        "family": catalog["family"],
        "catalog": str(catalog_path.relative_to(ROOT)),
        "template": str(template_path.relative_to(ROOT)),
        "generated": generated,
        "skipped": skipped,
        "validated": validated,
        "generated_count": len(generated),
        "skipped_count": len(skipped),
        "validated_count": len(validated),
        "runtime_mode": "SHADOW_ONLY_READ_ONLY",
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }

    digest = write_report(report)

    print(f"generated = {len(generated)}")
    print(f"skipped = {len(skipped)}")
    print(f"validated = {len(validated)}")
    print(f"hash = {digest}")

    if args.git_batch:
        git_batch(
            message=(
                "FORGE-META-BUILDER-006 "
                "Template Engine Ready"
            ),
            push=args.push
        )


if __name__ == "__main__":
    main()
