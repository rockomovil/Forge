#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    ("Capability Registry", ROOT / "runtime/capabilities/registry.json"),
    ("Service Registry", ROOT / "runtime/services/registry.json"),
    ("Event Bus", ROOT / "runtime/events/events.jsonl"),
    ("Runtime Context", ROOT / "runtime/context/runtime_context.json"),
    ("Configuration", ROOT / "runtime/config/forge_config.json"),
    ("Workspace", ROOT / "runtime/config/workspace.json"),
    ("Kernel Logger", ROOT / "runtime/logs/forge.log.jsonl"),
]

ok = 0

print()
print("========================================")
print(" Forge Kernel Health Monitor")
print("========================================")
print()

for name, path in CHECKS:

    if path.exists():
        print(f"[ OK ] {name:<24} {path}")
        ok += 1
    else:
        print(f"[FAIL] {name:<24} {path}")

health = round((ok / len(CHECKS)) * 100, 2)

report = {
    "health_percent": health,
    "checks_total": len(CHECKS),
    "checks_passed": ok,
    "checks_failed": len(CHECKS) - ok,
    "status": "HEALTHY" if ok == len(CHECKS) else "DEGRADED"
}

health_file = ROOT / "runtime" / "health.json"
health_file.write_text(
    json.dumps(report, indent=2, ensure_ascii=False)
)

print()
print("----------------------------------------")
print(f"Kernel Health : {health}%")
print(f"Checks Passed : {ok}/{len(CHECKS)}")
print(f"Status        : {report['status']}")
print("----------------------------------------")
print()
print("Health report:")
print(health_file)
