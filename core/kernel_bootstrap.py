#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import json

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "Capability Registry":
        ROOT / "runtime/capabilities/registry.json",

    "Service Registry":
        ROOT / "runtime/services/registry.json",

    "Event Bus":
        ROOT / "runtime/events/events.jsonl",

    "Runtime Context":
        ROOT / "runtime/context/runtime_context.json",

    "Configuration":
        ROOT / "runtime/config/forge_config.json",

    "Workspace":
        ROOT / "runtime/config/workspace.json",

    "Logger":
        ROOT / "runtime/logs/forge.log.jsonl",

    "Dependency Graph":
        ROOT / "runtime/dependencies/dependency_graph.json"
}

ok = 0

print()
print("Forge Kernel Bootstrap")
print("----------------------")
print()

for name, path in FILES.items():

    if path.exists():
        print(f"[ OK ] {name:<22}")
        ok += 1
    else:
        print(f"[FAIL] {name:<22}")

manifest = {
    "kernel_name": "Forge Kernel",
    "kernel_version": "0.1.0",
    "generated_at": datetime.now(UTC).isoformat(),
    "components": ok,
    "expected_components": len(FILES),
    "health": round(ok / len(FILES) * 100, 2),
    "status": "READY" if ok == len(FILES) else "DEGRADED"
}

MANIFEST = ROOT / "runtime/kernel/kernel_manifest.json"

MANIFEST.parent.mkdir(parents=True, exist_ok=True)

MANIFEST.write_text(
    json.dumps(
        manifest,
        indent=2,
        ensure_ascii=False
    )
)

print()
print("--------------------------------------")
print(f'Kernel Health : {manifest["health"]}%')
print(f'Status        : {manifest["status"]}')
print("--------------------------------------")
print()
print("Manifest:")
print(MANIFEST)
