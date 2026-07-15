#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

MASTER = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_master_controller.json").read_text()
)

QUEUE = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_layer_refactoring_queue.json").read_text()
)

gateway = {
    "module": "FORGE-KAPI-0031",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "execution_authorized": (
        MASTER["controller_ready"]
        and MASTER["master_state"] == "READY_FOR_EXECUTION"
    ),
    "execution_mode": MASTER["execution_mode"],
    "worker_count": MASTER["worker_count"],
    "pending_operations": QUEUE["queue_size"],
    "parallel_execution": MASTER["parallel_execution"],
    "safety": {
        "shadow_only": True,
        "code_mutation": False,
        "automatic_commit": False,
        "automatic_push": False
    }
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_execution_gateway.json"
outfile.write_text(json.dumps(gateway, indent=2))

print("=" * 60)
print("FORGE-KAPI-0031")
print("Refactoring Execution Gateway Engine")
print("=" * 60)
print("Authorized        :", gateway["execution_authorized"])
print("Execution Mode    :", gateway["execution_mode"])
print("Workers           :", gateway["worker_count"])
print("Pending           :", gateway["pending_operations"])
print("Shadow Only       :", gateway["safety"]["shadow_only"])
print("Output            :", outfile)
print()
print("STATUS : PASS")
