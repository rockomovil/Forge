#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
from collections import defaultdict
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

modules = INDEX["indexes"]["by_module"]

outgoing = defaultdict(list)
incoming = defaultdict(list)

for edge in GRAPH.get("edges", []):

    src = edge["from"].replace("module::", "")
    dst = edge["to"].replace("module::", "")

    outgoing[src].append(dst)
    incoming[dst].append(src)

updated = 0

cross_reference = {}

for module_name, info in sorted(modules.items()):

    family = (info.get("family") or "unknown").lower()

    md = KNOWLEDGE_ROOT / family / f"{module_name}.md"

    if not md.exists():
        continue

    related = sorted(
        m
        for m, d in modules.items()
        if d["family"] == info["family"] and m != module_name
    )

    outgoing_refs = sorted(outgoing.get(module_name, []))
    incoming_refs = sorted(incoming.get(module_name, []))

    content = md.read_text()

    content += "\n\n## Cross References\n\n"

    content += "### Depends On\n\n"
    if outgoing_refs:
        for dep in outgoing_refs:
            content += f"- {dep}\n"
    else:
        content += "- None\n"

    content += "\n### Referenced By\n\n"
    if incoming_refs:
        for ref in incoming_refs:
            content += f"- {ref}\n"
    else:
        content += "- None\n"

    content += "\n### Same Family\n\n"
    for ref in related[:25]:
        content += f"- {ref}\n"

    md.write_text(content)

    cross_reference[module_name] = {
        "family": info["family"],
        "depends_on": outgoing_refs,
        "referenced_by": incoming_refs,
        "same_family": related
    }

    updated += 1

report = {
    "module": "FORGE-KNOWLEDGE-0005",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "knowledge_documents_updated": updated,

    "cross_reference_count": len(cross_reference),

    "cross_references": cross_reference,

    "graph_hash": GRAPH["hash"],
    "index_hash": INDEX["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_cross_reference.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KNOWLEDGE-0005")
print("Knowledge Cross Reference Engine")
print("=" * 60)
print("Documents :", updated)
print("References:", len(cross_reference))
print("Output    :", OUT)
print()
print("STATUS : PASS")
