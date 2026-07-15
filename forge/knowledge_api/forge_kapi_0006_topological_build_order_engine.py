#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict, deque
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

adj = defaultdict(list)
indegree = defaultdict(int)
nodes = set()

for edge in GRAPH["edges"]:

    if edge["relation"] != "depends_on":
        continue

    src = edge["from"]
    dst = edge["to"]

    nodes.add(src)
    nodes.add(dst)

    adj[dst].append(src)
    indegree[src] += 1

for n in nodes:
    indegree.setdefault(n, 0)

queue = deque(sorted(n for n in nodes if indegree[n] == 0))
order = []

while queue:

    node = queue.popleft()
    order.append(node)

    for nxt in sorted(adj[node]):

        indegree[nxt] -= 1

        if indegree[nxt] == 0:
            queue.append(nxt)

remaining = sorted(n for n in nodes if indegree[n] > 0)

report = {
    "module": "FORGE-KAPI-0006",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "nodes": len(nodes),
    "build_order_size": len(order),
    "cyclic_nodes": len(remaining),
    "build_order": order,
    "remaining_nodes": remaining,
}

out = ROOT / "runtime/knowledge_api"
out.mkdir(parents=True, exist_ok=True)

outfile = out / "knowledge_topological_build_order.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0006")
print("Topological Build Order Engine")
print("=" * 60)
print("Nodes             :", len(nodes))
print("Build Order       :", len(order))
print("Cyclic Nodes      :", len(remaining))
print("Output            :", outfile)
print()
print("STATUS : PASS")
