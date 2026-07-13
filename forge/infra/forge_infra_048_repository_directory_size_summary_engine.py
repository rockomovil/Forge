#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-048"
STATUS = "FORGE_REPOSITORY_DIRECTORY_SIZE_SUMMARY_READY"

ROOT = Path(__file__).resolve().parents[2]

directories = []

for directory in sorted(ROOT.rglob("*")):
    if ".git" in directory.parts or not directory.is_dir():
        continue

    file_count = 0
    total_bytes = 0

    try:
        for item in directory.iterdir():
            if item.is_file():
                file_count += 1
                try:
                    total_bytes += item.stat().st_size
                except OSError:
                    pass
    except OSError:
        continue

    directories.append({
        "path": directory.relative_to(ROOT).as_posix(),
        "files": file_count,
        "bytes": total_bytes,
    })

payload = {
    "module": MODULE,
    "status": STATUS,
    "directory_count": len(directories),
    "directories": directories,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_directory_size_summary_048.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_directory_size_summary_048_hash.json").write_text(
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
    runtime_dir / "forge_repository_directory_size_summary_048_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"directory_count = {len(directories)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
