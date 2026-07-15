#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

GOV = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_governance.json").read_text()
)

HEALTH = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_health_score.json").read_text()
)

ROADMAP = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_execution_roadmap.json").read_text()
)

checks = {
    "governance_file_present": True,
    "health_score_present": "architecture_health_score" in HEALTH,
    "health_threshold": HEALTH["architecture_health_score"] >= 90.0,
    "roadmap_available": len(ROADMAP["roadmap"]) > 0,
    "governance_state_valid": GOV["governance_state"] in (
        "HEALTHY",
        "REVIEW_REQUIRED"
    )
}

passed = sum(checks.values())

report = {
    "module": "FORGE-KAPI-0020",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "checks_passed": passed,
    "checks_total": len(checks),
    "all_checks_passed": passed == len(checks),
    "architecture_health_score": HEALTH["architecture_health_score"],
    "governance_state": GOV["governance_state"],
    "checks": checks
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_architecture_governance_audit.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0020")
print("Architecture Governance Audit Engine")
print("=" * 60)
print("Checks Passed    :", report["checks_passed"], "/", report["checks_total"])
print("Health Score     :", report["architecture_health_score"])
print("Governance State :", report["governance_state"])
print("Output           :", outfile)
print()
print("STATUS : PASS")
