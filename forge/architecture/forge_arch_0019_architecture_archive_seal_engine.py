#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

CERT_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_certification.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_seal.json"

cert = json.loads(CERT_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0019",
    "status": "PASS" if cert["architecture_archive_certified"] else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "architecture_archive_sealed": cert["architecture_archive_certified"],
    "sealed_at": datetime.now(UTC).isoformat(),
    "certification_hash": cert["hash"],
    "summary": cert["summary"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0019")
print("Architecture Archive Seal Engine")
print("=" * 60)
print("Sealed   :", result["architecture_archive_sealed"])
print("Modules  :", result["summary"]["module_count"])
print("Families :", result["summary"]["family_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
