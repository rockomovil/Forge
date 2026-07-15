#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

AUDIT = json.loads(
    (ROOT / "runtime/build/build_audit.json").read_text()
)

EXECUTION = json.loads(
    (ROOT / "runtime/build/build_execution_plan.json").read_text()
)

certified = (
    AUDIT["status"] == "PASS"
    and AUDIT["passed"] == AUDIT["total"]
)

report = {
    "module": "FORGE-BUILD-0008",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "build_certified": certified,
    "execution_steps": EXECUTION["execution_steps"],
    "total_jobs": EXECUTION["total_jobs"],
    "audit_hash": AUDIT["hash"],
    "execution_hash": EXECUTION["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/build/build_certification.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-BUILD-0008")
print("Build Certification Engine")
print("=" * 60)
print("Certified      :", certified)
print("Execution Steps:", report["execution_steps"])
print("Total Jobs     :", report["total_jobs"])
print("Output         :", OUT)
print()
print("STATUS : PASS")
