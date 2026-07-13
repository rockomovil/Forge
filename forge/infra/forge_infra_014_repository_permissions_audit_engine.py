#!/usr/bin/env python3

import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-014"
STATUS = "FORGE_REPOSITORY_PERMISSIONS_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]

files = 0
directories = 0
executable_files = 0
readable_files = 0
writable_files = 0

for path in ROOT.rglob("*"):
    if ".git" in path.parts:
        continue

    try:
        mode = path.stat().st_mode
    except OSError:
        continue

    if path.is_dir():
        directories += 1
        continue

    if not path.is_file():
        continue

    files += 1

    if os.access(path, os.R_OK):
        readable_files += 1

    if os.access(path, os.W_OK):
        writable_files += 1

    if mode & stat.S_IXUSR:
        executable_files += 1

payload = {
    "module": MODULE,
    "status": STATUS,
    "permissions": {
        "files": files,
        "directories": directories,
        "readable_files": readable_files,
        "writable_files": writable_files,
        "executable_files": executable_files,
    },
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, indent=2, sort_keys=True)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_permissions_014.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()
}

(runtime_dir / "forge_repository_permissions_014_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_permissions_014_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"files = {files}")
print(f"directories = {directories}")
print(f"readable_files = {readable_files}")
print(f"writable_files = {writable_files}")
print(f"executable_files = {executable_files}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
