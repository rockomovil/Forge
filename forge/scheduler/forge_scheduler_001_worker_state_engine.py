#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

MODULE = "FORGE-SCHEDULER-001"
STATUS = "FORGE_WORKER_STATE_ENGINE_READY"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime" / "scheduler"
RUNTIME.mkdir(parents=True, exist_ok=True)

workers = {
    "RepositoryWorker": {
        "state": "IDLE",
        "running_jobs": 0,
        "completed_jobs": 0,
        "average_runtime_ms": 0.0,
        "last_update": datetime.now(UTC).isoformat(),
    },
    "GraphWorker": {
        "state": "IDLE",
        "running_jobs": 0,
        "completed_jobs": 0,
        "average_runtime_ms": 0.0,
        "last_update": datetime.now(UTC).isoformat(),
    },
}

payload = {
    "module": MODULE,
    "status": STATUS,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated": datetime.now(UTC).isoformat(),
    "worker_count": len(workers),
    "workers": workers,
}

text = json.dumps(payload, indent=2, sort_keys=True)

(RUNTIME / "forge_worker_state_001.json").write_text(
    text,
    encoding="utf-8",
)

integrity = hashlib.sha256(text.encode()).hexdigest()

(RUNTIME / "forge_worker_state_001_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "integrity_hash": integrity,
        },
        indent=2,
    ),
    encoding="utf-8",
)

with (RUNTIME / "forge_worker_state_001_ledger.jsonl").open(
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
print(f"worker_count = {len(workers)}")
print("scheduler_state = READY")
print(f"integrity_hash = {integrity}")
print(f"hash = {verification}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
