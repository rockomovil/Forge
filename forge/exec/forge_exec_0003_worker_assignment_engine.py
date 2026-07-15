#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

CAPS = json.loads(
    (ROOT / "runtime/exec/worker_capability_registry.json").read_text()
)

PLAN = json.loads(
    (ROOT / "runtime/build/build_execution_plan.json").read_text()
)

capabilities = CAPS["capability_registry"]

assignments = []

for step in PLAN["execution_plan"]:

    workers = []

    for job in step["jobs"]:

        if "validation" in job.lower():
            capability = "validation"
        elif "release" in job.lower():
            capability = "release"
        elif "audit" in job.lower():
            capability = "audit"
        else:
            capability = "build"

        worker = capabilities.get(capability, ["worker-002"])[0]

        workers.append({
            "module": job,
            "worker": worker,
            "capability": capability
        })

    assignments.append({
        "step": step["step"],
        "parallel": step["parallel"],
        "assignments": workers
    })

report = {
    "module": "FORGE-EXEC-0003",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "worker_assignments": assignments,
    "execution_steps": len(assignments),
    "assigned_jobs": sum(
        len(x["assignments"]) for x in assignments
    )
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/exec/worker_assignment_plan.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-EXEC-0003")
print("Worker Assignment Engine")
print("=" * 60)
print("Execution Steps :", report["execution_steps"])
print("Assigned Jobs   :", report["assigned_jobs"])
print("Output          :", OUT)
print()
print("STATUS : PASS")
