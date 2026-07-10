import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]
RUNTIME = BASE / "runtime" / "atlas"

RUNTIME.mkdir(parents=True, exist_ok=True)

alert = {
    "module": "FORGE-KNOWLEDGE-038",
    "status": "ATLAS_SOURCE_ALERT_ENGINE_READY",
    "source_engine": "FORGE-KNOWLEDGE-037_ATLAS_SOURCE_MONITORING_ENGINE",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "alert": {
        "initialized": True,
        "source_alert_ready": True,
        "monitoring_alert_ready": True,
        "governance_alert_ready": True,
        "sovereign_alert_ready": True,
        "terminal_alert_ready": True,
        "release_alert_ready": True,
        "archive_alert_ready": True,
        "certification_alert_ready": True,
        "knowledge_alert_ready": True
    },
    "capabilities": {
        "source_anomaly_detection": True,
        "governance_event_detection": True,
        "sovereign_event_detection": True,
        "terminal_event_detection": True,
        "archive_event_detection": True,
        "knowledge_event_detection": True,
        "atlas_alert_generation": True,
        "alert_ledger_generation": True
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

payload = json.dumps(alert, sort_keys=True).encode()
hash_value = hashlib.sha256(payload).hexdigest()

alert["hash"] = hash_value

(RUNTIME / "source_alert.json").write_text(
    json.dumps(alert, indent=2)
)

(RUNTIME / "source_alert_hash.json").write_text(
    json.dumps({
        "module": "FORGE-KNOWLEDGE-038",
        "hash": hash_value
    }, indent=2)
)

with open(RUNTIME / "source_alert_ledger.jsonl", "a") as f:
    f.write(json.dumps(alert) + "\n")

print("FORGE-KNOWLEDGE-038 ATLAS SOURCE ALERT ENGINE READY")
print("hash =", hash_value)
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
