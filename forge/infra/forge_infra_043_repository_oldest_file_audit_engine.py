#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-043"
STATUS = "FORGE_REPOSITORY_OLDEST_FILE_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]

records = []

for path in ROOT.rglob("*"):
    if ".git" in path.parts or not path.is_file():
        continue

    try:
        mtime = path.stat().st_mtime
    except OSError:
        continue

    records.append((mtime, path.relative_to(ROOT).as_posix()))

records.sort()

oldest = [
    {
        "path": p,
        "modified": datetime.fromtimestamp(
            ts, tz=timezone.utc
        ).isoformat(),
    }
    for ts, p in records[:100]
]

payload = {
    "module": MODULE,
    "status": STATUS,
    "oldest_file_count": len(oldest),
    "oldest_files": oldest,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_oldest_file_audit_043.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_oldest_file_audit_043_hash.json").write_text(
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
    runtime_dir / "forge_repository_oldest_file_audit_043_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"oldest_file_count = {len(oldest)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
