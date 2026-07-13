#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PLAN = ROOT / "runtime/compiler/forge_build_plan_001.json"
OUT = ROOT / "runtime/graph"


def sha256(path: Path):

    h = hashlib.sha256()

    with path.open("rb") as f:

        while chunk := f.read(65536):

            h.update(chunk)

    return h.hexdigest()


plan = json.loads(PLAN.read_text())

nodes = []
edges = []

families = {}

for module in plan["modules"]:

    mid = module["module_id"]

    fam = module["family"]

    nodes.append({

        "id": mid,

        "type": "module",

        "code": module["module_code"],

        "family": fam

    })

    if fam not in families:

        families[fam] = {

            "id": f"family::{fam}",

            "type": "family",

            "name": fam

        }

    edges.append({

        "from": families[fam]["id"],

        "to": mid,

        "relation": "contains"

    })

payload = {

    "graph":
    "FORGE-GRAPH-001",

    "status":
    "FORGE_GRAPH_REGISTRY_READY",

    "runtime_mode":
    "SHADOW_ONLY_READ_ONLY",

    "nodes":
    list(families.values()) + nodes,

    "edges":
    edges,

    "family_count":
    len(families),

    "module_count":
    len(nodes),

    "edge_count":
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

report = OUT / "forge_graph_registry_001.json"

report.write_text(
    json.dumps(
        payload,
        indent=2
    ) + "\n"
)

digest = sha256(report)

(OUT / "forge_graph_registry_001_hash.json").write_text(

    json.dumps({

        "artifact":
        str(report.relative_to(ROOT)),

        "sha256":
        digest

    }, indent=2) + "\n"

)

with (
    OUT /
    "forge_graph_registry_001_ledger.jsonl"
).open("a") as f:

    f.write(
        json.dumps(payload) + "\n"
    )

print("FORGE-GRAPH-001")
print("FORGE_GRAPH_REGISTRY_READY")
print(f"families = {payload['family_count']}")
print(f"modules = {payload['module_count']}")
print(f"edges = {payload['edge_count']}")
print(f"graph_hash = {payload['graph_hash']}")
print(f"hash = {digest}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
