#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

OUT = ROOT / "architecture"
OUT.mkdir(parents=True, exist_ok=True)

generated = datetime.now(UTC).isoformat()

charter = """# FORGE Architecture Charter

Version: 1.0.0

## Vision

Forge is a deterministic engineering framework.

## Principles

1. Single Canonical Artifact
2. Immutable Pipeline
3. Single Responsibility
4. Fixed Module Structure
5. Deterministic Execution
6. Idempotency
7. Read Only Inputs
8. Append Only Outputs
9. Full Traceability
10. Self Validation
11. Schema First
12. Every Phase has exactly one Manifest

## Module Contract

INPUT
VALIDATION
PROCESS
OUTPUT
SUMMARY
LEDGER
STATUS

## Official Phases

Architecture
Build
Runtime
Deploy
Audit
Developer
"""

architecture = {
    "framework": "Forge",
    "architecture_version": "1.0.0",
    "generated": generated,
    "phase": "ARCHITECTURE",
    "status": "FOUNDATIONAL",
    "principles": 12,
    "phases": [
        "Architecture",
        "Build",
        "Runtime",
        "Deploy",
        "Audit",
        "Developer"
    ]
}

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Forge Architecture",
    "type": "object",
    "required": [
        "framework",
        "architecture_version",
        "phase",
        "status"
    ]
}

version = {
    "major": 1,
    "minor": 0,
    "patch": 0,
    "codename": "FOUNDATION"
}

(OUT / "architecture_charter.md").write_text(charter)

(OUT / "architecture.json").write_text(
    json.dumps(architecture, indent=4)
)

(OUT / "architecture.schema.json").write_text(
    json.dumps(schema, indent=4)
)

(OUT / "architecture_version.json").write_text(
    json.dumps(version, indent=4)
)

summary = f"""FORGE ARCHITECTURE

Version : {architecture['architecture_version']}

Status  : {architecture['status']}

Principles : {architecture['principles']}

Generated : {generated}
"""

(OUT / "architecture_summary.txt").write_text(summary)

ledger_entry = {
    "timestamp": generated,
    "module": "ARC-0001",
    "action": "CREATE_ARCHITECTURE_CHARTER",
    "version": architecture["architecture_version"]
}

with (OUT / "architecture_ledger.jsonl").open("w") as f:
    f.write(json.dumps(ledger_entry) + "\n")

manifest = {
    "generated": generated,
    "module": "ARC-0001",
    "artifact_count": 6,
    "status": "FOUNDATIONAL"
}

manifest["sha256"] = hashlib.sha256(
    json.dumps(manifest, sort_keys=True).encode()
).hexdigest()

(OUT / "architecture_manifest.json").write_text(
    json.dumps(manifest, indent=4)
)

print()
print("Architecture Charter")
print("--------------------")

for file in sorted(OUT.iterdir()):
    print(file.name)

print()
print("Generated :", len(list(OUT.iterdir())))
print("Output    :", OUT)

print()
print("STATUS : ARC0001_ARCHITECTURE_CHARTER_READY")
