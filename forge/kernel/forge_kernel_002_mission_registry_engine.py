#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import datetime, UTC
from pathlib import Path

MODULE = "FORGE-KERNEL-002"
STATUS = "FORGE_MISSION_REGISTRY_READY"

ROOT = Path(__file__).resolve().parents[2]

missions = [
    {
        "mission_id": "MISSION-000001",
        "name": "bootstrap_kernel",
        "priority": "CRITICAL",
        "state": "READY",
        "required_capabilities": [
            "repository_scan"
        ]
    }
]

runtime = {
    "module": MODULE,
    "status": STATUS,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated": datetime.now(UTC).isoformat(),
    "mission_count": len(missions),
    "missions": missions
}

payload = json.dumps(runtime, indent=2, sort_keys=True)

runtime_dir = ROOT / "runtime" / "kernel"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_mission_registry_002.json").write_text(
    payload,
    encoding="utf-8"
)

integrity = hashlib.sha256(payload.encode()).hexdigest()

(runtime_dir / "forge_mission_registry_002_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "integrity_hash": integrity
        },
        indent=2
    ),
    encoding="utf-8"
)

with (runtime_dir / "forge_mission_registry_002_ledger.jsonl").open(
    "a",
    encoding="utf-8"
) as f:
    f.write(
        json.dumps(
            {
                "timestamp": runtime["generated"],
                "module": MODULE,
                "status": STATUS,
                "integrity_hash": integrity
            }
        ) + "\n"
    )

print(MODULE)
print(STATUS)
print(f"mission_count = {len(missions)}")
print(f"integrity_hash = {integrity}")
print(f"hash = {hashlib.sha256((MODULE+STATUS+integrity).encode()).hexdigest()}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
