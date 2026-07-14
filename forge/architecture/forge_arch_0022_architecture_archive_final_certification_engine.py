#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

AUDIT_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_final_audit.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_final_certification.json"

audit = json.loads(AUDIT_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0022",
    "status": "PASS" if audit["status"] == "PASS" else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "architecture_archive_final_certified": audit["status"] == "PASS",
    "certified_at": datetime.now(UTC).isoformat(),
    "audit_hash": audit["hash"],
    "summary": audit["summary"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0022")
print("Architecture Archive Final Certification Engine")
print("=" * 60)
print("Certified:", result["architecture_archive_final_certified"])
print("Modules  :", result["summary"]["module_count"])
print("Families :", result["summary"]["family_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
