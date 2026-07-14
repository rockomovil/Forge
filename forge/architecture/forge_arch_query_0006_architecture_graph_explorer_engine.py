#!/usr/bin/env python3

from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/architecture/architecture_dependency_graph.json").read_text()
)

# ----------------------------------------------------------
# Locate graph structure
# ----------------------------------------------------------

if "graph" in GRAPH:
    G = GRAPH["graph"]
else:
    G = GRAPH

nodes = G.get("nodes", [])
edges = G.get("edges", [])

# ----------------------------------------------------------
# Build adjacency
# ----------------------------------------------------------

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

print("=" * 60)
print("FORGE-ARCH-QUERY-0006")
print("Architecture Graph Explorer Engine")
print("=" * 60)
print("Module:", module)
print()

print("Outgoing:", len(forward.get(module, [])))
for x in sorted(forward.get(module, [])):
    print("  ->", x)

print()

print("Incoming:", len(reverse.get(module, [])))
for x in sorted(reverse.get(module, [])):
    print("  <-", x)
