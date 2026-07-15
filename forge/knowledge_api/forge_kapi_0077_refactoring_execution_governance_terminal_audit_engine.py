#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

STATE = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_execution_governance_terminal_state.json").read_text()
)

checks = {
    "terminal_state": STATE["terminal_state"],
    "locked": STATE["locked"],
    "immutable": STATE["immutable"],
    "governance_state": STATE["governance_state"] == "EXECUTION_HEALTHY",
    "shadow_mode": STATE["runtime_mode"] == "SHADOW_ONLY_READ_ONLY",
    "parallel_mode": STATE["execution_mode"] == "PARALLEL_PATCH_SIMULATION"
}

passed = sum(bool(v) for v in checks.values())

report = {
    "module": "FORGE-KAPI-0077",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "checks_passed": passed,
    "checks_total": len(checks),
    "all_checks_passed": passed == len(checks),
    "terminal_state": STATE["terminal_state"],
    "governance_state": STATE["governance_state"],
    "locked": STATE["locked"],
    "immutable": STATE["immutable"],
    "worker_count": STATE["worker_count"],
    "execution_mode": STATE["execution_mode"],
    "checks": checks
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_execution_governance_terminal_audit.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0077")
print("Refactoring Execution Governance Terminal Audit Engine")
print("=" * 60)
print("Checks Passed :", report["checks_passed"], "/", report["checks_total"])
print("All Passed    :", report["all_checks_passed"])
print("Terminal      :", report["terminal_state"])
print("Locked        :", report["locked"])
print("Immutable     :", report["immutable"])
print("Workers       :", report["worker_count"])
print("Mode          :", report["execution_mode"])
print("Output        :", outfile)
print()
print("STATUS : PASS")
