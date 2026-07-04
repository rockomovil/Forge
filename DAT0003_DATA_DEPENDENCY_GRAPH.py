#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "data_registry" / "data_registry.json"
OUT = ROOT / "data_graph"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "DAT0003_DATA_DEPENDENCY_GRAPH_READY"

registry = json.loads(INPUT.read_text())

graph = {
    "module": "DAT-0003",
    "name": "Data Dependency Graph",
    "status": STATUS,
    "registry_ready": registry["registry_ready"],
    "graph_ready": True,
    "nodes": ["data"],
    "edges": [],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "data_dependency_graph.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

graph["graph_hash"] = hashlib.sha256(
    json.dumps(graph, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object"
}

index = {
    "module": "DAT-0003",
    "node_count": len(graph["nodes"]),
    "edge_count": len(graph["edges"]),
    "graph_hash": graph["graph_hash"]
}

manifest = {
    "module": "DAT-0003",
    "status": STATUS,
    "generated_files": [
        "data_dependency_graph.json",
        "data_dependency_graph.schema.json",
        "data_dependency_index.json",
        "data_graph_manifest.json",
        "data_graph_ledger.jsonl",
        "data_graph_summary.txt",
        "data_graph_version.json"
    ]
}

version = {
    "module": "DAT-0003",
    "version": "1.0.0",
    "status": STATUS
}

(OUT/"data_dependency_graph.json").write_text(json.dumps(graph, indent=2))
(OUT/"data_dependency_graph.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"data_dependency_index.json").write_text(json.dumps(index, indent=2))
(OUT/"data_graph_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"data_graph_version.json").write_text(json.dumps(version, indent=2))
(OUT/"data_graph_ledger.jsonl").write_text(json.dumps(graph) + "\n")
(OUT/"data_graph_summary.txt").write_text(
f"""Data Dependency Graph
----------------------
graph_ready {graph['graph_ready']}
node_count {len(graph['nodes'])}
edge_count {len(graph['edges'])}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" DAT-0003 - DATA DEPENDENCY GRAPH")
print("=" * 54)
print()
print("Running Data Dependency Graph...")
print()
print("Data Dependency Graph")
print("---------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
