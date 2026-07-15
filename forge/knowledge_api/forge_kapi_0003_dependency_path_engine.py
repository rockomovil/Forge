#!/usr/bin/env python3

from pathlib import Path
from collections import deque
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

adj = {}

for edge in GRAPH["edges"]:
    if edge["relation"] != "depends_on":
        continue
    adj.setdefault(edge["from"], []).append(edge["to"])

parser = argparse.ArgumentParser()
parser.add_argument("--from", dest="src", required=True)
parser.add_argument("--to", dest="dst", required=True)
args = parser.parse_args()

src = f"module::{args.src}"
dst = f"module::{args.dst}"

q = deque([[src]])
visited = {src}
path = None

while q:
    p = q.popleft()
    node = p[-1]

    if node == dst:
        path = p
        break

    for nxt in adj.get(node, []):
        if nxt not in visited:
            visited.add(nxt)
            q.append(p + [nxt])

print("=" * 60)
print("FORGE-KAPI-0003")
print("Dependency Path Engine")
print("=" * 60)

if path:
    print("Path Length :", len(path) - 1)
    print()
    for n in path:
        print(n)
else:
    print("No dependency path found.")

print()
print("STATUS : PASS")
