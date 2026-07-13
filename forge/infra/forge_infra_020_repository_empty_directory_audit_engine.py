#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-020"
STATUS = "FORGE_REPOSITORY_EMPTY_DIRECTORY_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]

empty_directories = []

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts or not path.is_dir():
        continue

    try:
        if not any(path.iterdir()):
            empty_directories.append(path.relative_to(ROOT).as_posix())
    except OSError:
        pass

payload = {
    "module": MODULE,
    "status": STATUS,
    "empty_directory_count": len(empty_directories),
    "empty_directories": empty_directories,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":"),
)

integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_empty_directory_020.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
).hexdigest()

(runtime_dir / "forge_repository_empty_directory_020_hash.json").write_text(
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
    runtime_dir / "forge_repository_empty_directory_020_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"empty_directory_count = {len(empty_directories)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
