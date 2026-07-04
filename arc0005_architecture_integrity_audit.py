#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT/"architecture_validation"/"architecture_validation.json"
OUT = ROOT/"architecture_audit"
OUT.mkdir(parents=True, exist_ok=True)

STATUS="ARC0005_ARCHITECTURE_INTEGRITY_AUDIT_READY"

validation=json.loads(INPUT.read_text())

checks=validation["validation_checks"]

audit={
    "module":"ARC-0005",
    "name":"Architecture Integrity Audit",
    "status":STATUS,
    "all_checks_passed":all(checks.values()),
    "audit_checks":checks,
    "audit_score":1.0 if all(checks.values()) else 0.0,
    "canonical_input":str(INPUT),
    "runtime_mode":"SHADOW_ONLY_READ_ONLY",
    "generated_at":datetime.now(timezone.utc).isoformat()
}

audit["audit_hash"]=hashlib.sha256(
    json.dumps(audit,sort_keys=True).encode()
).hexdigest()

schema={"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}

manifest={
    "module":"ARC-0005",
    "status":STATUS,
    "generated_files":[
        "architecture_audit.json",
        "architecture_audit.schema.json",
        "architecture_audit_manifest.json",
        "architecture_audit_ledger.jsonl",
        "architecture_audit_summary.txt",
        "architecture_audit_version.json"
    ]
}

version={
    "module":"ARC-0005",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"architecture_audit.json").write_text(json.dumps(audit,indent=2))
(OUT/"architecture_audit.schema.json").write_text(json.dumps(schema,indent=2))
(OUT/"architecture_audit_manifest.json").write_text(json.dumps(manifest,indent=2))
(OUT/"architecture_audit_version.json").write_text(json.dumps(version,indent=2))
(OUT/"architecture_audit_ledger.jsonl").write_text(json.dumps(audit)+"\n")
(OUT/"architecture_audit_summary.txt").write_text(
f"""Architecture Integrity Audit
------------------------------
audit_score {audit['audit_score']}
all_checks_passed {audit['all_checks_passed']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" ARC-0005 - ARCHITECTURE INTEGRITY AUDIT")
print("="*54)
print()
print("Running Architecture Integrity Audit...")
print()
print("Architecture Integrity Audit")
print("----------------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print("Generated : 6")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
