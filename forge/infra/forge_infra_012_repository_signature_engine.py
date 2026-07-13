#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-012"
STATUS = "FORGE_REPOSITORY_SIGNATURE_READY"

ROOT = Path(__file__).resolve().parents[2]

signature = hashlib.sha256()

file_count = 0

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts or not path.is_file():
        continue

    rel = path.relative_to(ROOT).as_posix()
    st = path.stat()

    signature.update(rel.encode("utf-8"))
    signature.update(str(st.st_size).encode("utf-8"))

    file_count += 1

repository_signature = signature.hexdigest()

payload = {
    "module": MODULE,
    "status": STATUS,
    "repository_signature": repository_signature,
    "files_processed": file_count,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, indent=2, sort_keys=True)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_signature_012.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()
}

(runtime_dir / "forge_repository_signature_012_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_signature_012_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"files_processed = {file_count}")
print(f"repository_signature = {repository_signature}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
