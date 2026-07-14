#!/usr/bin/env python3

from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX = json.loads(
    (ROOT/"runtime/architecture/module_index.json").read_text()
)

GRAPH = json.loads(
    (ROOT/"runtime/architecture/architecture_dependency_graph.json").read_text()
)

parser = argparse.ArgumentParser()
parser.add_argument("query")
args = parser.parse_args()

query = args.query.lower()

matches = []

for name, meta in INDEX["indexes"]["by_name"].items():
    if query in name.lower():
        matches.append((name, meta))

print("="*60)
print("FORGE-ARCH-QUERY-0003")
print("Architecture Dependency Resolver Engine")
print("="*60)

if not matches:
    print("No module found.")
    raise SystemExit(0)

for name, meta in matches:
    print(name)
    print("  Family :", meta["family"])
    print("  Path   :", meta["relative_path"])

    node = GRAPH.get("nodes", {}).get(name)

    if node is not None:
        print("  Graph  : PRESENT")
    else:
        print("  Graph  : NOT PRESENT")

    print()
