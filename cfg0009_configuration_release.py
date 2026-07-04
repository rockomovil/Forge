#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "configuration_manifest" / "configuration_manifest.json"
OUT = ROOT / "configuration_release"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "CFG0009_CONFIGURATION_RELEASE_READY"

manifest = json.loads(INPUT.read_text())

release = {
    "module": "CFG-0009",
    "name": "Configuration Release",
    "status": STATUS,
    "release_ready": True,
    "locked": manifest["locked"],
    "immutable": manifest["immutable"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "configuration_release.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

release["release_hash"] = hashlib.sha256(
    json.dumps(release, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "type":"object"
}

manifest_out = {
    "module":"CFG-0009",
    "status":STATUS,
    "generated_files":[
        "configuration_release.json",
        "configuration_release.schema.json",
        "configuration_release_manifest.json",
        "configuration_release_ledger.jsonl",
        "configuration_release_summary.txt",
        "configuration_release_version.json"
    ]
}

version = {
    "module":"CFG-0009",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"configuration_release.json").write_text(json.dumps(release, indent=2))
(OUT/"configuration_release.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"configuration_release_manifest.json").write_text(json.dumps(manifest_out, indent=2))
(OUT/"configuration_release_version.json").write_text(json.dumps(version, indent=2))
(OUT/"configuration_release_ledger.jsonl").write_text(json.dumps(release) + "\n")
(OUT/"configuration_release_summary.txt").write_text(
f"""Configuration Release
-----------------------
release_ready {release['release_ready']}
locked {release['locked']}
immutable {release['immutable']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" CFG-0009 - CONFIGURATION RELEASE")
print("="*54)
print()
print("Running Configuration Release...")
print()
print("Configuration Release")
print("---------------------")
for f in manifest_out["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest_out['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
