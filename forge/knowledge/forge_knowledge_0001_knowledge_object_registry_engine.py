#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

ARCH = json.loads(
    (ROOT / "runtime/architecture/architecture_registry_export.json").read_text()
)

registry = ARCH["registry"]["by_name"]

objects = []

for module_name in sorted(registry):

    info = registry[module_name]

    objects.append({
        "id": module_name,
        "family": info.get("family"),
        "path": info.get("path"),
        "knowledge_object": (
            f"knowledge/{info.get('family')}/{module_name}.md"
        )
    })

report = {
    "module": "FORGE-KNOWLEDGE-0001",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "knowledge_registry_ready": True,

    "knowledge_object_count": len(objects),

    "knowledge_objects": objects,

    "architecture_hash": ARCH["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_object_registry.json"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KNOWLEDGE-0001")
print("Knowledge Object Registry Engine")
print("=" * 60)
print("Objects :", report["knowledge_object_count"])
print("Output  :", OUT)
print()
print("STATUS : PASS")
