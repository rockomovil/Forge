#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

CERT = json.loads(
    (ROOT / "runtime/knowledge/knowledge_certification.json").read_text()
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

release = {
    "module": "FORGE-KNOWLEDGE-0012",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "released_at": datetime.now(UTC).isoformat(),

    "knowledge_release_ready": True,
    "release_level": "FOUNDATION",

    "knowledge": {
        "modules": INDEX["module_count"],
        "families": len(INDEX["indexes"]["by_family"]),
        "concepts": CONCEPTS["concept_count"],
        "semantic_nodes": SEMANTIC["node_count"],
        "semantic_edges": SEMANTIC["edge_count"]
    },

    "certification": {
        "certified": CERT["knowledge_certified"],
        "level": CERT["certification_level"]
    },

    "artifacts": {
        "registry": "runtime/knowledge/knowledge_object_registry.json",
        "index": "runtime/knowledge/knowledge_index.json",
        "concepts": "runtime/knowledge/knowledge_concepts.json",
        "semantic_graph": "runtime/knowledge/knowledge_semantic_graph.json",
        "validation": "runtime/knowledge/knowledge_validation.json",
        "certification": "runtime/knowledge/knowledge_certification.json"
    },

    "source_hashes": {
        "knowledge": INDEX["hash"],
        "semantic": SEMANTIC["hash"],
        "concepts": CONCEPTS["hash"],
        "certification": CERT["hash"]
    }
}

release["hash"] = hashlib.sha256(
    json.dumps(release, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_release.json"
OUT.write_text(json.dumps(release, indent=2))

print("=" * 60)
print("FORGE-KNOWLEDGE-0012")
print("Knowledge Release Engine")
print("=" * 60)
print("Release Ready :", release["knowledge_release_ready"])
print("Modules       :", release["knowledge"]["modules"])
print("Families      :", release["knowledge"]["families"])
print("Concepts      :", release["knowledge"]["concepts"])
print("Nodes         :", release["knowledge"]["semantic_nodes"])
print("Edges         :", release["knowledge"]["semantic_edges"])
print("Output        :", OUT)
print()
print("STATUS : PASS")
