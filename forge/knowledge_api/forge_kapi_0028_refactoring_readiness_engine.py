#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

PROGRESS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_progress.json").read_text()
)

GOVERNANCE = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_governance.json").read_text()
)

AUDIT = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_architecture_governance_audit.json").read_text()
)

QUEUE = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_layer_refactoring_queue.json").read_text()
)

ready = (
    AUDIT["all_checks_passed"]
    and GOVERNANCE["governance_state"] == "HEALTHY"
    and PROGRESS["pending_refactorings"] > 0
)

report = {
    "module": "FORGE-KAPI-0028",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "refactoring_ready": ready,
    "governance_state": GOVERNANCE["governance_state"],
    "audit_passed": AUDIT["all_checks_passed"],
    "pending_refactorings": PROGRESS["pending_refactorings"],
    "queue_size": QUEUE["queue_size"],
    "execution_mode": (
        "PARALLEL_BATCH_EXECUTION"
        if ready else
        "WAIT"
    )
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_readiness.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0028")
print("Refactoring Readiness Engine")
print("=" * 60)
print("Ready             :", report["refactoring_ready"])
print("Governance        :", report["governance_state"])
print("Audit Passed      :", report["audit_passed"])
print("Pending           :", report["pending_refactorings"])
print("Execution Mode    :", report["execution_mode"])
print("Output            :", outfile)
print()
print("STATUS : PASS")
