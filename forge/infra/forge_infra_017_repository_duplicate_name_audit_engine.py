#!/usr/bin/env python3

import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-017"
STATUS = "FORGE_REPOSITORY_DUPLICATE_NAME_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]

names = defaultdict(list)

for path in ROOT.rglob("*"):
    if ".git" in path.parts or not path.is_file():
        continue
    names[path.name].append(path.relative_to(ROOT).as_posix())

duplicates = {
    name: sorted(paths)
    for name, paths in names.items()
    if len(paths) > 1
}

payload = {
    "module": MODULE,
    "status": STATUS,
    "files_scanned": sum(len(v) for v in names.values()),
    "duplicate_name_groups": len(duplicates),
    "duplicate_names": duplicates,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, indent=2, sort_keys=True)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_duplicate_names_017.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest(),
}

(runtime_dir / "forge_repository_duplicate_names_017_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_duplicate_names_017_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"files_scanned = {payload['files_scanned']}")
print(f"duplicate_name_groups = {payload['duplicate_name_groups']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
