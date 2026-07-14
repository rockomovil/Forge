#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

MANIFEST_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_manifest.json"
FINALIZATION_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_finalization.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_audit.json"

manifest = json.loads(MANIFEST_FILE.read_text())
finalization = json.loads(FINALIZATION_FILE.read_text())

checks = {
    "terminal_finalized": finalization["terminal_finalized"],
    "manifest_ready": manifest["terminal_manifest_ready"],
    "module_count": manifest["module_count"] == 1546,
    "family_count": manifest["family_count"] == 46,
    "prefix_count": manifest["prefix_count"] == 571,
    "artifact_count": len(manifest["artifacts"]) == 13,
}

result = {
    "module": "FORGE-ARCH-0036",
    "status": "PASS" if all(checks.values()) else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "audit_timestamp": datetime.now(UTC).isoformat(),
    "checks": checks,
    "passed": sum(checks.values()),
    "total": len(checks),
    "terminal_manifest_hash": manifest["hash"],
    "terminal_finalization_hash": finalization["hash"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0036")
print("Architecture Terminal Audit Engine")
print("=" * 60)
print("Checks :", result["passed"], "/", result["total"])
print("Status :", result["status"])
print("Output :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
