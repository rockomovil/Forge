#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-010"
STATUS = "FORGE_REPOSITORY_FINGERPRINT_READY"

ROOT = Path(__file__).resolve().parents[2]

fingerprint = hashlib.sha256()

files = sorted(
    p for p in ROOT.rglob("*")
    if p.is_file() and ".git" not in p.parts
)

for path in files:
    rel = path.relative_to(ROOT).as_posix()
    stat = path.stat()
    fingerprint.update(rel.encode())
    fingerprint.update(str(stat.st_size).encode())
    fingerprint.update(str(stat.st_mtime_ns).encode())

payload = {
    "module": MODULE,
    "status": STATUS,
    "repository_fingerprint": fingerprint.hexdigest(),
    "files_scanned": len(files),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, sort_keys=True, indent=2)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_fingerprint_010.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest(),
}

(runtime_dir / "forge_repository_fingerprint_010_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_fingerprint_010_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"files_scanned = {len(files)}")
print(f"repository_fingerprint = {payload['repository_fingerprint']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
