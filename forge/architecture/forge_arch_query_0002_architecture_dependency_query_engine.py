#!/usr/bin/env python3

from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = ROOT / "runtime" / "architecture" / "architecture_dependency_graph.json"

graph = json.loads(GRAPH.read_text())

nodes = graph.get("nodes", {})
edges = graph.get("edges", [])

parser = argparse.ArgumentParser()
parser.add_argument("module", help="Module name")
args = parser.parse_args()

module = args.module

outgoing = []
incoming = []

for edge in edges:
    src = edge.get("from")
    dst = edge.get("to")

    if src == module:
        outgoing.append(dst)

    if dst == module:
        incoming.append(src)

print("=" * 60)
print("FORGE-ARCH-QUERY-0002")
print("Architecture Dependency Query Engine")
print("=" * 60)
print("Module :", module)
print()

print("OUTGOING DEPENDENCIES :", len(outgoing))
for dep in sorted(outgoing):
    print("  ->", dep)

print()

print("INCOMING DEPENDENCIES :", len(incoming))
for dep in sorted(incoming):
    print("  <-", dep)

print()

if module in nodes:
    print("NODE METADATA")
    print(json.dumps(nodes[module], indent=2))
else:
    print("Module not found.")
