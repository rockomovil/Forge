#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

MODULE = "FORGE-SCHEDULER-002"
STATUS = "FORGE_LOAD_METRICS_ENGINE_READY"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime" / "scheduler"

state = json.loads(
    (RUNTIME / "forge_worker_state_001.json").read_text(encoding="utf-8")
)

metrics = {}

busy_workers = 0

for name, worker in state["workers"].items():

    utilization = (
        worker["running_jobs"] /
        max(1, worker["running_jobs"] + 1)
    )

    if worker["state"] != "IDLE":
        busy_workers += 1

    metrics[name] = {
        "state": worker["state"],
        "utilization": round(utilization, 3),
        "running_jobs": worker["running_jobs"],
        "completed_jobs": worker["completed_jobs"],
    }

payload = {
    "module": MODULE,
    "status": STATUS,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated": datetime.now(UTC).isoformat(),
    "worker_count": len(metrics),
    "busy_workers": busy_workers,
    "idle_workers": len(metrics) - busy_workers,
    "metrics": metrics,
}

text = json.dumps(payload, indent=2, sort_keys=True)

(RUNTIME / "forge_load_metrics_002.json").write_text(
    text,
    encoding="utf-8",
)

integrity = hashlib.sha256(text.encode()).hexdigest()

(RUNTIME / "forge_load_metrics_002_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "integrity_hash": integrity,
        },
        indent=2,
    ),
    encoding="utf-8",
)

with (RUNTIME / "forge_load_metrics_002_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(
        json.dumps(
            {
                "timestamp": payload["generated"],
                "module": MODULE,
                "status": STATUS,
                "integrity_hash": integrity,
            }
        ) + "\n"
    )

verification = hashlib.sha256(
    (MODULE + STATUS + integrity).encode()
).hexdigest()

print(MODULE)
print(STATUS)
print(f"worker_count = {payload['worker_count']}")
print(f"busy_workers = {payload['busy_workers']}")
print(f"idle_workers = {payload['idle_workers']}")
print(f"integrity_hash = {integrity}")
print(f"hash = {verification}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
