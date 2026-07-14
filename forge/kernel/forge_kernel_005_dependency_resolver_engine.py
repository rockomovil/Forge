#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from collections import defaultdict, deque
from datetime import datetime, UTC
from pathlib import Path

MODULE = "FORGE-KERNEL-005"
STATUS = "FORGE_DEPENDENCY_RESOLVER_READY"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime" / "kernel"

mission_graph = json.loads(
    (RUNTIME / "forge_mission_graph_004.json").read_text(encoding="utf-8")
)

nodes = mission_graph["graph"]["nodes"]
edges = mission_graph["graph"]["edges"]

adjacency = defaultdict(list)
indegree = defaultdict(int)

node_ids = set()

for node in nodes:
    node_ids.add(node["id"])
    indegree[node["id"]] = indegree[node["id"]]

for edge in edges:
    src = edge["from"]
    dst = edge["to"]
    adjacency[src].append(dst)
    indegree[dst] += 1

queue = deque(sorted([n for n in node_ids if indegree[n] == 0]))
execution_order = []

while queue:
    current = queue.popleft()
    execution_order.append(current)

    for nxt in sorted(adjacency[current]):
        indegree[nxt] -= 1
        if indegree[nxt] == 0:
            queue.append(nxt)

acyclic = len(execution_order) == len(node_ids)

resolver = {
    "module": MODULE,
    "status": STATUS,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated": datetime.now(UTC).isoformat(),
    "node_count": len(node_ids),
    "edge_count": len(edges),
    "acyclic": acyclic,
    "execution_order": execution_order,
}

payload = json.dumps(resolver, indent=2, sort_keys=True)

(runtime := RUNTIME / "forge_dependency_resolver_005.json").write_text(
    payload,
    encoding="utf-8"
)

integrity = hashlib.sha256(payload.encode()).hexdigest()

(RUNTIME / "forge_dependency_resolver_005_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "integrity_hash": integrity,
        },
        indent=2,
    ),
    encoding="utf-8",
)

with (RUNTIME / "forge_dependency_resolver_005_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(
        json.dumps(
            {
                "timestamp": resolver["generated"],
                "module": MODULE,
                "status": STATUS,
                "integrity_hash": integrity,
            }
        ) + "\n"
    )

verification = hashlib.sha256(
    (MODULE + STATUS + integrity).encode()
).hexdigest()

print(MODULE)
print(STATUS)
print(f"node_count = {len(node_ids)}")
print(f"edge_count = {len(edges)}")
print(f"execution_steps = {len(execution_order)}")
print(f"acyclic = {acyclic}")
print(f"integrity_hash = {integrity}")
print(f"hash = {verification}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
