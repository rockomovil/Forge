#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

DASHBOARD = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_dashboard.json").read_text()
)

ROADMAP = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_execution_roadmap.json").read_text()
)

HEALTH = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_health_score.json").read_text()
)

governance = {
    "module": "FORGE-KAPI-0019",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "architecture_health_score": HEALTH["architecture_health_score"],
    "governance_state": (
        "HEALTHY"
        if HEALTH["architecture_health_score"] >= 90
        else "REVIEW_REQUIRED"
    ),
    "roadmap_completed": 0,
    "roadmap_total": len(ROADMAP["roadmap"]),
    "next_action": (
        ROADMAP["roadmap"][0]["title"]
        if ROADMAP["roadmap"] else None
    ),
    "dashboard_snapshot": DASHBOARD["summary"]
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_architecture_governance.json"
outfile.write_text(json.dumps(governance, indent=2))

print("=" * 60)
print("FORGE-KAPI-0019")
print("Architecture Governance Engine")
print("=" * 60)
print("Governance State :", governance["governance_state"])
print("Health Score     :", governance["architecture_health_score"])
print("Roadmap          :", governance["roadmap_completed"],
      "/", governance["roadmap_total"])
print("Next Action      :", governance["next_action"])
print("Output           :", outfile)
print()
print("STATUS : PASS")
