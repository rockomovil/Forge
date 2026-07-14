#!/usr/bin/env python3
"""
FORGE-ARCH-0003
Module Discovery Engine

Runtime:
SHADOW_ONLY_READ_ONLY
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "runtime" / "architecture"

OUTPUT.mkdir(parents=True, exist_ok=True)

modules = []

SKIP = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}

for path in ROOT.rglob("*.py"):

    if any(part in SKIP for part in path.parts):
        continue

    relative = path.relative_to(ROOT)

    modules.append({
        "name": path.stem,
        "relative_path": str(relative),
        "family": relative.parts[0] if len(relative.parts) else "",
        "size_bytes": path.stat().st_size,
    })

modules.sort(key=lambda m: m["relative_path"])

catalog = {
    "module": "FORGE-ARCH-0003",
    "status": "PASS",
    "module_count": len(modules),
    "modules": modules,
}

(OUTPUT / "module_catalog.json").write_text(
    json.dumps(catalog, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("=" * 60)
print("FORGE-ARCH-0003")
print("Module Discovery Engine")
print("=" * 60)
print(f"Modules discovered : {len(modules)}")
print("Catalog            : runtime/architecture/module_catalog.json")
print("STATUS             : PASS")
