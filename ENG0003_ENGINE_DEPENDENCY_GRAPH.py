#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

INPUT = ROOT / "engine_registry" / "engine_registry.json"
OUT = ROOT / "engine_graph"
OUT.mkdir(parents=True, exist_ok=True)

STATUS = "ENG0003_ENGINE_DEPENDENCY_GRAPH_READY"

registry = json.loads(INPUT.read_text())

graph = {
    "module": "ENG-0003",
    "name": "Engine Dependency Graph",
    "status": STATUS,
    "registry_ready": registry["registry_ready"],
    "graph_ready": True,
    "nodes": ["engine"],
    "edges": [],
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "canonical_input": str(INPUT),
    "canonical_output": str(OUT / "engine_dependency_graph.json"),
    "generated_at": datetime.now(timezone.utc).isoformat()
}

graph["graph_hash"] = hashlib.sha256(
    json.dumps(graph, sort_keys=True).encode()
).hexdigest()

schema = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "type":"object"
}

index = {
    "module":"ENG-0003",
    "node_count":len(graph["nodes"]),
    "edge_count":len(graph["edges"]),
    "graph_hash":graph["graph_hash"]
}

manifest = {
    "module":"ENG-0003",
    "status":STATUS,
    "generated_files":[
        "engine_dependency_graph.json",
        "engine_dependency_graph.schema.json",
        "engine_dependency_index.json",
        "engine_graph_manifest.json",
        "engine_graph_ledger.jsonl",
        "engine_graph_summary.txt",
        "engine_graph_version.json"
    ]
}

version = {
    "module":"ENG-0003",
    "version":"1.0.0",
    "status":STATUS
}

(OUT/"engine_dependency_graph.json").write_text(json.dumps(graph,indent=2))
(OUT/"engine_dependency_graph.schema.json").write_text(json.dumps(schema,indent=2))
(OUT/"engine_dependency_index.json").write_text(json.dumps(index,indent=2))
(OUT/"engine_graph_manifest.json").write_text(json.dumps(manifest,indent=2))
(OUT/"engine_graph_version.json").write_text(json.dumps(version,indent=2))
(OUT/"engine_graph_ledger.jsonl").write_text(json.dumps(graph)+"\n")
(OUT/"engine_graph_summary.txt").write_text(
f"""Engine Dependency Graph
------------------------
graph_ready {graph['graph_ready']}
node_count {len(graph['nodes'])}
edge_count {len(graph['edges'])}
status {STATUS}
"""
)

print("="*54)
print(" FORGE")
print(" ENG-0003 - ENGINE DEPENDENCY GRAPH")
print("="*54)
print()
print("Running Engine Dependency Graph...")
print()
print("Engine Dependency Graph")
print("-----------------------")
for f in manifest["generated_files"]:
    print(f)
print()
print(f"Generated : {len(manifest['generated_files'])}")
print(f"Output    : {OUT}")
print()
print(f"STATUS : {STATUS}")
print()
print(f"STATUS : {STATUS}")

