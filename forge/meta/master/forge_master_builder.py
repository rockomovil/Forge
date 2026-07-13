#!/usr/bin/env python3

from pathlib import Path
import subprocess
import yaml
import sys

ROOT = Path(__file__).resolve().parents[2]

MASTER = ROOT / "forge/meta/master/forge_master.yaml"

cfg = yaml.safe_load(MASTER.read_text())

families = cfg["families"]

print()
print("FORGE MASTER BUILDER")
print("--------------------")
print()

print("Families :", len(families))
print()

for catalog in families:

    print("BUILD :", catalog)

    subprocess.run(
        [
            "python3",
            str(ROOT/"forge/meta/forge_meta_builder.py"),
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
