#!/usr/bin/env python3

from __future__ import annotations

from forge.runtime.workers.base_worker import BaseWorker


class GraphWorker(BaseWorker):

    NAME = "GraphWorker"
    TOPIC = "graph"

    def handle(self, message):

        print(f"[{self.NAME}] {message}")
