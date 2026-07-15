#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

SCHEDULE_FILE = ROOT / "runtime" / "exec" / "execution_schedule.json"
OUTPUT_FILE = ROOT / "runtime" / "exec" / "execution_dispatch_queue.json"

if not SCHEDULE_FILE.is_file():
    raise FileNotFoundError(f"Missing execution schedule: {SCHEDULE_FILE}")

schedule = json.loads(SCHEDULE_FILE.read_text())

dispatch_queue = []
dispatch_id = 1

for step in schedule["execution_schedule"]:
    for job in step["jobs"]:
        dispatch_queue.append({
            "dispatch_id": dispatch_id,
            "step": step["step"],
            "parallel": step["parallel"],
            "worker": job["worker"],
            "module": job["module"],
            "capability": job["capability"],
            "state": "READY",
        })
        dispatch_id += 1

report = {
    "module": "FORGE-EXEC-0005",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),
    "dispatch_queue": dispatch_queue,
    "dispatch_count": len(dispatch_queue),
    "scheduler_steps": schedule["steps"],
    "schedule_hash": schedule["hash"],
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-EXEC-0005")
print("Execution Dispatcher Engine")
print("=" * 60)
print("Dispatches :", report["dispatch_count"])
print("Steps      :", report["scheduler_steps"])
print("Output     :", OUTPUT_FILE)
print()
print("STATUS :", report["status"])
