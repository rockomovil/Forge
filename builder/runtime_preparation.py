#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

INSTALL = ROOT / "generated/install/installation_manifest.json"
REGISTRY = ROOT / "generated/registry/forge_registry.json"
METADATA = ROOT / "generated/metadata/forge_metadata.json"
INDEX = ROOT / "generated/index/artifact_index.json"

OUT = ROOT / "runtime"
OUT.mkdir(parents=True, exist_ok=True)

required = {
    "installation": INSTALL,
    "registry": REGISTRY,
    "metadata": METADATA,
    "artifact_index": INDEX,
}

checks = []
runtime_ready = True

print()
print("Runtime Preparation")
print("-------------------")

for name, file in required.items():

    ok = file.exists()

    checks.append(
        {
            "component": name,
            "path": str(file.relative_to(ROOT)),
            "exists": ok
        }
    )

    print(f"{name:<18} {'OK' if ok else 'MISSING'}")

    if not ok:
        runtime_ready = False

state = {
    "generated": datetime.now(UTC).isoformat(),
    "runtime_ready": runtime_ready,
    "execution_started": False,
    "modules_loaded": 0,
    "plugins_loaded": 0,
    "scheduler_started": False,
    "event_bus_started": False,
}

manifest = {
    "generated": datetime.now(UTC).isoformat(),
    "runtime_version": "1.0.0",
    "runtime_ready": runtime_ready,
    "checks": checks,
}

environment = {
    "workspace": str(ROOT),
    "python": "3.12",
    "phase": "RUNTIME",
    "stage": "PREPARATION"
}

report = {
    "generated": datetime.now(UTC).isoformat(),
    "passed": sum(c["exists"] for c in checks),
    "failed": sum(not c["exists"] for c in checks),
    "runtime_ready": runtime_ready,
}

ledger = []

for c in checks:
    ledger.append({
        "timestamp": datetime.now(UTC).isoformat(),
        **c
    })

manifest["sha256"] = hashlib.sha256(
    json.dumps(manifest, sort_keys=True).encode()
).hexdigest()

(OUT / "runtime_state.json").write_text(
    json.dumps(state, indent=4)
)

(OUT / "runtime_manifest.json").write_text(
    json.dumps(manifest, indent=4)
)

(OUT / "runtime_environment.json").write_text(
    json.dumps(environment, indent=4)
)

(OUT / "runtime_report.json").write_text(
    json.dumps(report, indent=4)
)

with (OUT / "runtime_ledger.jsonl").open("w") as f:
    for item in ledger:
        f.write(json.dumps(item) + "\n")

(OUT / "runtime_summary.txt").write_text(
f"""FORGE RUNTIME

Runtime Ready : {'YES' if runtime_ready else 'NO'}

Checks Passed : {report['passed']}
Checks Failed : {report['failed']}

Generated     : {manifest['generated']}
Version       : {manifest['runtime_version']}
"""
)

print()

print("Runtime Ready :", "YES" if runtime_ready else "NO")
print("Output        :", OUT)

print()
print("STATUS : RT0001_RUNTIME_PREPARATION_READY")
