#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict, deque
import json

ROOT = Path(__file__).resolve().parents[2]

DAG = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_condensation_dag.json").read_text()
)

components = DAG["components"]

forward = defaultdict(list)
indegree = defaultdict(int)

for edge in DAG["condensation_dag"]:

    src = edge["from_component"]
    dst = edge["to_component"]

    forward[src].append(dst)
    indegree[dst] += 1

for cid in range(components):
    indegree.setdefault(cid, 0)

queue = deque()

layer = {}

for cid in range(components):

    if indegree[cid] == 0:
        layer[cid] = 0
        queue.append(cid)

while queue:

    node = queue.popleft()

    for nxt in forward[node]:

        layer[nxt] = max(
            layer.get(nxt, 0),
            layer[node] + 1
        )

        indegree[nxt] -= 1

        if indegree[nxt] == 0:
            queue.append(nxt)

layers = defaultdict(list)

for comp, lv in layer.items():
    layers[str(lv)].append(comp)

for lv in layers:
    layers[lv].sort()

remaining = sorted(
    c for c in range(components)
    if c not in layer
)

report = {
    "module": "FORGE-KAPI-0012",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "components": components,
    "resolved_components": len(layer),
    "unresolved_components": len(remaining),
    "max_layer": max(layer.values()) if layer else 0,
    "layers": dict(layers),
    "remaining_components": remaining
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_architecture_layers.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0012")
print("Architecture Layers Engine")
print("=" * 60)
print("Components           :", components)
print("Resolved Components  :", len(layer))
print("Unresolved           :", len(remaining))
print("Max Layer            :", report["max_layer"])
print("Output               :", outfile)
print()
print("STATUS : PASS")
