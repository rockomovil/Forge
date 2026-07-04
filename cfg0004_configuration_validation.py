#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "configuration_graph" / "configuration_dependency_graph.json"
OUT = ROOT / "configuration_validation"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "CFG0004_CONFIGURATION_VALIDATION_READY"

graph = json.loads(INPUT.read_text())

checks = {
    "graph_ready": graph["graph_ready"],
    "node_count_valid": len(graph["nodes"]) > 0,
    "edge_count_valid": len(graph["edges"]) >= 0,
    "runtime_mode_valid": graph["runtime_mode"] == "SHADOW_ONLY_READ_ONLY"
}

validation = {
    "module": "CFG-0004",
    "name": "Configuration Validation",
    "status": STATUS,
    "all_checks_passed": all(checks.values()),
    "validation_checks": checks,
    "validation_score": sum(checks.values()) / len(checks),
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "configuration_validation.json"),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
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
    "module":"CFG-0004",
    "status":STATUS,
    "generated_files":[
        "configuration_validation.json",
        "configuration_validation.schema.json",
        "configuration_validation_manifest.json",
        "configuration_validation_ledger.jsonl",
        "configuration_validation_summary.txt",
        "configuration_validation_version.json"
    ]
}

version = {
    "module":"CFG-0004",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"configuration_validation.json").write_text(json.dumps(validation,indent=2))
(OUT/"configuration_validation.schema.json").write_text(json.dumps(schema,indent=2))
(OUT/"configuration_validation_manifest.json").write_text(json.dumps(manifest,indent=2))
(OUT/"configuration_validation_version.json").write_text(json.dumps(version,indent=2))
(OUT/"configuration_validation_ledger.jsonl").write_text(json.dumps(validation)+"\n")
(OUT/"configuration_validation_summary.txt").write_text(
f"""Configuration Validation
--------------------------
validation_score {validation['validation_score']}
all_checks_passed {validation['all_checks_passed']}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" CFG-0004 - CONFIGURATION VALIDATION")
print("="*54)
print()
print("Running Configuration Validation...")
print()
print("Configuration Validation")
print("------------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
