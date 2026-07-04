#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "data_validation" / "data_validation.json"
OUT = ROOT / "data_audit"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "DAT0005_DATA_INTEGRITY_AUDIT_READY"

validation = json.loads(INPUT.read_text())

audit = {
    "module": "DAT-0005",
    "name": "Data Integrity Audit",
    "status": STATUS,
    "all_checks_passed": validation["all_checks_passed"],
    "validation_score": validation["validation_score"],
    "audit_score": 1.0 if validation["all_checks_passed"] else 0.0,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "data_audit.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

audit["audit_hash"] = hashlib.sha256(
    json.dumps(audit, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object"
}

manifest = {
    "module": "DAT-0005",
    "status": STATUS,
    "generated_files": [
        "data_audit.json",
        "data_audit.schema.json",
        "data_audit_manifest.json",
        "data_audit_ledger.jsonl",
        "data_audit_summary.txt",
        "data_audit_version.json"
    ]
}

version = {
    "module": "DAT-0005",
    "version": "1.0.0",
    "status": STATUS
}

(OUT/"data_audit.json").write_text(json.dumps(audit, indent=2))
(OUT/"data_audit.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"data_audit_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"data_audit_version.json").write_text(json.dumps(version, indent=2))
(OUT/"data_audit_ledger.jsonl").write_text(json.dumps(audit) + "\n")
(OUT/"data_audit_summary.txt").write_text(
f"""Data Integrity Audit
----------------------
audit_score {audit['audit_score']}
all_checks_passed {audit['all_checks_passed']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" DAT-0005 - DATA INTEGRITY AUDIT")
print("=" * 54)
print()
print("Running Data Integrity Audit...")
print()
print("Data Integrity Audit")
print("--------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
