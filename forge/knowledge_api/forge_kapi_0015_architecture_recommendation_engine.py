#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

HEALTH = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_health_score.json").read_text()
)

SCC = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_strongly_connected_components.json").read_text()
)

CENTRALITY = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_centrality_analysis.json").read_text()
)

recommendations = []

if HEALTH["largest_scc"] > 10:
    recommendations.append({
        "priority": "HIGH",
        "category": "cycles",
        "message": (
            f"Refactor largest strongly connected component "
            f"({HEALTH['largest_scc']} modules)."
        )
    })

if HEALTH["cyclic_components"] > 0:
    recommendations.append({
        "priority": "HIGH",
        "category": "cycles",
        "message": (
            f"Reduce {HEALTH['cyclic_components']} cyclic components."
        )
    })

for module in CENTRALITY["ranking"][:10]:

    if module["in_degree"] > 100:

        recommendations.append({
            "priority": "MEDIUM",
            "category": "coupling",
            "module": module["node"],
            "message": (
                f"High fan-in ({module['in_degree']}) "
                "consider interface extraction."
            )
        })

report = {
    "module": "FORGE-KAPI-0015",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "architecture_health_score":
        HEALTH["architecture_health_score"],
    "recommendation_count": len(recommendations),
    "recommendations": recommendations
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_architecture_recommendations.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0015")
print("Architecture Recommendation Engine")
print("=" * 60)
print("Health Score     :", HEALTH["architecture_health_score"])
print("Recommendations  :", len(recommendations))
print()

for rec in recommendations:
    print(
        f'[{rec["priority"]}] '
        f'{rec["category"]} - '
        f'{rec["message"]}'
    )

print()
print("Output :", outfile)
print()
print("STATUS : PASS")
