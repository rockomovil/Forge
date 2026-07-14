#!/usr/bin/env python3
"""
FORGE-ARCH-0001
Enterprise Architecture Audit Engine

FORGE-ARCH-0002
Repository Discovery Engine - Initial Version
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "runtime" / "architecture"

FAMILIES = [
    "forge",
    "runtime",
    "registry",
    "galaxy",
    "builder",
    "services",
    "tests",
    "docs",
    "scripts",
]

OUTPUT.mkdir(parents=True, exist_ok=True)

inventory = {
    "module": "FORGE-ARCH-0001",
    "status": "PASS",
    "root": str(ROOT),
    "directories": 0,
    "files": 0,
    "python_files": 0,
    "families": {},
}

for family in FAMILIES:
    inventory["families"][family] = {
        "exists": False,
        "directories": 0,
        "files": 0,
        "python_files": 0,
    }

for item in ROOT.rglob("*"):

    if ".git" in item.parts:
        continue

    relative = item.relative_to(ROOT)
    parts = relative.parts

    family = parts[0] if parts else None

    if item.is_dir():
        inventory["directories"] += 1

        if family in inventory["families"]:
            inventory["families"][family]["exists"] = True
            inventory["families"][family]["directories"] += 1

    else:
        inventory["files"] += 1

        if item.suffix == ".py":
            inventory["python_files"] += 1

        if family in inventory["families"]:
            inventory["families"][family]["exists"] = True
            inventory["families"][family]["files"] += 1

            if item.suffix == ".py":
                inventory["families"][family]["python_files"] += 1

(OUTPUT / "enterprise_inventory.json").write_text(
    json.dumps(inventory, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

report = {
    "module": "FORGE-ARCH-0002",
    "status": "PASS",
    "families_discovered": sum(
        1 for v in inventory["families"].values() if v["exists"]
    ),
    "directories": inventory["directories"],
    "files": inventory["files"],
    "python_files": inventory["python_files"],
}

(OUTPUT / "engineering_report.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("=" * 60)
print("FORGE-ARCH-0002")
print("Repository Discovery Engine")
print("=" * 60)
print()

for name, data in inventory["families"].items():
    if data["exists"]:
        print(
            f"{name:10} "
            f"dirs={data['directories']:4} "
            f"files={data['files']:5} "
            f"py={data['python_files']:4}"
        )

print()
print(f"Directories : {inventory['directories']}")
print(f"Files       : {inventory['files']}")
print(f"Python      : {inventory['python_files']}")
print()
print("STATUS : PASS")
