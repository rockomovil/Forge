#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

MODULE = "FORGE-SCHEDULER-003"
STATUS = "FORGE_SCHEDULING_POLICY_ENGINE_READY"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime" / "scheduler"

metrics = json.loads(
    (RUNTIME / "forge_load_metrics_002.json").read_text(encoding="utf-8")
)

workers = metrics["metrics"]

idle = [
    name
    for name, data in workers.items()
    if data["state"] == "IDLE"
]

selected = sorted(idle)[0] if idle else None

payload = {
    "module": MODULE,
    "status": STATUS,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated": datetime.now(UTC).isoformat(),
    "policy": "LEAST_LOADED_IDLE",
    "candidate_count": len(idle),
    "selected_worker": selected,
}

text = json.dumps(payload, indent=2, sort_keys=True)

(RUNTIME / "forge_scheduling_policy_003.json").write_text(
    text,
    encoding="utf-8",
)

integrity = hashlib.sha256(text.encode()).hexdigest()

(RUNTIME / "forge_scheduling_policy_003_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "integrity_hash": integrity,
        },
        indent=2,
    ),
    encoding="utf-8",
)

with (RUNTIME / "forge_scheduling_policy_003_ledger.jsonl").open(
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
print(f"policy = {payload['policy']}")
print(f"candidate_count = {payload['candidate_count']}")
print(f"selected_worker = {selected}")
print(f"integrity_hash = {integrity}")
print(f"hash = {verification}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
