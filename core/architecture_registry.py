#!/usr/bin/env python3

from pathlib import Path
import json
from datetime import datetime, UTC

ROOT = Path(__file__).resolve().parents[1]

OUTPUT = ROOT / "runtime" / "architecture" / "architecture_registry.json"

registry = {
    "generated_at": datetime.now(UTC).isoformat(),
    "architecture": {
        "style": "Hybrid",
        "layers": [
            {
                "name": "Meta Layer",
                "purpose": "Self evaluation, self optimization and architecture intelligence."
            },
            {
                "name": "Application Layer",
                "style": "Clean Architecture",
                "purpose": "Use cases and orchestration."
            },
            {
                "name": "Domain Layer",
                "style": "Onion Architecture",
                "purpose": "Business rules and domain model."
            },
            {
                "name": "Ports",
                "style": "Hexagonal",
                "purpose": "Interfaces exposed by the domain."
            },
            {
                "name": "Adapters",
                "style": "Hexagonal",
                "purpose": "External implementations."
            },
            {
                "name": "Infrastructure",
                "purpose": "Filesystem, databases, APIs, Git, Docker, LLMs."
            }
        ],
        "principles": [
            "SOLID",
            "Dependency Inversion",
            "Separation of Concerns",
            "Domain First",
            "Ports and Adapters",
            "Self Inspection",
            "Self Refactoring"
        ]
    }
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(registry, indent=2, ensure_ascii=False))

print()
print("Forge Architecture")
print("------------------")
print("Style : Hybrid")
print()

for layer in registry["architecture"]["layers"]:
    print("-", layer["name"])

print()
print("Principles")

for p in registry["architecture"]["principles"]:
    print(" •", p)

print()
print("Registry:", OUTPUT)
