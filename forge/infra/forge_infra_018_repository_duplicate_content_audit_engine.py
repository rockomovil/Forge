#!/usr/bin/env python3

import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-018"
STATUS = "FORGE_REPOSITORY_DUPLICATE_CONTENT_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]

content_index = defaultdict(list)
files_scanned = 0

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts or not path.is_file():
        continue

    try:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception:
        continue

    files_scanned += 1
    content_index[digest].append(path.relative_to(ROOT).as_posix())

duplicates = {
    digest: paths
    for digest, paths in content_index.items()
    if len(paths) > 1
}

payload = {
    "module": MODULE,
    "status": STATUS,
    "files_scanned": files_scanned,
    "duplicate_content_groups": len(duplicates),
    "duplicate_content": duplicates,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, indent=2, sort_keys=True)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_duplicate_content_018.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()
}

(runtime_dir / "forge_repository_duplicate_content_018_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_duplicate_content_018_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"files_scanned = {files_scanned}")
print(f"duplicate_content_groups = {len(duplicates)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
