#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_PLAN = ROOT / "runtime/compiler/forge_build_plan_001.json"
OUT = ROOT / "runtime/compiler"


def load_plan(path: Path) -> dict:

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"BUILD_PLAN_NOT_FOUND: {path}")


def build_graph(plan: dict):

    modules = sorted(
        plan["modules"],
        key=lambda x: x["module_id"]
    )

    graph = []
    adjacency = defaultdict(list)
    reverse = defaultdict(list)

    previous = None

    for m in modules:

        mid = m["module_id"]

        depends = []

        #
        # Dependencia secuencial mínima
        #

        if previous is not None:
            depends.append(previous)

        previous = mid

        graph.append({
            "module_id": mid,
            "module_code": m["module_code"],
            "family": m["family"],
            "depends_on": depends,
            "required_by": []
        })

    lookup = {
        n["module_id"]: n
        for n in graph
    }

    for node in graph:

        for dep in node["depends_on"]:

            adjacency[dep].append(node["module_id"])
            reverse[node["module_id"]].append(dep)

    for node in graph:

        node["required_by"] = adjacency[node["module_id"]]

    graph_hash = hashlib.sha256(

        json.dumps(
            graph,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

    ).hexdigest()

    payload = {

        "compiler": "FORGE-COMPILER-002",

        "status":
        "FORGE_DEPENDENCY_GRAPH_READY",

        "families":
        plan["family_count"],

        "modules":
        len(graph),

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY",

        "graph_hash":
        graph_hash,

        "generated":
        datetime.now(
            timezone.utc
        ).isoformat(),

        "nodes":
        graph

    }

    return payload


def write(payload):

    OUT.mkdir(
        parents=True,
        exist_ok=True
    )

    graph = OUT / "forge_dependency_graph_001.json"

    graph.write_text(

        json.dumps(
            payload,
            indent=2
        ) + "\n",

        encoding="utf-8"

    )

    digest = hashlib.sha256(
        graph.read_bytes()
    ).hexdigest()

    hashfile = OUT / "forge_dependency_graph_001_hash.json"

    hashfile.write_text(

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

    ledger = OUT / "forge_dependency_graph_001_ledger.jsonl"

    with ledger.open("a") as f:

        f.write(
            json.dumps(payload) + "\n"
        )

    return digest


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(

        "--plan",

        default=str(
            DEFAULT_PLAN.relative_to(ROOT)
        )

    )

    args = parser.parse_args()

    plan = load_plan(
        ROOT / args.plan
    )

    payload = build_graph(plan)

    digest = write(payload)

    print("FORGE-COMPILER-002")
    print("FORGE_DEPENDENCY_GRAPH_READY")
    print(f"modules = {payload['modules']}")
    print(f"graph_hash = {payload['graph_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()

