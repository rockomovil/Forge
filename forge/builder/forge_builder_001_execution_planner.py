#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PLAN = ROOT / "runtime/compiler/forge_build_plan_001.json"
SCHEDULE = ROOT / "runtime/compiler/forge_parallel_build_schedule_001.json"
OUT = ROOT / "runtime/builder"


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


plan = json.loads(PLAN.read_text())
schedule = json.loads(SCHEDULE.read_text())

levels = []

for level_number, module_ids in enumerate(schedule["levels"], start=1):

    modules = []

    for mid in module_ids:

        item = next(

            m

            for m in plan["modules"]

            if m["module_id"] == mid

        )

        modules.append({

            "module_id":
            item["module_id"],

            "module_code":
            item["module_code"],

            "family":
            item["family"],

            "script":
            item["script"]

        })

    levels.append({

        "level":
        level_number,

        "parallelism":
        len(modules),

        "modules":
        modules

    })


payload = {

    "builder":
    "FORGE-BUILDER-001",

    "status":
    "FORGE_EXECUTION_PLANNER_READY",

    "runtime_mode":
    "SHADOW_ONLY_READ_ONLY",

    "families":
    len(
        {
            m["family"]
            for l in levels
            for m in l["modules"]
        }
    ),

    "modules":
    sum(
        len(x["modules"])
        for x in levels
    ),

    "levels":
    len(levels),

    "execution_plan":
    levels,

    "generated":
    datetime.now(
        timezone.utc
    ).isoformat()

}

payload["planner_hash"] = hashlib.sha256(

    json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":")
    ).encode()

).hexdigest()

OUT.mkdir(
    parents=True,
    exist_ok=True
)

report = OUT / "forge_execution_plan_001.json"

report.write_text(
    json.dumps(
        payload,
        indent=2
    ) + "\n"
)

digest = sha256(report)

(OUT / "forge_execution_plan_001_hash.json").write_text(

    json.dumps({

        "artifact":
        str(report.relative_to(ROOT)),

        "sha256":
        digest

    }, indent=2) + "\n"

)

with (
    OUT /
    "forge_execution_plan_001_ledger.jsonl"
).open("a") as f:

    f.write(
        json.dumps(payload) + "\n"
    )

print("FORGE-BUILDER-001")
print("FORGE_EXECUTION_PLANNER_READY")
print(f"families = {payload['families']}")
print(f"modules = {payload['modules']}")
print(f"levels = {payload['levels']}")
print(f"planner_hash = {payload['planner_hash']}")
print(f"hash = {digest}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
