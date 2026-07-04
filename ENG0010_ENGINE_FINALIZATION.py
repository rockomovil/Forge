#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "engine_release" / "engine_release.json"
OUT = ROOT / "engine_finalization"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "ENG0010_ENGINE_FINALIZATION_READY"

release = json.loads(INPUT.read_text())

finalization = {
    "module": "ENG-0010",
    "name": "Engine Finalization",
    "status": STATUS,
    "finalized": release["released"],
    "all_checks_passed": release["all_checks_passed"],
    "audit_score": release["audit_score"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "engine_finalization.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

finalization["engine_finalization_hash"] = hashlib.sha256(
    json.dumps(finalization, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object"
}

manifest = {
    "module": "ENG-0010",
    "status": STATUS,
    "generated_files": [
        "engine_finalization.json",
        "engine_finalization.schema.json",
        "engine_finalization_manifest.json",
        "engine_finalization_ledger.jsonl",
        "engine_finalization_summary.txt",
        "engine_finalization_version.json"
    ]
}

version = {
    "module": "ENG-0010",
    "version": "1.0.0",
    "status": STATUS
}

(OUT / "engine_finalization.json").write_text(json.dumps(finalization, indent=2))
(OUT / "engine_finalization.schema.json").write_text(json.dumps(schema, indent=2))
(OUT / "engine_finalization_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT / "engine_finalization_version.json").write_text(json.dumps(version, indent=2))
(OUT / "engine_finalization_ledger.jsonl").write_text(json.dumps(finalization) + "\n")
(OUT / "engine_finalization_summary.txt").write_text(
f"""Engine Finalization
---------------------
finalized {finalization['finalized']}
audit_score {finalization['audit_score']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" ENG-0010 - ENGINE FINALIZATION")
print("=" * 54)
print()
print("Running Engine Finalization...")
print()
print("Engine Finalization")
print("-------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
