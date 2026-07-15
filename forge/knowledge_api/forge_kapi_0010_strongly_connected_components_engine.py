#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

adj = defaultdict(list)
nodes = set()

for edge in GRAPH["edges"]:

    if edge["relation"] != "depends_on":
        continue

    src = edge["from"]
    dst = edge["to"]

    nodes.add(src)
    nodes.add(dst)
    adj[src].append(dst)

index = 0
stack = []
on_stack = set()
indices = {}
lowlink = {}
components = []


def strongconnect(v):
    global index

    indices[v] = index
    lowlink[v] = index
    index += 1

    stack.append(v)
    on_stack.add(v)

    for w in adj.get(v, []):

        if w not in indices:

            strongconnect(w)
            lowlink[v] = min(lowlink[v], lowlink[w])

        elif w in on_stack:

            lowlink[v] = min(lowlink[v], indices[w])

    if lowlink[v] == indices[v]:

        component = []

        while True:

            w = stack.pop()
            on_stack.remove(w)
            component.append(w)

            if w == v:
                break

        components.append(sorted(component))


for node in sorted(nodes):
    if node not in indices:
        strongconnect(node)

components.sort(key=len, reverse=True)

report = {
    "module": "FORGE-KAPI-0010",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "nodes": len(nodes),
    "components": len(components),
    "cyclic_components": sum(1 for c in components if len(c) > 1),
    "largest_component": len(components[0]) if components else 0,
    "strongly_connected_components": components
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_strongly_connected_components.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0010")
print("Strongly Connected Components Engine")
print("=" * 60)
print("Nodes               :", len(nodes))
print("Components          :", len(components))
print("Cyclic Components   :", report["cyclic_components"])
print("Largest Component   :", report["largest_component"])
print()

print("TOP 20 COMPONENTS\n")

for i, comp in enumerate(components[:20], 1):
    print(f"{i:2d}. size={len(comp):3d}")

print()
print("Output :", outfile)
print()
print("STATUS : PASS")
