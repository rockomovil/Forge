#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-019"
STATUS = "FORGE_REPOSITORY_LARGE_FILE_AUDIT_READY"

ROOT = Path(__file__).resolve().parents[2]
THRESHOLD_BYTES = 10 * 1024 * 1024

large_files = []
files_scanned = 0
scan_errors = []

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts or not path.is_file():
        continue

    try:
        size = path.stat().st_size
    except OSError as error:
        scan_errors.append({
            "path": path.relative_to(ROOT).as_posix(),
            "error": str(error),
        })
        continue

    files_scanned += 1

    if size >= THRESHOLD_BYTES:
        large_files.append({
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": size,
        })

payload = {
    "module": MODULE,
    "status": STATUS,
    "threshold_bytes": THRESHOLD_BYTES,
    "files_scanned": files_scanned,
    "large_file_count": len(large_files),
    "large_files": large_files,
    "scan_error_count": len(scan_errors),
    "scan_errors": scan_errors,
    "audit_valid": len(scan_errors) == 0,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical_payload = json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":"),
)

integrity_hash = hashlib.sha256(
    canonical_payload.encode("utf-8")
).hexdigest()

payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

report_path = runtime_dir / "forge_repository_large_file_019.json"
hash_path = runtime_dir / "forge_repository_large_file_019_hash.json"
ledger_path = runtime_dir / "forge_repository_large_file_019_ledger.jsonl"

report_path.write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()

hash_payload = {
    "module": MODULE,
    "hash": final_hash,
}

hash_path.write_text(
    json.dumps(hash_payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

with ledger_path.open("a", encoding="utf-8") as ledger:
    ledger.write(
        json.dumps(payload, sort_keys=True) + "\n"
    )

print(MODULE)
print(STATUS)
print(f"files_scanned = {files_scanned}")
print(f"large_file_count = {len(large_files)}")
print(f"scan_error_count = {len(scan_errors)}")
print(f"audit_valid = {payload['audit_valid']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")

if not payload["audit_valid"]:
    raise SystemExit(1)
