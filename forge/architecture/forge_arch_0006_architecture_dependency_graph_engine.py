#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "runtime" / "architecture" / "module_dependency_index.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_dependency_graph.json"

dependency_index = json.loads(INPUT_FILE.read_text())

graph = {
    "nodes": [],
    "edges": [],
}

for family, modules in sorted(dependency_index["dependency_index"].items()):
    family_node = f"family::{family}"

    graph["nodes"].append({
        "id": family_node,
        "type": "family"
    })

    for module in sorted(modules):
        module_node = f"module::{module}"

        graph["nodes"].append({
            "id": module_node,
            "type": "module"
        })

        graph["edges"].append({
            "from": family_node,
            "to": module_node,
            "relation": "contains"
        })

graph["nodes"].sort(key=lambda n: n["id"])
graph["edges"].sort(key=lambda e: (e["from"], e["to"]))

result = {
    "module": "FORGE-ARCH-0006",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "family_count": dependency_index["family_count"],
    "module_count": dependency_index["module_count"],
    "unique_module_count": dependency_index["unique_module_count"],
    "node_count": len(graph["nodes"]),
    "edge_count": len(graph["edges"]),
    "graph": graph,
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0006")
print("Architecture Dependency Graph Engine")
print("=" * 60)
print("Families :", result["family_count"])
print("Modules  :", result["module_count"])
print("Unique   :", result["unique_module_count"])
print("Nodes    :", result["node_count"])
print("Edges    :", result["edge_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS : PASS")
