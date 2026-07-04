#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "architecture_lock" / "architecture_lock.json"
OUT = ROOT / "architecture_manifest"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "ARC0008_ARCHITECTURE_MANIFEST_READY"

lock = json.loads(INPUT.read_text())

manifest = {
    "module": "ARC-0008",
    "name": "Architecture Manifest",
    "status": STATUS,
    "locked": lock["locked"],
    "immutable": lock["immutable"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "architecture_manifest.json"),
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "artifacts": [
        "architecture_manifest.json",
        "architecture_manifest.schema.json",
        "architecture_manifest_index.json",
        "architecture_manifest_ledger.jsonl",
        "architecture_manifest_summary.txt",
        "architecture_manifest_version.json"
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
    "module": "ARC-0008",
    "artifact_count": len(manifest["artifacts"]),
    "artifacts": manifest["artifacts"],
    "manifest_hash": manifest["manifest_hash"]
}

version = {
    "module": "ARC-0008",
    "version": "1.0.0",
    "status": STATUS
}

(OUT/"architecture_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"architecture_manifest.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"architecture_manifest_index.json").write_text(json.dumps(index, indent=2))
(OUT/"architecture_manifest_version.json").write_text(json.dumps(version, indent=2))
(OUT/"architecture_manifest_ledger.jsonl").write_text(json.dumps(manifest) + "\n")
(OUT/"architecture_manifest_summary.txt").write_text(
f"""Architecture Manifest
-----------------------
artifact_count {len(manifest['artifacts'])}
locked {manifest['locked']}
immutable {manifest['immutable']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" ARC-0008 - ARCHITECTURE MANIFEST")
print("=" * 54)
print()
print("Running Architecture Manifest...")
print()
print("Architecture Manifest")
print("---------------------")
for f in manifest["artifacts"]:
    print(f)
print()
print(f"Generated : {len(manifest['artifacts'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
