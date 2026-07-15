#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

CERT = json.loads(
    (ROOT / "runtime/build/build_certification.json").read_text()
)

AUDIT = json.loads(
    (ROOT / "runtime/build/build_audit.json").read_text()
)

EXEC = json.loads(
    (ROOT / "runtime/build/build_execution_plan.json").read_text()
)

released = (
    CERT["build_certified"]
    and AUDIT["status"] == "PASS"
)

report = {
    "module": "FORGE-BUILD-0009",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "build_release_ready": released,
    "execution_steps": EXEC["execution_steps"],
    "total_jobs": EXEC["total_jobs"],

    "artifacts": {
        "audit": AUDIT["hash"],
        "certification": CERT["hash"],
        "execution": EXEC["hash"]
    }
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/build/build_release.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-BUILD-0009")
print("Build Release Engine")
print("=" * 60)
print("Release Ready :", released)
print("Execution     :", report["execution_steps"])
print("Jobs          :", report["total_jobs"])
print("Output        :", OUT)
print()
print("STATUS : PASS")
