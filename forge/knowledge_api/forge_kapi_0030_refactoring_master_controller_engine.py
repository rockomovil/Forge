#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

ORCHESTRATOR = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_orchestrator.json").read_text()
)

READINESS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_readiness.json").read_text()
)

PROGRESS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_progress.json").read_text()
)

controller = {
    "module": "FORGE-KAPI-0030",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "controller_ready": READINESS["refactoring_ready"],
    "execution_mode": ORCHESTRATOR["execution_mode"],
    "worker_count": ORCHESTRATOR["worker_count"],
    "parallel_execution": ORCHESTRATOR["parallel_execution"],
    "pending_refactorings": PROGRESS["pending_refactorings"],
    "completed_refactorings": PROGRESS["completed_refactorings"],
    "master_state": (
        "READY_FOR_EXECUTION"
        if READINESS["refactoring_ready"]
        else "WAIT"
    ),
    "workers": ORCHESTRATOR["workers"]
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_master_controller.json"
outfile.write_text(json.dumps(controller, indent=2))

print("=" * 60)
print("FORGE-KAPI-0030")
print("Refactoring Master Controller Engine")
print("=" * 60)
print("Controller Ready :", controller["controller_ready"])
print("Execution Mode   :", controller["execution_mode"])
print("Workers          :", controller["worker_count"])
print("Master State     :", controller["master_state"])
print("Output           :", outfile)
print()
print("STATUS : PASS")
