#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

CERT_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_certification.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_seal.json"

cert = json.loads(CERT_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0029",
    "status": "PASS" if cert["registry_certified"] else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "registry_sealed": cert["registry_certified"],
    "sealed_at": datetime.now(UTC).isoformat(),
    "certification_hash": cert["hash"],
    "module_count": cert["module_count"],
    "family_count": cert["family_count"],
    "prefix_count": cert["prefix_count"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0029")
print("Architecture Registry Seal Engine")
print("=" * 60)
print("Sealed   :", result["registry_sealed"])
print("Modules  :", result["module_count"])
print("Families :", result["family_count"])
print("Prefixes :", result["prefix_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
