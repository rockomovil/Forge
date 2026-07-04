#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "configuration" / "configuration.json"
OUT = ROOT / "configuration_registry"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "CFG0002_CONFIGURATION_REGISTRY_READY"

cfg = json.loads(INPUT.read_text())

registry = {
    "module": "CFG-0002",
    "name": "Configuration Registry",
    "status": STATUS,
    "configuration_ready": cfg["configuration_ready"],
    "registry_ready": True,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "configuration_registry.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

registry["registry_hash"] = hashlib.sha256(
    json.dumps(registry, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object"
}

manifest = {
    "module": "CFG-0002",
    "status": STATUS,
    "generated_files": [
        "configuration_registry.json",
        "configuration_registry.schema.json",
        "configuration_registry_manifest.json",
        "configuration_registry_ledger.jsonl",
        "configuration_registry_summary.txt",
        "configuration_registry_version.json"
    ]
}

version = {
    "module": "CFG-0002",
    "version": "1.0.0",
    "status": STATUS
}

(OUT/"configuration_registry.json").write_text(json.dumps(registry, indent=2))
(OUT/"configuration_registry.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"configuration_registry_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"configuration_registry_version.json").write_text(json.dumps(version, indent=2))
(OUT/"configuration_registry_ledger.jsonl").write_text(json.dumps(registry) + "\n")
(OUT/"configuration_registry_summary.txt").write_text(
f"""Configuration Registry
------------------------
configuration_ready {registry['configuration_ready']}
registry_ready {registry['registry_ready']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" CFG-0002 - CONFIGURATION REGISTRY")
print("=" * 54)
print()
print("Running Configuration Registry...")
print()
print("Configuration Registry")
print("----------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
