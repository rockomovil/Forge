#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

HEALTH = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_health_score.json").read_text()
)

METRICS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_metrics.json").read_text()
)

ROADMAP = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_execution_roadmap.json").read_text()
)

RECOMMENDATIONS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_recommendations.json").read_text()
)

dashboard = {
    "module": "FORGE-KAPI-0018",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "summary": {
        "architecture_health_score": HEALTH["architecture_health_score"],
        "components": METRICS["components"],
        "layers": METRICS["layers"],
        "largest_scc": METRICS["largest_scc"],
        "roadmap_phases": len(ROADMAP["roadmap"]),
        "recommendations": RECOMMENDATIONS["recommendation_count"]
    },
    "kpis": {
        "average_scc_size": METRICS["average_scc_size"],
        "largest_layer_size": METRICS["largest_layer_size"],
        "average_layer_size": METRICS["average_layer_size"]
    },
    "next_phase": ROADMAP["roadmap"][0] if ROADMAP["roadmap"] else None
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_architecture_dashboard.json"
outfile.write_text(json.dumps(dashboard, indent=2))

print("=" * 60)
print("FORGE-KAPI-0018")
print("Architecture Evolution Dashboard Engine")
print("=" * 60)
print("Health Score    :", HEALTH["architecture_health_score"])
print("Components      :", METRICS["components"])
print("Layers          :", METRICS["layers"])
print("Largest SCC     :", METRICS["largest_scc"])
print("Roadmap Phases  :", len(ROADMAP["roadmap"]))
print("Recommendations :", RECOMMENDATIONS["recommendation_count"])
print("Output          :", outfile)
print()
print("STATUS : PASS")
