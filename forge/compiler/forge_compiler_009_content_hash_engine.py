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


def sha256_file(path: Path) -> str:
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
        "--plan",
        default=str(PLAN.relative_to(ROOT))
    )
    args = parser.parse_args()

    plan = load(ROOT / args.plan)

    hashes = []

    for module in plan["modules"]:

        script = ROOT / module["script"]

        hashes.append({
            "module_id": module["module_id"],
            "script": module["script"],
            "content_hash": sha256_file(script)
        })

    payload = {
        "compiler": "FORGE-COMPILER-009",
        "status": "FORGE_CONTENT_HASH_ENGINE_READY",
        "runtime_mode": "SHADOW_ONLY_READ_ONLY",
        "modules": len(hashes),
        "generated": datetime.now(timezone.utc).isoformat(),
        "hashes": hashes
    }

    payload["engine_hash"] = hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        ).encode()
    ).hexdigest()

    OUT.mkdir(parents=True, exist_ok=True)

    report = OUT / "forge_content_hash_report_001.json"
    report.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8"
    )

    digest = sha256_file(report)

    (OUT / "forge_content_hash_report_001_hash.json").write_text(
        json.dumps({
            "artifact": str(report.relative_to(ROOT)),
            "sha256": digest
        }, indent=2) + "\n",
        encoding="utf-8"
    )

    with (OUT / "forge_content_hash_report_001_ledger.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")

    print("FORGE-COMPILER-009")
    print("FORGE_CONTENT_HASH_ENGINE_READY")
    print(f"modules = {len(hashes)}")
    print(f"engine_hash = {payload['engine_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()
