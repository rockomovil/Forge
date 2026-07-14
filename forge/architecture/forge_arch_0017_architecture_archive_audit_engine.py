#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

ARCHIVE_FILE = ROOT / "runtime" / "architecture" / "architecture_archive.json"
LOCK_FILE = ROOT / "runtime" / "architecture" / "architecture_lock.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_audit.json"

archive = json.loads(ARCHIVE_FILE.read_text())
lock = json.loads(LOCK_FILE.read_text())

checks = {
    "archive_created": archive["architecture_archived"],
    "locked": lock["architecture_locked"],
    "immutable": lock["immutable"],
    "module_count_match":
        archive["summary"]["module_count"] == 1546,
    "family_count_match":
        archive["summary"]["family_count"] == 46,
}

result = {
    "module": "FORGE-ARCH-0017",
    "status": "PASS" if all(checks.values()) else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "audit_timestamp": datetime.now(UTC).isoformat(),
    "checks": checks,
    "passed": sum(checks.values()),
    "total": len(checks),
    "archive_hash": archive["hash"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0017")
print("Architecture Archive Audit Engine")
print("=" * 60)
print("Checks :", result["passed"], "/", result["total"])
print("Status :", result["status"])
print("Output :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
