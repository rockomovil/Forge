#!/usr/bin/env python3

from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX = json.loads(
    (ROOT / "runtime/architecture/module_index.json").read_text()
)

GRAPH = json.loads(
    (ROOT / "runtime/architecture/architecture_dependency_graph.json").read_text()
)

by_name = INDEX["indexes"]["by_name"]
nodes = GRAPH.get("nodes", {})

parser = argparse.ArgumentParser()
parser.add_argument("query")
args = parser.parse_args()

query = args.query.lower()

matches = []

for name, meta in by_name.items():

    score = 0

    if query == name.lower():
        score += 100

    if query in name.lower():
        score += 50

    if query in meta["relative_path"].lower():
        score += 25

    if query in meta["family"].lower():
        score += 10

    if score:
        canonical = name if name in nodes else None

        matches.append({
            "score": score,
            "canonical": canonical,
            "name": name,
            "family": meta["family"],
            "path": meta["relative_path"],
            "graph": canonical is not None,
        })

matches.sort(key=lambda x: (-x["score"], x["name"]))

print("=" * 60)
print("FORGE-ARCH-QUERY-0005")
print("Canonical Identifier Resolver Engine")
print("=" * 60)
print("Query   :", args.query)
print("Matches :", len(matches))
print()

for m in matches:
    print(m["name"])
    print("  Score     :", m["score"])
    print("  Family    :", m["family"])
    print("  Path      :", m["path"])
    print("  In Graph  :", m["graph"])
    if m["canonical"]:
        print("  Canonical :", m["canonical"])
    print()
