#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-036"
STATUS = "FORGE_REPOSITORY_FILENAME_LENGTH_STATISTICS_READY"

ROOT = Path(__file__).resolve().parents[2]

count = 0
total_length = 0
max_length = 0
max_name = ""

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts or not path.is_file():
        continue

    name = path.name
    length = len(name)

    count += 1
    total_length += length

    if length > max_length:
        max_length = length
        max_name = name

average_length = round(total_length / count, 2) if count else 0

payload = {
    "module": MODULE,
    "status": STATUS,
    "files_scanned": count,
    "average_filename_length": average_length,
    "maximum_filename_length": max_length,
    "longest_filename": max_name,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_filename_length_statistics_036.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_filename_length_statistics_036_hash.json").write_text(
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
    runtime_dir / "forge_repository_filename_length_statistics_036_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"files_scanned = {count}")
print(f"average_filename_length = {average_length}")
print(f"maximum_filename_length = {max_length}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
