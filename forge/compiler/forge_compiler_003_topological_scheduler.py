#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_GRAPH = ROOT / "runtime/compiler/forge_dependency_graph_001.json"
OUT = ROOT / "runtime/compiler"


def load_graph(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"DEPENDENCY_GRAPH_NOT_FOUND: {path}")


def topological_levels(nodes):

    indegree = {}
    adjacency = defaultdict(list)

    lookup = {}

    for node in nodes:

        mid = node["module_id"]

        lookup[mid] = node

        indegree[mid] = len(node["depends_on"])

        for dep in node["depends_on"]:
            adjacency[dep].append(mid)

    current = deque(
        sorted(
            mid
            for mid, deg in indegree.items()
            if deg == 0
        )
    )

    visited = []

    levels = []

    while current:

        level = sorted(current)

        levels.append(level)

        nxt = deque()

        while current:

            n = current.popleft()

            visited.append(n)

            for child in adjacency[n]:

                indegree[child] -= 1

                if indegree[child] == 0:
                    nxt.append(child)

        current = deque(sorted(nxt))

    if len(visited) != len(nodes):
        raise SystemExit("DEPENDENCY_CYCLE_DETECTED")

    return levels, visited


def build_schedule(graph):

    levels, order = topological_levels(graph["nodes"])

    payload = {

        "compiler":
        "FORGE-COMPILER-003",

        "status":
        "FORGE_BUILD_SCHEDULE_READY",

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY",

        "families":
        graph["families"],

        "modules":
        graph["modules"],

        "parallel_levels":
        len(levels),

        "execution_order":
        order,

        "levels":
        levels,

        "generated":
        datetime.now(
            timezone.utc
        ).isoformat()

    }

    payload["schedule_hash"] = hashlib.sha256(

        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

    ).hexdigest()

    return payload


def write(payload):

    OUT.mkdir(
        parents=True,
        exist_ok=True
    )

    schedule = OUT / "forge_build_schedule_001.json"

    schedule.write_text(

        json.dumps(
            payload,
            indent=2
        ) + "\n",

        encoding="utf-8"

    )

    digest = hashlib.sha256(
        schedule.read_bytes()
    ).hexdigest()

    hashfile = OUT / "forge_build_schedule_001_hash.json"

    hashfile.write_text(

        json.dumps(
            {
                "artifact":
                str(schedule.relative_to(ROOT)),
                "sha256":
                digest
            },
            indent=2
        ) + "\n"

    )

    ledger = OUT / "forge_build_schedule_001_ledger.jsonl"

    with ledger.open("a") as f:

        f.write(
            json.dumps(payload) + "\n"
        )

    return digest


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(

        "--graph",

        default=str(
            DEFAULT_GRAPH.relative_to(ROOT)
        )

    )

    args = parser.parse_args()

    graph = load_graph(
        ROOT / args.graph
    )

    payload = build_schedule(graph)

    digest = write(payload)

    print("FORGE-COMPILER-003")
    print("FORGE_BUILD_SCHEDULE_READY")
    print(f"modules = {payload['modules']}")
    print(f"parallel_levels = {payload['parallel_levels']}")
    print(f"schedule_hash = {payload['schedule_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()
