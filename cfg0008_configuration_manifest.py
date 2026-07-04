#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "configuration_lock" / "configuration_lock.json"
OUT = ROOT / "configuration_manifest"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "CFG0008_CONFIGURATION_MANIFEST_READY"

lock = json.loads(INPUT.read_text())

manifest = {
    "module": "CFG-0008",
    "name": "Configuration Manifest",
    "status": STATUS,
    "locked": lock["locked"],
    "immutable": lock["immutable"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "configuration_manifest.json"),
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "artifacts": [
        "configuration_manifest.json",
        "configuration_manifest.schema.json",
        "configuration_manifest_index.json",
        "configuration_manifest_manifest.json",
        "configuration_manifest_ledger.jsonl",
        "configuration_manifest_summary.txt",
        "configuration_manifest_version.json"
    ]
}

manifest["manifest_hash"] = hashlib.sha256(
    json.dumps(manifest, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "type":"object"
}

index = {
    "module":"CFG-0008",
    "artifact_count":len(manifest["artifacts"]),
    "artifacts":manifest["artifacts"],
    "manifest_hash":manifest["manifest_hash"]
}

meta = {
    "module":"CFG-0008",
    "status":STATUS,
    "generated_files":manifest["artifacts"]
}

version = {
    "module":"CFG-0008",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"configuration_manifest.json").write_text(json.dumps(manifest,indent=2))
(OUT/"configuration_manifest.schema.json").write_text(json.dumps(schema,indent=2))
(OUT/"configuration_manifest_index.json").write_text(json.dumps(index,indent=2))
(OUT/"configuration_manifest_manifest.json").write_text(json.dumps(meta,indent=2))
(OUT/"configuration_manifest_version.json").write_text(json.dumps(version,indent=2))
(OUT/"configuration_manifest_ledger.jsonl").write_text(json.dumps(manifest)+"\n")
(OUT/"configuration_manifest_summary.txt").write_text(
f"""Configuration Manifest
------------------------
artifact_count {len(manifest['artifacts'])}
locked {manifest['locked']}
immutable {manifest['immutable']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" CFG-0008 - CONFIGURATION MANIFEST")
print("="*54)
print()
print("Running Configuration Manifest...")
print()
print("Configuration Manifest")
print("----------------------")
for f in manifest["artifacts"]:
    print(f)
print()
print(f"Generated : {len(manifest['artifacts'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
