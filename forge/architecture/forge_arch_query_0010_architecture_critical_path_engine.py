#!/usr/bin/env python3

from pathlib import Path
import argparse
import json
from collections import deque

ROOT = Path(__file__).resolve().parents[2]

graph = json.loads(
    (ROOT / "runtime/architecture/architecture_dependency_graph.json").read_text()
)

G = graph.get("graph", graph)
edges = G.get("edges", [])

forward = {}
reverse = {}

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

    forward.setdefault(src, set()).add(dst)
    reverse.setdefault(dst, set()).add(src)

parser = argparse.ArgumentParser()
parser.add_argument("module")
args = parser.parse_args()

root = canon(args.module)

visited = {root}
queue = deque([(root, 0)])

levels = {}

while queue:
    node, depth = queue.popleft()

    if depth:
        levels.setdefault(depth, []).append(node)

    for parent in sorted(reverse.get(node, [])):
        if parent not in visited:
            visited.add(parent)
            queue.append((parent, depth + 1))

print("=" * 60)
print("FORGE-ARCH-QUERY-0010")
print("Architecture Critical Path Engine")
print("=" * 60)
print("Root :", root)
print("Depth:", max(levels.keys(), default=0))
print()

for depth in sorted(levels):
    print(f"LEVEL {depth}")
    for node in sorted(levels[depth]):
        print("  ", node)
    print()

print("Critical Path Size :", len(visited) - 1)
print("STATUS : PASS")
