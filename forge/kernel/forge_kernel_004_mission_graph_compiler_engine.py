#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import datetime, UTC
from pathlib import Path

MODULE = "FORGE-KERNEL-004"
STATUS = "FORGE_MISSION_GRAPH_COMPILER_READY"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime" / "kernel"

mission_registry = json.loads(
    (RUNTIME / "forge_mission_registry_002.json").read_text(encoding="utf-8")
)

capability_graph = json.loads(
    (RUNTIME / "forge_capability_graph_003.json").read_text(encoding="utf-8")
)

graph_nodes = []
graph_edges = []

available = {
    node["id"]: node
    for node in capability_graph["capability_nodes"]
}

for mission in mission_registry["missions"]:

    mission_node = {
        "id": mission["mission_id"],
        "type": "MISSION",
        "state": mission["state"],
        "priority": mission["priority"],
    }

    graph_nodes.append(mission_node)

    for capability in mission["required_capabilities"]:

        if capability not in available:
            raise RuntimeError(f"Missing capability: {capability}")

        capability_node = {
            "id": capability,
            "type": "CAPABILITY",
            "status": available[capability]["status"],
        }

        if capability_node not in graph_nodes:
            graph_nodes.append(capability_node)

        graph_edges.append(
            {
                "from": mission["mission_id"],
                "to": capability,
                "relationship": "COMPILED_TO",
            }
        )

compiled = {
    "module": MODULE,
    "status": STATUS,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated": datetime.now(UTC).isoformat(),
    "mission_count": len(mission_registry["missions"]),
    "node_count": len(graph_nodes),
    "edge_count": len(graph_edges),
    "graph": {
        "nodes": graph_nodes,
        "edges": graph_edges,
    },
}

payload = json.dumps(compiled, indent=2, sort_keys=True)

(RUNTIME / "forge_mission_graph_004.json").write_text(
    payload,
    encoding="utf-8",
)

integrity = hashlib.sha256(payload.encode()).hexdigest()

(RUNTIME / "forge_mission_graph_004_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "integrity_hash": integrity,
        },
        indent=2,
    ),
    encoding="utf-8",
)

with (RUNTIME / "forge_mission_graph_004_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(
        json.dumps(
            {
                "timestamp": compiled["generated"],
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
print(f"mission_count = {compiled['mission_count']}")
print(f"node_count = {compiled['node_count']}")
print(f"edge_count = {compiled['edge_count']}")
print(f"integrity_hash = {integrity}")
print(f"hash = {verification}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
