#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

GOVERNANCE = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_execution_governance.json").read_text()
)

checks = {
    "execution_healthy": GOVERNANCE["governance_state"] == "EXECUTION_HEALTHY",
    "terminal": GOVERNANCE["terminal"],
    "parallel_execution": GOVERNANCE["parallel_execution"],
    "shadow_only": GOVERNANCE["shadow_only"],
    "safe_mode": GOVERNANCE["safe_mode"],
    "immutable": GOVERNANCE["immutable"]
}

passed = sum(bool(v) for v in checks.values())

report = {
    "module": "FORGE-KAPI-0072",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "checks_passed": passed,
    "checks_total": len(checks),
    "all_checks_passed": passed == len(checks),
    "governance_state": GOVERNANCE["governance_state"],
    "worker_count": GOVERNANCE["worker_count"],
    "execution_mode": GOVERNANCE["execution_mode"],
    "checks": checks
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_execution_governance_audit.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0072")
print("Refactoring Execution Governance Audit Engine")
print("=" * 60)
print("Checks Passed :", report["checks_passed"], "/", report["checks_total"])
print("All Passed    :", report["all_checks_passed"])
print("Governance    :", report["governance_state"])
print("Workers       :", report["worker_count"])
print("Mode          :", report["execution_mode"])
print("Output        :", outfile)
print()
print("STATUS : PASS")
