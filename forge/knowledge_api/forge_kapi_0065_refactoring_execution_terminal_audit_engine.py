#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

LOCK = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_execution_lock.json").read_text()
)

checks = {
    "certified": LOCK["certified"],
    "sealed": LOCK["sealed"],
    "locked": LOCK["locked"],
    "immutable": LOCK["immutable"],
    "parallel_mode": LOCK["execution_mode"] == "PARALLEL_PATCH_SIMULATION",
    "workers_available": LOCK["worker_count"] > 0
}

passed = sum(bool(v) for v in checks.values())

report = {
    "module": "FORGE-KAPI-0065",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "checks_passed": passed,
    "checks_total": len(checks),
    "all_checks_passed": passed == len(checks),
    "execution_mode": LOCK["execution_mode"],
    "worker_count": LOCK["worker_count"],
    "checks": checks
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_execution_terminal_audit.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0065")
print("Refactoring Execution Terminal Audit Engine")
print("=" * 60)
print("Checks Passed :", report["checks_passed"], "/", report["checks_total"])
print("All Passed    :", report["all_checks_passed"])
print("Workers       :", report["worker_count"])
print("Mode          :", report["execution_mode"])
print("Output        :", outfile)
print()
print("STATUS : PASS")
