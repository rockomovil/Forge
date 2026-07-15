#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

READINESS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_readiness.json").read_text()
)

SCHEDULE = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_execution_schedule.json").read_text()
)

workers = []

for batch in SCHEDULE["execution_schedule"]:

    workers.append({
        "worker": f"worker_{batch['batch']:03d}",
        "batch": batch["batch"],
        "modules": len(batch["modules"]),
        "parallelizable": batch["parallelizable"],
        "status": (
            "READY"
            if READINESS["refactoring_ready"]
            else "WAIT"
        )
    })

report = {
    "module": "FORGE-KAPI-0029",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "execution_mode": READINESS["execution_mode"],
    "workers": workers,
    "worker_count": len(workers),
    "parallel_execution": all(
        w["parallelizable"] for w in workers
    ),
    "ready": READINESS["refactoring_ready"]
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_orchestrator.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0029")
print("Refactoring Orchestrator Engine")
print("=" * 60)
print("Workers           :", report["worker_count"])
print("Execution Mode    :", report["execution_mode"])
print("Parallel          :", report["parallel_execution"])
print("Ready             :", report["ready"])
print("Output            :", outfile)
print()
print("STATUS : PASS")
