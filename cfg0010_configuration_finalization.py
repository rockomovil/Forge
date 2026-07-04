#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "configuration_release" / "configuration_release.json"
OUT = ROOT / "configuration_finalization"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "CFG0010_CONFIGURATION_FINALIZATION_READY"

release = json.loads(INPUT.read_text())

finalization = {
    "module": "CFG-0010",
    "name": "Configuration Finalization",
    "status": STATUS,
    "configuration_finalized": True,
    "release_ready": release["release_ready"],
    "locked": release["locked"],
    "immutable": release["immutable"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "configuration_finalization.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

finalization["finalization_hash"] = hashlib.sha256(
    json.dumps(finalization, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object"
}

manifest = {
    "module": "CFG-0010",
    "status": STATUS,
    "generated_files": [
        "configuration_finalization.json",
        "configuration_finalization.schema.json",
        "configuration_finalization_manifest.json",
        "configuration_finalization_ledger.jsonl",
        "configuration_finalization_summary.txt",
        "configuration_finalization_version.json"
    ]
}

version = {
    "module": "CFG-0010",
    "version": "1.0.0",
    "status": STATUS
}

(OUT/"configuration_finalization.json").write_text(json.dumps(finalization, indent=2))
(OUT/"configuration_finalization.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"configuration_finalization_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"configuration_finalization_version.json").write_text(json.dumps(version, indent=2))
(OUT/"configuration_finalization_ledger.jsonl").write_text(json.dumps(finalization) + "\n")
(OUT/"configuration_finalization_summary.txt").write_text(
f"""Configuration Finalization
----------------------------
configuration_finalized {finalization['configuration_finalized']}
release_ready {finalization['release_ready']}
locked {finalization['locked']}
immutable {finalization['immutable']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" CFG-0010 - CONFIGURATION FINALIZATION")
print("=" * 54)
print()
print("Running Configuration Finalization...")
print()
print("Configuration Finalization")
print("--------------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
