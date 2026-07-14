#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

SEAL_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_seal.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_lock.json"

seal = json.loads(SEAL_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0030",
    "status": "PASS" if seal["registry_sealed"] else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "registry_locked": seal["registry_sealed"],
    "immutable": True,
    "locked_at": datetime.now(UTC).isoformat(),
    "seal_hash": seal["hash"],
    "module_count": seal["module_count"],
    "family_count": seal["family_count"],
    "prefix_count": seal["prefix_count"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0030")
print("Architecture Registry Lock Engine")
print("=" * 60)
print("Locked   :", result["registry_locked"])
print("Immutable:", result["immutable"])
print("Modules  :", result["module_count"])
print("Families :", result["family_count"])
print("Prefixes :", result["prefix_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
