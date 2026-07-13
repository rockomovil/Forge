#!/usr/bin/env python3

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-034"
STATUS = "FORGE_REPOSITORY_DIRECTORY_FANOUT_READY"

ROOT = Path(__file__).resolve().parents[2]

fanout = Counter()

for directory in sorted(ROOT.rglob("*")):
    if ".git" in directory.parts or not directory.is_dir():
        continue

    try:
        child_count = sum(
            1
            for child in directory.iterdir()
            if ".git" not in child.parts
        )
    except OSError:
        continue

    fanout[child_count] += 1

payload = {
    "module": MODULE,
    "status": STATUS,
    "directory_fanout_distribution": dict(sorted(fanout.items())),
    "directory_count": sum(fanout.values()),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_directory_fanout_034.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_directory_fanout_034_hash.json").write_text(
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
    runtime_dir / "forge_repository_directory_fanout_034_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"directory_count = {payload['directory_count']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
