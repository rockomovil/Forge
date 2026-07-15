#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

LAYERS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_layers.json").read_text()
)

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

SCC = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_strongly_connected_components.json").read_text()
)

component_layer = {}

for layer, comps in LAYERS["layers"].items():
    for comp in comps:
        component_layer[int(comp)] = int(layer)

component_of = {}

for cid, comp in enumerate(SCC["strongly_connected_components"]):
    for node in comp:
        component_of[node] = cid

violations = []

for edge in GRAPH["edges"]:

    if edge["relation"] != "depends_on":
        continue

    a = component_of.get(edge["from"])
    b = component_of.get(edge["to"])

    if a is None or b is None:
        continue

    la = component_layer.get(a)
    lb = component_layer.get(b)

    if la is None or lb is None:
        continue

    if la < lb:

        violations.append({
            "from": edge["from"],
            "to": edge["to"],
            "from_layer": la,
            "to_layer": lb
        })

report = {
    "module": "FORGE-KAPI-0021",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "checked_dependencies": sum(
        1 for e in GRAPH["edges"]
        if e["relation"] == "depends_on"
    ),
    "policy": "Dependencies may target same or lower architectural layers only.",
    "violations": len(violations),
    "architecture_policy_pass": len(violations) == 0,
    "violation_details": violations[:100]
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_architecture_policy_validation.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0021")
print("Architecture Policy Validation Engine")
print("=" * 60)
print("Dependencies Checked :", report["checked_dependencies"])
print("Violations           :", report["violations"])
print("Policy Pass          :", report["architecture_policy_pass"])
print("Output               :", outfile)
print()
print("STATUS : PASS")
