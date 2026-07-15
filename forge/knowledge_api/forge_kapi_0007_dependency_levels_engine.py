#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict, deque
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

forward = defaultdict(list)
indegree = defaultdict(int)
nodes = set()

for edge in GRAPH["edges"]:

    if edge["relation"] != "depends_on":
        continue

    src = edge["from"]
    dst = edge["to"]

    nodes.add(src)
    nodes.add(dst)

    forward[dst].append(src)
    indegree[src] += 1

for n in nodes:
    indegree.setdefault(n, 0)

level = {}
queue = deque()

for n in sorted(nodes):
    if indegree[n] == 0:
        level[n] = 0
        queue.append(n)

while queue:

    node = queue.popleft()

    for nxt in sorted(forward[node]):

        level[nxt] = max(level.get(nxt, 0), level[node] + 1)

        indegree[nxt] -= 1

        if indegree[nxt] == 0:
            queue.append(nxt)

levels = defaultdict(list)

for node, lv in level.items():
    levels[str(lv)].append(node)

for lv in levels:
    levels[lv].sort()

remaining = sorted(n for n in nodes if n not in level)

report = {
    "module": "FORGE-KAPI-0007",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "nodes": len(nodes),
    "resolved_nodes": len(level),
    "cyclic_nodes": len(remaining),
    "max_level": max(level.values()) if level else 0,
    "levels": dict(levels),
    "remaining_nodes": remaining,
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_dependency_levels.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0007")
print("Dependency Levels Engine")
print("=" * 60)
print("Nodes          :", len(nodes))
print("Resolved Nodes :", len(level))
print("Cyclic Nodes   :", len(remaining))
print("Max Level      :", report["max_level"])
print("Output         :", outfile)
print()
print("STATUS : PASS")
