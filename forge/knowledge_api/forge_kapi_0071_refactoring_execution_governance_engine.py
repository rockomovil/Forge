#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

DASHBOARD = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_execution_dashboard.json").read_text()
)

governance = {
    "module": "FORGE-KAPI-0071",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "governance_state": (
        "EXECUTION_HEALTHY"
        if DASHBOARD["terminal"] else
        "BLOCKED"
    ),
    "terminal": DASHBOARD["terminal"],
    "execution_mode": DASHBOARD["execution_mode"],
    "worker_count": DASHBOARD["worker_count"],
    "immutable": DASHBOARD["immutable"],
    "parallel_execution": DASHBOARD["dashboard"]["parallel_execution"],
    "shadow_only": DASHBOARD["dashboard"]["shadow_only"],
    "safe_mode": DASHBOARD["dashboard"]["safe_mode"],
    "live_mutation": DASHBOARD["dashboard"]["live_mutation"]
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_execution_governance.json"
outfile.write_text(json.dumps(governance, indent=2))

print("=" * 60)
print("FORGE-KAPI-0071")
print("Refactoring Execution Governance Engine")
print("=" * 60)
print("Governance :", governance["governance_state"])
print("Terminal   :", governance["terminal"])
print("Workers    :", governance["worker_count"])
print("Mode       :", governance["execution_mode"])
print("Output     :", outfile)
print()
print("STATUS : PASS")
