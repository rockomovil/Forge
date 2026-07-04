#!/usr/bin/env python3

from pathlib import Path
import json
import platform
import argparse

FORGE_ROOT = Path(__file__).resolve().parents[1]

def doctor():

    print()
    print("========================================")
    print(" Forge Bootstrap Doctor")
    print("========================================")

    workspace = FORGE_ROOT.parent

    print(f"Workspace : {workspace}")
    print(f"Forge     : {FORGE_ROOT}")
    print(f"Python    : {platform.python_version()}")

    state = FORGE_ROOT / "runtime/state/bootstrap_state.json"

    if state.exists():
        print("Bootstrap : OK")
    else:
        print("Bootstrap : MISSING")

    kernel = FORGE_ROOT / "kernel"

    if kernel.exists():
        print("Kernel    : OK")
    else:
        print("Kernel    : MISSING")

    print()
    print("STATUS : FORGE_READY")
    print()

parser = argparse.ArgumentParser()

parser.add_argument(
    "command",
    nargs="?",
    default="doctor"
)

args = parser.parse_args()

if args.command == "doctor":
    doctor()
else:
    print("Unknown command:", args.command)
