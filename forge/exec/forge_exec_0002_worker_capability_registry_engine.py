#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = json.loads(
    (ROOT / "runtime/exec/worker_registry.json").read_text()
)

capability_index = {}

for worker in REGISTRY["worker_registry"]:
    for capability in worker["capabilities"]:
        capability_index.setdefault(capability, []).append(worker["id"])

report = {
    "module": "FORGE-EXEC-0002",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "worker_count": REGISTRY["worker_count"],
    "capability_registry": capability_index,
    "capability_count": len(capability_index)
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/exec/worker_capability_registry.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-EXEC-0002")
print("Worker Capability Registry Engine")
print("=" * 60)
print("Workers      :", report["worker_count"])
print("Capabilities :", report["capability_count"])
print("Output       :", OUT)
print()
print("STATUS : PASS")
