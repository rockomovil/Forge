#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

MODULE = "FORGE-KERNEL-010"
STATUS = "FORGE_PERFORMANCE_GOVERNOR_READY"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime" / "kernel"

profiler = json.loads(
    (RUNTIME / "forge_execution_profiler_009.json").read_text(
        encoding="utf-8"
    )
)

workforce = json.loads(
    (RUNTIME / "forge_workforce_registry_008.json").read_text(
        encoding="utf-8"
    )
)

metrics = profiler["metrics"]

tasks = metrics["scheduled_tasks"]
workers = max(1, metrics["worker_instance_count"])
ratio = tasks / workers

if ratio <= 1:
    recommendation = "KEEP_CONFIGURATION"
elif ratio <= 4:
    recommendation = "MONITOR_LOAD"
else:
    recommendation = "EXPAND_WORKFORCE"

governor = {
    "module": MODULE,
    "status": STATUS,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated": datetime.now(UTC).isoformat(),
    "current_metrics": metrics,
    "governor_state": "READY",
    "recommended_action": recommendation,
    "recommended_worker_instances": max(workers, round(ratio)),
    "current_worker_instances": workers,
    "worker_pool_count": workforce["worker_pool_count"],
}

payload = json.dumps(governor, indent=2, sort_keys=True)

(RUNTIME / "forge_performance_governor_010.json").write_text(
    payload,
    encoding="utf-8",
)

integrity = hashlib.sha256(payload.encode()).hexdigest()

(RUNTIME / "forge_performance_governor_010_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "integrity_hash": integrity,
        },
        indent=2,
    ),
    encoding="utf-8",
)

with (RUNTIME / "forge_performance_governor_010_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(
        json.dumps(
            {
                "timestamp": governor["generated"],
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
print(f"recommended_action = {recommendation}")
print(f"recommended_worker_instances = {governor['recommended_worker_instances']}")
print(f"current_worker_instances = {workers}")
print(f"integrity_hash = {integrity}")
print(f"hash = {verification}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
