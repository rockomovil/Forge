#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict, deque


class MissionDispatcher:

    def __init__(self):

        self.queues = defaultdict(deque)

    def submit(self, topic: str, mission: dict):

        self.queues[topic].append(mission)

    def dispatch(self, topic: str):

        if not self.queues[topic]:
            return None

        return self.queues[topic].popleft()

    def pending(self, topic: str):

        return len(self.queues[topic])


if __name__ == "__main__":

    dispatcher = MissionDispatcher()

    dispatcher.submit(
        "repository",
        {
            "id": "MISSION-001",
            "action": "scan_repository",
        },
    )

    dispatcher.submit(
        "graph",
        {
            "id": "MISSION-002",
            "action": "build_graph",
        },
    )

    repo = dispatcher.dispatch("repository")
    graph = dispatcher.dispatch("graph")

    print("FORGE-RUNTIME-005")
    print("FORGE_MISSION_DISPATCHER_READY")
    print(f"repository_dispatch = {repo['id']}")
    print(f"graph_dispatch = {graph['id']}")
    print("FORGE-RUNTIME-005 VERIFIED")
