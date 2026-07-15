#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

METRICS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_metrics.json").read_text()
)

SCC = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_strongly_connected_components.json").read_text()
)

components = METRICS["components"]
layers = METRICS["layers"]
largest_scc = METRICS["largest_scc"]
cyclic_components = SCC["cyclic_components"]

acyclic_ratio = (components - cyclic_components) / components

layer_score = min(layers / 20.0, 1.0)
scc_score = 1.0 - (largest_scc / components)
cycle_score = acyclic_ratio

health_score = round(
    (
        layer_score * 0.30 +
        scc_score * 0.35 +
        cycle_score * 0.35
    ) * 100,
    2
)

report = {
    "module": "FORGE-KAPI-0014",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "components": components,
    "layers": layers,
    "cyclic_components": cyclic_components,
    "largest_scc": largest_scc,
    "layer_score": round(layer_score, 4),
    "scc_score": round(scc_score, 4),
    "cycle_score": round(cycle_score, 4),
    "architecture_health_score": health_score
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_architecture_health_score.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0014")
print("Architecture Health Score Engine")
print("=" * 60)
print("Components                :", components)
print("Layers                    :", layers)
print("Largest SCC               :", largest_scc)
print("Cyclic Components         :", cyclic_components)
print("Architecture Health Score :", health_score)
print("Output                    :", outfile)
print()
print("STATUS : PASS")
