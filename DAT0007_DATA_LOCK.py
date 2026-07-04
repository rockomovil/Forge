#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "data_certification" / "data_certification.json"
OUT = ROOT / "data_lock"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "DAT0007_DATA_LOCK_READY"

cert = json.loads(INPUT.read_text())

lock = {
    "module": "DAT-0007",
    "name": "Data Lock",
    "status": STATUS,
    "locked": cert["certified"],
    "immutable": True,
    "mutation_allowed": False,
    "delete_allowed": False,
    "rollback_allowed": False,
    "unlock_allowed": False,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "data_lock.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

lock["lock_hash"] = hashlib.sha256(
    json.dumps(lock, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "type":"object"
}

manifest = {
    "module":"DAT-0007",
    "status":STATUS,
    "generated_files":[
        "data_lock.json",
        "data_lock.schema.json",
        "data_lock_manifest.json",
        "data_lock_ledger.jsonl",
        "data_lock_summary.txt",
        "data_lock_version.json"
    ]
}

version = {
    "module":"DAT-0007",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"data_lock.json").write_text(json.dumps(lock, indent=2))
(OUT/"data_lock.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"data_lock_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"data_lock_version.json").write_text(json.dumps(version, indent=2))
(OUT/"data_lock_ledger.jsonl").write_text(json.dumps(lock) + "\n")
(OUT/"data_lock_summary.txt").write_text(
f"""Data Lock
---------
locked {lock['locked']}
immutable {lock['immutable']}
mutation_allowed {lock['mutation_allowed']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" DAT-0007 - DATA LOCK")
print("="*54)
print()
print("Running Data Lock...")
print()
print("Data Lock")
print("---------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
