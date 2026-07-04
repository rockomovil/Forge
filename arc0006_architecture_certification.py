#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT/"architecture_audit"/"architecture_audit.json"
OUT = ROOT/"architecture_certification"
OUT.mkdir(parents=True, exist_ok=True)

STATUS="ARC0006_ARCHITECTURE_CERTIFICATION_READY"

audit=json.loads(INPUT.read_text())

cert={
    "module":"ARC-0006",
    "name":"Architecture Certification",
    "status":STATUS,
    "all_checks_passed":audit["all_checks_passed"],
    "audit_score":audit["audit_score"],
    "certified":audit["all_checks_passed"],
    "canonical_input":str(INPUT),
    "runtime_mode":"SHADOW_ONLY_READ_ONLY",
    "generated_at":datetime.now(timezone.utc).isoformat()
}

cert["certification_hash"]=hashlib.sha256(
    json.dumps(cert,sort_keys=True).encode()
).hexdigest()

schema={
"$schema":"https://json-schema.org/draft/2020-12/schema",
"type":"object"
}

manifest={
"module":"ARC-0006",
"status":STATUS,
"generated_files":[
"architecture_certification.json",
"architecture_certification.schema.json",
"architecture_certification_manifest.json",
"architecture_certification_ledger.jsonl",
"architecture_certification_summary.txt",
"architecture_certification_version.json"
]
}

version={
"module":"ARC-0006",
"version":"1.0.0",
"status":STATUS
}

(OUT/"architecture_certification.json").write_text(json.dumps(cert,indent=2))
(OUT/"architecture_certification.schema.json").write_text(json.dumps(schema,indent=2))
(OUT/"architecture_certification_manifest.json").write_text(json.dumps(manifest,indent=2))
(OUT/"architecture_certification_version.json").write_text(json.dumps(version,indent=2))
(OUT/"architecture_certification_ledger.jsonl").write_text(json.dumps(cert)+"\n")
(OUT/"architecture_certification_summary.txt").write_text(
f"""Architecture Certification
----------------------------
certified {cert['certified']}
audit_score {cert['audit_score']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" ARC-0006 - ARCHITECTURE CERTIFICATION")
print("="*54)
print()
print("Running Architecture Certification...")
print()
print("Architecture Certification")
print("--------------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print("Generated : 6")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
