#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "data_lock" / "data_lock.json"
OUT = ROOT / "data_manifest"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "DAT0008_DATA_MANIFEST_READY"

lock = json.loads(INPUT.read_text())

manifest = {
    "module": "DAT-0008",
    "name": "Data Manifest",
    "status": STATUS,
    "locked": lock["locked"],
    "immutable": lock["immutable"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "data_manifest.json"),
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "artifacts": [
        "data_manifest.json",
        "data_manifest.schema.json",
        "data_manifest_index.json",
        "data_manifest_manifest.json",
        "data_manifest_ledger.jsonl",
        "data_manifest_summary.txt",
        "data_manifest_version.json"
    ]
}

manifest["manifest_hash"] = hashlib.sha256(
    json.dumps(manifest, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object"
}

index = {
    "module": "DAT-0008",
    "artifact_count": len(manifest["artifacts"]),
    "artifacts": manifest["artifacts"],
    "manifest_hash": manifest["manifest_hash"]
}

meta = {
    "module": "DAT-0008",
    "status": STATUS,
    "generated_files": manifest["artifacts"]
}

version = {
    "module": "DAT-0008",
    "version": "1.0.0",
    "status": STATUS
}

(OUT/"data_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"data_manifest.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"data_manifest_index.json").write_text(json.dumps(index, indent=2))
(OUT/"data_manifest_manifest.json").write_text(json.dumps(meta, indent=2))
(OUT/"data_manifest_version.json").write_text(json.dumps(version, indent=2))
(OUT/"data_manifest_ledger.jsonl").write_text(json.dumps(manifest) + "\n")
(OUT/"data_manifest_summary.txt").write_text(
f"""Data Manifest
-------------
artifact_count {len(manifest['artifacts'])}
locked {manifest['locked']}
immutable {manifest['immutable']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" DAT-0008 - DATA MANIFEST")
print("=" * 54)
print()
print("Running Data Manifest...")
print()
print("Data Manifest")
print("-------------")
for f in manifest["artifacts"]:
    print(f)
print()
print(f"Generated : {len(manifest['artifacts'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
