#!/usr/bin/env python3

from pathlib import Path
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]

REPORT = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_policy_validation.json").read_text()
)

source = Counter()
target = Counter()

for v in REPORT["violation_details"]:
    source[v["from"]] += 1
    target[v["to"]] += 1

summary = {
    "module": "FORGE-KAPI-0023",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "total_violations": REPORT["violations"],
    "top_source_hotspots": [
        {"module": m, "violations": n}
        for m, n in source.most_common(50)
    ],
    "top_target_hotspots": [
        {"module": m, "violations": n}
        for m, n in target.most_common(50)
    ]
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_layer_violation_hotspots.json"
outfile.write_text(json.dumps(summary, indent=2))

print("=" * 60)
print("FORGE-KAPI-0023")
print("Layer Violation Hotspots Engine")
print("=" * 60)
print("Violations :", summary["total_violations"])
print("Top Sources:", len(summary["top_source_hotspots"]))
print("Top Targets:", len(summary["top_target_hotspots"]))
print("Output     :", outfile)
print()
print("STATUS : PASS")
