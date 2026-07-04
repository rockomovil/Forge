#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import json

ROOT = Path(__file__).resolve().parents[1]

VALIDATED = ROOT / "runtime" / "builder" / "validated_specifications.json"
FIR_SPEC = ROOT / "runtime" / "fir" / "fir_specification.json"
OUT = ROOT / "runtime" / "fir" / "fir_units.json"

if not VALIDATED.exists():
    raise SystemExit("ERROR: validated_specifications.json missing")

if not FIR_SPEC.exists():
    raise SystemExit("ERROR: fir_specification.json missing")

validated = json.loads(VALIDATED.read_text())
fir_spec = json.loads(FIR_SPEC.read_text())

units = {
    "generated_at": datetime.now(UTC).isoformat(),
    "builder": "BLD-0006",
    "fir_version": fir_spec["fir_version"],
    "units": []
}

for spec in validated["specifications"]:

    if spec["status"] != "VALID":
        continue

    unit = {
        "identity": {
            "id": spec["id"],
            "name": spec["name"]
        },
        "classification": {
            "type": "capability",
            "status": "FIR_READY"
        },
        "architecture": {
            "style": "Hybrid",
            "validated_by": "BLD-0004"
        },
        "dependencies": [],
        "capabilities": {
            "register": True
        },
        "interfaces": {
            "cli": False,
            "service": False
        },
        "artifacts": {
            "python": True,
            "tests": True,
            "documentation": True,
            "capability_registry": True,
            "release": False,
            "metrics": True
        },
        "quality": {
            "architecture_score": spec["score"],
            "checks_passed": spec["passed"],
            "checks_total": spec["total"]
        },
        "metadata": {
            "created_at": datetime.now(UTC).isoformat(),
            "source": "validated_specifications.json"
        }
    }

    units["units"].append(unit)

OUT.write_text(json.dumps(units, indent=2, ensure_ascii=False))

print()
print("FIR Units")
print("---------")

for unit in units["units"]:
    print(
        f'{unit["identity"]["id"]:<12} '
        f'{unit["classification"]["status"]:<12} '
        f'{unit["identity"]["name"]}'
    )

print()
print("FIR Version :", units["fir_version"])
print("FIR Units   :", len(units["units"]))
print("Output      :", OUT)

if not units["units"]:
    raise SystemExit("ERROR: no FIR units generated")

print()
print("STATUS : BLD0006_FIR_BUILDER_READY")
