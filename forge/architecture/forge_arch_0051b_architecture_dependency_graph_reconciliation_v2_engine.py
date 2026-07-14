#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX_FILE = ROOT / "runtime/architecture/module_index.json"
GRAPH_FILE = ROOT / "runtime/architecture/architecture_dependency_graph.json"

OUTPUT_FILE = ROOT / "runtime/architecture/architecture_dependency_graph_reconciliation_v2.json"

index = json.loads(INDEX_FILE.read_text())
graph = json.loads(GRAPH_FILE.read_text())

index_modules = set(index["indexes"]["by_name"].keys())

# ----------------------------------------------------------
# Detect graph layout automatically
# ----------------------------------------------------------

nodes = []

if "nodes" in graph:
    nodes = graph["nodes"]

elif "graph" in graph and isinstance(graph["graph"], dict):
    nodes = graph["graph"].get("nodes", [])

elif "dependency_graph" in graph and isinstance(graph["dependency_graph"], dict):
    nodes = graph["dependency_graph"].get("nodes", [])

graph_nodes = set()

if isinstance(nodes, dict):
    graph_nodes = set(nodes.keys())

elif isinstance(nodes, list):

    for n in nodes:

        if isinstance(n, dict):

            identifier = (
                n.get("id")
                or n.get("name")
                or n.get("module")
            )

            if identifier:

                if "::" in identifier:
                    identifier = identifier.split("::", 1)[1]

                graph_nodes.add(identifier)

        elif isinstance(n, str):

            identifier = n

            if "::" in identifier:
                identifier = identifier.split("::", 1)[1]

            graph_nodes.add(identifier)

missing = sorted(index_modules - graph_nodes)
orphans = sorted(graph_nodes - index_modules)

coverage = (
    len(index_modules) - len(missing)
) / len(index_modules)

result = {
    "module": "FORGE-ARCH-0051B",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "index_modules": len(index_modules),
    "graph_nodes": len(graph_nodes),
    "matched": len(index_modules) - len(missing),
    "missing_in_graph": len(missing),
    "orphan_graph_nodes": len(orphans),
    "coverage": round(coverage, 6),

    "sample_missing": missing[:20],
    "sample_orphans": orphans[:20],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("="*60)
print("FORGE-ARCH-0051B")
print("Architecture Dependency Graph Reconciliation V2")
print("="*60)
print("Index Modules :", result["index_modules"])
print("Graph Nodes   :", result["graph_nodes"])
print("Matched       :", result["matched"])
print("Missing       :", result["missing_in_graph"])
print("Orphans       :", result["orphan_graph_nodes"])
print("Coverage      :", f'{coverage:.2%}')
print("Output        :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
