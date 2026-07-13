#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PLAN = ROOT / "runtime/compiler/forge_build_plan_001.json"

CACHE = ROOT / "runtime/compiler/cache"

OUT = ROOT / "runtime/compiler"


def sha256(path: Path):

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def load(path: Path):

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def cache_name(module, digest):

    return f"{module:03d}_{digest}.json"


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(

        "--plan",

        default=str(
            PLAN.relative_to(ROOT)
        )

    )

    args = parser.parse_args()

    plan = load(
        ROOT / args.plan
    )

    CACHE.mkdir(
        parents=True,
        exist_ok=True
    )

    cached = []
    reused = []
    missing = []

    for module in plan["modules"]:

        runtime = ROOT / module["runtime_artifact"]

        if not runtime.exists():

            missing.append(
                module["module_id"]
            )

            continue

        digest = sha256(runtime)

        artifact = CACHE / cache_name(

            module["module_id"],
            digest

        )

        if artifact.exists():

            reused.append(
                module["module_id"]
            )

        else:

            shutil.copy2(
                runtime,
                artifact
            )

            cached.append(
                module["module_id"]
            )

    payload = {

        "compiler":
        "FORGE-COMPILER-008",

        "status":
        "FORGE_ARTIFACT_CACHE_READY",

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY",

        "modules":
        len(plan["modules"]),

        "cached":
        cached,

        "reused":
        reused,

        "missing":
        missing,

        "cache_entries":
        len(
            list(
                CACHE.glob("*.json")
            )
        ),

        "generated":
        datetime.now(
            timezone.utc
        ).isoformat()

    }

    payload["cache_hash"] = hashlib.sha256(

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

    report = OUT / "forge_artifact_cache_report_001.json"

    report.write_text(

        json.dumps(
            payload,
            indent=2
        ) + "\n"

    )

    digest = sha256(report)

    (OUT /
     "forge_artifact_cache_report_001_hash.json").write_text(

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
        "forge_artifact_cache_report_001_ledger.jsonl"
    ).open("a") as f:

        f.write(
            json.dumps(payload) + "\n"
        )

    print("FORGE-COMPILER-008")
    print("FORGE_ARTIFACT_CACHE_READY")
    print(f"modules = {payload['modules']}")
    print(f"cached = {len(cached)}")
    print(f"reused = {len(reused)}")
    print(f"missing = {len(missing)}")
    print(f"cache_entries = {payload['cache_entries']}")
    print(f"cache_hash = {payload['cache_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()
