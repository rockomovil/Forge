#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

LOCK_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_lock.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_final_audit.json"

lock = json.loads(LOCK_FILE.read_text())

checks = {
    "archive_locked": lock["architecture_archive_locked"],
    "immutable": lock["immutable"],
    "module_count": lock["summary"]["module_count"] == 1546,
    "family_count": lock["summary"]["family_count"] == 46,
}

result = {
    "module": "FORGE-ARCH-0021",
    "status": "PASS" if all(checks.values()) else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "checks": checks,
    "passed": sum(checks.values()),
    "total": len(checks),
    "audited_at": datetime.now(UTC).isoformat(),
    "lock_hash": lock["hash"],
    "summary": lock["summary"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0021")
print("Architecture Archive Final Audit Engine")
print("=" * 60)
print("Checks  :", result["passed"], "/", result["total"])
print("Status  :", result["status"])
print("Modules :", result["summary"]["module_count"])
print("Families:", result["summary"]["family_count"])
print("Output  :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
