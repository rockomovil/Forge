#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

PLAN = json.loads(
    (ROOT / "runtime/exec/worker_assignment_plan.json").read_text()
)

schedule = []

slot = 1

for step in PLAN["worker_assignments"]:

    jobs = []

    for assignment in step["assignments"]:
        jobs.append({
            "slot": slot,
            "worker": assignment["worker"],
            "module": assignment["module"],
            "capability": assignment["capability"]
        })
        slot += 1

    schedule.append({
        "step": step["step"],
        "parallel": step["parallel"],
        "jobs": jobs
    })

report = {
    "module": "FORGE-EXEC-0004",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "execution_schedule": schedule,
    "steps": len(schedule),
    "scheduled_jobs": slot - 1
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/exec/execution_schedule.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-EXEC-0004")
print("Execution Scheduler Engine")
print("=" * 60)
print("Steps          :", report["steps"])
print("Scheduled Jobs :", report["scheduled_jobs"])
print("Output         :", OUT)
print()
print("STATUS : PASS")
