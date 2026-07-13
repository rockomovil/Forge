#!/usr/bin/env python3

from pathlib import Path
import subprocess
import yaml
import sys

# ROOT = repositorio Forge
ROOT = Path(__file__).resolve().parents[3]

MASTER = ROOT / "forge" / "meta" / "master" / "forge_master.yaml"

if not MASTER.exists():
    raise SystemExit(f"MASTER_CATALOG_NOT_FOUND: {MASTER}")

cfg = yaml.safe_load(MASTER.read_text(encoding="utf-8"))

families = cfg.get("families", [])

print()
print("FORGE MASTER BUILDER")
print("--------------------")
print(f"Families : {len(families)}")
print()

for catalog in families:

    catalog_path = ROOT / catalog

    if not catalog_path.exists():
        raise SystemExit(f"CATALOG_NOT_FOUND: {catalog_path}")

    print(f"BUILD -> {catalog}")

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "forge" / "meta" / "forge_meta_builder.py"),
            "--catalog",
            catalog,
            "--resume",
            "--execute"
        ],
        cwd=ROOT,
        check=True
    )

print()
print("MASTER BUILD PASS")
