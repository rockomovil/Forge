#!/usr/bin/env python3
"""
FORGE-ARCH-0004
Module Index Engine

Builds searchable indexes from module_catalog.json

Runtime:
SHADOW_ONLY_READ_ONLY
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RUNTIME = ROOT / "runtime" / "architecture"

CATALOG = RUNTIME / "module_catalog.json"

INDEX = RUNTIME / "module_index.json"

if not CATALOG.exists():
    raise SystemExit(
        "ERROR: runtime/architecture/module_catalog.json not found.\n"
        "Run FORGE-ARCH-0003 first."
    )

catalog = json.loads(
    CATALOG.read_text(encoding="utf-8")
)

modules = catalog["modules"]

by_family = defaultdict(list)
by_prefix = defaultdict(list)
by_name = {}

for module in modules:

    family = module["family"]

    name = module["name"]

    prefix = name.split("_")[0].upper()

    entry = {
        "name": name,
        "path": module["relative_path"],
    }

    by_family[family].append(entry)

    by_prefix[prefix].append(entry)

    by_name[name] = module

index = {
    "module": "FORGE-ARCH-0004",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "module_count": len(modules),
    "family_count": len(by_family),
    "prefix_count": len(by_prefix),
    "indexes": {
        "by_family": dict(sorted(by_family.items())),
        "by_prefix": dict(sorted(by_prefix.items())),
        "by_name": by_name,
    },
}

INDEX.write_text(
    json.dumps(
        index,
        indent=2,
        ensure_ascii=False,
        sort_keys=True,
    ),
    encoding="utf-8",
)

print("=" * 60)
print("FORGE-ARCH-0004")
print("Module Index Engine")
print("=" * 60)
print(f"Modules : {len(modules)}")
print(f"Families: {len(by_family)}")
print(f"Prefixes: {len(by_prefix)}")
print(f"Output  : {INDEX}")
print()
print("STATUS : PASS")
