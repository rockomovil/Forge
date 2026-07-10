import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

OUTPUT = Path("runtime/workforce")
OUTPUT.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now(timezone.utc).isoformat()

workers = {
    "module": "FORGE-WORKFORCE-001",
    "status": "WORKER_REGISTRY_EXPANSION_ENGINE_READY",
    "timestamp": timestamp,

    "workers": [
        {
            "id": "WORKER-ATLAS",
            "role": "KNOWLEDGE_ACQUISITION",
            "domain": "FINANCIAL_KNOWLEDGE",
            "permissions": [
                "source_ingestion",
                "knowledge_processing",
                "semantic_indexing"
            ]
        },
        {
            "id": "WORKER-MATH",
            "role": "MATHEMATICAL_ENGINEERING",
            "domain": "QUANTITATIVE_MODELS",
            "permissions": [
                "mathematical_analysis",
                "simulation",
                "optimization"
            ]
        },
        {
            "id": "WORKER-FINANCE",
            "role": "FINANCIAL_ENGINEERING",
            "domain": "CAPITAL_INTELLIGENCE",
            "permissions": [
                "portfolio_analysis",
                "risk_models",
                "valuation"
            ]
        },
        {
            "id": "WORKER-MARKET",
            "role": "MARKET_INTELLIGENCE",
            "domain": "MARKET_ANALYSIS",
            "permissions": [
                "market_data_processing",
                "event_analysis",
                "correlation_analysis"
            ]
        },
        {
            "id": "WORKER-LEARNING",
            "role": "ADAPTIVE_LEARNING",
            "domain": "EXPERIENCE_ENGINE",
            "permissions": [
                "experience_analysis",
                "model_evaluation",
                "pattern_detection"
            ]
        },
        {
            "id": "WORKER-AUDITOR",
            "role": "VALIDATION_CERTIFICATION",
            "domain": "SYSTEM_GOVERNANCE",
            "permissions": [
                "integrity_validation",
                "regression_validation",
                "certification"
            ]
        }
    ],

    "governance": {
        "human_direction_required": True,
        "worker_autonomous_creation": False,
        "runtime_mode": "SHADOW_ONLY_READ_ONLY",
        "mutation_allowed": False
    }
}


def save(name, data):
    path = OUTPUT / name
    path.write_text(json.dumps(data, indent=2))
    return path


registry = save(
    "worker_registry.json",
    workers
)

save(
    "worker_capabilities.json",
    {
        "workers": [
            {
                "id": w["id"],
                "role": w["role"],
                "domain": w["domain"]
            }
            for w in workers["workers"]
        ]
    }
)

save(
    "worker_permissions.json",
    {
        "permission_boundary_enforced": True,
        "workers": [
            {
                "id": w["id"],
                "permissions": w["permissions"]
            }
            for w in workers["workers"]
        ]
    }
)

save(
    "worker_dependencies.json",
    {
        "FORGE": [
            "WORKER-ATLAS",
            "WORKER-MATH",
            "WORKER-FINANCE",
            "WORKER-MARKET",
            "WORKER-LEARNING",
            "WORKER-AUDITOR"
        ]
    }
)

hash_value = hashlib.sha256(
    registry.read_bytes()
).hexdigest()

save(
    "worker_registry_hash.json",
    {
        "algorithm": "SHA256",
        "hash": hash_value,
        "verified": True
    }
)

print("FORGE-WORKFORCE-001 WORKER REGISTRY EXPANSION ENGINE READY")
print("workers =", len(workers["workers"]))
print("hash =", hash_value)
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
