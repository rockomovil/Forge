#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "data_finalization" / "data_finalization.json"
OUT = ROOT / "engine"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "ENG0001_ENGINE_CHARTER_READY"

data = json.loads(INPUT.read_text())

charter = {
    "module": "ENG-0001",
    "name": "Engine Charter",
    "status": STATUS,
    "data_finalized": data["data_finalized"],
    "engine_ready": True,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "engine.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

charter["engine_hash"] = hashlib.sha256(
    json.dumps(charter, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "type":"object"
}

manifest = {
    "module":"ENG-0001",
    "status":STATUS,
    "generated_files":[
        "engine.json",
        "engine.schema.json",
        "engine_manifest.json",
        "engine_ledger.jsonl",
        "engine_summary.txt",
        "engine_version.json"
    ]
}

version = {
    "module":"ENG-0001",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"engine.json").write_text(json.dumps(charter, indent=2))
(OUT/"engine.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"engine_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"engine_version.json").write_text(json.dumps(version, indent=2))
(OUT/"engine_ledger.jsonl").write_text(json.dumps(charter) + "\n")
(OUT/"engine_summary.txt").write_text(
f"""Engine Charter
---------------
engine_ready {charter['engine_ready']}
data_finalized {charter['data_finalized']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" ENG-0001 - ENGINE CHARTER")
print("=" * 54)
print()
print("Running Engine Charter...")
print()
print("Engine Charter")
print("--------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")

