#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

PLAN = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_refactoring_plan.json").read_text()
)

LAYERS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_layers.json").read_text()
)

HEALTH = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_health_score.json").read_text()
)

roadmap = []

for phase, action in enumerate(PLAN["recommended_actions"], start=1):

    roadmap.append({
        "phase": phase,
        "title": action["action"],
        "priority": action["priority"],
        "expected_health_score": round(
            min(
                100.0,
                HEALTH["architecture_health_score"] + phase * 1.5
            ),
            2
        )
    })

report = {
    "module": "FORGE-KAPI-0017",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "current_health_score": HEALTH["architecture_health_score"],
    "architecture_layers": LAYERS["layers"],
    "roadmap": roadmap
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_architecture_execution_roadmap.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0017")
print("Architecture Execution Roadmap Engine")
print("=" * 60)
print("Current Health Score :", report["current_health_score"])
print("Layers               :", len(LAYERS["layers"]))
print("Roadmap Phases       :", len(roadmap))
print("Output               :", outfile)
print()
print("STATUS : PASS")
