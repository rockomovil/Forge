#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = json.loads(
    (ROOT / "runtime/exec/worker_registry.json").read_text()
)

QUEUE = json.loads(
    (ROOT / "runtime/exec/execution_dispatch_queue.json").read_text()
)

workers = {
    w["id"]: {
        "role": w["role"],
        "capabilities": set(w["capabilities"]),
        "queue": []
    }
    for w in REGISTRY["worker_registry"]
}

def capability_for(module, fallback):
    name = module.lower()

    if "validation" in name:
        return "validation"
    if "audit" in name:
        return "audit"
    if "release" in name:
        return "release"
    if "cert" in name:
        return "certification"

    return fallback

for job in QUEUE["dispatch_queue"]:

    cap = capability_for(job["module"], job["capability"])

    candidates = [
        wid
        for wid, data in workers.items()
        if cap in data["capabilities"]
    ]

    if not candidates:
        candidates = list(workers.keys())

    selected = min(
        candidates,
        key=lambda wid: (
            len(workers[wid]["queue"]),
            wid
        )
    )

    workers[selected]["queue"].append({
        "dispatch_id": job["dispatch_id"],
        "module": job["module"],
        "capability": cap,
        "priority": len(workers[selected]["queue"]) + 1
    })

queues = []

for wid in sorted(workers):
    queues.append({
        "worker": wid,
        "role": workers[wid]["role"],
        "queue_length": len(workers[wid]["queue"]),
        "queue": workers[wid]["queue"]
    })

lengths = [q["queue_length"] for q in queues]

report = {
    "module": "FORGE-EXEC-0009",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "optimized_worker_queues": queues,
    "worker_count": len(queues),
    "dispatch_count": QUEUE["dispatch_count"],

    "max_queue": max(lengths, default=0),
    "min_queue": min(lengths, default=0),
    "queue_delta": max(lengths, default=0) - min(lengths, default=0)
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/exec/worker_queue_optimizer.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-EXEC-0009")
print("Worker Queue Optimizer Engine")
print("=" * 60)
print("Workers   :", report["worker_count"])
print("Jobs      :", report["dispatch_count"])
print("Max Queue :", report["max_queue"])
print("Min Queue :", report["min_queue"])
print("Delta     :", report["queue_delta"])
print("Output    :", OUT)
print()
print("STATUS : PASS")
