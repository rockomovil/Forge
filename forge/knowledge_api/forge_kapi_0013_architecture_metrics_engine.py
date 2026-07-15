#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import json

ROOT = Path(__file__).resolve().parents[2]

LAYERS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_layers.json").read_text()
)

SCC = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_strongly_connected_components.json").read_text()
)

layer_sizes = {
    int(level): len(nodes)
    for level, nodes in LAYERS["layers"].items()
}

largest_layer = max(layer_sizes.values()) if layer_sizes else 0
average_layer = (
    sum(layer_sizes.values()) / len(layer_sizes)
    if layer_sizes else 0
)

component_sizes = [
    len(component)
    for component in SCC["strongly_connected_components"]
]

distribution = defaultdict(int)

for size in component_sizes:
    distribution[size] += 1

report = {
    "module": "FORGE-KAPI-0013",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "components": LAYERS["components"],
    "layers": len(layer_sizes),
    "max_layer": LAYERS["max_layer"],
    "largest_layer_size": largest_layer,
    "average_layer_size": round(average_layer, 3),
    "largest_scc": max(component_sizes) if component_sizes else 0,
    "average_scc_size": round(
        sum(component_sizes) / len(component_sizes),
        3
    ) if component_sizes else 0,
    "scc_size_distribution": dict(sorted(distribution.items())),
    "layer_sizes": dict(sorted(layer_sizes.items()))
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_architecture_metrics.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0013")
print("Architecture Metrics Engine")
print("=" * 60)
print("Components          :", report["components"])
print("Layers              :", report["layers"])
print("Maximum Layer       :", report["max_layer"])
print("Largest Layer       :", report["largest_layer_size"])
print("Average Layer Size  :", report["average_layer_size"])
print("Largest SCC         :", report["largest_scc"])
print("Average SCC Size    :", report["average_scc_size"])
print("Output              :", outfile)
print()
print("STATUS : PASS")
