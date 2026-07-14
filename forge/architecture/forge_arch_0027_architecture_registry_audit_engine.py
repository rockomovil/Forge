#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

REGISTRY_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_export.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_audit.json"

registry = json.loads(REGISTRY_FILE.read_text())

checks = {
    "registry_ready": registry["architecture_registry_ready"],
    "module_count": registry["module_count"] == 1546,
    "family_count": registry["family_count"] == 46,
    "prefix_count": registry["prefix_count"] == 571,
    "by_name": len(registry["registry"]["by_name"]) == 1418,
    "by_family": len(registry["registry"]["by_family"]) == 46,
    "by_prefix": len(registry["registry"]["by_prefix"]) == 571,
}

result = {
    "module": "FORGE-ARCH-0027",
    "status": "PASS" if all(checks.values()) else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "audit_timestamp": datetime.now(UTC).isoformat(),
    "checks": checks,
    "passed": sum(checks.values()),
    "total": len(checks),
    "registry_hash": registry["hash"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0027")
print("Architecture Registry Audit Engine")
print("=" * 60)
print("Checks :", result["passed"], "/", result["total"])
print("Status :", result["status"])
print("Output :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
