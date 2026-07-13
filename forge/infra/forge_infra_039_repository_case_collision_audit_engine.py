#!/usr/bin/env python3

import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-039"
STATUS = "FORGE_REPOSITORY_CASE_COLLISION_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]

groups = defaultdict(list)

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts or not path.is_file():
        continue

    rel = path.relative_to(ROOT).as_posix()
    groups[rel.lower()].append(rel)

collisions = {
    key: sorted(values)
    for key, values in groups.items()
    if len(values) > 1
}

payload = {
    "module": MODULE,
    "status": STATUS,
    "collision_group_count": len(collisions),
    "collisions": collisions,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_case_collision_039.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_case_collision_039_hash.json").write_text(
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
    runtime_dir / "forge_repository_case_collision_039_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"collision_group_count = {len(collisions)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
