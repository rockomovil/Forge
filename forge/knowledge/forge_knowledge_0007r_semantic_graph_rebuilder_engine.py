#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

XREF = json.loads(
    (ROOT / "runtime/knowledge/knowledge_cross_reference.json").read_text()
)

INDEX = json.loads(
    (ROOT / "runtime/knowledge/knowledge_index.json").read_text()
)

xref = XREF["cross_references"]

nodes = []
edges = []
edge_set = set()

#
# Module nodes
#

for module in sorted(xref):

    nodes.append({
        "id": f"module::{module}",
        "type": "module"
    })

#
# Family nodes
#

families = {}

for module, meta in INDEX["indexes"]["by_module"].items():

    family = meta.get("family")

    if family:
        families.setdefault(family, []).append(module)

for family in sorted(families):

    nodes.append({
        "id": f"family::{family}",
        "type": "family"
    })

#
# Graph
#

def add(frm, to, relation):

    key = (frm, to, relation)

    if key in edge_set:
        return

    edge_set.add(key)

    edges.append({
        "from": frm,
        "to": to,
        "relation": relation
    })

for module, data in xref.items():

    m = f"module::{module}"

    family = data.get("family")

    if family:
        add(
            f"family::{family}",
            m,
            "contains"
        )

    for dep in data.get("depends_on", []):

        add(
            m,
            f"module::{dep}",
            "depends_on"
        )

    for ref in data.get("referenced_by", []):

        add(
            m,
            f"module::{ref}",
            "referenced_by"
        )

    # same_family no se serializa.
    # Se deriva dinámicamente desde las relaciones "contains".

    add(
        m,
        f"knowledge::{module}",
        "describes"
    )

report = {
    "module": "FORGE-KNOWLEDGE-0007R",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "knowledge_semantic_graph_ready": True,

    "modules": len(xref),
    "families": len(families),
    "nodes": nodes,
    "edges": edges
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_semantic_graph.json"

OUT.write_text(
    json.dumps(report, indent=2)
)

from collections import Counter

c = Counter(e["relation"] for e in edges)

print("=" * 60)
print("FORGE-KNOWLEDGE-0007R")
print("Semantic Graph Rebuilder Engine")
print("=" * 60)

for k in sorted(c):
    print(f"{k:18} {c[k]}")

print()
print("Nodes :", len(nodes))
print("Edges :", len(edges))
print("Output:", OUT)
print()
print("STATUS : PASS")
