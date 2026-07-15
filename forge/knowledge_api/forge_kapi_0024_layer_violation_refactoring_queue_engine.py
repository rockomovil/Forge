#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

HOTSPOTS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_layer_violation_hotspots.json").read_text()
)

CLASSIFICATION = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_layer_violation_classification.json").read_text()
)

queue = []

priority = 1

for item in HOTSPOTS["top_source_hotspots"]:

    queue.append({
        "priority": priority,
        "module": item["module"],
        "reason": "High outgoing layer violations",
        "violation_count": item["violations"]
    })

    priority += 1

report = {
    "module": "FORGE-KAPI-0024",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "total_violations": HOTSPOTS["total_violations"],
    "transition_classes": CLASSIFICATION["transition_types"],
    "queue_size": len(queue),
    "refactoring_queue": queue
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_layer_refactoring_queue.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0024")
print("Layer Violation Refactoring Queue Engine")
print("=" * 60)
print("Violations        :", report["total_violations"])
print("Transition Types  :", report["transition_classes"])
print("Queue Size        :", report["queue_size"])
print("Output            :", outfile)
print()
print("STATUS : PASS")
