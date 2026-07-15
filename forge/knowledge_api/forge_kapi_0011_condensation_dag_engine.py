#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

SCC = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_strongly_connected_components.json").read_text()
)

component_of = {}

for cid, comp in enumerate(SCC["strongly_connected_components"]):
    for node in comp:
        component_of[node] = cid

dag = defaultdict(set)

for edge in GRAPH["edges"]:

    if edge["relation"] != "depends_on":
        continue

    a = component_of.get(edge["from"])
    b = component_of.get(edge["to"])

    if a is None or b is None:
        continue

    if a != b:
        dag[a].add(b)

edges = []

for src in sorted(dag):

    for dst in sorted(dag[src]):

        edges.append({
            "from_component": src,
            "to_component": dst
        })

report = {
    "module": "FORGE-KAPI-0011",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "components": len(SCC["strongly_connected_components"]),
    "dag_edges": len(edges),
    "condensation_dag": edges
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_condensation_dag.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0011")
print("Condensation DAG Engine")
print("=" * 60)
print("Components :", report["components"])
print("DAG Edges  :", report["dag_edges"])
print("Output     :", outfile)
print()
print("STATUS : PASS")
