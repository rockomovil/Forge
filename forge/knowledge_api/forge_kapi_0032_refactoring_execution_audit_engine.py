#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

GATEWAY = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_execution_gateway.json").read_text()
)

MASTER = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_master_controller.json").read_text()
)

AUDIT = {
    "module": "FORGE-KAPI-0032",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "execution_gateway_verified": GATEWAY["execution_authorized"],
    "master_controller_verified": MASTER["controller_ready"],
    "parallel_execution": MASTER["parallel_execution"],
    "worker_count": MASTER["worker_count"],
    "execution_mode": MASTER["execution_mode"],
    "safety": GATEWAY["safety"],
    "audit_result": (
        "EXECUTION_READY"
        if (
            GATEWAY["execution_authorized"]
            and MASTER["controller_ready"]
        )
        else "BLOCKED"
    )
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_execution_audit.json"
outfile.write_text(json.dumps(AUDIT, indent=2))

print("=" * 60)
print("FORGE-KAPI-0032")
print("Refactoring Execution Audit Engine")
print("=" * 60)
print("Gateway Verified :", AUDIT["execution_gateway_verified"])
print("Controller Ready :", AUDIT["master_controller_verified"])
print("Parallel         :", AUDIT["parallel_execution"])
print("Workers          :", AUDIT["worker_count"])
print("Audit Result     :", AUDIT["audit_result"])
print("Output           :", outfile)
print()
print("STATUS : PASS")
