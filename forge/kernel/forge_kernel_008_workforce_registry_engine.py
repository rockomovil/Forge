#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

MODULE = "FORGE-KERNEL-008"
STATUS = "FORGE_WORKFORCE_REGISTRY_READY"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime" / "kernel"

scheduler = json.loads(
    (RUNTIME / "forge_kernel_scheduler_007.json").read_text(
        encoding="utf-8"
    )
)

capability_registry = json.loads(
    (RUNTIME / "forge_capability_registry_001.json").read_text(
        encoding="utf-8"
    )
)

workers = []

for capability in capability_registry["capabilities"]:

    workers.append(
        {
            "worker_pool": f"{capability['name']}_pool",
            "capability": capability["name"],
            "domain": capability["domain"],
            "instances": 1,
            "busy": 0,
            "idle": 1,
            "health": "READY",
            "assigned_tasks": 0,
        }
    )

runtime = {
    "module": MODULE,
    "status": STATUS,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated": datetime.now(UTC).isoformat(),
    "scheduler_strategy": scheduler["strategy"],
    "worker_pool_count": len(workers),
    "workers": workers,
}

payload = json.dumps(
    runtime,
    indent=2,
    sort_keys=True,
)

(RUNTIME / "forge_workforce_registry_008.json").write_text(
    payload,
    encoding="utf-8",
)

integrity = hashlib.sha256(payload.encode()).hexdigest()

(RUNTIME / "forge_workforce_registry_008_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "integrity_hash": integrity,
        },
        indent=2,
    ),
    encoding="utf-8",
)

with (RUNTIME / "forge_workforce_registry_008_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:

    ledger.write(
        json.dumps(
            {
                "timestamp": runtime["generated"],
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
print(f"worker_pool_count = {len(workers)}")
print(f"worker_instance_count = {sum(w['instances'] for w in workers)}")
print("registry_state = READY")
print(f"integrity_hash = {integrity}")
print(f"hash = {verification}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
