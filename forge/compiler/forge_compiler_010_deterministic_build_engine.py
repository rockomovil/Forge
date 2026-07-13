#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CONTENT = ROOT / "runtime/compiler/forge_content_hash_report_001.json"
CACHE = ROOT / "runtime/compiler/cache"
OUT = ROOT / "runtime/compiler"


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--content",
        default=str(CONTENT.relative_to(ROOT))
    )

    args = parser.parse_args()

    content = load(ROOT / args.content)

    deterministic = []
    missing = []

    for entry in content["hashes"]:

        module = entry["module_id"]
        digest = entry["content_hash"]

        pattern = f"{module:03d}_{digest}.json"

        artifact = CACHE / pattern

        if artifact.exists():

            deterministic.append({
                "module_id": module,
                "content_hash": digest,
                "cache_hit": True
            })

        else:

            missing.append(module)

            deterministic.append({
                "module_id": module,
                "content_hash": digest,
                "cache_hit": False
            })

    payload = {

        "compiler":
        "FORGE-COMPILER-010",

        "status":
        "FORGE_DETERMINISTIC_BUILD_READY",

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY",

        "modules":
        len(deterministic),

        "cache_hits":
        sum(x["cache_hit"] for x in deterministic),

        "cache_misses":
        len(missing),

        "generated":
        datetime.now(timezone.utc).isoformat(),

        "artifacts":
        deterministic

    }

    payload["deterministic_hash"] = hashlib.sha256(

        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

    ).hexdigest()

    OUT.mkdir(parents=True, exist_ok=True)

    report = OUT / "forge_deterministic_build_report_001.json"

    report.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8"
    )

    digest = sha256(report)

    (OUT / "forge_deterministic_build_report_001_hash.json").write_text(

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
        "forge_deterministic_build_report_001_ledger.jsonl"
    ).open("a", encoding="utf-8") as f:

        f.write(json.dumps(payload) + "\n")

    print("FORGE-COMPILER-010")
    print("FORGE_DETERMINISTIC_BUILD_READY")
    print(f"modules = {payload['modules']}")
    print(f"cache_hits = {payload['cache_hits']}")
    print(f"cache_misses = {payload['cache_misses']}")
    print(f"deterministic_hash = {payload['deterministic_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()
