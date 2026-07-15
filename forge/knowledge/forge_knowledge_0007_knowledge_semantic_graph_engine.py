#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
from collections import defaultdict
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX = json.loads(
    (ROOT / "runtime/knowledge/knowledge_index.json").read_text()
)

XREF = json.loads(
    (ROOT / "runtime/knowledge/knowledge_cross_reference.json").read_text()
)

modules = INDEX["indexes"]["by_module"]

family_nodes = {}
module_nodes = {}
edges = []

#
# Families
#

for family in sorted(INDEX["indexes"]["by_family"]):
    node_id = f"family::{family}"

    family_nodes[node_id] = {
        "id": node_id,
        "type": "family",
        "name": family
    }

#
# Modules
#

for module_name, info in sorted(modules.items()):

    module_id = f"module::{module_name}"

    module_nodes[module_id] = {
        "id": module_id,
        "type": "module",
        "name": module_name,
        "family": info["family"]
    }

    edges.append({
        "from": f"family::{info['family']}",
        "to": module_id,
        "relation": "contains"
    })

#
# Semantic relations
#

for module_name, refs in XREF["cross_references"].items():

    src = f"module::{module_name}"

    for dep in refs["depends_on"]:

        dst = f"module::{dep}"

        if dst in module_nodes:

            edges.append({
                "from": src,
                "to": dst,
                "relation": "depends_on"
            })

    for ref in refs["referenced_by"]:

        dst = f"module::{ref}"

        if dst in module_nodes:

            edges.append({
                "from": src,
                "to": dst,
                "relation": "referenced_by"
            })

nodes = (
    list(family_nodes.values()) +
    list(module_nodes.values())
)

report = {
    "module": "FORGE-KNOWLEDGE-0007",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "semantic_graph_ready": True,

    "family_count": len(family_nodes),
    "module_count": len(module_nodes),

    "node_count": len(nodes),
    "edge_count": len(edges),

    "nodes": nodes,
    "edges": edges,

    "knowledge_hash": INDEX["hash"],
    "cross_reference_hash": XREF["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_semantic_graph.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KNOWLEDGE-0007")
print("Knowledge Semantic Graph Engine")
print("=" * 60)
print("Families :", len(family_nodes))
print("Modules  :", len(module_nodes))
print("Nodes    :", len(nodes))
print("Edges    :", len(edges))
print("Output   :", OUT)
print()
print("STATUS : PASS")
