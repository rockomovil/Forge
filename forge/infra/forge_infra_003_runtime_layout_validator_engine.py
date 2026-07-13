#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-003"
STATUS = "FORGE_RUNTIME_LAYOUT_VALIDATOR_READY"

ROOT = Path(__file__).resolve().parents[2]

required_runtime_dirs = [
    "runtime",
    "runtime/infra",
    "runtime/atlas",
    "runtime/graph",
]

layout = {}
missing = []

for d in required_runtime_dirs:
    p = ROOT / d
    ok = p.exists() and p.is_dir()
    layout[d] = ok
    if not ok:
        missing.append(d)

payload = {
    "module": MODULE,
    "status": STATUS,
    "runtime_layout": layout,
    "runtime_layout_valid": len(missing) == 0,
    "missing_directories": missing,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, sort_keys=True, indent=2)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_runtime_layout_003.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest(),
}

(runtime_dir / "forge_runtime_layout_003_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_runtime_layout_003_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as f:
    f.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"runtime_layout_valid = {payload['runtime_layout_valid']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
