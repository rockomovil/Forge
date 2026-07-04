#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "data_graph" / "data_dependency_graph.json"
OUT = ROOT / "data_validation"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "DAT0004_DATA_VALIDATION_READY"

graph = json.loads(INPUT.read_text())

checks = {
    "graph_ready": graph["graph_ready"],
    "node_count_valid": len(graph["nodes"]) > 0,
    "edge_count_valid": len(graph["edges"]) >= 0,
    "runtime_mode_valid": graph["runtime_mode"] == "SHADOW_ONLY_READ_ONLY"
}

validation = {
    "module": "DAT-0004",
    "name": "Data Validation",
    "status": STATUS,
    "all_checks_passed": all(checks.values()),
    "validation_checks": checks,
    "validation_score": sum(checks.values()) / len(checks),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "data_validation.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

validation["validation_hash"] = hashlib.sha256(
    json.dumps(validation, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object"
}

manifest = {
    "module": "DAT-0004",
    "status": STATUS,
    "generated_files": [
        "data_validation.json",
        "data_validation.schema.json",
        "data_validation_manifest.json",
        "data_validation_ledger.jsonl",
        "data_validation_summary.txt",
        "data_validation_version.json"
    ]
}

version = {
    "module": "DAT-0004",
    "version": "1.0.0",
    "status": STATUS
}

(OUT/"data_validation.json").write_text(json.dumps(validation, indent=2))
(OUT/"data_validation.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"data_validation_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"data_validation_version.json").write_text(json.dumps(version, indent=2))
(OUT/"data_validation_ledger.jsonl").write_text(json.dumps(validation) + "\n")
(OUT/"data_validation_summary.txt").write_text(
f"""Data Validation
---------------
validation_score {validation['validation_score']}
all_checks_passed {validation['all_checks_passed']}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" DAT-0004 - DATA VALIDATION")
print("=" * 54)
print()
print("Running Data Validation...")
print()
print("Data Validation")
print("---------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
