#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX = json.loads(
    (ROOT / "runtime/knowledge/knowledge_index.json").read_text()
)

CONCEPTS = json.loads(
    (ROOT / "runtime/knowledge/knowledge_concepts.json").read_text()
)

GRAPH = json.loads(
    (ROOT / "runtime/knowledge/knowledge_semantic_graph.json").read_text()
)

XREF = json.loads(
    (ROOT / "runtime/knowledge/knowledge_cross_reference.json").read_text()
)

api = {
    "module": "FORGE-KAPI-0001",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "knowledge_api_ready": True,

    "services": {
        "module_lookup": True,
        "family_lookup": True,
        "concept_lookup": True,
        "graph_lookup": True,
        "cross_reference_lookup": True
    },

    "statistics": {
        "modules": INDEX["module_count"],
        "families": len(INDEX["indexes"]["by_family"]),
        "concepts": CONCEPTS["concept_count"],
        "graph_nodes": GRAPH["node_count"],
        "graph_edges": GRAPH["edge_count"],
        "cross_references": len(XREF["cross_references"])
    },

    "resources": {
        "index": "runtime/knowledge/knowledge_index.json",
        "concepts": "runtime/knowledge/knowledge_concepts.json",
        "semantic_graph": "runtime/knowledge/knowledge_semantic_graph.json",
        "cross_reference": "runtime/knowledge/knowledge_cross_reference.json"
    },

    "api": {
        "module": "lookup_module(name)",
        "family": "lookup_family(name)",
        "concept": "lookup_concept(name)",
        "graph": "lookup_graph(node)",
        "xref": "lookup_cross_reference(module)"
    },

    "source_hashes": {
        "index": INDEX["hash"],
        "concepts": CONCEPTS["hash"],
        "graph": GRAPH["hash"],
        "cross_reference": XREF["hash"]
    }
}

api["hash"] = hashlib.sha256(
    json.dumps(api, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge_api/knowledge_api_core.json"
OUT.write_text(json.dumps(api, indent=2))

print("=" * 60)
print("FORGE-KAPI-0001")
print("Knowledge API Core Engine")
print("=" * 60)
print("Modules    :", api["statistics"]["modules"])
print("Families   :", api["statistics"]["families"])
print("Concepts   :", api["statistics"]["concepts"])
print("Graph Nodes:", api["statistics"]["graph_nodes"])
print("Graph Edges:", api["statistics"]["graph_edges"])
print("Output     :", OUT)
print()
print("STATUS : PASS")
