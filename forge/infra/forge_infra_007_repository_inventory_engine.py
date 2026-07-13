#!/usr/bin/env python3

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-007"
STATUS = "FORGE_REPOSITORY_INVENTORY_READY"

ROOT = Path(__file__).resolve().parents[2]

counter = Counter()

for path in ROOT.rglob("*"):
    if ".git" in path.parts:
        continue
    if path.is_file():
        ext = path.suffix.lower() if path.suffix else "<no_extension>"
        counter[ext] += 1

inventory = dict(sorted(counter.items()))

payload = {
    "module": MODULE,
    "status": STATUS,
    "file_inventory": inventory,
    "extension_types": len(inventory),
    "total_files": sum(inventory.values()),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, sort_keys=True, indent=2)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_inventory_007.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest(),
}

(runtime_dir / "forge_repository_inventory_007_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_inventory_007_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"extension_types = {payload['extension_types']}")
print(f"total_files = {payload['total_files']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
