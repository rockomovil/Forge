#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict
from queue import Queue
from threading import Lock


class MessageBus:

    def __init__(self):

        self._queues = defaultdict(Queue)
        self._lock = Lock()

    def publish(self, topic: str, message):

        with self._lock:
            self._queues[topic].put(message)

    def consume(self, topic: str):

        return self._queues[topic].get()

    def pending(self, topic: str):

        return self._queues[topic].qsize()


if __name__ == "__main__":

    bus = MessageBus()

    bus.publish(
        "demo",
        {
            "event": "runtime_ready"
        }
    )

    print("FORGE-RUNTIME-002")
    print("FORGE_MESSAGE_BUS_READY")
    print(f"pending_messages = {bus.pending('demo')}")

    message = bus.consume("demo")

    print(f"received = {message['event']}")
    print("FORGE-RUNTIME-002 VERIFIED")
