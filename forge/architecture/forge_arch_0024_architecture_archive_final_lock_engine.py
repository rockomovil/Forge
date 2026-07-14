#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

SEAL_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_final_seal.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_final_lock.json"

seal = json.loads(SEAL_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0024",
    "status": "PASS" if seal["architecture_archive_final_sealed"] else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "architecture_archive_final_locked": seal["architecture_archive_final_sealed"],
    "immutable": True,
    "locked_at": datetime.now(UTC).isoformat(),
    "seal_hash": seal["hash"],
    "summary": seal["summary"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0024")
print("Architecture Archive Final Lock Engine")
print("=" * 60)
print("Locked   :", result["architecture_archive_final_locked"])
print("Immutable:", result["immutable"])
print("Modules  :", result["summary"]["module_count"])
print("Families :", result["summary"]["family_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
