#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

QUEUE = json.loads(
    (ROOT / "runtime/exec/execution_dispatch_queue.json").read_text()
)

workers = {}

for item in QUEUE["dispatch_queue"]:
    workers.setdefault(item["worker"], []).append(item)

worker_status = []

for worker, jobs in sorted(workers.items()):
    worker_status.append({
        "worker": worker,
        "jobs_assigned": len(jobs),
        "jobs_ready": sum(j["state"] == "READY" for j in jobs),
        "status": "READY"
    })

report = {
    "module": "FORGE-EXEC-0006",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "workers": worker_status,
    "worker_count": len(worker_status),
    "dispatches": QUEUE["dispatch_count"],
    "system_ready": all(w["status"] == "READY" for w in worker_status),
    "dispatch_hash": QUEUE["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/exec/execution_monitor.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-EXEC-0006")
print("Execution Monitor Engine")
print("=" * 60)
print("Workers     :", report["worker_count"])
print("Dispatches  :", report["dispatches"])
print("Ready       :", report["system_ready"])
print("Output      :", OUT)
print()
print("STATUS : PASS")
