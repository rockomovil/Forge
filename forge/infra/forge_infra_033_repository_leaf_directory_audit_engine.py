#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-033"
STATUS = "FORGE_REPOSITORY_LEAF_DIRECTORY_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]

leaf_directories = []

for directory in sorted(ROOT.rglob("*")):
    if ".git" in directory.parts or not directory.is_dir():
        continue

    try:
        children = [
            child for child in directory.iterdir()
            if ".git" not in child.parts
        ]
    except OSError:
        continue

    if not any(child.is_dir() for child in children):
        leaf_directories.append(directory.relative_to(ROOT).as_posix())

payload = {
    "module": MODULE,
    "status": STATUS,
    "leaf_directory_count": len(leaf_directories),
    "leaf_directories": leaf_directories,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_leaf_directory_033.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_leaf_directory_033_hash.json").write_text(
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
    runtime_dir / "forge_repository_leaf_directory_033_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"leaf_directory_count = {len(leaf_directories)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
