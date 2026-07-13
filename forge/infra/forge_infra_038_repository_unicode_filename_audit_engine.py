#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-038"
STATUS = "FORGE_REPOSITORY_UNICODE_FILENAME_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]

unicode_files = []

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts or not path.is_file():
        continue

    name = path.name
    if any(ord(c) > 127 for c in name):
        unicode_files.append(path.relative_to(ROOT).as_posix())

payload = {
    "module": MODULE,
    "status": STATUS,
    "unicode_filename_count": len(unicode_files),
    "unicode_filenames": unicode_files,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_unicode_filename_038.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_unicode_filename_038_hash.json").write_text(
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

with (runtime_dir / "forge_repository_unicode_filename_038_ledger.jsonl").open(
    "a", encoding="utf-8"
) as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"unicode_filename_count = {len(unicode_files)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
