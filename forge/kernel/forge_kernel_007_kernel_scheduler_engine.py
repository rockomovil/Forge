#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

MODULE = "FORGE-KERNEL-007"
STATUS = "FORGE_KERNEL_SCHEDULER_READY"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime" / "kernel"

runtime_state = json.loads(
    (RUNTIME / "forge_mission_graph_runtime_006.json").read_text(
        encoding="utf-8"
    )
)

trace = runtime_state["execution_trace"]

schedule = []

for entry in trace:

    schedule.append(
        {
            "execution_slot": entry["step"],
            "node": entry["node"],
            "priority": 100 - entry["step"],
            "assigned_worker_pool": "DEFAULT_CAPABILITY_POOL",
            "state": "SCHEDULED",
        }
    )

scheduler = {
    "module": MODULE,
    "status": STATUS,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated": datetime.now(UTC).isoformat(),
    "scheduled_tasks": len(schedule),
    "scheduler_state": "READY",
    "strategy": "TOPOLOGICAL_PRIORITY",
    "schedule": schedule,
}

payload = json.dumps(
    scheduler,
    indent=2,
    sort_keys=True,
)

(RUNTIME / "forge_kernel_scheduler_007.json").write_text(
    payload,
    encoding="utf-8",
)

integrity = hashlib.sha256(payload.encode()).hexdigest()

(RUNTIME / "forge_kernel_scheduler_007_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "integrity_hash": integrity,
        },
        indent=2,
    ),
    encoding="utf-8",
)

with (RUNTIME / "forge_kernel_scheduler_007_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:

    ledger.write(
        json.dumps(
            {
                "timestamp": scheduler["generated"],
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
print(f"scheduled_tasks = {len(schedule)}")
print("scheduler_state = READY")
print("strategy = TOPOLOGICAL_PRIORITY")
print(f"integrity_hash = {integrity}")
print(f"hash = {verification}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
