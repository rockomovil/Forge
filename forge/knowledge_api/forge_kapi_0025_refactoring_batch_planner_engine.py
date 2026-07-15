#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

QUEUE = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_layer_refactoring_queue.json").read_text()
)

batch_size = 5

batches = []

items = QUEUE["refactoring_queue"]

for i in range(0, len(items), batch_size):

    chunk = items[i:i + batch_size]

    batches.append({
        "batch": len(batches) + 1,
        "size": len(chunk),
        "modules": [x["module"] for x in chunk],
        "estimated_priority": min(x["priority"] for x in chunk)
    })

report = {
    "module": "FORGE-KAPI-0025",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "queue_size": len(items),
    "batch_size": batch_size,
    "batch_count": len(batches),
    "batches": batches
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_batches.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0025")
print("Refactoring Batch Planner Engine")
print("=" * 60)
print("Queue Size  :", report["queue_size"])
print("Batch Size  :", report["batch_size"])
print("Batch Count :", report["batch_count"])
print("Output      :", outfile)
print()
print("STATUS : PASS")
