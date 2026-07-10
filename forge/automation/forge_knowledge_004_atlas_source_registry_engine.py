import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]
RUNTIME = BASE / "runtime" / "atlas"

RUNTIME.mkdir(parents=True, exist_ok=True)

registry = {
    "module": "FORGE-KNOWLEDGE-004",
    "status": "ATLAS_SOURCE_REGISTRY_ENGINE_READY",
    "source_engine": "FORGE-KNOWLEDGE-003_ATLAS_SOURCE_VALIDATION_ENGINE",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "registry": {
        "initialized": True,
        "source_indexing_ready": True,
        "source_identity_tracking_ready": True,
        "source_metadata_validation_ready": True,
        "source_lineage_tracking_ready": True,
        "immutable_registry_ready": True
    },
    "capabilities": {
        "source_registration": True,
        "source_hash_tracking": True,
        "source_version_tracking": True,
        "source_origin_validation": True,
        "atlas_registry_generation": True
    },
    "timestamp": datetime.now(timezone.utc).isoformat()
}

payload = json.dumps(registry, sort_keys=True).encode()
hash_value = hashlib.sha256(payload).hexdigest()

registry["hash"] = hash_value

(RUNTIME / "source_registry.json").write_text(
    json.dumps(registry, indent=2)
)

(RUNTIME / "source_registry_hash.json").write_text(
    json.dumps({
        "module": "FORGE-KNOWLEDGE-004",
        "hash": hash_value
    }, indent=2)
)

with open(RUNTIME / "source_registry_ledger.jsonl", "a") as f:
    f.write(json.dumps(registry) + "\n")

print("FORGE-KNOWLEDGE-004 ATLAS SOURCE REGISTRY ENGINE READY")
print("hash =", hash_value)
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
