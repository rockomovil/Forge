#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "engine_seal" / "engine_seal.json"
OUT = ROOT / "engine_lock"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "ENG0008_ENGINE_LOCK_READY"

seal = json.loads(INPUT.read_text())

lock = {
    "module": "ENG-0008",
    "name": "Engine Lock",
    "status": STATUS,
    "locked": seal["sealed"],
    "all_checks_passed": seal["all_checks_passed"],
    "audit_score": seal["audit_score"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "engine_lock.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

lock["engine_lock_hash"] = hashlib.sha256(
    json.dumps(lock, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object"
}

manifest = {
    "module": "ENG-0008",
    "status": STATUS,
    "generated_files": [
        "engine_lock.json",
        "engine_lock.schema.json",
        "engine_lock_manifest.json",
        "engine_lock_ledger.jsonl",
        "engine_lock_summary.txt",
        "engine_lock_version.json"
    ]
}

version = {
    "module": "ENG-0008",
    "version": "1.0.0",
    "status": STATUS
}

(OUT / "engine_lock.json").write_text(json.dumps(lock, indent=2))
(OUT / "engine_lock.schema.json").write_text(json.dumps(schema, indent=2))
(OUT / "engine_lock_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT / "engine_lock_version.json").write_text(json.dumps(version, indent=2))
(OUT / "engine_lock_ledger.jsonl").write_text(json.dumps(lock) + "\n")
(OUT / "engine_lock_summary.txt").write_text(
f"""Engine Lock
-----------
locked {lock['locked']}
audit_score {lock['audit_score']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" ENG-0008 - ENGINE LOCK")
print("=" * 54)
print()
print("Running Engine Lock...")
print()
print("Engine Lock")
print("-----------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
