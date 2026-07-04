#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def count_capabilities():
    f = ROOT / "runtime/capabilities/registry.json"
    if not f.exists():
        return 0
    return len(json.loads(f.read_text()))

def count_services():
    f = ROOT / "runtime/services/registry.json"
    if not f.exists():
        return 0
    return len(json.loads(f.read_text()))

def kernel_health():

    f = ROOT / "runtime/kernel/kernel_manifest.json"

    if not f.exists():
        return "UNKNOWN"

    return json.loads(f.read_text())["health"]

print()
print("=========================================================")
print("            FORGE ENGINEERING OPERATING SYSTEM")
print("=========================================================")
print()

print(f"Kernel Health ......... {kernel_health()}%")
print(f"Capabilities .......... {count_capabilities()}")
print(f"Services .............. {count_services()}")
print()

print("Builder ............... OFF")
print("Hermes ............... OFF")
print("Atlas ................ OFF")
print("Projects ............. 1")
print()

print("=========================================================")
print(" 1. Kernel")
print(" 2. Builder")
print(" 3. Projects")
print(" 4. Hermes")
print(" 5. Atlas")
print(" 6. Health")
print(" 7. Exit")
print("=========================================================")
print()
print("Stage : Command Center Bootstrap")
