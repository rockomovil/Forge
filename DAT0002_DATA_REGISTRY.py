#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "data" / "data.json"
OUT = ROOT / "data_registry"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "DAT0002_DATA_REGISTRY_READY"

data = json.loads(INPUT.read_text())

registry = {
    "module": "DAT-0002",
    "name": "Data Registry",
    "status": STATUS,
    "data_ready": data["data_ready"],
    "registry_ready": True,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "data_registry.json"),
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
    "module": "DAT-0002",
    "status": STATUS,
    "generated_files": [
        "data_registry.json",
        "data_registry.schema.json",
        "data_registry_manifest.json",
        "data_registry_ledger.jsonl",
        "data_registry_summary.txt",
        "data_registry_version.json"
    ]
}

version = {
    "module": "DAT-0002",
    "version": "1.0.0",
    "status": STATUS
}

(OUT/"data_registry.json").write_text(json.dumps(registry, indent=2))
(OUT/"data_registry.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"data_registry_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"data_registry_version.json").write_text(json.dumps(version, indent=2))
(OUT/"data_registry_ledger.jsonl").write_text(json.dumps(registry) + "\n")
(OUT/"data_registry_summary.txt").write_text(
f"""Data Registry
--------------
data_ready {registry['data_ready']}
registry_ready {registry['registry_ready']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" DAT-0002 - DATA REGISTRY")
print("="*54)
print()
print("Running Data Registry...")
print()
print("Data Registry")
print("-------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
