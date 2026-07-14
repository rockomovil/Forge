#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

COMPLETION_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_completion.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_sovereign_certificate.json"

completion = json.loads(COMPLETION_FILE.read_text())

issued = completion["architecture_terminal_completed"]

result = {
    "module": "FORGE-ARCH-0041",
    "status": "PASS" if issued else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "sovereign_certificate_issued": issued,
    "certificate_level": "TERMINAL_SOVEREIGN",
    "issued_at": datetime.now(UTC).isoformat(),
    "completion_hash": completion["hash"],
    "module_count": completion["module_count"],
    "family_count": completion["family_count"],
    "prefix_count": completion["prefix_count"],
    "artifact_count": completion["artifact_count"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0041")
print("Architecture Terminal Sovereign Certificate Engine")
print("=" * 60)
print("Certificate :", result["sovereign_certificate_issued"])
print("Level       :", result["certificate_level"])
print("Modules     :", result["module_count"])
print("Families    :", result["family_count"])
print("Prefixes    :", result["prefix_count"])
print("Artifacts   :", result["artifact_count"])
print("Output      :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
