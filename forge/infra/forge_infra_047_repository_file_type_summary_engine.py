#!/usr/bin/env python3

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-047"
STATUS = "FORGE_REPOSITORY_FILE_TYPE_SUMMARY_READY"

ROOT = Path(__file__).resolve().parents[2]

summary = Counter()

for path in ROOT.rglob("*"):
    if ".git" in path.parts:
        continue

    if path.is_symlink():
        summary["symlink"] += 1
    elif path.is_file():
        summary["file"] += 1
    elif path.is_dir():
        summary["directory"] += 1
    else:
        summary["other"] += 1

payload = {
    "module": MODULE,
    "status": STATUS,
    "summary": dict(sorted(summary.items())),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_file_type_summary_047.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_file_type_summary_047_hash.json").write_text(
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
    runtime_dir / "forge_repository_file_type_summary_047_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"file_count = {summary['file']}")
print(f"directory_count = {summary['directory']}")
print(f"symlink_count = {summary['symlink']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
