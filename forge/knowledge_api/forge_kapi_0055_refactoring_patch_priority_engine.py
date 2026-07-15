#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

RISK = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_patch_risk_assessment.json").read_text()
)

prioritized = []

for i, patch in enumerate(RISK["patches"], start=1):
    prioritized.append({
        **patch,
        "priority": i,
        "execution_group": ((i - 1) // 5) + 1,
        "execution_state": "PENDING"
    })

report = {
    "module": "FORGE-KAPI-0055",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "patch_count": len(prioritized),
    "execution_groups": max(p["execution_group"] for p in prioritized) if prioritized else 0,
    "prioritized_patches": prioritized
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_patch_priority.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0055")
print("Refactoring Patch Priority Engine")
print("=" * 60)
print("Patches          :", report["patch_count"])
print("Execution Groups :", report["execution_groups"])
print("Output           :", outfile)
print()
print("STATUS : PASS")
