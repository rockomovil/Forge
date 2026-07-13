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


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--canonical",
        default=str(CANONICAL.relative_to(ROOT))
    )

    args = parser.parse_args()

    canonical = load(ROOT / args.canonical)

    CACHE.mkdir(parents=True, exist_ok=True)

    migrated = []
    reused = []
    missing = []

    for entry in canonical["hashes"]:

        module = entry["module_id"]

        digest = entry["canonical_hash"]

        runtime = ROOT / \
            f"runtime/atlas/{entry['module_code'][16:].lower()}.json"

        #
        # buscar artefacto runtime por prefijo
        #

        candidates = list(
            (ROOT / "runtime/atlas").glob(
                f"*_{module}.json"
            )
        )

        if not candidates:

            missing.append(module)
            continue

        runtime = candidates[0]

        target = CACHE / f"{module:03d}_{digest}.json"

        if target.exists():

            reused.append(module)

        else:

            shutil.copy2(
                runtime,
                target
            )

            migrated.append(module)

    payload = {

        "compiler":
        "FORGE-COMPILER-012",

        "status":
        "FORGE_CACHE_UNIFICATION_READY",

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY",

        "modules":
        len(canonical["hashes"]),

        "migrated":
        migrated,

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

    payload["unification_hash"] = hashlib.sha256(

        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

    ).hexdigest()

    OUT.mkdir(parents=True, exist_ok=True)

    report = OUT / \
        "forge_cache_unification_report_001.json"

    report.write_text(

        json.dumps(
            payload,
            indent=2
        ) + "\n",

        encoding="utf-8"

    )

    digest = sha256(report)

    (OUT /
     "forge_cache_unification_report_001_hash.json").write_text(

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
        "forge_cache_unification_report_001_ledger.jsonl"
    ).open("a", encoding="utf-8") as f:

        f.write(
            json.dumps(payload) + "\n"
        )

    print("FORGE-COMPILER-012")
    print("FORGE_CACHE_UNIFICATION_READY")
    print(f"modules = {payload['modules']}")
    print(f"migrated = {len(migrated)}")
    print(f"reused = {len(reused)}")
    print(f"missing = {len(missing)}")
    print(f"cache_entries = {payload['cache_entries']}")
    print(f"unification_hash = {payload['unification_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()
