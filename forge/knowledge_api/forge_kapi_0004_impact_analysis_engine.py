#!/usr/bin/env python3

from pathlib import Path
from collections import deque
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

reverse = {}

for edge in GRAPH["edges"]:

    if edge["relation"] != "depends_on":
        continue

    reverse.setdefault(edge["to"], []).append(edge["from"])

parser = argparse.ArgumentParser()
parser.add_argument("--module", required=True)
args = parser.parse_args()

target = f"module::{args.module}"

visited = set()
queue = deque([target])

while queue:

    node = queue.popleft()

    for parent in reverse.get(node, []):

        if parent not in visited:
            visited.add(parent)
            queue.append(parent)

print("=" * 60)
print("FORGE-KAPI-0004")
print("Impact Analysis Engine")
print("=" * 60)
print("Target           :", target)
print("Affected Modules :", len(visited))
print()

for module in sorted(visited)[:200]:
    print(module)

print()
print("STATUS : PASS")
