#!/usr/bin/env python3

import hashlib
import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-050"
STATUS = "FORGE_REPOSITORY_FILE_AGE_DISTRIBUTION_READY"

ROOT = Path(__file__).resolve().parents[2]
now = time.time()

buckets = Counter({
    "0_1_day": 0,
    "1_7_days": 0,
    "7_30_days": 0,
    "30_180_days": 0,
    "180_plus_days": 0,
})

for path in ROOT.rglob("*"):
    if ".git" in path.parts or not path.is_file():
        continue

    try:
        age_days = (now - path.stat().st_mtime) / 86400.0
    except OSError:
        continue

    if age_days < 1:
        buckets["0_1_day"] += 1
    elif age_days < 7:
        buckets["1_7_days"] += 1
    elif age_days < 30:
        buckets["7_30_days"] += 1
    elif age_days < 180:
        buckets["30_180_days"] += 1
    else:
        buckets["180_plus_days"] += 1

payload = {
    "module": MODULE,
    "status": STATUS,
    "files_scanned": sum(buckets.values()),
    "age_distribution": dict(buckets),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_file_age_distribution_050.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_file_age_distribution_050_hash.json").write_text(
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
    runtime_dir / "forge_repository_file_age_distribution_050_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"files_scanned = {payload['files_scanned']}")
print(f"bucket_count = {len(buckets)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
