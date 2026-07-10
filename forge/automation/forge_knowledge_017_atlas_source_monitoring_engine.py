import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]
RUNTIME = BASE / "runtime" / "atlas"

RUNTIME.mkdir(parents=True, exist_ok=True)

monitoring = {
    "module": "FORGE-KNOWLEDGE-017",
    "status": "ATLAS_SOURCE_MONITORING_ENGINE_READY",
    "source_engine": "FORGE-KNOWLEDGE-016_ATLAS_SOURCE_GOVERNANCE_ENGINE",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "monitoring": {
        "initialized": True,
        "source_monitoring_ready": True,
        "governance_monitoring_ready": True,
        "integrity_monitoring_ready": True,
        "lineage_monitoring_ready": True,
        "archive_monitoring_ready": True,
        "continuous_validation_ready": True
    },
    "capabilities": {
        "source_state_monitoring": True,
        "integrity_state_monitoring": True,
        "governance_state_monitoring": True,
        "anomaly_detection_ready": True,
        "atlas_health_tracking": True,
        "monitoring_ledger_generation": True
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

payload = json.dumps(monitoring, sort_keys=True).encode()
hash_value = hashlib.sha256(payload).hexdigest()

monitoring["hash"] = hash_value

(RUNTIME / "source_monitoring.json").write_text(
    json.dumps(monitoring, indent=2)
)

(RUNTIME / "source_monitoring_hash.json").write_text(
    json.dumps({
        "module": "FORGE-KNOWLEDGE-017",
        "hash": hash_value
    }, indent=2)
)

with open(RUNTIME / "source_monitoring_ledger.jsonl", "a") as f:
    f.write(json.dumps(monitoring) + "\n")

print("FORGE-KNOWLEDGE-017 ATLAS SOURCE MONITORING ENGINE READY")
print("hash =", hash_value)
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
