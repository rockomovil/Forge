#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

MASTER = ROOT / "forge/meta/master/forge_master.yaml"
OUT = ROOT / "runtime/compiler"


def load_master():

    return yaml.safe_load(
        MASTER.read_text(
            encoding="utf-8"
        )
    )


def load_catalog(path):

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def main():

    master = load_master()

    nodes = []

    lookup = {}

    for catalog_name in master["families"]:

        catalog = load_catalog(
            ROOT / catalog_name
        )

        family = catalog["family"]

        for module in catalog["modules"]:

            mid = module["id"]

            lookup[mid] = {

                "module_id": mid,

                "module_code":
                f"FORGE-KNOWLEDGE-{mid:03d}",

                "family": family,

                "depends_on":
                module.get(
                    "depends_on",
                    []
                ),

                "required_by": []

            }

    for node in lookup.values():

        for dep in node["depends_on"]:

            lookup[dep]["required_by"].append(
                node["module_id"]
            )

    payload = {

        "compiler":
        "FORGE-COMPILER-004",

        "status":
        "FORGE_SEMANTIC_DEPENDENCY_GRAPH_READY",

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY",

        "families":
        len(master["families"]),

        "modules":
        len(lookup),

        "generated":
        datetime.now(
            timezone.utc
        ).isoformat(),

        "nodes":
        sorted(
            lookup.values(),
            key=lambda x: x["module_id"]
        )

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

    graph = OUT / "forge_semantic_dependency_graph_001.json"

    graph.write_text(
        json.dumps(
            payload,
            indent=2
        ) + "\n"
    )

    digest = hashlib.sha256(
        graph.read_bytes()
    ).hexdigest()

    (OUT / "forge_semantic_dependency_graph_001_hash.json").write_text(

        json.dumps(
            {
                "artifact":
                str(graph.relative_to(ROOT)),
                "sha256":
                digest
            },
            indent=2
        ) + "\n"

    )

    with (OUT / "forge_semantic_dependency_graph_001_ledger.jsonl").open("a") as f:

        f.write(
            json.dumps(payload) + "\n"
        )

    print("FORGE-COMPILER-004")
    print("FORGE_SEMANTIC_DEPENDENCY_GRAPH_READY")
    print(f"families = {payload['families']}")
    print(f"modules = {payload['modules']}")
    print(f"graph_hash = {payload['graph_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()
