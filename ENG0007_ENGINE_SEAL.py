#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "engine_certification" / "engine_certification.json"
OUT = ROOT / "engine_seal"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "ENG0007_ENGINE_SEAL_READY"

cert = json.loads(INPUT.read_text())

seal = {
    "module": "ENG-0007",
    "name": "Engine Seal",
    "status": STATUS,
    "sealed": cert["certified"],
    "all_checks_passed": cert["all_checks_passed"],
    "audit_score": cert["audit_score"],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "engine_seal.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

seal["engine_seal_hash"] = hashlib.sha256(
    json.dumps(seal, sort_keys=True).encode()
).hexdigest()

schema = {
    "\$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object"
}

manifest = {
    "module": "ENG-0007",
    "status": STATUS,
    "generated_files": [
        "engine_seal.json",
        "engine_seal.schema.json",
        "engine_seal_manifest.json",
        "engine_seal_ledger.jsonl",
        "engine_seal_summary.txt",
        "engine_seal_version.json"
    ]
}

version = {
    "module": "ENG-0007",
    "version": "1.0.0",
    "status": STATUS
}

(OUT / "engine_seal.json").write_text(json.dumps(seal, indent=2))
(OUT / "engine_seal.schema.json").write_text(json.dumps(schema, indent=2))
(OUT / "engine_seal_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT / "engine_seal_version.json").write_text(json.dumps(version, indent=2))
(OUT / "engine_seal_ledger.jsonl").write_text(json.dumps(seal) + "\n")
(OUT / "engine_seal_summary.txt").write_text(
f"""Engine Seal
-----------
sealed {seal['sealed']}
audit_score {seal['audit_score']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" ENG-0007 - ENGINE SEAL")
print("=" * 54)
print()
print("Running Engine Seal...")
print()
print("Engine Seal")
print("-----------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
