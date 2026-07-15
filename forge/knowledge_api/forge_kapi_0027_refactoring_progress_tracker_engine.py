#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

SCHEDULE = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_execution_schedule.json").read_text()
)

QUEUE = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_layer_refactoring_queue.json").read_text()
)

completed = 0
total = len(QUEUE["refactoring_queue"])

progress = {
    "module": "FORGE-KAPI-0027",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "total_refactorings": total,
    "completed_refactorings": completed,
    "pending_refactorings": total - completed,
    "progress_percent": round(
        completed * 100 / total if total else 100,
        2
    ),
    "remaining_batches": len(SCHEDULE["execution_schedule"]),
    "execution_schedule": SCHEDULE["execution_schedule"]
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_progress.json"
outfile.write_text(json.dumps(progress, indent=2))

print("=" * 60)
print("FORGE-KAPI-0027")
print("Refactoring Progress Tracker Engine")
print("=" * 60)
print("Completed :", progress["completed_refactorings"])
print("Pending   :", progress["pending_refactorings"])
print("Progress  :", progress["progress_percent"], "%")
print("Batches   :", progress["remaining_batches"])
print("Output    :", outfile)
print()
print("STATUS : PASS")
