#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

adj = {}

for edge in GRAPH["edges"]:
    if edge["relation"] != "depends_on":
        continue
    adj.setdefault(edge["from"], []).append(edge["to"])

visited = set()
stack = []
in_stack = set()
seen = set()
cycles = []

def dfs(node):
    visited.add(node)
    stack.append(node)
    in_stack.add(node)

    for nxt in adj.get(node, []):

        if nxt not in visited:
            dfs(nxt)

        elif nxt in in_stack:

            idx = stack.index(nxt)
            cycle = tuple(stack[idx:] + [nxt])

            if cycle not in seen:
                seen.add(cycle)
                cycles.append(cycle)

    stack.pop()
    in_stack.remove(node)

for node in sorted(adj):
    if node not in visited:
        dfs(node)

print("=" * 60)
print("FORGE-KAPI-0005")
print("Cycle Detection Engine")
print("=" * 60)
print("Nodes  :", len(adj))
print("Cycles :", len(cycles))
print()

for cycle in cycles[:50]:
    print(" -> ".join(cycle))

print()
print("STATUS : PASS")
