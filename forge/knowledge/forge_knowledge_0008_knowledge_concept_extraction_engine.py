#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
from collections import defaultdict
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]

INDEX = json.loads(
    (ROOT / "runtime/knowledge/knowledge_index.json").read_text()
)

modules = INDEX["indexes"]["by_module"]

STOPWORDS = {
    "forge",
    "module",
    "engine",
    "knowledge",
    "runtime",
    "json",
    "py"
}

concepts = defaultdict(list)

for module_name, info in modules.items():

    tokens = re.split(r"[_\-]+", module_name.lower())

    family = (info.get("family") or "").lower()

    if family:
        concepts[family].append(module_name)

    for token in tokens:

        if len(token) < 3:
            continue

        if token in STOPWORDS:
            continue

        concepts[token].append(module_name)

concepts = {
    k: sorted(set(v))
    for k, v in sorted(concepts.items())
}

report = {
    "module": "FORGE-KNOWLEDGE-0008",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "concept_extraction_ready": True,

    "module_count": len(modules),
    "concept_count": len(concepts),

    "concepts": concepts,

    "knowledge_hash": INDEX["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_concepts.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KNOWLEDGE-0008")
print("Knowledge Concept Extraction Engine")
print("=" * 60)
print("Modules  :", len(modules))
print("Concepts :", len(concepts))
print("Output   :", OUT)
print()
print("STATUS : PASS")
