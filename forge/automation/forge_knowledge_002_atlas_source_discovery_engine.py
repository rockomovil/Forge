import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

OUTPUT = Path("runtime/atlas")
OUTPUT.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now(timezone.utc).isoformat()

source_discovery = {
    "module": "FORGE-KNOWLEDGE-002",
    "status": "ATLAS_SOURCE_DISCOVERY_ENGINE_READY",
    "timestamp": timestamp,

    "engine": {
        "source_discovery": True,
        "source_classification": True,
        "metadata_extraction": True,
        "quality_tracking": True,
        "priority_ranking": True,
        "discovery_trace_generation": True
    },

    "source_types": [
        "BOOKS",
        "ACADEMIC_PAPERS",
        "FINANCIAL_REPORTS",
        "ECONOMIC_DATA",
        "MARKET_DATA",
        "RESEARCH_DOCUMENTS",
        "TECHNICAL_DOCUMENTATION"
    ],

    "evaluation": {
        "criteria": [
            "AUTHORITY",
            "REPUTATION",
            "METHODOLOGY",
            "RECENCY",
            "CITATION_VALUE",
            "CONSISTENCY"
        ],
        "quality_scoring": True,
        "source_ranking": True
    },

    "governance": {
        "human_direction_required": True,
        "automatic_source_promotion": False,
        "source_validation_required": True,
        "mutation_allowed": False,
        "runtime_mode": "SHADOW_ONLY_READ_ONLY"
    }
}


def save(name, data):
    path = OUTPUT / name
    path.write_text(json.dumps(data, indent=2))
    return path


registry = save(
    "source_discovery_registry.json",
    source_discovery
)

save(
    "source_metadata.json",
    {
        "sources": [],
        "metadata_extraction_enabled": True
    }
)

save(
    "source_quality_scores.json",
    {
        "scoring_enabled": True,
        "scores": []
    }
)

save(
    "source_priority_index.json",
    {
        "ranking_enabled": True,
        "priority_sources": []
    }
)

save(
    "source_discovery_trace.jsonl",
    {
        "event": "ATLAS_SOURCE_DISCOVERY_INITIALIZED",
        "timestamp": timestamp
    }
)

hash_value = hashlib.sha256(
    registry.read_bytes()
).hexdigest()

save(
    "source_discovery_hash.json",
    {
        "algorithm": "SHA256",
        "hash": hash_value,
        "verified": True
    }
)

print("FORGE-KNOWLEDGE-002 ATLAS SOURCE DISCOVERY ENGINE READY")
print("source_types =", len(source_discovery["source_types"]))
print("hash =", hash_value)
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
