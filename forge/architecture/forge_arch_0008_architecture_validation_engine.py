#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX_FILE = ROOT / "runtime" / "architecture" / "module_index.json"
DEPENDENCY_FILE = ROOT / "runtime" / "architecture" / "module_dependency_index.json"
GRAPH_FILE = ROOT / "runtime" / "architecture" / "architecture_dependency_graph.json"
METRICS_FILE = ROOT / "runtime" / "architecture" / "architecture_metrics.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_validation.json"

index = json.loads(INDEX_FILE.read_text())
dependency = json.loads(DEPENDENCY_FILE.read_text())
graph = json.loads(GRAPH_FILE.read_text())
metrics = json.loads(METRICS_FILE.read_text())

checks = {
    "module_count_match":
        index["module_count"] ==
        dependency["module_count"] ==
        graph["module_count"] ==
        metrics["module_count"],

    "family_count_match":
        index["family_count"] ==
        dependency["family_count"] ==
        graph["family_count"] ==
        metrics["family_count"],

    "unique_module_count_match":
        dependency["unique_module_count"] ==
        graph["unique_module_count"] ==
        metrics["unique_module_count"],

    "graph_nodes_match":
        graph["node_count"] == len(graph["graph"]["nodes"]),

    "graph_edges_match":
        graph["edge_count"] == len(graph["graph"]["edges"]),
}

result = {
    "module": "FORGE-ARCH-0008",
    "status": "PASS" if all(checks.values()) else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "checks": checks,
    "passed": sum(checks.values()),
    "total": len(checks),
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0008")
print("Architecture Validation Engine")
print("=" * 60)
print("Checks :", result["passed"], "/", result["total"])
print("Status :", result["status"])
print("Output :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
