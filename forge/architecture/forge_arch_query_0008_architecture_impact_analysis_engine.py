#!/usr/bin/env python3

from pathlib import Path
import argparse
import json

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

module = canon(args.module)

affected = set()

stack = [module]

while stack:
    current = stack.pop()

    for dep in reverse.get(current, []):
        if dep not in affected:
            affected.add(dep)
            stack.append(dep)

print("=" * 60)
print("FORGE-ARCH-QUERY-0008")
print("Architecture Impact Analysis Engine")
print("=" * 60)
print("Module          :", module)
print("Affected Modules:", len(affected))
print()

for dep in sorted(affected):
    print(dep)

print()
print("STATUS : PASS")
