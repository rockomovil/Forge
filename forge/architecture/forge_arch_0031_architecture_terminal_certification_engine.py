#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

LOCK_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_lock.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_certification.json"

lock = json.loads(LOCK_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0031",
    "status": "PASS" if lock["registry_locked"] else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "terminal_certified": lock["registry_locked"],
    "immutable": lock["immutable"],
    "certified_at": datetime.now(UTC).isoformat(),
    "registry_lock_hash": lock["hash"],
    "module_count": lock["module_count"],
    "family_count": lock["family_count"],
    "prefix_count": lock["prefix_count"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0031")
print("Architecture Terminal Certification Engine")
print("=" * 60)
print("Certified:", result["terminal_certified"])
print("Immutable:", result["immutable"])
print("Modules  :", result["module_count"])
print("Families :", result["family_count"])
print("Prefixes :", result["prefix_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
