#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
from collections import defaultdict
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = json.loads(
    (ROOT / "runtime/knowledge/knowledge_object_registry.json").read_text()
)

objects = REGISTRY["knowledge_objects"]

by_family = defaultdict(list)
by_prefix = defaultdict(list)
by_runtime = defaultdict(list)
by_module = {}

for obj in objects:

    module = obj["id"]
    family = obj.get("family") or "unknown"
    runtime = "SHADOW_ONLY_READ_ONLY"

    prefix = module.split("_")[0] if "_" in module else module

    by_family[family].append(module)
    by_prefix[prefix].append(module)
    by_runtime[runtime].append(module)

    by_module[module] = {
        "family": family,
        "path": obj.get("path"),
        "knowledge_object": obj.get("knowledge_object")
    }

report = {
    "module": "FORGE-KNOWLEDGE-0002",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "knowledge_index_ready": True,

    "module_count": len(objects),

    "indexes": {
        "by_family": dict(sorted(by_family.items())),
        "by_prefix": dict(sorted(by_prefix.items())),
        "by_runtime": dict(sorted(by_runtime.items())),
        "by_module": by_module,
        "by_tags": {}
    },

    "registry_hash": REGISTRY["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_index.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KNOWLEDGE-0002")
print("Knowledge Index Engine")
print("=" * 60)
print("Modules  :", report["module_count"])
print("Families :", len(by_family))
print("Prefixes :", len(by_prefix))
print("Runtime  :", len(by_runtime))
print("Output   :", OUT)
print()
print("STATUS : PASS")
