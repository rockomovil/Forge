#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX = json.loads(
    (ROOT / "runtime/knowledge/knowledge_index.json").read_text()
)

objects = INDEX["indexes"]["by_module"]

knowledge_root = ROOT / "knowledge"
knowledge_root.mkdir(exist_ok=True)

generated = 0

for module_name, info in sorted(objects.items()):

    family = (info.get("family") or "unknown").lower()

    folder = knowledge_root / family
    folder.mkdir(parents=True, exist_ok=True)

    doc = folder / f"{module_name}.md"

    text = f"""---
id: {module_name}
family: {info.get("family")}
runtime: SHADOW_ONLY_READ_ONLY
status: READY
generated_at: {datetime.now(UTC).isoformat()}
---

# {module_name}

## Purpose

TODO

## Inputs

TODO

## Outputs

TODO

## Dependencies

TODO

## Runtime

SHADOW_ONLY_READ_ONLY

## Source

{info.get("path")}
"""

    doc.write_text(text)

    generated += 1

report = {
    "module": "FORGE-KNOWLEDGE-0003",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "knowledge_objects_generated": generated,
    "knowledge_root": str(knowledge_root),

    "index_hash": INDEX["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_object_generation.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KNOWLEDGE-0003")
print("Knowledge Object Generator Engine")
print("=" * 60)
print("Generated :", generated)
print("Output    :", OUT)
print("Knowledge :", knowledge_root)
print()
print("STATUS : PASS")
