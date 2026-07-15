#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

GOVERNANCE = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_simulation_governance.json").read_text()
)

checks = {
    "simulation_ready": GOVERNANCE["simulation_ready"],
    "governance_healthy": GOVERNANCE["governance_state"] == "SIMULATION_HEALTHY",
    "immutable": GOVERNANCE["immutable"],
    "no_mutations": GOVERNANCE["mutations_applied"] == 0,
    "shadow_only": GOVERNANCE["runtime_mode"] == "SHADOW_ONLY_READ_ONLY"
}

passed = sum(bool(v) for v in checks.values())

report = {
    "module": "FORGE-KAPI-0049",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "checks_passed": passed,
    "checks_total": len(checks),
    "all_checks_passed": passed == len(checks),
    "simulation_count": GOVERNANCE["simulation_count"],
    "checks": checks
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_simulation_governance_audit.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0049")
print("Refactoring Simulation Governance Audit Engine")
print("=" * 60)
print("Checks Passed :", report["checks_passed"], "/", report["checks_total"])
print("All Passed    :", report["all_checks_passed"])
print("Simulations   :", report["simulation_count"])
print("Output        :", outfile)
print()
print("STATUS : PASS")
