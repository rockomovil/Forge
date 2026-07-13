#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MASTER = ROOT / "forge" / "meta" / "master" / "forge_master.yaml"
RUNTIME_DIR = ROOT / "runtime" / "compiler"


@dataclass(frozen=True)
class ModulePlan:
    module_id: int
    module_code: str
    family: str
    catalog: str
    slug: str
    title: str
    status: str
    script: str
    runtime_artifact: str
    hash_artifact: str
    ledger_artifact: str


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"MASTER_NOT_FOUND: {path}") from exc
    except yaml.YAMLError as exc:
        raise SystemExit(f"MASTER_INVALID_YAML: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("MASTER_INVALID_STRUCTURE")

    return data


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"CATALOG_NOT_FOUND: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"CATALOG_INVALID_JSON[{path}]: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit(f"CATALOG_INVALID_STRUCTURE: {path}")

    return data


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def compile_plan(master_path: Path) -> dict[str, Any]:
    master = load_yaml(master_path)

    families = master.get("families")
    if not isinstance(families, list) or not families:
        raise SystemExit("MASTER_FAMILIES_EMPTY")

    modules: list[ModulePlan] = []
    seen_ids: dict[int, str] = {}
    seen_slugs: dict[str, str] = {}
    family_summaries: list[dict[str, Any]] = []

    for family_order, catalog_value in enumerate(families, start=1):
        if not isinstance(catalog_value, str) or not catalog_value.strip():
            raise SystemExit(f"MASTER_INVALID_CATALOG_ENTRY: {catalog_value!r}")

        catalog_path = resolve_repo_path(catalog_value)
        catalog = load_json(catalog_path)

        family_name = str(catalog.get("family", "")).strip()
        raw_modules = catalog.get("modules")

        if not family_name:
            raise SystemExit(f"CATALOG_FAMILY_MISSING: {catalog_path}")

        if not isinstance(raw_modules, list) or not raw_modules:
            raise SystemExit(f"CATALOG_MODULES_EMPTY: {catalog_path}")

        family_ids: list[int] = []

        for raw in raw_modules:
            module_id = int(raw["id"])
            slug = str(raw["slug"]).strip()
            title = str(raw["title"]).strip()
            status = str(raw["status"]).strip()

            if module_id in seen_ids:
                raise SystemExit(
                    f"DUPLICATE_MODULE_ID: {module_id} "
                    f"in {catalog_value} and {seen_ids[module_id]}"
                )

            global_slug = f"{family_name}:{slug}"
            if global_slug in seen_slugs:
                raise SystemExit(
                    f"DUPLICATE_FAMILY_SLUG: {global_slug} "
                    f"in {catalog_value} and {seen_slugs[global_slug]}"
                )

            seen_ids[module_id] = catalog_value
            seen_slugs[global_slug] = catalog_value
            family_ids.append(module_id)

            base = f"{slug}_{module_id:03d}"

            modules.append(
                ModulePlan(
                    module_id=module_id,
                    module_code=f"FORGE-KNOWLEDGE-{module_id:03d}",
                    family=family_name,
                    catalog=str(catalog_path.relative_to(ROOT)),
                    slug=slug,
                    title=title,
                    status=status,
                    script=(
                        f"forge/automation/"
                        f"forge_knowledge_{module_id:03d}_atlas_{slug}_engine.py"
                    ),
                    runtime_artifact=f"runtime/atlas/{base}.json",
                    hash_artifact=f"runtime/atlas/{base}_hash.json",
                    ledger_artifact=f"runtime/atlas/{base}_ledger.jsonl",
                )
            )

        sorted_family_ids = sorted(family_ids)
        contiguous = all(
            current == previous + 1
            for previous, current in zip(
                sorted_family_ids,
                sorted_family_ids[1:]
            )
        )

        family_summaries.append(
            {
                "order": family_order,
                "family": family_name,
                "catalog": str(catalog_path.relative_to(ROOT)),
                "module_count": len(family_ids),
                "first_module_id": min(family_ids),
                "last_module_id": max(family_ids),
                "contiguous_ids": contiguous,
            }
        )

    modules.sort(key=lambda item: item.module_id)

    build_order = [item.module_id for item in modules]
    global_contiguous = all(
        current == previous + 1
        for previous, current in zip(build_order, build_order[1:])
    )

    plan: dict[str, Any] = {
        "compiler": "FORGE-COMPILER-001",
        "status": "FORGE_BUILD_PLAN_READY",
        "master": str(master_path.relative_to(ROOT)),
        "master_name": master.get("name", "FORGE_MASTER_BUILD"),
        "master_version": master.get("version", 1),
        "runtime_mode": master.get(
            "runtime_mode",
            "SHADOW_ONLY_READ_ONLY"
        ),
        "family_count": len(family_summaries),
        "module_count": len(modules),
        "first_module_id": build_order[0],
        "last_module_id": build_order[-1],
        "global_contiguous_ids": global_contiguous,
        "families": family_summaries,
        "build_order": build_order,
        "modules": [asdict(item) for item in modules],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    canonical = json.dumps(
        plan,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    plan["hash"] = hashlib.sha256(canonical).hexdigest()

    return plan


def write_plan(plan: dict[str, Any]) -> tuple[Path, Path, Path]:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    plan_path = RUNTIME_DIR / "forge_build_plan_001.json"
    hash_path = RUNTIME_DIR / "forge_build_plan_001_hash.json"
    ledger_path = RUNTIME_DIR / "forge_build_plan_001_ledger.jsonl"

    plan_path.write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    file_hash = hashlib.sha256(plan_path.read_bytes()).hexdigest()

    hash_path.write_text(
        json.dumps(
            {
                "compiler": "FORGE-COMPILER-001",
                "artifact": str(plan_path.relative_to(ROOT)),
                "sha256": file_hash,
                "plan_hash": plan["hash"],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(plan, ensure_ascii=False) + "\n")

    return plan_path, hash_path, ledger_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compila forge_master.yaml en un plan de construcción."
    )
    parser.add_argument(
        "--master",
        default=str(DEFAULT_MASTER.relative_to(ROOT)),
    )
    parser.add_argument(
        "--strict-contiguous",
        action="store_true",
    )
    args = parser.parse_args()

    master_path = resolve_repo_path(args.master)
    plan = compile_plan(master_path)

    if args.strict_contiguous and not plan["global_contiguous_ids"]:
        raise SystemExit("BUILD_PLAN_NON_CONTIGUOUS_MODULE_IDS")

    plan_path, hash_path, ledger_path = write_plan(plan)

    print("FORGE-COMPILER-001")
    print("FORGE_BUILD_PLAN_READY")
    print(f"families = {plan['family_count']}")
    print(f"modules = {plan['module_count']}")
    print(
        f"range = FORGE-KNOWLEDGE-{plan['first_module_id']:03d}"
        f"..FORGE-KNOWLEDGE-{plan['last_module_id']:03d}"
    )
    print(f"contiguous = {plan['global_contiguous_ids']}")
    print(f"plan = {plan_path.relative_to(ROOT)}")
    print(f"hash_artifact = {hash_path.relative_to(ROOT)}")
    print(f"ledger = {ledger_path.relative_to(ROOT)}")
    print(f"hash = {plan['hash']}")
    print(f"runtime_mode = {plan['runtime_mode']}")


if __name__ == "__main__":
    main()
