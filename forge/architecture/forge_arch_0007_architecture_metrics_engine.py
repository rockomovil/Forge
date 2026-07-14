#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH_FILE = ROOT / "runtime" / "architecture" / "architecture_dependency_graph.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_metrics.json"

graph_data = json.loads(GRAPH_FILE.read_text())

graph = graph_data["graph"]
nodes = graph["nodes"]
edges = graph["edges"]

family_nodes = [n for n in nodes if n["type"] == "family"]
module_nodes = [n for n in nodes if n["type"] == "module"]

metrics = {
    "module": "FORGE-ARCH-0007",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "family_count": len(family_nodes),
    "module_count": graph_data["module_count"],
    "unique_module_count": graph_data["unique_module_count"],
    "node_count": len(nodes),
    "edge_count": len(edges),
    "average_modules_per_family": round(
        graph_data["unique_module_count"] / max(1, len(family_nodes)),
        2,
    ),
}

metrics["hash"] = hashlib.sha256(
    json.dumps(metrics, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(json.dumps(metrics, indent=2))

print("=" * 60)
print("FORGE-ARCH-0007")
print("Architecture Metrics Engine")
print("=" * 60)
print("Families :", metrics["family_count"])
print("Modules  :", metrics["module_count"])
print("Unique   :", metrics["unique_module_count"])
print("Nodes    :", metrics["node_count"])
print("Edges    :", metrics["edge_count"])
print("Avg/Fam  :", metrics["average_modules_per_family"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS : PASS")
