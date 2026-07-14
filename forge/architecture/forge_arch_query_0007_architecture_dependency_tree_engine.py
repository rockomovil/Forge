#!/usr/bin/env python3

from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]

graph = json.loads(
    (ROOT/"runtime/architecture/architecture_dependency_graph.json").read_text()
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
        x = x.split("::",1)[1]
    return x

for e in edges:
    s = canon(e.get("from") or e.get("source"))
    t = canon(e.get("to") or e.get("target"))
    if s and t:
        adj.setdefault(s, []).append(t)

parser = argparse.ArgumentParser()
parser.add_argument("module")
args = parser.parse_args()

visited = set()

def walk(node, depth=0):
    if node in visited:
        return
    visited.add(node)
    print("  " * depth + node)
    for child in sorted(adj.get(node, [])):
        walk(child, depth + 1)

print("=" * 60)
print("FORGE-ARCH-QUERY-0007")
print("Architecture Dependency Tree Engine")
print("=" * 60)

walk(canon(args.module))
