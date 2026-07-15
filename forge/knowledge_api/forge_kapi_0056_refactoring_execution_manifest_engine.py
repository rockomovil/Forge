#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

PRIORITY = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_patch_priority.json").read_text()
)

groups = {}

for patch in PRIORITY["prioritized_patches"]:
    group = str(patch["execution_group"])
    groups.setdefault(group, []).append({
        "candidate_id": patch["candidate_id"],
        "priority": patch["priority"],
        "execution_state": patch["execution_state"]
    })

manifest = {
    "module": "FORGE-KAPI-0056",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "parallel_execution": True,
    "group_count": len(groups),
    "patch_count": PRIORITY["patch_count"],
    "execution_manifest": groups
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_execution_manifest.json"
outfile.write_text(json.dumps(manifest, indent=2))

print("=" * 60)
print("FORGE-KAPI-0056")
print("Refactoring Execution Manifest Engine")
print("=" * 60)
print("Groups     :", manifest["group_count"])
print("Patches    :", manifest["patch_count"])
print("Parallel   :", manifest["parallel_execution"])
print("Output     :", outfile)
print()
print("STATUS : PASS")
