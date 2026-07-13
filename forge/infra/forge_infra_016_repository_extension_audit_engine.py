#!/usr/bin/env python3

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-016"
STATUS = "FORGE_REPOSITORY_EXTENSION_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]

extensions = Counter()
files = 0

for path in ROOT.rglob("*"):
    if ".git" in path.parts or not path.is_file():
        continue

    files += 1
    ext = path.suffix.lower() if path.suffix else "<no_extension>"
    extensions[ext] += 1

payload = {
    "module": MODULE,
    "status": STATUS,
    "files_audited": files,
    "extension_types": len(extensions),
    "extensions": dict(sorted(extensions.items())),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, indent=2, sort_keys=True)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_extension_016.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()
}

(runtime_dir / "forge_repository_extension_016_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_extension_016_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"files_audited = {files}")
print(f"extension_types = {len(extensions)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
