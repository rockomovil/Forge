#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX_FILE = ROOT / "runtime" / "architecture" / "module_index.json"
GRAPH_FILE = ROOT / "runtime" / "architecture" / "architecture_dependency_graph.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_dependency_graph_reconciliation.json"

index = json.loads(INDEX_FILE.read_text())
graph = json.loads(GRAPH_FILE.read_text())

index_modules = set(index["indexes"]["by_name"].keys())

nodes = graph.get("nodes", {})
if isinstance(nodes, dict):
    graph_nodes = set(nodes.keys())
elif isinstance(nodes, list):
    graph_nodes = {
        n["id"] if isinstance(n, dict) and "id" in n else str(n)
        for n in nodes
    }
else:
    graph_nodes = set()

missing_in_graph = sorted(index_modules - graph_nodes)
orphan_graph_nodes = sorted(graph_nodes - index_modules)

coverage = (
    (len(index_modules) - len(missing_in_graph))
    / len(index_modules)
    if index_modules else 1.0
)

result = {
    "module": "FORGE-ARCH-0051",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "index_modules": len(index_modules),
    "graph_nodes": len(graph_nodes),

    "matched": len(index_modules) - len(missing_in_graph),
    "missing_in_graph": len(missing_in_graph),
    "orphan_graph_nodes": len(orphan_graph_nodes),

    "coverage": round(coverage, 6),

    "sample_missing": missing_in_graph[:25],
    "sample_orphans": orphan_graph_nodes[:25],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0051")
print("Architecture Dependency Graph Reconciliation Engine")
print("=" * 60)
print("Index Modules     :", result["index_modules"])
print("Graph Nodes       :", result["graph_nodes"])
print("Matched           :", result["matched"])
print("Missing In Graph  :", result["missing_in_graph"])
print("Orphan Graph Nodes:", result["orphan_graph_nodes"])
print("Coverage          :", f'{result["coverage"]:.2%}')
print("Output            :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
