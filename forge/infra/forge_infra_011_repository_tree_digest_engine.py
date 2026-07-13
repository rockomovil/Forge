#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-011"
STATUS = "FORGE_REPOSITORY_TREE_DIGEST_READY"

ROOT = Path(__file__).resolve().parents[2]

directories = sorted(
    p.relative_to(ROOT).as_posix()
    for p in ROOT.rglob("*")
    if p.is_dir() and ".git" not in p.parts
)

tree_digest = hashlib.sha256()

for directory in directories:
    tree_digest.update(directory.encode())

payload = {
    "module": MODULE,
    "status": STATUS,
    "directory_count": len(directories),
    "tree_digest": tree_digest.hexdigest(),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, indent=2, sort_keys=True)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_tree_digest_011.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest(),
}

(runtime_dir / "forge_repository_tree_digest_011_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_tree_digest_011_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"directory_count = {payload['directory_count']}")
print(f"tree_digest = {payload['tree_digest']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
