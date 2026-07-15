#!/usr/bin/env python3

from pathlib import Path
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]

REPORT = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_policy_validation.json").read_text()
)

counter = Counter()

for v in REPORT["violation_details"]:
    key = f'{v["from_layer"]}->{v["to_layer"]}'
    counter[key] += 1

ranking = [
    {
        "transition": k,
        "violations": n
    }
    for k, n in sorted(
        counter.items(),
        key=lambda x: (-x[1], x[0])
    )
]

summary = {
    "module": "FORGE-KAPI-0022",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "policy_pass": REPORT["architecture_policy_pass"],
    "total_violations": REPORT["violations"],
    "transition_types": len(ranking),
    "top_transitions": ranking[:25],
    "classification": ranking
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_layer_violation_classification.json"
outfile.write_text(json.dumps(summary, indent=2))

print("=" * 60)
print("FORGE-KAPI-0022")
print("Layer Violation Classifier Engine")
print("=" * 60)
print("Violations      :", summary["total_violations"])
print("Transition Types:", summary["transition_types"])
print("Top Classes     :", len(summary["top_transitions"]))
print("Output          :", outfile)
print()
print("STATUS : PASS")
