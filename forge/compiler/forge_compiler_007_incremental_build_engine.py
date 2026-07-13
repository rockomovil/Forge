#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PLAN = ROOT / "runtime/compiler/forge_build_plan_001.json"
OUT = ROOT / "runtime/compiler"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--plan",
        default=str(PLAN.relative_to(ROOT))
    )

    args = parser.parse_args()

    plan = load(ROOT / args.plan)

    unchanged = []
    rebuild = []
    missing = []

    for module in plan["modules"]:

        script = ROOT / module["script"]
        runtime = ROOT / module["runtime_artifact"]
        hashfile = ROOT / module["hash_artifact"]

        if not script.exists():
            missing.append(module["module_id"])
            continue

        if not runtime.exists():
            rebuild.append(module["module_id"])
            continue

        if not hashfile.exists():
            rebuild.append(module["module_id"])
            continue

        hash_payload = load(hashfile)

        current = sha256(runtime)

        stored = hash_payload.get("sha256")

        if current == stored:
            unchanged.append(module["module_id"])
        else:
            rebuild.append(module["module_id"])

    payload = {

        "compiler":
        "FORGE-COMPILER-007",

        "status":
        "FORGE_INCREMENTAL_BUILD_READY",

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY",

        "modules":
        len(plan["modules"]),

        "unchanged":
        unchanged,

        "rebuild":
        rebuild,

        "missing":
        missing,

        "generated":
        datetime.now(
            timezone.utc
        ).isoformat()

    }

    payload["incremental_hash"] = hashlib.sha256(

        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

    ).hexdigest()

    OUT.mkdir(
        parents=True,
        exist_ok=True
    )

    report = OUT / "forge_incremental_build_report_001.json"

    report.write_text(
        json.dumps(
            payload,
            indent=2
        ) + "\n"
    )

    digest = sha256(report)

    (OUT /
     "forge_incremental_build_report_001_hash.json").write_text(

        json.dumps(
            {
                "artifact":
                str(report.relative_to(ROOT)),
                "sha256":
                digest
            },
            indent=2
        ) + "\n"
    )

    with (
        OUT /
        "forge_incremental_build_report_001_ledger.jsonl"
    ).open("a") as f:

        f.write(
            json.dumps(payload) + "\n"
        )

    print("FORGE-COMPILER-007")
    print("FORGE_INCREMENTAL_BUILD_READY")
    print(f"modules = {payload['modules']}")
    print(f"unchanged = {len(unchanged)}")
    print(f"rebuild = {len(rebuild)}")
    print(f"missing = {len(missing)}")
    print(f"incremental_hash = {payload['incremental_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()
