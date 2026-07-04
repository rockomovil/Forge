#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import json

ROOT = Path(__file__).resolve().parents[1]

OUTPUT = ROOT / "runtime" / "fir" / "fir_specification.json"

fir = {

    "generated_at": datetime.now(UTC).isoformat(),

    "fir_version": "1.0",

    "name": "Forge Intermediate Representation",

    "description":
        "Canonical engineering representation used internally by Forge.",

    "pipeline":[

        "Specification",

        "Parser",

        "Architecture Validator",

        "FIR",

        "Generators",

        "Validation",

        "Release"

    ],

    "required_sections":[

        "identity",

        "classification",

        "architecture",

        "dependencies",

        "capabilities",

        "interfaces",

        "artifacts",

        "quality",

        "metadata"

    ],

    "artifact_targets":[

        "python",

        "tests",

        "documentation",

        "capability_registry",

        "command_center",

        "release",

        "metrics"

    ],

    "future_targets":[

        "rust",

        "go",

        "cpp",

        "web",

        "api",

        "docker",

        "terraform"

    ],

    "design_principles":[

        "Single Source of Truth",

        "Deterministic Generation",

        "Architecture First",

        "Language Independent",

        "Extensible",

        "Reproducible"

    ]

}

OUTPUT.write_text(
    json.dumps(
        fir,
        indent=2,
        ensure_ascii=False
    )
)

print()
print("Forge Intermediate Representation")
print("---------------------------------")
print()

print("Version :", fir["fir_version"])

print()

print("Pipeline")

for step in fir["pipeline"]:
    print(" •", step)

print()

print("Required Sections :", len(fir["required_sections"]))

print("Artifact Targets  :", len(fir["artifact_targets"]))

print("Future Targets    :", len(fir["future_targets"]))

print()

print("Specification:")
print(OUTPUT)

