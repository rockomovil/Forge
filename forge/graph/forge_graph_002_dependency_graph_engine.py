#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

GRAPH = ROOT / "runtime/graph/forge_graph_registry_001.json"
PLAN = ROOT / "runtime/compiler/forge_build_plan_001.json"
OUT = ROOT / "runtime/graph"


def sha256(path: Path):

    h = hashlib.sha256()

    with path.open("rb") as f:

        while chunk := f.read(65536):

            h.update(chunk)

    return h.hexdigest()


graph = json.loads(GRAPH.read_text())
plan = json.loads(PLAN.read_text())

nodes = graph["nodes"]
edges = list(graph["edges"])

module_nodes = {
    n["id"]: n
    for n in nodes
    if n["type"] == "module"
}

execution = sorted(
    plan["modules"],
    key=lambda m: m["module_id"]
)

previous = None

for module in execution:

    mid = module["module_id"]

    if previous is not None:

        edges.append({

            "from": previous,

            "to": mid,

            "relation": "execution_order"

        })

    previous = mid

payload = {

    "graph":
    "FORGE-GRAPH-002",

    "status":
    "FORGE_DEPENDENCY_GRAPH_READY",

    "runtime_mode":
    "SHADOW_ONLY_READ_ONLY",

    "nodes":
    nodes,

    "edges":
    edges,

    "family_count":
    len(
        {
            n["family"]
            for n in module_nodes.values()
        }
    ),

    "module_count":
    len(module_nodes),

    "dependency_edges":
    len(edges),

    "generated":
    datetime.now(
        timezone.utc
    ).isoformat()

}

payload["graph_hash"] = hashlib.sha256(

    json.dumps(

        payload,

        sort_keys=True,

        separators=(",", ":")

    ).encode()

).hexdigest()

OUT.mkdir(
    parents=True,
    exist_ok=True
)

report = OUT / "forge_dependency_graph_002.json"

report.write_text(
    json.dumps(
        payload,
        indent=2
    ) + "\n"
)

digest = sha256(report)

(OUT / "forge_dependency_graph_002_hash.json").write_text(

    json.dumps({

        "artifact":
        str(report.relative_to(ROOT)),

        "sha256":
        digest

    }, indent=2) + "\n"

)

with (
    OUT /
    "forge_dependency_graph_002_ledger.jsonl"
).open("a") as f:

    f.write(
        json.dumps(payload) + "\n"
    )

print("FORGE-GRAPH-002")
print("FORGE_DEPENDENCY_GRAPH_READY")
print(f"families = {payload['family_count']}")
print(f"modules = {payload['module_count']}")
print(f"edges = {payload['dependency_edges']}")
print(f"graph_hash = {payload['graph_hash']}")
print(f"hash = {digest}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
