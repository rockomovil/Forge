#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

FINALIZATION_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_finalization.json"
REGISTRY_FILE = ROOT / "runtime" / "architecture" / "architecture_registry_export.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_manifest.json"

finalization = json.loads(FINALIZATION_FILE.read_text())
registry = json.loads(REGISTRY_FILE.read_text())

manifest = {
    "module": "FORGE-ARCH-0035",
    "status": "PASS" if finalization["terminal_finalized"] else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),
    "terminal_manifest_ready": finalization["terminal_finalized"],
    "terminal_finalization_hash": finalization["hash"],
    "registry_hash": registry["hash"],
    "module_count": registry["module_count"],
    "family_count": registry["family_count"],
    "prefix_count": registry["prefix_count"],
    "artifacts": [
        "module_index.json",
        "module_dependency_index.json",
        "architecture_dependency_graph.json",
        "architecture_metrics.json",
        "architecture_validation.json",
        "architecture_certification.json",
        "architecture_seal.json",
        "architecture_lock.json",
        "architecture_manifest.json",
        "architecture_release.json",
        "architecture_archive.json",
        "architecture_registry_export.json",
        "architecture_terminal_finalization.json"
    ]
}

manifest["hash"] = hashlib.sha256(
    json.dumps(manifest, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(manifest, indent=2))

print("=" * 60)
print("FORGE-ARCH-0035")
print("Architecture Terminal Manifest Engine")
print("=" * 60)
print("Manifest :", manifest["terminal_manifest_ready"])
print("Modules  :", manifest["module_count"])
print("Families :", manifest["family_count"])
print("Prefixes :", manifest["prefix_count"])
print("Artifacts:", len(manifest["artifacts"]))
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", manifest["status"])
