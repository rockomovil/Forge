import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

OUTPUT = Path("runtime/atlas")
OUTPUT.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now(timezone.utc).isoformat()

atlas = {
    "module": "FORGE-KNOWLEDGE-001",
    "status": "ATLAS_FOUNDATION_ENGINE_READY",
    "timestamp": timestamp,

    "purpose": {
        "system": "ATLAS",
        "role": "KNOWLEDGE_ACQUISITION_LAYER",
        "objective": "BUILD_FINANCIAL_KNOWLEDGE_FOUNDATION"
    },

    "capabilities": {
        "source_registry": True,
        "knowledge_domain_management": True,
        "metadata_management": True,
        "ingestion_pipeline_definition": True,
        "validation_interface": True,
        "memory_interface": True
    },

    "knowledge_domains": [
        "FINANCE",
        "MATHEMATICS",
        "FINANCIAL_MATHEMATICS",
        "ECONOMICS",
        "ACCOUNTING",
        "MARKETS",
        "RISK_MANAGEMENT",
        "MACHINE_LEARNING",
        "TRADING_SYSTEMS"
    ],

    "governance": {
        "human_direction_required": True,
        "automatic_knowledge_promotion": False,
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
    "atlas_registry.json",
    atlas
)

save(
    "knowledge_domains.json",
    {
        "domains": atlas["knowledge_domains"],
        "count": len(atlas["knowledge_domains"])
    }
)

save(
    "source_registry.json",
    {
        "sources": [],
        "validation_required": True
    }
)

save(
    "knowledge_pipeline.json",
    {
        "pipeline": [
            "SOURCE_DISCOVERY",
            "SOURCE_VALIDATION",
            "INGESTION",
            "EXTRACTION",
            "CLASSIFICATION",
            "MEMORY_STORAGE"
        ]
    }
)

save(
    "atlas_validation_interface.json",
    {
        "validation_enabled": True,
        "requires_certification": True
    }
)

hash_value = hashlib.sha256(
    registry.read_bytes()
).hexdigest()

save(
    "atlas_hash.json",
    {
        "algorithm": "SHA256",
        "hash": hash_value,
        "verified": True
    }
)

print("FORGE-KNOWLEDGE-001 ATLAS FOUNDATION ENGINE READY")
print("domains =", len(atlas["knowledge_domains"]))
print("hash =", hash_value)
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
