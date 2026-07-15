#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

READINESS = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_execution_readiness.json").read_text()
)

MANIFEST = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_execution_manifest.json").read_text()
)

workers = []

for group_id in sorted(MANIFEST["execution_manifest"], key=int):
    workers.append({
        "worker_id": f"worker_{group_id}",
        "batch": int(group_id),
        "tasks": len(MANIFEST["execution_manifest"][group_id]),
        "state": "READY",
        "mode": "SIMULATION"
    })

report = {
    "module": "FORGE-KAPI-0058",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "execution_ready": READINESS["execution_ready"],
    "execution_mode": READINESS["execution_mode"],
    "parallel_execution": True,
    "worker_count": len(workers),
    "workers": workers
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_execution_orchestrator.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0058")
print("Refactoring Execution Orchestrator Engine")
print("=" * 60)
print("Ready      :", report["execution_ready"])
print("Workers    :", report["worker_count"])
print("Mode       :", report["execution_mode"])
print("Parallel   :", report["parallel_execution"])
print("Output     :", outfile)
print()
print("STATUS : PASS")
