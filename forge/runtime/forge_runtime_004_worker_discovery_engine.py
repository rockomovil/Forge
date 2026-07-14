#!/usr/bin/env python3

from __future__ import annotations

import importlib
import inspect
import pkgutil

from forge.runtime.workers.base_worker import BaseWorker
import forge.runtime.workers as workers_pkg


workers = []

for _, module_name, _ in pkgutil.iter_modules(workers_pkg.__path__):

    if module_name == "base_worker":
        continue

    module = importlib.import_module(
        f"forge.runtime.workers.{module_name}"
    )

    for _, obj in inspect.getmembers(module, inspect.isclass):

        if (
            issubclass(obj, BaseWorker)
            and obj is not BaseWorker
        ):

            workers.append(
                {
                    "name": obj.NAME,
                    "topic": obj.TOPIC,
                }
            )

print("FORGE-RUNTIME-004")
print("FORGE_WORKER_DISCOVERY_READY")
print(f"workers_discovered = {len(workers)}")

for worker in workers:

    print(
        f"{worker['name']} -> {worker['topic']}"
    )

print("FORGE-RUNTIME-004 VERIFIED")
