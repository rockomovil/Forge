#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import shutil

ROOT = Path(__file__).resolve().parents[1]

SRC = ROOT / "generated/python"
OUT = ROOT / "generated/package"

OUT.mkdir(parents=True, exist_ok=True)

generated = 0

for module in sorted(SRC.glob("*.py")):

    pkg = OUT / module.stem
    pkg.mkdir(parents=True, exist_ok=True)

    shutil.copy2(module, pkg / module.name)

    (pkg / "__init__.py").write_text(
        f'"""Package {module.stem}"""\n'
    )

    (pkg / "VERSION").write_text("1.0.0\n")

    (pkg / "MANIFEST.json").write_text(
f'''{{
  "module":"{module.stem}",
  "generated":"{datetime.now(UTC).isoformat()}",
  "version":"1.0.0"
}}
'''
    )

    generated += 1

print()
print("Package Backend")
print("----------------")

for pkg in sorted(OUT.iterdir()):
    if pkg.is_dir():
        print(pkg.name)

print()
print("Generated :", generated)
print("Output    :", OUT)

print()
print("STATUS : BLD0011_PACKAGE_BACKEND_READY")
