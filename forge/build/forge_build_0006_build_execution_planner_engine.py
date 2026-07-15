#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

PARALLEL = json.loads(
    (ROOT / "runtime/build/parallel_build_plan.json").read_text()
)

INCREMENTAL = json.loads(
    (ROOT / "runtime/build/incremental_build_plan.json").read_text()
)

execution_plan = []

parallel_levels = PARALLEL["parallel_execution_plan"]
incremental = set(INCREMENTAL["rebuild_required"])

step = 1

for level in parallel_levels:

    jobs = [
        m for m in level["modules"]
        if m in incremental
    ]

    if not jobs:
        continue

    execution_plan.append({
        "step": step,
        "parallel": True,
        "level": level["level"],
        "jobs": jobs,
        "job_count": len(jobs)
    })

    step += 1

report = {
    "module": "FORGE-BUILD-0006",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "execution_plan": execution_plan,
    "execution_steps": len(execution_plan),
    "total_jobs": sum(x["job_count"] for x in execution_plan),
    "incremental_build": True,
    "parallel_execution": True
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/build/build_execution_plan.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-BUILD-0006")
print("Build Execution Planner Engine")
print("=" * 60)
print("Execution Steps :", report["execution_steps"])
print("Total Jobs      :", report["total_jobs"])
print("Parallel        :", report["parallel_execution"])
print("Incremental     :", report["incremental_build"])
print("Output          :", OUT)
print()
print("STATUS : PASS")
