#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

LOCK_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_final_lock.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_finalization.json"

lock = json.loads(LOCK_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0025",
    "status": "PASS" if lock["architecture_archive_final_locked"] else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "architecture_archive_finalized": lock["architecture_archive_final_locked"],
    "immutable": lock["immutable"],
    "finalized_at": datetime.now(UTC).isoformat(),
    "lock_hash": lock["hash"],
    "summary": lock["summary"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0025")
print("Architecture Archive Finalization Engine")
print("=" * 60)
print("Finalized:", result["architecture_archive_finalized"])
print("Immutable:", result["immutable"])
print("Modules  :", result["summary"]["module_count"])
print("Families :", result["summary"]["family_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
