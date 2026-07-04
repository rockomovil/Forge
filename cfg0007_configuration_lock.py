#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "configuration_certification" / "configuration_certification.json"
OUT = ROOT / "configuration_lock"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "CFG0007_CONFIGURATION_LOCK_READY"

cert = json.loads(INPUT.read_text())

lock = {
    "module": "CFG-0007",
    "name": "Configuration Lock",
    "status": STATUS,
    "locked": cert["certified"],
    "immutable": True,
    "mutation_allowed": False,
    "delete_allowed": False,
    "rollback_allowed": False,
    "unlock_allowed": False,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "configuration_lock.json"),
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
    "module":"CFG-0007",
    "status":STATUS,
    "generated_files":[
        "configuration_lock.json",
        "configuration_lock.schema.json",
        "configuration_lock_manifest.json",
        "configuration_lock_ledger.jsonl",
        "configuration_lock_summary.txt",
        "configuration_lock_version.json"
    ]
}

version = {
    "module":"CFG-0007",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"configuration_lock.json").write_text(json.dumps(lock, indent=2))
(OUT/"configuration_lock.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"configuration_lock_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"configuration_lock_version.json").write_text(json.dumps(version, indent=2))
(OUT/"configuration_lock_ledger.jsonl").write_text(json.dumps(lock) + "\n")
(OUT/"configuration_lock_summary.txt").write_text(
f"""Configuration Lock
------------------
locked {lock['locked']}
immutable {lock['immutable']}
mutation_allowed {lock['mutation_allowed']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" CFG-0007 - CONFIGURATION LOCK")
print("="*54)
print()
print("Running Configuration Lock...")
print()
print("Configuration Lock")
print("------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
