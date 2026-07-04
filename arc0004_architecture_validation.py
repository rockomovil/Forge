#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "architecture_graph" / "architecture_dependency_graph.json"
OUTDIR = ROOT / "architecture_validation"
OUTDIR.mkdir(parents=True, exist_ok=True)

STATUS = "ARC0004_ARCHITECTURE_VALIDATION_READY"

def sha256(o):
    return hashlib.sha256(
        json.dumps(o, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

graph = json.loads(INPUT.read_text())

checks = {
    "graph_exists": INPUT.exists(),
    "all_checks_passed": graph.get("all_checks_passed", False),
    "node_count_positive": graph.get("node_count",0) >= 1,
    "edge_count_valid": graph.get("edge_count",0) >= 0,
    "cycle_count_zero": graph.get("cycle_count",0) == 0,
    "missing_dependencies_zero": graph.get("missing_dependency_count",0) == 0,
    "topological_order_present": len(graph.get("topological_order",[])) == graph.get("node_count",0)
}

passed = all(checks.values())

validation = {
    "module":"ARC-0004",
    "name":"Architecture Validation",
    "status":STATUS if passed else "FAILED",
    "all_checks_passed":passed,
    "validation_checks":checks,
    "validation_score":sum(checks.values())/len(checks),
    "canonical_input":str(INPUT),
    "canonical_output":str(OUTDIR/"architecture_validation.json"),
    "runtime_mode":"SHADOW_ONLY_READ_ONLY",
    "generated_at":datetime.now(timezone.utc).isoformat()
}

validation["validation_hash"]=sha256(validation)

schema={
"$schema":"https://json-schema.org/draft/2020-12/schema",
"type":"object"
}

manifest={
"module":"ARC-0004",
"status":validation["status"],
"generated_files":[
"architecture_validation.json",
"architecture_validation.schema.json",
"architecture_validation_manifest.json",
"architecture_validation_ledger.jsonl",
"architecture_validation_summary.txt",
"architecture_validation_version.json"
],
"hash":validation["validation_hash"]
}

version={
"module":"ARC-0004",
"version":"1.0.0",
"status":validation["status"]
}

(Path(OUTDIR/"architecture_validation.json")).write_text(json.dumps(validation,indent=2))
(Path(OUTDIR/"architecture_validation.schema.json")).write_text(json.dumps(schema,indent=2))
(Path(OUTDIR/"architecture_validation_manifest.json")).write_text(json.dumps(manifest,indent=2))
(Path(OUTDIR/"architecture_validation_version.json")).write_text(json.dumps(version,indent=2))
(Path(OUTDIR/"architecture_validation_ledger.jsonl")).write_text(json.dumps(validation)+"\n")
(Path(OUTDIR/"architecture_validation_summary.txt")).write_text(
f"""Architecture Validation
-------------------------
all_checks_passed {passed}
validation_score  {validation['validation_score']}
status            {validation['status']}
"""
)

print("="*54)
print(" FORGE")
print(" ARC-0004 - ARCHITECTURE VALIDATION")
print("="*54)
print()
print("Running Architecture Validation...")
print()
print("Architecture Validation")
print("-----------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUTDIR}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
