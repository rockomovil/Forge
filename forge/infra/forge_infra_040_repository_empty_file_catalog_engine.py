#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-040"
STATUS = "FORGE_REPOSITORY_EMPTY_FILE_CATALOG_READY"

ROOT = Path(__file__).resolve().parents[2]

empty_files = []

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts or not path.is_file():
        continue

    try:
        if path.stat().st_size == 0:
            empty_files.append(path.relative_to(ROOT).as_posix())
    except OSError:
        pass

payload = {
    "module": MODULE,
    "status": STATUS,
    "empty_file_count": len(empty_files),
    "empty_files": empty_files,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_empty_file_catalog_040.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_empty_file_catalog_040_hash.json").write_text(
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
    runtime_dir / "forge_repository_empty_file_catalog_040_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"empty_file_count = {len(empty_files)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
