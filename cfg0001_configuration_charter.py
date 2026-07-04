#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "architecture_finalization" / "architecture_finalization.json"
OUT = ROOT / "configuration"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "CFG0001_CONFIGURATION_CHARTER_READY"

arch = json.loads(INPUT.read_text())

charter = {
    "module": "CFG-0001",
    "name": "Configuration Charter",
    "status": STATUS,
    "architecture_finalized": arch["architecture_finalized"],
    "configuration_ready": True,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "configuration.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

charter["configuration_hash"] = hashlib.sha256(
    json.dumps(charter, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "type":"object"
}

manifest = {
    "module":"CFG-0001",
    "status":STATUS,
    "generated_files":[
        "configuration.json",
        "configuration.schema.json",
        "configuration_manifest.json",
        "configuration_ledger.jsonl",
        "configuration_summary.txt",
        "configuration_version.json"
    ]
}

version = {
    "module":"CFG-0001",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"configuration.json").write_text(json.dumps(charter, indent=2))
(OUT/"configuration.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"configuration_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"configuration_version.json").write_text(json.dumps(version, indent=2))
(OUT/"configuration_ledger.jsonl").write_text(json.dumps(charter) + "\n")
(OUT/"configuration_summary.txt").write_text(
f"""Configuration Charter
-----------------------
configuration_ready {charter['configuration_ready']}
architecture_finalized {charter['architecture_finalized']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" CFG-0001 - CONFIGURATION CHARTER")
print("="*54)
print()
print("Running Configuration Charter...")
print()
print("Configuration Charter")
print("---------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
