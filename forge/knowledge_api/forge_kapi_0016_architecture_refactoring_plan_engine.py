#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

RECOMMENDATIONS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_recommendations.json").read_text()
)

SCC = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_strongly_connected_components.json").read_text()
)

CENTRALITY = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_centrality_analysis.json").read_text()
)

largest = SCC["strongly_connected_components"][0]

top_coupled = [
    x for x in CENTRALITY["ranking"]
    if x["in_degree"] >= 100
]

plan = {
    "module": "FORGE-KAPI-0016",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "health_score": RECOMMENDATIONS["architecture_health_score"],
    "largest_cycle_size": len(largest),
    "largest_cycle_modules": largest,
    "high_coupling_modules": top_coupled,
    "recommended_actions": [
        {
            "priority": 1,
            "action": "Break largest strongly connected component"
        },
        {
            "priority": 2,
            "action": "Introduce interfaces around high fan-in modules"
        },
        {
            "priority": 3,
            "action": "Reduce cyclic dependencies"
        },
        {
            "priority": 4,
            "action": "Increase architectural layering"
        }
    ]
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_architecture_refactoring_plan.json"
outfile.write_text(json.dumps(plan, indent=2))

print("=" * 60)
print("FORGE-KAPI-0016")
print("Architecture Refactoring Plan Engine")
print("=" * 60)
print("Health Score        :", plan["health_score"])
print("Largest SCC         :", plan["largest_cycle_size"])
print("High Fan-In Modules :", len(top_coupled))
print("Actions             :", len(plan["recommended_actions"]))
print("Output              :", outfile)
print()
print("STATUS : PASS")
