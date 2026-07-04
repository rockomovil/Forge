#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "engine_graph" / "engine_dependency_graph.json"
OUT = ROOT / "engine_validation"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "ENG0004_ENGINE_VALIDATION_READY"

graph = json.loads(INPUT.read_text())

checks = {
    "graph_ready": graph["graph_ready"],
    "node_count_valid": len(graph["nodes"]) > 0,
    "edge_count_valid": len(graph["edges"]) >= 0,
    "runtime_mode_valid": graph["runtime_mode"] == "SHADOW_ONLY_READ_ONLY"
}

validation = {
    "module": "ENG-0004",
    "name": "Engine Validation",
    "status": STATUS,
    "all_checks_passed": all(checks.values()),
    "validation_checks": checks,
    "validation_score": sum(checks.values()) / len(checks),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "engine_validation.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

validation["validation_hash"] = hashlib.sha256(
    json.dumps(validation, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "type":"object"
}

manifest = {
    "module":"ENG-0004",
    "status":STATUS,
    "generated_files":[
        "engine_validation.json",
        "engine_validation.schema.json",
        "engine_validation_manifest.json",
        "engine_validation_ledger.jsonl",
        "engine_validation_summary.txt",
        "engine_validation_version.json"
    ]
}

version = {
    "module":"ENG-0004",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"engine_validation.json").write_text(json.dumps(validation, indent=2))
(OUT/"engine_validation.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"engine_validation_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"engine_validation_version.json").write_text(json.dumps(version, indent=2))
(OUT/"engine_validation_ledger.jsonl").write_text(json.dumps(validation) + "\n")
(OUT/"engine_validation_summary.txt").write_text(
f"""Engine Validation
-----------------
validation_score {validation['validation_score']}
all_checks_passed {validation['all_checks_passed']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" ENG-0004 - ENGINE VALIDATION")
print("=" * 54)
print()
print("Running Engine Validation...")
print()
print("Engine Validation")
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

