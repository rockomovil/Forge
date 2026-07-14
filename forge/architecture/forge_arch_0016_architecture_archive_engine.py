#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

FINALIZATION_FILE = ROOT / "runtime" / "architecture" / "architecture_finalization.json"
MANIFEST_FILE = ROOT / "runtime" / "architecture" / "architecture_manifest.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_archive.json"

finalization = json.loads(FINALIZATION_FILE.read_text())
manifest = json.loads(MANIFEST_FILE.read_text())

archive = {
    "module": "FORGE-ARCH-0016",
    "status": "PASS" if finalization["architecture_finalized"] else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "architecture_archived": finalization["architecture_finalized"],
    "archived_at": datetime.now(UTC).isoformat(),
    "finalization_hash": finalization["hash"],
    "manifest_hash": manifest["hash"],
    "summary": finalization["summary"],
}

archive["hash"] = hashlib.sha256(
    json.dumps(archive, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(archive, indent=2))

print("=" * 60)
print("FORGE-ARCH-0016")
print("Architecture Archive Engine")
print("=" * 60)
print("Archived :", archive["architecture_archived"])
print("Modules  :", archive["summary"]["module_count"])
print("Families :", archive["summary"]["family_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", archive["status"])
