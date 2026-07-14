#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

CERTIFICATE_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_certificate.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_state.json"

certificate = json.loads(CERTIFICATE_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0039",
    "status": "PASS" if certificate["terminal_certificate_issued"] else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "terminal_state": "CERTIFIED_FINAL",
    "terminal_ready": certificate["terminal_certificate_issued"],
    "immutable": True,
    "locked": True,
    "sealed": True,
    "certified": True,
    "state_timestamp": datetime.now(UTC).isoformat(),
    "certificate_hash": certificate["hash"],
    "module_count": certificate["module_count"],
    "family_count": certificate["family_count"],
    "prefix_count": certificate["prefix_count"],
    "artifact_count": certificate["artifact_count"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0039")
print("Architecture Terminal State Engine")
print("=" * 60)
print("State     :", result["terminal_state"])
print("Ready     :", result["terminal_ready"])
print("Modules   :", result["module_count"])
print("Families  :", result["family_count"])
print("Prefixes  :", result["prefix_count"])
print("Artifacts :", result["artifact_count"])
print("Output    :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
