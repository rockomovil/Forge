#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

FINALIZATION_FILE = ROOT / "runtime" / "architecture" / "architecture_archive_finalization.json"
INDEX_FILE = ROOT / "runtime" / "architecture" / "module_index.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_export.json"

finalization = json.loads(FINALIZATION_FILE.read_text())
index = json.loads(INDEX_FILE.read_text())

registry = {
    "module": "FORGE-ARCH-0026",
    "status": "PASS" if finalization["architecture_archive_finalized"] else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "exported_at": datetime.now(UTC).isoformat(),
    "architecture_registry_ready": finalization["architecture_archive_finalized"],
    "module_count": index["module_count"],
    "family_count": index["family_count"],
    "prefix_count": index["prefix_count"],
    "registry": index["indexes"],
    "finalization_hash": finalization["hash"],
}

registry["hash"] = hashlib.sha256(
    json.dumps(registry, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(registry, indent=2))

print("=" * 60)
print("FORGE-ARCH-0026")
print("Architecture Registry Export Engine")
print("=" * 60)
print("Registry :", registry["architecture_registry_ready"])
print("Modules  :", registry["module_count"])
print("Families :", registry["family_count"])
print("Prefixes :", registry["prefix_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", registry["status"])
