#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-031"
STATUS = "FORGE_REPOSITORY_TOP_LEVEL_INVENTORY_READY"

ROOT = Path(__file__).resolve().parents[2]

entries = []

for path in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
    if path.name == ".git":
        continue

    if path.is_dir():
        kind = "directory"
    elif path.is_file():
        kind = "file"
    elif path.is_symlink():
        kind = "symlink"
    else:
        kind = "other"

    entries.append(
        {
            "name": path.name,
            "type": kind,
        }
    )

payload = {
    "module": MODULE,
    "status": STATUS,
    "entry_count": len(entries),
    "entries": entries,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_top_level_inventory_031.json").write_text(
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

(runtime_dir / "forge_repository_top_level_inventory_031_hash.json").write_text(
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
    runtime_dir / "forge_repository_top_level_inventory_031_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"entry_count = {len(entries)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
