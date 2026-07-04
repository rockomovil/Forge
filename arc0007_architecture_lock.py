#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "architecture_certification" / "architecture_certification.json"
OUT = ROOT / "architecture_lock"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "ARC0007_ARCHITECTURE_LOCK_READY"

cert = json.loads(INPUT.read_text())

lock = {
    "module": "ARC-0007",
    "name": "Architecture Lock",
    "status": STATUS,
    "locked": cert["certified"],
    "immutable": True,
    "mutation_allowed": False,
    "delete_allowed": False,
    "unlock_allowed": False,
    "rollback_allowed": False,
    "all_checks_passed": cert["all_checks_passed"],
    "canonical_input": str(INPUT),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
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
    "module":"ARC-0007",
    "status":STATUS,
    "generated_files":[
        "architecture_lock.json",
        "architecture_lock.schema.json",
        "architecture_lock_manifest.json",
        "architecture_lock_ledger.jsonl",
        "architecture_lock_summary.txt",
        "architecture_lock_version.json"
    ]
}

version = {
    "module":"ARC-0007",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"architecture_lock.json").write_text(json.dumps(lock,indent=2))
(OUT/"architecture_lock.schema.json").write_text(json.dumps(schema,indent=2))
(OUT/"architecture_lock_manifest.json").write_text(json.dumps(manifest,indent=2))
(OUT/"architecture_lock_version.json").write_text(json.dumps(version,indent=2))
(OUT/"architecture_lock_ledger.jsonl").write_text(json.dumps(lock)+"\n")
(OUT/"architecture_lock_summary.txt").write_text(
f"""Architecture Lock
-----------------
locked {lock['locked']}
immutable {lock['immutable']}
mutation_allowed {lock['mutation_allowed']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" ARC-0007 - ARCHITECTURE LOCK")
print("="*54)
print()
print("Running Architecture Lock...")
print()
print("Architecture Lock")
print("-----------------")
for f in manifest["generated_files"]:
    print(f)
print()
print("Generated : 6")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
