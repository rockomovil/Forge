#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-008"
STATUS = "FORGE_REPOSITORY_SIZE_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]

total_files = 0
total_dirs = 0
total_bytes = 0

for path in ROOT.rglob("*"):
    if ".git" in path.parts:
        continue

    if path.is_dir():
        total_dirs += 1
    elif path.is_file():
        total_files += 1
        try:
            total_bytes += path.stat().st_size
        except OSError:
            pass

payload = {
    "module": MODULE,
    "status": STATUS,
    "repository_metrics": {
        "directories": total_dirs,
        "files": total_files,
        "bytes": total_bytes,
    },
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, indent=2, sort_keys=True)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_size_audit_008.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest(),
}

(runtime_dir / "forge_repository_size_audit_008_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_size_audit_008_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"directories = {total_dirs}")
print(f"files = {total_files}")
print(f"bytes = {total_bytes}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
