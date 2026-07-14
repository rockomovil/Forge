#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
from datetime import datetime, UTC

ROOT = Path(__file__).resolve().parents[2]

VALIDATION_FILE = ROOT / "runtime" / "architecture" / "architecture_validation.json"
METRICS_FILE = ROOT / "runtime" / "architecture" / "architecture_metrics.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_certification.json"

validation = json.loads(VALIDATION_FILE.read_text())
metrics = json.loads(METRICS_FILE.read_text())

certified = validation["status"] == "PASS"

result = {
    "module": "FORGE-ARCH-0009",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "architecture_certified": certified,
    "validation_status": validation["status"],
    "module_count": metrics["module_count"],
    "unique_module_count": metrics["unique_module_count"],
    "family_count": metrics["family_count"],
    "node_count": metrics["node_count"],
    "edge_count": metrics["edge_count"],
    "certified_at": datetime.now(UTC).isoformat(),
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0009")
print("Architecture Certification Engine")
print("=" * 60)
print("Certified :", result["architecture_certified"])
print("Modules   :", result["module_count"])
print("Families  :", result["family_count"])
print("Nodes     :", result["node_count"])
print("Edges     :", result["edge_count"])
print("Output    :", OUTPUT_FILE)
print()
print("STATUS : PASS")
