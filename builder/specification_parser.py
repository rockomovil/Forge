#!/usr/bin/env python3

from pathlib import Path
import json
from datetime import datetime, UTC

ROOT = Path(__file__).resolve().parents[1]

SPEC_DIR = ROOT / "builder" / "specifications"

OUTPUT = ROOT / "runtime" / "builder" / "parsed_specifications.json"

parsed = {
    "generated_at": datetime.now(UTC).isoformat(),
    "specifications":[]
}

count = 0

for file in sorted(SPEC_DIR.glob("*.json")):

    spec = json.loads(file.read_text())

    parsed["specifications"].append({

        "id": spec["id"],

        "name": spec["name"],

        "type": spec["type"],

        "architecture": spec["architecture"],

        "dependencies": spec["dependencies"],

        "status":"PARSED"

    })

    count += 1

OUTPUT.write_text(
    json.dumps(
        parsed,
        indent=2,
        ensure_ascii=False
    )
)

print()
print("Parsed Specifications")
print("---------------------")

for s in parsed["specifications"]:

    print(
        f'{s["id"]:<12} {s["name"]}'
    )

print()
print("Specification Count :", count)
print("Output              :", OUTPUT)
