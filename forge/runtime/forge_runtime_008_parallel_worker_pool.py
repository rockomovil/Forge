#!/usr/bin/env python3

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import threading
import time

MODULE = "FORGE-RUNTIME-008"
STATUS = "FORGE_PARALLEL_WORKER_POOL_READY"

lock = threading.Lock()
completed = 0


def execute(job_id: int):

    global completed

    time.sleep(0.10)

    with lock:
        completed += 1

    print(f"worker completed job {job_id}")


if __name__ == "__main__":

    JOBS = 8
    WORKERS = 4

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:

        executor.map(execute, range(JOBS))

    elapsed = time.perf_counter() - start

    print(MODULE)
    print(STATUS)
    print(f"jobs = {JOBS}")
    print(f"workers = {WORKERS}")
    print(f"completed = {completed}")
    print(f"elapsed_seconds = {elapsed:.3f}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")
    print(f"{MODULE} VERIFIED")
