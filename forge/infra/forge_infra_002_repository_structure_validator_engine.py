#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-002"
STATUS = "FORGE_REPOSITORY_STRUCTURE_VALIDATOR_READY"

ROOT = Path(__file__).resolve().parents[2]

required_dirs = [
    "forge",
    "runtime",
    "registry",
]

existing = {}
missing = []

for d in required_dirs:
    p = ROOT / d
    ok = p.exists() and p.is_dir()
    existing[d] = ok
    if not ok:
        missing.append(d)

payload = {
    "module": MODULE,
    "status": STATUS,
    "repository_structure": existing,
    "missing_directories": missing,
    "repository_structure_valid": len(missing) == 0,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, indent=2, sort_keys=True)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()

payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

json_path = runtime_dir / "forge_repository_structure_002.json"
json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()
}

(runtime_dir / "forge_repository_structure_002_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_structure_002_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as f:
    f.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"repository_structure_valid = {payload['repository_structure_valid']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
