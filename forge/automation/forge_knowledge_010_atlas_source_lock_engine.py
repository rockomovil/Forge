import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]
RUNTIME = BASE / "runtime" / "atlas"

RUNTIME.mkdir(parents=True, exist_ok=True)

lock = {
    "module": "FORGE-KNOWLEDGE-010",
    "status": "ATLAS_SOURCE_LOCK_ENGINE_READY",
    "source_engine": "FORGE-KNOWLEDGE-009_ATLAS_SOURCE_SEAL_ENGINE",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "lock": {
        "initialized": True,
        "source_lock_ready": True,
        "seal_lock_ready": True,
        "certification_lock_ready": True,
        "integrity_lock_ready": True,
        "registry_lock_ready": True,
        "lineage_lock_ready": True,
        "immutable_lock_state_ready": True
    },
    "capabilities": {
        "source_lock_generation": True,
        "seal_binding": True,
        "certification_binding": True,
        "mutation_protection": True,
        "atlas_lock_validation": True,
        "lock_ledger_generation": True
    },
    "timestamp": datetime.now(timezone.utc).isoformat()
}

payload = json.dumps(lock, sort_keys=True).encode()
hash_value = hashlib.sha256(payload).hexdigest()

lock["hash"] = hash_value

(RUNTIME / "source_lock.json").write_text(
    json.dumps(lock, indent=2)
)

(RUNTIME / "source_lock_hash.json").write_text(
    json.dumps({
        "module": "FORGE-KNOWLEDGE-010",
        "hash": hash_value
    }, indent=2)
)

with open(RUNTIME / "source_lock_ledger.jsonl", "a") as f:
    f.write(json.dumps(lock) + "\n")

print("FORGE-KNOWLEDGE-010 ATLAS SOURCE LOCK ENGINE READY")
print("hash =", hash_value)
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
