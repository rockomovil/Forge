#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

AUDIT_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_audit.json"
REGISTRY_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_export.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_certification.json"

audit = json.loads(AUDIT_FILE.read_text())
registry = json.loads(REGISTRY_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0028",
    "status": "PASS" if audit["status"] == "PASS" else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "registry_certified": audit["status"] == "PASS",
    "certified_at": datetime.now(UTC).isoformat(),
    "audit_hash": audit["hash"],
    "registry_hash": registry["hash"],
    "module_count": registry["module_count"],
    "family_count": registry["family_count"],
    "prefix_count": registry["prefix_count"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0028")
print("Architecture Registry Certification Engine")
print("=" * 60)
print("Certified:", result["registry_certified"])
print("Modules  :", result["module_count"])
print("Families :", result["family_count"])
print("Prefixes :", result["prefix_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
