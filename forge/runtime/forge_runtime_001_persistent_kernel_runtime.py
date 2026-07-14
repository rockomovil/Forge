#!/usr/bin/env python3

from __future__ import annotations

import queue
import threading
import time
from dataclasses import dataclass
from typing import Callable, Any


RUNTIME = "FORGE-RUNTIME-001"


@dataclass
class Job:
    name: str
    fn: Callable[..., Any]
    args: tuple = ()
    kwargs: dict | None = None


class PersistentKernelRuntime:

    def __init__(self):

        self.jobs = queue.Queue()
        self.running = False

    def submit(self, job: Job):

        self.jobs.put(job)

    def worker(self):

        while self.running:

            try:
                job = self.jobs.get(timeout=0.25)

            except queue.Empty:
                continue

            try:

                kwargs = job.kwargs or {}

                print(f"[START] {job.name}")

                job.fn(*job.args, **kwargs)

                print(f"[DONE ] {job.name}")

            except Exception as exc:

                print(f"[ERROR] {job.name}: {exc}")

            finally:

                self.jobs.task_done()

    def start(self):

        self.running = True

        threading.Thread(
            target=self.worker,
            daemon=True,
        ).start()

        print(f"{RUNTIME} READY")

    def stop(self):

        self.running = False


def demo():

    print("Kernel Runtime Alive")


if __name__ == "__main__":

    runtime = PersistentKernelRuntime()

    runtime.start()

    runtime.submit(
        Job(
            "demo",
            demo,
        )
    )

    runtime.jobs.join()

    time.sleep(0.5)

    runtime.stop()
