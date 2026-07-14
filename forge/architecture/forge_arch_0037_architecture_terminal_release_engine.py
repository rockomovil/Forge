#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

AUDIT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_audit.json"
MANIFEST_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_manifest.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_release.json"

audit = json.loads(AUDIT_FILE.read_text())
manifest = json.loads(MANIFEST_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0037",
    "status": "PASS" if audit["status"] == "PASS" else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "terminal_release_ready": audit["status"] == "PASS",
    "released_at": datetime.now(UTC).isoformat(),
    "terminal_audit_hash": audit["hash"],
    "terminal_manifest_hash": manifest["hash"],
    "module_count": manifest["module_count"],
    "family_count": manifest["family_count"],
    "prefix_count": manifest["prefix_count"],
    "artifact_count": len(manifest["artifacts"]),
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0037")
print("Architecture Terminal Release Engine")
print("=" * 60)
print("Release  :", result["terminal_release_ready"])
print("Modules  :", result["module_count"])
print("Families :", result["family_count"])
print("Prefixes :", result["prefix_count"])
print("Artifacts:", result["artifact_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
