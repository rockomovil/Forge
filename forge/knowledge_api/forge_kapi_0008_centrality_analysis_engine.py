#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

out_degree = defaultdict(int)
in_degree = defaultdict(int)
nodes = set()

for edge in GRAPH["edges"]:

    if edge["relation"] != "depends_on":
        continue

    src = edge["from"]
    dst = edge["to"]

    nodes.add(src)
    nodes.add(dst)

    out_degree[src] += 1
    in_degree[dst] += 1

report = []

for node in nodes:

    report.append({
        "node": node,
        "out_degree": out_degree[node],
        "in_degree": in_degree[node],
        "total_degree": out_degree[node] + in_degree[node]
    })

report.sort(
    key=lambda x: (
        x["total_degree"],
        x["out_degree"],
        x["in_degree"]
    ),
    reverse=True
)

result = {
    "module": "FORGE-KAPI-0008",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "nodes": len(nodes),
    "dependency_edges": sum(out_degree.values()),
    "ranking": report,
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_centrality_analysis.json"
outfile.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-KAPI-0008")
print("Centrality Analysis Engine")
print("=" * 60)
print("Nodes        :", len(nodes))
print("Edges        :", result["dependency_edges"])
print()

print("TOP 20 MODULES\n")

for item in report[:20]:
    print(
        f'{item["total_degree"]:4d}  '
        f'OUT={item["out_degree"]:3d}  '
        f'IN={item["in_degree"]:3d}  '
        f'{item["node"]}'
    )

print()
print("Output :", outfile)
print()
print("STATUS : PASS")
