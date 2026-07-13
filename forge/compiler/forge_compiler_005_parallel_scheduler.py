#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GRAPH = ROOT / "runtime/compiler/forge_semantic_dependency_graph_001.json"
OUT = ROOT / "runtime/compiler"


def load_graph(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"SEMANTIC_GRAPH_NOT_FOUND: {path}")


def build_parallel_levels(nodes: list[dict]):

    indegree = {}
    adjacency = defaultdict(list)

    lookup = {}

    for node in nodes:

        mid = node["module_id"]

        lookup[mid] = node

        indegree[mid] = len(node["depends_on"])

        for dep in node["depends_on"]:
            adjacency[dep].append(mid)

    processed = set()
    levels = []

    while len(processed) < len(nodes):

        ready = sorted(
            mid
            for mid, deg in indegree.items()
            if deg == 0 and mid not in processed
        )

        if not ready:
            raise SystemExit("DEPENDENCY_CYCLE_DETECTED")

        levels.append(ready)

        for mid in ready:

            processed.add(mid)

            for child in adjacency[mid]:
                indegree[child] -= 1

    return levels


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph",
        default=str(DEFAULT_GRAPH.relative_to(ROOT))
    )

    args = parser.parse_args()

    graph = load_graph(ROOT / args.graph)

    levels = build_parallel_levels(graph["nodes"])

    execution_order = [
        module
        for level in levels
        for module in level
    ]

    payload = {

        "compiler":
        "FORGE-COMPILER-005",

        "status":
        "FORGE_PARALLEL_BUILD_SCHEDULER_READY",

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY",

        "families":
        graph["families"],

        "modules":
        graph["modules"],

        "parallel_levels":
        len(levels),

        "max_parallelism":
        max(len(level) for level in levels),

        "execution_order":
        execution_order,

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

    OUT.mkdir(
        parents=True,
        exist_ok=True
    )

    schedule = OUT / "forge_parallel_build_schedule_001.json"

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

    (OUT / "forge_parallel_build_schedule_001_hash.json").write_text(

        json.dumps(
            {
                "artifact":
                str(schedule.relative_to(ROOT)),
                "sha256":
                digest
            },
            indent=2
        ) + "\n",
        encoding="utf-8"
    )

    with (
        OUT /
        "forge_parallel_build_schedule_001_ledger.jsonl"
    ).open("a", encoding="utf-8") as handle:

        handle.write(
            json.dumps(payload) + "\n"
        )

    print("FORGE-COMPILER-005")
    print("FORGE_PARALLEL_BUILD_SCHEDULER_READY")
    print(f"families = {payload['families']}")
    print(f"modules = {payload['modules']}")
    print(f"parallel_levels = {payload['parallel_levels']}")
    print(f"max_parallelism = {payload['max_parallelism']}")
    print(f"schedule_hash = {payload['schedule_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()
