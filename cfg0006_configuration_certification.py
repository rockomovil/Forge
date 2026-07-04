#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "configuration_audit" / "configuration_audit.json"
OUT = ROOT / "configuration_certification"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "CFG0006_CONFIGURATION_CERTIFICATION_READY"

audit = json.loads(INPUT.read_text())

cert = {
    "module": "CFG-0006",
    "name": "Configuration Certification",
    "status": STATUS,
    "certified": audit["all_checks_passed"],
    "all_checks_passed": audit["all_checks_passed"],
    "audit_score": audit["audit_score"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "configuration_certification.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

cert["certification_hash"] = hashlib.sha256(
    json.dumps(cert, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "type":"object"
}

manifest = {
    "module":"CFG-0006",
    "status":STATUS,
    "generated_files":[
        "configuration_certification.json",
        "configuration_certification.schema.json",
        "configuration_certification_manifest.json",
        "configuration_certification_ledger.jsonl",
        "configuration_certification_summary.txt",
        "configuration_certification_version.json"
    ]
}

version = {
    "module":"CFG-0006",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"configuration_certification.json").write_text(json.dumps(cert, indent=2))
(OUT/"configuration_certification.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"configuration_certification_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"configuration_certification_version.json").write_text(json.dumps(version, indent=2))
(OUT/"configuration_certification_ledger.jsonl").write_text(json.dumps(cert) + "\n")
(OUT/"configuration_certification_summary.txt").write_text(
f"""Configuration Certification
-----------------------------
certified {cert['certified']}
audit_score {cert['audit_score']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" CFG-0006 - CONFIGURATION CERTIFICATION")
print("="*54)
print()
print("Running Configuration Certification...")
print()
print("Configuration Certification")
print("---------------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
