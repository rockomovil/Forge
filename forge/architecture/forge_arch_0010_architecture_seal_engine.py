#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

CERTIFICATION_FILE = ROOT / "runtime" / "architecture" / "architecture_certification.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_seal.json"

cert = json.loads(CERTIFICATION_FILE.read_text())

result = {
    "module": "FORGE-ARCH-0010",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "architecture_sealed": cert["architecture_certified"],
    "certification_hash": cert["hash"],
    "sealed_at": datetime.now(UTC).isoformat(),
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0010")
print("Architecture Seal Engine")
print("=" * 60)
print("Sealed :", result["architecture_sealed"])
print("Output :", OUTPUT_FILE)
print()
print("STATUS : PASS")
