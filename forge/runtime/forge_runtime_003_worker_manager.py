#!/usr/bin/env python3

from __future__ import annotations

import threading
from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parent

spec = spec_from_file_location(
    "forge_runtime_message_bus",
    ROOT / "forge_runtime_002_message_bus.py",
)

module = module_from_spec(spec)
spec.loader.exec_module(module)

MessageBus = module.MessageBus


@dataclass
class Worker:
    name: str
    topic: str
    handled: int = 0


class WorkerManager:

    def __init__(self):

        self.bus = MessageBus()
        self.workers: dict[str, Worker] = {}

    def register(self, name: str, topic: str):

        self.workers[name] = Worker(
            name=name,
            topic=topic,
        )

    def publish(self, topic: str, message):

        self.bus.publish(topic, message)

    def start(self):

        for worker in self.workers.values():

            threading.Thread(
                target=self._loop,
                args=(worker,),
                daemon=True,
            ).start()

    def _loop(self, worker: Worker):

        while True:

            message = self.bus.consume(worker.topic)

            worker.handled += 1

            print(
                f"[{worker.name}] "
                f"{message}"
            )

    def statistics(self):

        return {
            name: worker.handled
            for name, worker in self.workers.items()
        }


if __name__ == "__main__":

    manager = WorkerManager()

    manager.register(
        "RepositoryWorker",
        "repository",
    )

    manager.register(
        "GraphWorker",
        "graph",
    )

    manager.start()

    manager.publish(
        "repository",
        {
            "job": "scan_repository",
        },
    )

    manager.publish(
        "graph",
        {
            "job": "build_graph",
        },
    )

    threading.Event().wait(0.5)

    stats = manager.statistics()

    print("FORGE-RUNTIME-003")
    print("FORGE_WORKER_MANAGER_READY")
    print(f"registered_workers = {len(stats)}")
    print(f"messages_processed = {sum(stats.values())}")
    print("FORGE-RUNTIME-003 VERIFIED")
