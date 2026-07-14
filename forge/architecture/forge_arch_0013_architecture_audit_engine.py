#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

MANIFEST_FILE = ROOT / "runtime" / "architecture" / "architecture_manifest.json"
VALIDATION_FILE = ROOT / "runtime" / "architecture" / "architecture_validation.json"
CERTIFICATION_FILE = ROOT / "runtime" / "architecture" / "architecture_certification.json"
SEAL_FILE = ROOT / "runtime" / "architecture" / "architecture_seal.json"
LOCK_FILE = ROOT / "runtime" / "architecture" / "architecture_lock.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_audit.json"

manifest = json.loads(MANIFEST_FILE.read_text())
validation = json.loads(VALIDATION_FILE.read_text())
certification = json.loads(CERTIFICATION_FILE.read_text())
seal = json.loads(SEAL_FILE.read_text())
lock = json.loads(LOCK_FILE.read_text())

checks = {
    "validation_pass": validation["status"] == "PASS",
    "certified": certification["architecture_certified"],
    "sealed": seal["architecture_sealed"],
    "locked": lock["architecture_locked"],
    "immutable": lock["immutable"],
}

result = {
    "module": "FORGE-ARCH-0013",
    "status": "PASS" if all(checks.values()) else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "audit_timestamp": datetime.now(UTC).isoformat(),
    "checks": checks,
    "passed": sum(checks.values()),
    "total": len(checks),
    "manifest_hash": manifest["hash"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0013")
print("Architecture Audit Engine")
print("=" * 60)
print("Checks :", result["passed"], "/", result["total"])
print("Status :", result["status"])
print("Output :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
