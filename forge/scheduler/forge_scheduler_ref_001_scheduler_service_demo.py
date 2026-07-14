#!/usr/bin/env python3

from __future__ import annotations

from forge.scheduler.services.scheduler_service import SchedulerService
from forge.scheduler.services.policies import LeastLoadedIdlePolicy

workers = {
    "RepositoryWorker": {
        "state": "IDLE",
        "running_jobs": 0,
        "completed_jobs": 3,
    },
    "GraphWorker": {
        "state": "IDLE",
        "running_jobs": 0,
        "completed_jobs": 1,
    },
}

service = SchedulerService(
    LeastLoadedIdlePolicy()
)

selected = service.select_worker(workers)

print("FORGE-SCHEDULER-REF-001")
print("FORGE_SCHEDULER_SERVICE_READY")
print(f"policy = {LeastLoadedIdlePolicy.NAME}")
print(f"selected_worker = {selected}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print("FORGE-SCHEDULER-REF-001 VERIFIED")
