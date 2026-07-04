#!/usr/bin/env python3

from pathlib import Path
import json
from datetime import datetime, UTC

ROOT = Path(__file__).resolve().parents[1]

OUTPUT = ROOT / "runtime" / "dependencies" / "dependency_graph.json"

GRAPH = {
    "generated_at": datetime.now(UTC).isoformat(),
    "kernel_version": "0.1",
    "nodes": [
        {
            "id": "F0001",
            "name": "Capability Registry",
            "depends_on": []
        },
        {
            "id": "F0002",
            "name": "Service Registry",
            "depends_on": [
                "F0001"
            ]
        },
        {
            "id": "F0003",
            "name": "Event Bus",
            "depends_on": [
                "F0001",
                "F0002"
            ]
        },
        {
            "id": "F0004",
            "name": "Runtime Context",
            "depends_on": [
                "F0001"
            ]
        },
        {
            "id": "F0005",
            "name": "Configuration Manager",
            "depends_on": [
                "F0004"
            ]
        },
        {
            "id": "F0006",
            "name": "Kernel Logger",
            "depends_on": [
                "F0003",
                "F0005"
            ]
        },
        {
            "id": "F0007R",
            "name": "Workspace Locator",
            "depends_on": [
                "F0004",
                "F0005"
            ]
        },
        {
            "id": "F0008",
            "name": "Kernel Health Monitor",
            "depends_on": [
                "F0001",
                "F0002",
                "F0003",
                "F0004",
                "F0005",
                "F0006",
                "F0007R"
            ]
        },
        {
            "id": "F0009",
            "name": "Dependency Resolver",
            "depends_on": [
                "F0001",
                "F0002",
                "F0003",
                "F0004",
                "F0005",
                "F0006",
                "F0007R",
                "F0008"
            ]
        }
    ]
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

OUTPUT.write_text(
    json.dumps(
        GRAPH,
        indent=2,
        ensure_ascii=False
    )
)

print()
print("Dependency Graph")
print("----------------")

for node in GRAPH["nodes"]:

    deps = ", ".join(node["depends_on"])

    if deps == "":
        deps = "(root)"

    print(f'{node["id"]:<8} -> {deps}')

print()
print("Nodes :", len(GRAPH["nodes"]))
print("Graph :", OUTPUT)
