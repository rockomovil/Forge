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


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_hash(module):

    script = ROOT / module["script"]

    runtime = ROOT / module["runtime_artifact"]

    catalog = module.get("catalog")

    h = hashlib.sha256()

    #
    # Canonical identity
    #

    h.update(str(module["module_id"]).encode())

    h.update(module["module_code"].encode())

    h.update(module["family"].encode())

    #
    # Script content
    #

    h.update(script.read_bytes())

    #
    # Runtime artifact (if exists)
    #

    if runtime.exists():

        h.update(runtime.read_bytes())

    #
    # Optional catalog
    #

    if catalog:

        c = ROOT / catalog

        if c.exists():

            h.update(c.read_bytes())

    return h.hexdigest()


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

    hashes = []

    for module in plan["modules"]:

        digest = canonical_hash(module)

        hashes.append({

            "module_id":
            module["module_id"],

            "module_code":
            module["module_code"],

            "family":
            module["family"],

            "canonical_hash":
            digest

        })

    payload = {

        "compiler":
        "FORGE-COMPILER-011",

        "status":
        "FORGE_CANONICAL_HASH_ENGINE_READY",

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY",

        "modules":
        len(hashes),

        "generated":
        datetime.now(
            timezone.utc
        ).isoformat(),

        "hashes":
        hashes

    }

    payload["engine_hash"] = sha256_bytes(

        json.dumps(

            payload,

            sort_keys=True,

            separators=(",", ":")

        ).encode()

    )

    OUT.mkdir(
        parents=True,
        exist_ok=True
    )

    report = OUT / "forge_canonical_hash_report_001.json"

    report.write_text(

        json.dumps(
            payload,
            indent=2
        ) + "\n",

        encoding="utf-8"

    )

    digest = sha256_file(report)

    (OUT /
     "forge_canonical_hash_report_001_hash.json").write_text(

        json.dumps({

            "artifact":
            str(report.relative_to(ROOT)),

            "sha256":
            digest

        }, indent=2) + "\n",

        encoding="utf-8"

    )

    with (
        OUT /
        "forge_canonical_hash_report_001_ledger.jsonl"
    ).open("a", encoding="utf-8") as f:

        f.write(
            json.dumps(payload) + "\n"
        )

    print("FORGE-COMPILER-011")
    print("FORGE_CANONICAL_HASH_ENGINE_READY")
    print(f"modules = {payload['modules']}")
    print(f"engine_hash = {payload['engine_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()
