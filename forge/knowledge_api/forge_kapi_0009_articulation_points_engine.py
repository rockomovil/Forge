#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

adj = defaultdict(set)
nodes = set()

for edge in GRAPH["edges"]:

    if edge["relation"] != "depends_on":
        continue

    u = edge["from"]
    v = edge["to"]

    nodes.add(u)
    nodes.add(v)

    # Grafo no dirigido para detectar puntos de articulación
    adj[u].add(v)
    adj[v].add(u)

disc = {}
low = {}
parent = {}
visited = set()
articulation = set()
time = 0

def dfs(u):
    global time

    visited.add(u)
    disc[u] = time
    low[u] = time
    time += 1

    children = 0

    for v in sorted(adj[u]):

        if v not in visited:

            parent[v] = u
            children += 1

            dfs(v)

            low[u] = min(low[u], low[v])

            if u not in parent and children > 1:
                articulation.add(u)

            if u in parent and low[v] >= disc[u]:
                articulation.add(u)

        elif parent.get(u) != v:
            low[u] = min(low[u], disc[v])

for node in sorted(nodes):
    if node not in visited:
        dfs(node)

ranking = []

for node in sorted(articulation):
    ranking.append({
        "node": node,
        "degree": len(adj[node])
    })

ranking.sort(
    key=lambda x: (x["degree"], x["node"]),
    reverse=True
)

report = {
    "module": "FORGE-KAPI-0009",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "nodes": len(nodes),
    "articulation_points": len(ranking),
    "ranking": ranking
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_articulation_points.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0009")
print("Articulation Points Engine")
print("=" * 60)
print("Nodes                :", len(nodes))
print("Critical Modules     :", len(ranking))
print()

print("TOP 20\n")

for item in ranking[:20]:
    print(f'{item["degree"]:4d}  {item["node"]}')

print()
print("Output :", outfile)
print()
print("STATUS : PASS")
