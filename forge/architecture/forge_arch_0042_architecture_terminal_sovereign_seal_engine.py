#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

CERT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_sovereign_certificate.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_sovereign_seal.json"

cert = json.loads(CERT_FILE.read_text())

sealed = cert["sovereign_certificate_issued"]

result = {
    "module": "FORGE-ARCH-0042",
    "status": "PASS" if sealed else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "sovereign_sealed": sealed,
    "seal_level": "TERMINAL_SOVEREIGN",
    "sealed_at": datetime.now(UTC).isoformat(),
    "certificate_hash": cert["hash"],
    "module_count": cert["module_count"],
    "family_count": cert["family_count"],
    "prefix_count": cert["prefix_count"],
    "artifact_count": cert["artifact_count"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0042")
print("Architecture Terminal Sovereign Seal Engine")
print("=" * 60)
print("Sealed     :", result["sovereign_sealed"])
print("Level      :", result["seal_level"])
print("Modules    :", result["module_count"])
print("Families   :", result["family_count"])
print("Prefixes   :", result["prefix_count"])
print("Artifacts  :", result["artifact_count"])
print("Output     :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
