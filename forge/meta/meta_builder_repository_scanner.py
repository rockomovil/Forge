#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

AUTOMATION = ROOT / "forge" / "automation"
RUNTIME = ROOT / "runtime" / "atlas"

SCRIPT_RE = re.compile(
    r"forge_knowledge_(\d+)_atlas_(.+)_engine\.py$"
)


def load_catalog(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def find_script(module_id: int):
    prefix = f"forge_knowledge_{module_id:03d}_atlas_"

    matches = list(AUTOMATION.glob(prefix + "*_engine.py"))

    if len(matches) == 1:
        return matches[0]

    return None


def runtime_files(slug: str, module_id: int):

    base = RUNTIME / f"{slug}_{module_id:03d}"

    return {
        "runtime": base.with_suffix(".json"),
        "hash": RUNTIME / f"{slug}_{module_id:03d}_hash.json",
        "ledger": RUNTIME / f"{slug}_{module_id:03d}_ledger.jsonl",
    }


def module_state(module):

    idx = int(module["id"])

    slug = module["slug"]

    script = find_script(idx)

    if script is None:

        return "MISSING", {}

    files = runtime_files(slug, idx)

    exists = {
        k: v.exists()
        for k, v in files.items()
    }

    if all(exists.values()):

        return "COMPLETE", exists

    if any(exists.values()):

        return "PARTIAL", exists

    return "SCRIPT_ONLY", exists


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--catalog", required=True)

    parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    catalog = load_catalog(ROOT / args.catalog)

    modules = catalog["modules"]

    report = []

    summary = {
        "COMPLETE": 0,
        "PARTIAL": 0,
        "SCRIPT_ONLY": 0,
        "MISSING": 0,
    }

    first_missing = None

    for m in modules:

        status, artifacts = module_state(m)

        summary[status] += 1

        if first_missing is None and status != "COMPLETE":
            first_missing = int(m["id"])

        report.append({
            "id": int(m["id"]),
            "slug": m["slug"],
            "status": status,
            "artifacts": artifacts,
        })

    if args.json:

        print(json.dumps(
            {
                "summary": summary,
                "first_missing": first_missing,
                "modules": report,
            },
            indent=2
        ))

        return

    print()
    print("FORGE META BUILDER 003")
    print("----------------------")
    print()

    print(f"Family              : {catalog['family']}")
    print(f"Modules             : {len(report)}")
    print()

    for key in (
        "COMPLETE",
        "PARTIAL",
        "SCRIPT_ONLY",
        "MISSING",
    ):

        print(f"{key:<20}: {summary[key]}")

    print()

    if first_missing is None:

        print("Repository Status   : COMPLETE")

    else:

        print(f"First Missing       : {first_missing}")

        print("Repository Status   : INCOMPLETE")

    if summary["PARTIAL"]:

        print()
        print("Partial Modules")

        for r in report:

            if r["status"] == "PARTIAL":

                print(f"  {r['id']:03d}  {r['slug']}")

    if summary["SCRIPT_ONLY"]:

        print()
        print("Script Only Modules")

        for r in report:

            if r["status"] == "SCRIPT_ONLY":

                print(f"  {r['id']:03d}  {r['slug']}")


if __name__ == "__main__":
    main()

