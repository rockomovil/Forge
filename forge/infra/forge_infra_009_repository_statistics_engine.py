#!/usr/bin/env python3

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-009"
STATUS = "FORGE_REPOSITORY_STATISTICS_READY"

ROOT = Path(__file__).resolve().parents[2]

stats = Counter()

for path in ROOT.rglob("*"):
    if ".git" in path.parts:
        continue

    if path.is_file():
        stats["files"] += 1
    elif path.is_dir():
        stats["directories"] += 1

top_level = sorted(
    p.name for p in ROOT.iterdir()
    if not p.name.startswith(".")
)

payload = {
    "module": MODULE,
    "status": STATUS,
    "statistics": {
        "files": stats["files"],
        "directories": stats["directories"],
        "top_level_entries": len(top_level),
    },
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, sort_keys=True, indent=2)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_statistics_009.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest(),
}

(runtime_dir / "forge_repository_statistics_009_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_statistics_009_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"files = {stats['files']}")
print(f"directories = {stats['directories']}")
print(f"top_level_entries = {len(top_level)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
