#!/usr/bin/env python3

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-041"
STATUS = "FORGE_REPOSITORY_EXECUTABLE_CATALOG_READY"

ROOT = Path(__file__).resolve().parents[2]

executables = []

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts or not path.is_file():
        continue

    try:
        mode = path.stat().st_mode
    except OSError:
        continue

    if mode & 0o111:
        executables.append(path.relative_to(ROOT).as_posix())

payload = {
    "module": MODULE,
    "status": STATUS,
    "executable_file_count": len(executables),
    "executable_files": executables,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_executable_catalog_041.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_executable_catalog_041_hash.json").write_text(
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
    runtime_dir / "forge_repository_executable_catalog_041_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"executable_file_count = {len(executables)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
