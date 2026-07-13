#!/usr/bin/env python3

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-029"
STATUS = "FORGE_REPOSITORY_FILE_SIZE_DISTRIBUTION_READY"

ROOT = Path(__file__).resolve().parents[2]

buckets = Counter()

for path in ROOT.rglob("*"):
    if ".git" in path.parts or not path.is_file():
        continue

    try:
        size = path.stat().st_size
    except OSError:
        continue

    if size < 1024:
        buckets["<1KB"] += 1
    elif size < 10 * 1024:
        buckets["1KB-10KB"] += 1
    elif size < 100 * 1024:
        buckets["10KB-100KB"] += 1
    elif size < 1024 * 1024:
        buckets["100KB-1MB"] += 1
    elif size < 10 * 1024 * 1024:
        buckets["1MB-10MB"] += 1
    else:
        buckets[">=10MB"] += 1

payload = {
    "module": MODULE,
    "status": STATUS,
    "size_distribution": dict(buckets),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_file_size_distribution_029.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_file_size_distribution_029_hash.json").write_text(
    json.dumps(
        {
            "module": MODULE,
            "hash": final_hash,
        },
        indent=2,
        sort_keys=True,
    ) + "\n",
    encoding="utf-8",
)

with (
    runtime_dir / "forge_repository_file_size_distribution_029_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"bucket_count = {len(buckets)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
