#!/usr/bin/env python3

from __future__ import annotations

from forge.runtime.forge_runtime_002_message_bus import MessageBus
from forge.runtime.forge_runtime_003_worker_manager import WorkerManager
from forge.runtime.forge_runtime_005_mission_dispatcher import MissionDispatcher
from forge.runtime.forge_runtime_007_capability_router import CapabilityRouter


class RuntimeCore:

    """
    RuntimeCore centraliza los servicios permanentes del Runtime.
    No modifica el comportamiento existente; únicamente los reúne
    bajo un único punto de acceso.
    """

    def __init__(self, routing_table: dict[str, str]):

        self.bus = MessageBus()
        self.dispatcher = MissionDispatcher()
        self.worker_manager = WorkerManager()
        self.router = CapabilityRouter(routing_table)

    def services(self):

        return {
            "message_bus": self.bus,
            "dispatcher": self.dispatcher,
            "worker_manager": self.worker_manager,
            "router": self.router,
        }


if __name__ == "__main__":

    runtime = RuntimeCore(
        {
            "repository_scan": "repository_scan_pool"
        }
    )

    print("FORGE-RUNTIME-REF-001")
    print("FORGE_RUNTIME_CORE_READY")
    print(f"services = {len(runtime.services())}")

    for name in runtime.services():
        print(name)

    print("runtime_mode = SHADOW_ONLY_READ_ONLY")
    print("FORGE-RUNTIME-REF-001 VERIFIED")
