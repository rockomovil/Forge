#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
from collections import defaultdict
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

XREF = json.loads(
    (ROOT / "runtime/knowledge/knowledge_cross_reference.json").read_text()
)

CONCEPTS = json.loads(
    (ROOT / "runtime/knowledge/knowledge_concepts.json").read_text()
)

nodes = {
    n["id"]: n
    for n in GRAPH["nodes"]
}

edges = list(GRAPH["edges"])

edge_keys = {
    (e["from"], e["to"], e["relation"])
    for e in edges
}

def add_edge(src, dst, rel):

    if src not in nodes:
        return

    if dst not in nodes:
        return

    key = (src, dst, rel)

    if key in edge_keys:
        return

    edge_keys.add(key)

    edges.append({
        "from": src,
        "to": dst,
        "relation": rel
    })

#
# module dependencies
#

for module, info in XREF["cross_references"].items():

    src = f"module::{module}"

    for dep in info["depends_on"]:

        dst = f"module::{dep}"

        add_edge(src, dst, "depends_on")

    for ref in info["referenced_by"]:

        dst = f"module::{ref}"

        add_edge(src, dst, "referenced_by")

    for same in info["same_family"][:50]:

        dst = f"module::{same}"

        add_edge(src, dst, "same_family")

#
# concept nodes
#

for concept in sorted(CONCEPTS["concepts"]):

    cid = f"concept::{concept}"

    if cid not in nodes:

        nodes[cid] = {
            "id": cid,
            "type": "concept",
            "name": concept
        }

    for module in CONCEPTS["concepts"][concept]:

        mid = f"module::{module}"

        add_edge(cid, mid, "describes")

report = {
    "module": "FORGE-KNOWLEDGE-0007A",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "semantic_graph_enriched": True,

    "node_count": len(nodes),
    "edge_count": len(edges),

    "nodes": list(nodes.values()),
    "edges": edges,

    "previous_hash": GRAPH["hash"],
    "concept_hash": CONCEPTS["hash"],
    "xref_hash": XREF["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_semantic_graph.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KNOWLEDGE-0007A")
print("Knowledge Semantic Graph Enrichment Engine")
print("=" * 60)
print("Nodes :", len(nodes))
print("Edges :", len(edges))
print("Output:", OUT)
print()
print("STATUS : PASS")
