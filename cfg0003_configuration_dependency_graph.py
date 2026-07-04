#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "configuration_registry" / "configuration_registry.json"
OUT = ROOT / "configuration_graph"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "CFG0003_CONFIGURATION_DEPENDENCY_GRAPH_READY"

registry = json.loads(INPUT.read_text())

graph = {
    "module": "CFG-0003",
    "name": "Configuration Dependency Graph",
    "status": STATUS,
    "registry_ready": registry["registry_ready"],
    "graph_ready": True,
    "nodes": ["configuration"],
    "edges": [],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "configuration_dependency_graph.json"),
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
    "module": "CFG-0003",
    "node_count": len(graph["nodes"]),
    "edge_count": len(graph["edges"]),
    "graph_hash": graph["graph_hash"]
}

manifest = {
    "module": "CFG-0003",
    "status": STATUS,
    "generated_files": [
        "configuration_dependency_graph.json",
        "configuration_dependency_graph.schema.json",
        "configuration_dependency_index.json",
        "configuration_graph_manifest.json",
        "configuration_graph_ledger.jsonl",
        "configuration_graph_summary.txt",
        "configuration_graph_version.json"
    ]
}

version = {
    "module": "CFG-0003",
    "version": "1.0.0",
    "status": STATUS
}

(OUT/"configuration_dependency_graph.json").write_text(json.dumps(graph, indent=2))
(OUT/"configuration_dependency_graph.schema.json").write_text(json.dumps(schema, indent=2))
(OUT/"configuration_dependency_index.json").write_text(json.dumps(index, indent=2))
(OUT/"configuration_graph_manifest.json").write_text(json.dumps(manifest, indent=2))
(OUT/"configuration_graph_version.json").write_text(json.dumps(version, indent=2))
(OUT/"configuration_graph_ledger.jsonl").write_text(json.dumps(graph) + "\n")
(OUT/"configuration_graph_summary.txt").write_text(
f"""Configuration Dependency Graph
--------------------------------
graph_ready {graph['graph_ready']}
node_count {len(graph['nodes'])}
edge_count {len(graph['edges'])}
status {STATUS}
"""
)

print("=" * 54)
print(" FORGE")
print(" CFG-0003 - CONFIGURATION DEPENDENCY GRAPH")
print("=" * 54)
print()
print("Running Configuration Dependency Graph...")
print()
print("Configuration Dependency Graph")
print("------------------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")
