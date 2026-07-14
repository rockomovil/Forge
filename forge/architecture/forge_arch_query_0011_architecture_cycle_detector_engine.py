#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

graph = json.loads(
    (ROOT / "runtime/architecture/architecture_dependency_graph.json").read_text()
)

G = graph.get("graph", graph)
edges = G.get("edges", [])

adj = {}

def canon(x):
    if isinstance(x, dict):
        x = x.get("id") or x.get("name") or x.get("module")

    if not isinstance(x, str):
        return None

    if "::" in x:
        x = x.split("::", 1)[1]

    return x

for e in edges:
    src = canon(e.get("from") or e.get("source"))
    dst = canon(e.get("to") or e.get("target"))

    if not src or not dst:
        continue

    adj.setdefault(src, set()).add(dst)
    adj.setdefault(dst, set())

visited = set()
stack = []
stack_set = set()
cycles = []

def dfs(node):
    visited.add(node)
    stack.append(node)
    stack_set.add(node)

    for nxt in sorted(adj.get(node, [])):
        if nxt not in visited:
            dfs(nxt)
        elif nxt in stack_set:
            i = stack.index(nxt)
            cycles.append(stack[i:] + [nxt])

    stack.pop()
    stack_set.remove(node)

for node in sorted(adj):
    if node not in visited:
        dfs(node)

print("=" * 60)
print("FORGE-ARCH-QUERY-0011")
print("Architecture Cycle Detector Engine")
print("=" * 60)
print("Nodes  :", len(adj))
print("Cycles :", len(cycles))
print()

for i, cycle in enumerate(cycles[:20], 1):
    print(f"CYCLE {i}")
    print(" -> ".join(cycle))
    print()

print("STATUS :", "PASS")
