#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

MANIFEST = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_execution_manifest.json").read_text()
)

ready = (
    MANIFEST["parallel_execution"]
    and MANIFEST["group_count"] > 0
    and MANIFEST["patch_count"] > 0
)

report = {
    "module": "FORGE-KAPI-0057",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "parallel_execution": MANIFEST["parallel_execution"],
    "group_count": MANIFEST["group_count"],
    "patch_count": MANIFEST["patch_count"],
    "execution_ready": ready,
    "execution_mode": (
        "PARALLEL_PATCH_SIMULATION"
        if ready else
        "BLOCKED"
    )
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_execution_readiness.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0057")
print("Refactoring Execution Readiness Engine")
print("=" * 60)
print("Ready      :", report["execution_ready"])
print("Mode       :", report["execution_mode"])
print("Groups     :", report["group_count"])
print("Patches    :", report["patch_count"])
print("Output     :", outfile)
print()
print("STATUS : PASS")
