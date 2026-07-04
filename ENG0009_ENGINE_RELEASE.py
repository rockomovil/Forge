#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "engine_lock" / "engine_lock.json"
OUT = ROOT / "engine_release"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "ENG0009_ENGINE_RELEASE_READY"

lock = json.loads(INPUT.read_text())

release = {
    "module": "ENG-0009",
    "name": "Engine Release",
    "status": STATUS,
    "released": lock["locked"],
    "all_checks_passed": lock["all_checks_passed"],
    "audit_score": lock["audit_score"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "engine_release.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

release["engine_release_hash"] = hashlib.sha256(
    json.dumps(release, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object"
}

manifest = {
    "module": "ENG-0009",
    "status": STATUS,
    "generated_files": [
        "engine_release.json",
        "engine_release.schema.json",
        "engine_release_manifest.json",
        "engine_release_ledger.jsonl",
        "engine_release_summary.txt",
        "engine_release_version.json"
    ]
}

version = {
    "module": "ENG-0009",
    "version": "1.0.0",
    "status": STATUS
}

(OUT / "engine_release.json").write_text(json.dumps(release, indent=2))
(OUT / "engine_release.schema.json").write_text(json.dumps(schema, indent=2))
(OUT / "engine_release_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT / "engine_release_version.json").write_text(json.dumps(version, indent=2))
(OUT / "engine_release_ledger.jsonl").write_text(json.dumps(release) + "\n")
(OUT / "engine_release_summary.txt").write_text(
f"""Engine Release
--------------
released {release['released']}
audit_score {release['audit_score']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" ENG-0009 - ENGINE RELEASE")
print("=" * 54)
print()
print("Running Engine Release...")
print()
print("Engine Release")
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
