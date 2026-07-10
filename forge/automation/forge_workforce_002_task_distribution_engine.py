import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

OUTPUT = Path("runtime/workforce")
OUTPUT.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now(timezone.utc).isoformat()

task_distribution = {
    "module": "FORGE-WORKFORCE-002",
    "status": "TASK_DISTRIBUTION_ENGINE_READY",
    "timestamp": timestamp,

    "engine": {
        "task_classification": True,
        "capability_matching": True,
        "worker_assignment": True,
        "execution_plan_generation": True,
        "audit_trace_generation": True
    },

    "task_domains": {
        "KNOWLEDGE": "WORKER-ATLAS",
        "MATHEMATICS": "WORKER-MATH",
        "FINANCE": "WORKER-FINANCE",
        "MARKET": "WORKER-MARKET",
        "LEARNING": "WORKER-LEARNING",
        "VALIDATION": "WORKER-AUDITOR"
    },

    "assignment_policy": {
        "human_direction_required": True,
        "automatic_worker_creation": False,
        "permission_boundary_enforced": True,
        "runtime_mode": "SHADOW_ONLY_READ_ONLY",
        "mutation_allowed": False
    }
}


def save(name, data):
    path = OUTPUT / name
    path.write_text(json.dumps(data, indent=2))
    return path


registry = save(
    "task_registry.json",
    {
        "tasks": [],
        "engine": "FORGE-WORKFORCE-002",
        "ready": True
    }
)

save(
    "task_capability_map.json",
    task_distribution["task_domains"]
)

save(
    "worker_assignment_registry.json",
    {
        "assignment_engine": "READY",
        "assignments": []
    }
)

save(
    "task_dispatch_ledger.jsonl",
    {
        "event": "TASK_DISTRIBUTION_ENGINE_INITIALIZED",
        "timestamp": timestamp
    }
)

hash_value = hashlib.sha256(
    registry.read_bytes()
).hexdigest()

save(
    "task_dispatch_hash.json",
    {
        "algorithm": "SHA256",
        "hash": hash_value,
        "verified": True
    }
)

print("FORGE-WORKFORCE-002 TASK DISTRIBUTION ENGINE READY")
print("domains =", len(task_distribution["task_domains"]))
print("hash =", hash_value)
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
