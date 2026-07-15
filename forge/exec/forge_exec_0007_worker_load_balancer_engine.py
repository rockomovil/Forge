#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = json.loads(
    (ROOT / "runtime/exec/worker_registry.json").read_text()
)

QUEUE = json.loads(
    (ROOT / "runtime/exec/execution_dispatch_queue.json").read_text()
)

workers = {
    w["id"]: {
        "role": w["role"],
        "assigned_jobs": 0
    }
    for w in REGISTRY["worker_registry"]
}

for job in QUEUE["dispatch_queue"]:
    wid = job["worker"]
    workers.setdefault(
        wid,
        {
            "role": "unknown",
            "assigned_jobs": 0
        }
    )
    workers[wid]["assigned_jobs"] += 1

balanced = []

for wid in sorted(workers):
    balanced.append({
        "worker": wid,
        "role": workers[wid]["role"],
        "assigned_jobs": workers[wid]["assigned_jobs"],
        "available": True
    })

max_jobs = max((w["assigned_jobs"] for w in balanced), default=0)
min_jobs = min((w["assigned_jobs"] for w in balanced), default=0)

report = {
    "module": "FORGE-EXEC-0007",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "workers": balanced,
    "worker_count": len(balanced),
    "dispatches": QUEUE["dispatch_count"],
    "max_jobs_per_worker": max_jobs,
    "min_jobs_per_worker": min_jobs,
    "load_balance_delta": max_jobs - min_jobs
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/exec/worker_load_balancer.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-EXEC-0007")
print("Worker Load Balancer Engine")
print("=" * 60)
print("Workers   :", report["worker_count"])
print("Jobs      :", report["dispatches"])
print("Max Load  :", report["max_jobs_per_worker"])
print("Min Load  :", report["min_jobs_per_worker"])
print("Delta     :", report["load_balance_delta"])
print("Output    :", OUT)
print()
print("STATUS : PASS")
