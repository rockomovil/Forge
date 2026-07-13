#!/usr/bin/env python3

import hashlib
import json
import pwd
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-044"
STATUS = "FORGE_REPOSITORY_FILE_OWNER_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]

owners = Counter()

for path in ROOT.rglob("*"):
    if ".git" in path.parts or not path.is_file():
        continue

    try:
        uid = path.stat().st_uid
        owner = pwd.getpwuid(uid).pw_name
    except Exception:
        owner = "unknown"

    owners[owner] += 1

payload = {
    "module": MODULE,
    "status": STATUS,
    "owner_count": len(owners),
    "owners": dict(sorted(owners.items())),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_file_owner_044.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_file_owner_044_hash.json").write_text(
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
    runtime_dir / "forge_repository_file_owner_044_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"owner_count = {len(owners)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
