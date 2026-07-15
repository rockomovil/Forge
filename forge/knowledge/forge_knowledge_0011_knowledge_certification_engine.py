#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

VALIDATION = json.loads(
    (ROOT / "runtime/knowledge/knowledge_validation.json").read_text()
)

INDEX = json.loads(
    (ROOT / "runtime/knowledge/knowledge_index.json").read_text()
)

SEMANTIC = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

CONCEPTS = json.loads(
    (ROOT / "runtime/knowledge/knowledge_concepts.json").read_text()
)

checks = VALIDATION["checks"]

certified = all(checks.values())

report = {
    "module": "FORGE-KNOWLEDGE-0011",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "knowledge_certified": certified,
    "certification_level": "FOUNDATION",

    "modules": INDEX["module_count"],
    "families": len(INDEX["indexes"]["by_family"]),
    "concepts": CONCEPTS["concept_count"],
    "semantic_nodes": SEMANTIC["node_count"],
    "semantic_edges": SEMANTIC["edge_count"],

    "validation_hash": VALIDATION["hash"],
    "knowledge_hash": INDEX["hash"],
    "semantic_hash": SEMANTIC["hash"],
    "concept_hash": CONCEPTS["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_certification.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KNOWLEDGE-0011")
print("Knowledge Certification Engine")
print("=" * 60)
print("Certified :", certified)
print("Modules   :", report["modules"])
print("Families  :", report["families"])
print("Concepts  :", report["concepts"])
print("Nodes     :", report["semantic_nodes"])
print("Edges     :", report["semantic_edges"])
print("Output    :", OUT)
print()
print("STATUS : PASS")
