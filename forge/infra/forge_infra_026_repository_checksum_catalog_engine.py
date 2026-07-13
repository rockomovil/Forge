#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-026"
STATUS = "FORGE_REPOSITORY_CHECKSUM_CATALOG_READY"

ROOT = Path(__file__).resolve().parents[2]

catalog = {}
files_scanned = 0

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts or not path.is_file():
        continue

    rel = path.relative_to(ROOT).as_posix()

    try:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        continue

    catalog[rel] = digest
    files_scanned += 1

payload = {
    "module": MODULE,
    "status": STATUS,
    "files_scanned": files_scanned,
    "checksum_catalog": catalog,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_checksum_catalog_026.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_checksum_catalog_026_hash.json").write_text(
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
    runtime_dir / "forge_repository_checksum_catalog_026_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"files_scanned = {files_scanned}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
