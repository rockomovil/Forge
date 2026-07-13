#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CANONICAL = ROOT / "runtime/compiler/forge_canonical_hash_report_001.json"
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


def runtime_artifact(module_id: int):

    matches = sorted(
        (ROOT / "runtime/atlas").glob(f"*_{module_id}.json")
    )

    if not matches:
        raise FileNotFoundError(module_id)

    return matches[0]


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--canonical",
        default=str(CANONICAL.relative_to(ROOT))
    )

    parser.add_argument(
        "--cleanup-legacy",
        action="store_true"
    )

    args = parser.parse_args()

    canonical = load(ROOT / args.canonical)

    CACHE.mkdir(parents=True, exist_ok=True)

    cache_hits = []
    cache_misses = []
    rebuilt = []

    for entry in canonical["hashes"]:

        module = entry["module_id"]
        digest = entry["canonical_hash"]

        target = CACHE / f"{module:03d}_{digest}.json"

        if target.exists():

            cache_hits.append(module)
            continue

        runtime = runtime_artifact(module)

        shutil.copy2(runtime, target)

        cache_misses.append(module)
        rebuilt.append(module)

    removed = []

    if args.cleanup_legacy:

        canonical_names = {
            f"{x['module_id']:03d}_{x['canonical_hash']}.json"
            for x in canonical["hashes"]
        }

        for artifact in CACHE.glob("*.json"):

            if artifact.name not in canonical_names:

                removed.append(artifact.name)

                artifact.unlink()

    payload = {

        "compiler":
        "FORGE-COMPILER-013",

        "status":
        "FORGE_COMPILER_INTEGRATION_READY",

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY",

        "modules":
        len(canonical["hashes"]),

        "cache_hits":
        len(cache_hits),

        "cache_misses":
        len(cache_misses),

        "rebuilt":
        len(rebuilt),

        "legacy_removed":
        len(removed),

        "cache_entries":
        len(list(CACHE.glob("*.json"))),

        "generated":
        datetime.now(timezone.utc).isoformat()

    }

    payload["integration_hash"] = hashlib.sha256(

        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

    ).hexdigest()

    OUT.mkdir(parents=True, exist_ok=True)

    report = OUT / "forge_compiler_integration_report_001.json"

    report.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8"
    )

    digest = sha256(report)

    (OUT / "forge_compiler_integration_report_001_hash.json").write_text(

        json.dumps(
            {
                "artifact":
                str(report.relative_to(ROOT)),
                "sha256":
                digest
            },
            indent=2
        ) + "\n",

        encoding="utf-8"

    )

    with (
        OUT /
        "forge_compiler_integration_report_001_ledger.jsonl"
    ).open("a", encoding="utf-8") as f:

        f.write(json.dumps(payload) + "\n")

    print("FORGE-COMPILER-013")
    print("FORGE_COMPILER_INTEGRATION_READY")
    print(f"modules = {payload['modules']}")
    print(f"cache_hits = {payload['cache_hits']}")
    print(f"cache_misses = {payload['cache_misses']}")
    print(f"rebuilt = {payload['rebuilt']}")
    print(f"legacy_removed = {payload['legacy_removed']}")
    print(f"cache_entries = {payload['cache_entries']}")
    print(f"integration_hash = {payload['integration_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()
