#!/usr/bin/env python3

from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--node")
group.add_argument("--contains")
group.add_argument("--depends")
group.add_argument("--incoming")
group.add_argument("--relation")

args = parser.parse_args()

nodes = {n["id"]: n for n in GRAPH["nodes"]}

outgoing = {}
incoming = {}

for edge in GRAPH["edges"]:

    outgoing.setdefault(edge["from"], []).append(edge)
    incoming.setdefault(edge["to"], []).append(edge)

print("=" * 60)
print("FORGE-KAPI-0002")
print("Graph Query Engine")
print("=" * 60)

if args.node:

    node = args.node

    if node not in nodes:
        print("Node not found.")
        raise SystemExit(1)

    print(json.dumps(nodes[node], indent=2))

elif args.contains:

    family = f"family::{args.contains}"

    if family not in outgoing:
        print("Family not found.")
        raise SystemExit(1)

    print("MODULES\n")

    for edge in sorted(
        outgoing[family],
        key=lambda e: e["to"]
    ):
        print(edge["to"])

elif args.depends:

    node = f"module::{args.depends}"

    print("DEPENDS ON\n")

    found = False

    for edge in outgoing.get(node, []):

        if edge["relation"] == "depends_on":
            print(edge["to"])
            found = True

    if not found:
        print("None")

elif args.incoming:

    node = f"module::{args.incoming}"

    print("REFERENCED BY\n")

    found = False

    for edge in incoming.get(node, []):

        print(edge["from"])
        found = True

    if not found:
        print("None")

elif args.relation:

    relation = args.relation

    matches = [
        e for e in GRAPH["edges"]
        if e["relation"] == relation
    ]

    print(f"Relation : {relation}")
    print(f"Matches  : {len(matches)}\n")

    for edge in matches[:100]:
        print(f'{edge["from"]} -> {edge["to"]}')

print()
print("STATUS : PASS")
