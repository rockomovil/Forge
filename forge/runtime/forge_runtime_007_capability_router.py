#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path

MODULE = "FORGE-RUNTIME-007"
STATUS = "FORGE_CAPABILITY_ROUTER_READY"

ROOT = Path(__file__).resolve().parents[2]

capability_registry = json.loads(
    (
        ROOT
        / "runtime"
        / "kernel"
        / "forge_capability_registry_001.json"
    ).read_text(encoding="utf-8")
)

routing_table = {
    capability["name"]: f"{capability['name']}_pool"
    for capability in capability_registry["capabilities"]
}


class CapabilityRouter:

    def __init__(self, routes: dict[str, str]):
        self.routes = routes

    def resolve(self, capability: str) -> str:

        if capability not in self.routes:
            raise RuntimeError(f"Unknown capability: {capability}")

        return self.routes[capability]


if __name__ == "__main__":

    router = CapabilityRouter(routing_table)

    mission = {
        "mission_id": "MISSION-001",
        "required_capability": "repository_scan",
    }

    destination = router.resolve(
        mission["required_capability"]
    )

    print(MODULE)
    print(STATUS)
    print(f"routing_entries = {len(routing_table)}")
    print(f"mission_id = {mission['mission_id']}")
    print(f"destination = {destination}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")
    print(f"{MODULE} VERIFIED")
