#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

IMPACT_FILE = ROOT / "runtime/build/change_impact_plan.json"
VALIDATION_FILE = ROOT / "runtime/build/validation_plan.json"
ORDER_FILE = ROOT / "runtime/build/build_order_plan.json"
PARALLEL_FILE = ROOT / "runtime/build/parallel_build_plan.json"
INCREMENTAL_FILE = ROOT / "runtime/build/incremental_build_plan.json"
EXECUTION_FILE = ROOT / "runtime/build/build_execution_plan.json"

OUTPUT_FILE = ROOT / "runtime/build/build_audit.json"

impact = json.loads(IMPACT_FILE.read_text())
validation = json.loads(VALIDATION_FILE.read_text())
order = json.loads(ORDER_FILE.read_text())
parallel = json.loads(PARALLEL_FILE.read_text())
incremental = json.loads(INCREMENTAL_FILE.read_text())
execution = json.loads(EXECUTION_FILE.read_text())

target = impact["target_module"]

execution_jobs = [
    job
    for step in execution["execution_plan"]
    for job in step["jobs"]
]

checks = {
    "target_consistency": (
        target
        == validation["target_module"]
        == order["target_module"]
        == parallel["target_module"]
        == incremental["target_module"]
    ),
    "impact_validation_consistency": (
        set(impact["affected_modules"])
        == set(validation["validation_sequence"])
    ),
    "impact_order_consistency": (
        set(impact["affected_modules"])
        == set(order["build_order"])
    ),
    "impact_incremental_consistency": (
        set(impact["affected_modules"])
        == set(incremental["rebuild_required"])
    ),
    "execution_jobs_consistency": (
        set(execution_jobs)
        == set(incremental["rebuild_required"])
    ),
    "execution_job_count_consistency": (
        execution["total_jobs"] == len(execution_jobs)
    ),
    "parallel_enabled": execution["parallel_execution"] is True,
    "incremental_enabled": execution["incremental_build"] is True,
    "shadow_runtime": all(
        artifact["runtime_mode"] == "SHADOW_ONLY_READ_ONLY"
        for artifact in (
            impact,
            validation,
            order,
            parallel,
            incremental,
            execution,
        )
    ),
}

passed = sum(checks.values())
total = len(checks)
status = "PASS" if passed == total else "FAIL"

result = {
    "module": "FORGE-BUILD-0007",
    "status": status,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "audited_at": datetime.now(UTC).isoformat(),
    "target_module": target,
    "checks": checks,
    "passed": passed,
    "total": total,
    "execution_steps": execution["execution_steps"],
    "total_jobs": execution["total_jobs"],
    "artifact_hashes": {
        "impact": impact["hash"],
        "validation": validation["hash"],
        "order": order["hash"],
        "parallel": parallel["hash"],
        "incremental": incremental["hash"],
        "execution": execution["hash"],
    },
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-BUILD-0007")
print("Build Audit Engine")
print("=" * 60)
print("Target          :", result["target_module"])
print("Checks          :", result["passed"], "/", result["total"])
print("Execution Steps :", result["execution_steps"])
print("Total Jobs      :", result["total_jobs"])
print("Output          :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])

if result["status"] != "PASS":
    raise SystemExit(1)
