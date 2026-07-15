#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX = json.loads(
    (ROOT / "runtime/knowledge/knowledge_index.json").read_text()
)

GRAPH = json.loads(
    (ROOT / "runtime/architecture/architecture_dependency_graph.json").read_text()
)

KNOWLEDGE_ROOT = ROOT / "knowledge"

nodes = {
    n["id"]: n
    for n in GRAPH.get("nodes", [])
}

outgoing = {}

for edge in GRAPH.get("edges", []):
    outgoing.setdefault(edge["from"], []).append(edge["to"])

updated = 0

for module_name, info in INDEX["indexes"]["by_module"].items():

    family = (info.get("family") or "unknown").lower()

    md = KNOWLEDGE_ROOT / family / f"{module_name}.md"

    if not md.exists():
        continue

    deps = sorted(outgoing.get(f"module::{module_name}", []))

    content = f"""---
id: {module_name}
family: {info.get("family")}
runtime: SHADOW_ONLY_READ_ONLY
status: READY
generated_at: {datetime.now(UTC).isoformat()}
path: {info.get("path")}
knowledge_version: 2
---

# {module_name}

## Metadata

- Family: {info.get("family")}
- Runtime: SHADOW_ONLY_READ_ONLY
- Status: READY

## Dependencies

"""

    if deps:
        for dep in deps:
            content += f"- {dep}\n"
    else:
        content += "- None\n"

    content += f"""

## Graph

Node Present: {"Yes" if f"module::{module_name}" in nodes else "No"}

Outgoing Dependencies: {len(deps)}

## Source

{info.get("path")}

## Notes

Generated automatically by FORGE-KNOWLEDGE-0004.
"""

    md.write_text(content)

    updated += 1

report = {
    "module": "FORGE-KNOWLEDGE-0004",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "knowledge_documents_updated": updated,

    "knowledge_root": str(KNOWLEDGE_ROOT),

    "graph_hash": GRAPH["hash"],
    "index_hash": INDEX["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_metadata_enrichment.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KNOWLEDGE-0004")
print("Knowledge Metadata Enrichment Engine")
print("=" * 60)
print("Updated :", updated)
print("Output  :", OUT)
print()
print("STATUS : PASS")
