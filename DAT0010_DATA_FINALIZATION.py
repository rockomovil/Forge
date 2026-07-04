#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "data_release" / "data_release.json"
OUT = ROOT / "data_finalization"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "DAT0010_DATA_FINALIZATION_READY"

release = json.loads(INPUT.read_text())

finalization = {
    "module": "DAT-0010",
    "name": "Data Finalization",
    "status": STATUS,
    "data_finalized": True,
    "release_ready": release["release_ready"],
    "locked": release["locked"],
    "immutable": release["immutable"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "data_finalization.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

finalization["finalization_hash"] = hashlib.sha256(
    json.dumps(finalization, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "type":"object"
}

manifest = {
    "module":"DAT-0010",
    "status":STATUS,
    "generated_files":[
        "data_finalization.json",
        "data_finalization.schema.json",
        "data_finalization_manifest.json",
        "data_finalization_ledger.jsonl",
        "data_finalization_summary.txt",
        "data_finalization_version.json"
    ]
}

version = {
    "module":"DAT-0010",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"data_finalization.json").write_text(json.dumps(finalization, indent=2))
(OUT/"data_finalization.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"data_finalization_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"data_finalization_version.json").write_text(json.dumps(version, indent=2))
(OUT/"data_finalization_ledger.jsonl").write_text(json.dumps(finalization) + "\n")
(OUT/"data_finalization_summary.txt").write_text(
f"""Data Finalization
-------------------
data_finalized {finalization['data_finalized']}
release_ready {finalization['release_ready']}
locked {finalization['locked']}
immutable {finalization['immutable']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" DAT-0010 - DATA FINALIZATION")
print("=" * 54)
print()
print("Running Data Finalization...")
print()
print("Data Finalization")
print("-----------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")


if __name__ == "__main__":
    pass

