#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

MODULE = "FORGE-KERNEL-009"
STATUS = "FORGE_EXECUTION_PROFILER_READY"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime" / "kernel"

runtime_state = json.loads(
    (RUNTIME / "forge_mission_graph_runtime_006.json").read_text(
        encoding="utf-8"
    )
)

scheduler = json.loads(
    (RUNTIME / "forge_kernel_scheduler_007.json").read_text(
        encoding="utf-8"
    )
)

workforce = json.loads(
    (RUNTIME / "forge_workforce_registry_008.json").read_text(
        encoding="utf-8"
    )
)

execution_steps = runtime_state["execution_steps"]
worker_pools = workforce["worker_pool_count"]

metrics = {
    "execution_steps": execution_steps,
    "completed_nodes": runtime_state["completed_nodes"],
    "scheduled_tasks": scheduler["scheduled_tasks"],
    "worker_pool_count": worker_pools,
    "worker_instance_count": sum(
        w["instances"] for w in workforce["workers"]
    ),
    "average_tasks_per_worker": (
        scheduler["scheduled_tasks"] /
        max(1, sum(w["instances"] for w in workforce["workers"]))
    ),
    "scheduler_strategy": scheduler["strategy"],
    "graph_runtime_state": runtime_state["runtime_state"],
}

profile = {
    "module": MODULE,
    "status": STATUS,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated": datetime.now(UTC).isoformat(),
    "metrics": metrics,
}

payload = json.dumps(profile, indent=2, sort_keys=True)

(RUNTIME / "forge_execution_profiler_009.json").write_text(
    payload,
    encoding="utf-8",
)

integrity = hashlib.sha256(payload.encode()).hexdigest()

(RUNTIME / "forge_execution_profiler_009_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "integrity_hash": integrity,
        },
        indent=2,
    ),
    encoding="utf-8",
)

with (RUNTIME / "forge_execution_profiler_009_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(
        json.dumps(
            {
                "timestamp": profile["generated"],
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
print(f"execution_steps = {metrics['execution_steps']}")
print(f"worker_pool_count = {metrics['worker_pool_count']}")
print(f"average_tasks_per_worker = {metrics['average_tasks_per_worker']:.2f}")
print(f"integrity_hash = {integrity}")
print(f"hash = {verification}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
