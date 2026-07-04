#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "configuration_validation" / "configuration_validation.json"
OUT = ROOT / "configuration_audit"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "CFG0005_CONFIGURATION_INTEGRITY_AUDIT_READY"

validation = json.loads(INPUT.read_text())

audit = {
    "module": "CFG-0005",
    "name": "Configuration Integrity Audit",
    "status": STATUS,
    "all_checks_passed": validation["all_checks_passed"],
    "validation_score": validation["validation_score"],
    "audit_score": 1.0 if validation["all_checks_passed"] else 0.0,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "configuration_audit.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

audit["audit_hash"] = hashlib.sha256(
    json.dumps(audit, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "type":"object"
}

manifest = {
    "module":"CFG-0005",
    "status":STATUS,
    "generated_files":[
        "configuration_audit.json",
        "configuration_audit.schema.json",
        "configuration_audit_manifest.json",
        "configuration_audit_ledger.jsonl",
        "configuration_audit_summary.txt",
        "configuration_audit_version.json"
    ]
}

version = {
    "module":"CFG-0005",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"configuration_audit.json").write_text(json.dumps(audit, indent=2))
(OUT/"configuration_audit.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"configuration_audit_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"configuration_audit_version.json").write_text(json.dumps(version, indent=2))
(OUT/"configuration_audit_ledger.jsonl").write_text(json.dumps(audit) + "\n")
(OUT/"configuration_audit_summary.txt").write_text(
f"""Configuration Integrity Audit
-------------------------------
audit_score {audit['audit_score']}
all_checks_passed {audit['all_checks_passed']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" CFG-0005 - CONFIGURATION INTEGRITY AUDIT")
print("="*54)
print()
print("Running Configuration Integrity Audit...")
print()
print("Configuration Integrity Audit")
print("-----------------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
