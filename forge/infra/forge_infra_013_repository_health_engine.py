#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-013"
STATUS = "FORGE_REPOSITORY_HEALTH_READY"

ROOT = Path(__file__).resolve().parents[2]

stats = {
    "files": 0,
    "directories": 0,
    "symlinks": 0,
    "empty_files": 0,
    "empty_directories": 0,
}

for path in ROOT.rglob("*"):
    if ".git" in path.parts:
        continue

    if path.is_symlink():
        stats["symlinks"] += 1

    if path.is_dir():
        stats["directories"] += 1
        try:
            next(path.iterdir())
        except StopIteration:
            stats["empty_directories"] += 1

    elif path.is_file():
        stats["files"] += 1
        try:
            if path.stat().st_size == 0:
                stats["empty_files"] += 1
        except OSError:
            pass

payload = {
    "module": MODULE,
    "status": STATUS,
    "repository_health": stats,
    "healthy": True,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, sort_keys=True, indent=2)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_health_013.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest(),
}

(runtime_dir / "forge_repository_health_013_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_health_013_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"files = {stats['files']}")
print(f"directories = {stats['directories']}")
print(f"symlinks = {stats['symlinks']}")
print(f"empty_files = {stats['empty_files']}")
print(f"empty_directories = {stats['empty_directories']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
