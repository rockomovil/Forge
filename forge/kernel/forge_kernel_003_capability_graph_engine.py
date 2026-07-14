#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import datetime, UTC
from pathlib import Path

MODULE = "FORGE-KERNEL-003"
STATUS = "FORGE_CAPABILITY_GRAPH_READY"

ROOT = Path(__file__).resolve().parents[2]

runtime_dir = ROOT / "runtime" / "kernel"

capability_registry = json.loads(
    (runtime_dir / "forge_capability_registry_001.json").read_text(encoding="utf-8")
)

mission_registry = json.loads(
    (runtime_dir / "forge_mission_registry_002.json").read_text(encoding="utf-8")
)

capabilities = capability_registry["capabilities"]
missions = mission_registry["missions"]

capability_nodes = []
capability_edges = []

for capability in capabilities:
    capability_nodes.append(
        {
            "id": capability["name"],
            "domain": capability["domain"],
            "status": capability["status"],
        }
    )

for mission in missions:
    for capability in mission["required_capabilities"]:
        capability_edges.append(
            {
                "mission": mission["mission_id"],
                "capability": capability,
                "relationship": "REQUIRES",
            }
        )

graph = {
    "module": MODULE,
    "status": STATUS,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated": datetime.now(UTC).isoformat(),
    "capability_nodes": capability_nodes,
    "edges": capability_edges,
    "node_count": len(capability_nodes),
    "edge_count": len(capability_edges),
}

payload = json.dumps(graph, indent=2, sort_keys=True)

(runtime_dir / "forge_capability_graph_003.json").write_text(
    payload,
    encoding="utf-8",
)

integrity = hashlib.sha256(payload.encode()).hexdigest()

(runtime_dir / "forge_capability_graph_003_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "integrity_hash": integrity,
        },
        indent=2,
    ),
    encoding="utf-8",
)

with (runtime_dir / "forge_capability_graph_003_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(
        json.dumps(
            {
                "timestamp": graph["generated"],
                "module": MODULE,
                "status": STATUS,
                "integrity_hash": integrity,
            }
        )
        + "\n"
    )

verification_hash = hashlib.sha256(
    (MODULE + STATUS + integrity).encode()
).hexdigest()

print(MODULE)
print(STATUS)
print(f"node_count = {len(capability_nodes)}")
print(f"edge_count = {len(capability_edges)}")
print(f"integrity_hash = {integrity}")
print(f"hash = {verification_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
