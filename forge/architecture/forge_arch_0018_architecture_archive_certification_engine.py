#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

AUDIT_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_audit.json"
ARCHIVE_FILE = ROOT / "runtime" / "architecture" / "architecture_archive.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_certification.json"

audit = json.loads(AUDIT_FILE.read_text())
archive = json.loads(ARCHIVE_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0018",
    "status": "PASS" if audit["status"] == "PASS" else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "architecture_archive_certified": audit["status"] == "PASS",
    "certified_at": datetime.now(UTC).isoformat(),
    "audit_hash": audit["hash"],
    "archive_hash": archive["hash"],
    "summary": archive["summary"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0018")
print("Architecture Archive Certification Engine")
print("=" * 60)
print("Certified:", result["architecture_archive_certified"])
print("Modules  :", result["summary"]["module_count"])
print("Families :", result["summary"]["family_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
