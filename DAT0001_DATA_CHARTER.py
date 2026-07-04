#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "configuration_finalization" / "configuration_finalization.json"
OUT = ROOT / "data"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "DAT0001_DATA_CHARTER_READY"

cfg = json.loads(INPUT.read_text())

charter = {
    "module": "DAT-0001",
    "name": "Data Charter",
    "status": STATUS,
    "configuration_finalized": cfg["configuration_finalized"],
    "data_ready": True,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "data.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

charter["data_hash"] = hashlib.sha256(
    json.dumps(charter, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "type":"object"
}

manifest = {
    "module":"DAT-0001",
    "status":STATUS,
    "generated_files":[
        "data.json",
        "data.schema.json",
        "data_manifest.json",
        "data_ledger.jsonl",
        "data_summary.txt",
        "data_version.json"
    ]
}

version = {
    "module":"DAT-0001",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"data.json").write_text(json.dumps(charter,indent=2))
(OUT/"data.schema.json").write_text(json.dumps(schema,indent=2))
(OUT/"data_manifest.json").write_text(json.dumps(manifest,indent=2))
(OUT/"data_version.json").write_text(json.dumps(version,indent=2))
(OUT/"data_ledger.jsonl").write_text(json.dumps(charter)+"\n")
(OUT/"data_summary.txt").write_text(
f"""Data Charter
-------------
data_ready {charter['data_ready']}
configuration_finalized {charter['configuration_finalized']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" DAT-0001 - DATA CHARTER")
print("="*54)
print()
print("Running Data Charter...")
print()
print("Data Charter")
print("------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
