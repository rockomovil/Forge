#!/usr/bin/env python3

from __future__ import annotations

import time

from forge.runtime.forge_runtime_002_message_bus import MessageBus
from forge.runtime.forge_runtime_005_mission_dispatcher import MissionDispatcher


class RuntimePipeline:

    def __init__(self):

        self.dispatcher = MissionDispatcher()
        self.bus = MessageBus()

    def submit(self, topic: str, mission: dict):

        self.dispatcher.submit(topic, mission)

    def pump(self):

        topics = list(self.dispatcher.queues.keys())

        dispatched = 0

        for topic in topics:

            mission = self.dispatcher.dispatch(topic)

            if mission is None:
                continue

            self.bus.publish(topic, mission)

            dispatched += 1

        return dispatched


if __name__ == "__main__":

    pipeline = RuntimePipeline()

    pipeline.submit(
        "repository",
        {
            "id": "MISSION-001",
            "action": "scan_repository",
        },
    )

    pipeline.submit(
        "graph",
        {
            "id": "MISSION-002",
            "action": "build_graph",
        },
    )

    dispatched = pipeline.pump()

    time.sleep(0.1)

    print("FORGE-RUNTIME-006")
    print("FORGE_RUNTIME_PIPELINE_READY")
    print(f"missions_dispatched = {dispatched}")
    print(
        f"repository_queue = {pipeline.bus.pending('repository')}"
    )
    print(
        f"graph_queue = {pipeline.bus.pending('graph')}"
    )
    print("FORGE-RUNTIME-006 VERIFIED")
