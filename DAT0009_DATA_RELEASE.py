#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "data_manifest" / "data_manifest.json"
OUT = ROOT / "data_release"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "DAT0009_DATA_RELEASE_READY"

manifest = json.loads(INPUT.read_text())

release = {
    "module": "DAT-0009",
    "name": "Data Release",
    "status": STATUS,
    "release_ready": True,
    "locked": manifest["locked"],
    "immutable": manifest["immutable"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "data_release.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

release["release_hash"] = hashlib.sha256(
    json.dumps(release, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object"
}

manifest_out = {
    "module": "DAT-0009",
    "status": STATUS,
    "generated_files": [
        "data_release.json",
        "data_release.schema.json",
        "data_release_manifest.json",
        "data_release_ledger.jsonl",
        "data_release_summary.txt",
        "data_release_version.json"
    ]
}

version = {
    "module": "DAT-0009",
    "version": "1.0.0",
    "status": STATUS
}

(OUT/"data_release.json").write_text(json.dumps(release, indent=2))
(OUT/"data_release.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"data_release_manifest.json").write_text(json.dumps(manifest_out, indent=2))
(OUT/"data_release_version.json").write_text(json.dumps(version, indent=2))
(OUT/"data_release_ledger.jsonl").write_text(json.dumps(release) + "\n")
(OUT/"data_release_summary.txt").write_text(
f"""Data Release
------------
release_ready {release['release_ready']}
locked {release['locked']}
immutable {release['immutable']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" DAT-0009 - DATA RELEASE")
print("=" * 54)
print()
print("Running Data Release...")
print()
print("Data Release")
print("------------")
for f in manifest_out["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest_out['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
