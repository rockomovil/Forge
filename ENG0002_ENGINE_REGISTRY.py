#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "engine" / "engine.json"
OUT = ROOT / "engine_registry"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "ENG0002_ENGINE_REGISTRY_READY"

engine = json.loads(INPUT.read_text())

registry = {
    "module": "ENG-0002",
    "name": "Engine Registry",
    "status": STATUS,
    "engine_ready": engine["engine_ready"],
    "registry_ready": True,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "engine_registry.json"),
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
    "module": "ENG-0002",
    "status": STATUS,
    "generated_files": [
        "engine_registry.json",
        "engine_registry.schema.json",
        "engine_registry_manifest.json",
        "engine_registry_ledger.jsonl",
        "engine_registry_summary.txt",
        "engine_registry_version.json"
    ]
}

version = {
    "module": "ENG-0002",
    "version": "1.0.0",
    "status": STATUS
}

(OUT/"engine_registry.json").write_text(json.dumps(registry, indent=2))
(OUT/"engine_registry.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"engine_registry_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"engine_registry_version.json").write_text(json.dumps(version, indent=2))
(OUT/"engine_registry_ledger.jsonl").write_text(json.dumps(registry) + "\n")
(OUT/"engine_registry_summary.txt").write_text(
f"""Engine Registry
---------------
engine_ready {registry['engine_ready']}
registry_ready {registry['registry_ready']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" ENG-0002 - ENGINE REGISTRY")
print("=" * 54)
print()
print("Running Engine Registry...")
print()
print("Engine Registry")
print("---------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")

