#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

AUDIT_FILE = ROOT / "runtime" / "architecture" / "architecture_audit.json"
MANIFEST_FILE = ROOT / "runtime" / "architecture" / "architecture_manifest.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_release.json"

audit = json.loads(AUDIT_FILE.read_text())
manifest = json.loads(MANIFEST_FILE.read_text())

release = {
    "module": "FORGE-ARCH-0014",
    "status": "PASS" if audit["status"] == "PASS" else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "release_ready": audit["status"] == "PASS",
    "released_at": datetime.now(UTC).isoformat(),
    "manifest_hash": manifest["hash"],
    "audit_hash": audit["hash"],
    "summary": manifest["summary"],
}

release["hash"] = hashlib.sha256(
    json.dumps(release, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(release, indent=2))

print("=" * 60)
print("FORGE-ARCH-0014")
print("Architecture Release Engine")
print("=" * 60)
print("Release :", release["release_ready"])
print("Modules :", release["summary"]["module_count"])
print("Families:", release["summary"]["family_count"])
print("Output  :", OUTPUT_FILE)
print()
print("STATUS :", release["status"])
