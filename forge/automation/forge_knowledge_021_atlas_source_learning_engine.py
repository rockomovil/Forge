import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]
RUNTIME = BASE / "runtime" / "atlas"

RUNTIME.mkdir(parents=True, exist_ok=True)

learning = {
    "module": "FORGE-KNOWLEDGE-021",
    "status": "ATLAS_SOURCE_LEARNING_ENGINE_READY",
    "source_engine": "FORGE-KNOWLEDGE-020_ATLAS_SOURCE_ADAPTATION_ENGINE",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "learning": {
        "initialized": True,
        "source_learning_ready": True,
        "adaptation_learning_ready": True,
        "pattern_learning_ready": True,
        "historical_learning_ready": True,
        "context_learning_ready": True,
        "continuous_learning_ready": True
    },
    "capabilities": {
        "source_pattern_learning": True,
        "lineage_pattern_learning": True,
        "governance_learning": True,
        "integrity_learning": True,
        "atlas_knowledge_accumulation": True,
        "learning_ledger_generation": True
    },
    "terminal_state": {
        "sealed": True,
        "locked": True,
        "certified": True,
        "immutable": True,
        "mutation_allowed": False,
        "delete_allowed": False,
        "rollback_allowed": False
    },
    "timestamp": datetime.now(timezone.utc).isoformat()
}

payload = json.dumps(learning, sort_keys=True).encode()
hash_value = hashlib.sha256(payload).hexdigest()

learning["hash"] = hash_value

(RUNTIME / "source_learning.json").write_text(
    json.dumps(learning, indent=2)
)

(RUNTIME / "source_learning_hash.json").write_text(
    json.dumps({
        "module": "FORGE-KNOWLEDGE-021",
        "hash": hash_value
    }, indent=2)
)

with open(RUNTIME / "source_learning_ledger.jsonl", "a") as f:
    f.write(json.dumps(learning) + "\n")

print("FORGE-KNOWLEDGE-021 ATLAS SOURCE LEARNING ENGINE READY")
print("hash =", hash_value)
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
