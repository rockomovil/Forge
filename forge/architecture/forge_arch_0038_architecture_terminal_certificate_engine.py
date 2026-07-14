#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

RELEASE_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_release.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_certificate.json"

release = json.loads(RELEASE_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0038",
    "status": "PASS" if release["terminal_release_ready"] else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "terminal_certificate_issued": release["terminal_release_ready"],
    "issued_at": datetime.now(UTC).isoformat(),
    "terminal_release_hash": release["hash"],
    "module_count": release["module_count"],
    "family_count": release["family_count"],
    "prefix_count": release["prefix_count"],
    "artifact_count": release["artifact_count"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0038")
print("Architecture Terminal Certificate Engine")
print("=" * 60)
print("Certificate:", result["terminal_certificate_issued"])
print("Modules    :", result["module_count"])
print("Families   :", result["family_count"])
print("Prefixes   :", result["prefix_count"])
print("Artifacts  :", result["artifact_count"])
print("Output     :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
