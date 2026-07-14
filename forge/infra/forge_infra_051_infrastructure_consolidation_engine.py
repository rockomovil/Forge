#!/usr/bin/env python3

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-051"
STATUS = "FORGE_INFRASTRUCTURE_CONSOLIDATION_READY"
EXPECTED_MODULES = 50
EXPECTED_RUNTIME_MODE = "SHADOW_ONLY_READ_ONLY"

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "runtime" / "infra"

module_pattern = re.compile(r"FORGE-INFRA-(\d{3})")
modules = {}
errors = []

for path in sorted(RUNTIME_DIR.glob("*.json")):
    if path.name.endswith("_hash.json"):
        continue

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append({
            "path": path.relative_to(ROOT).as_posix(),
            "error": str(error),
        })
        continue

    module = data.get("module") or data.get("infra") or ""
    match = module_pattern.fullmatch(module)

    if not match:
        continue

    number = int(match.group(1))

    if 1 <= number <= EXPECTED_MODULES:
        modules[number] = {
            "module": module,
            "status": data.get("status"),
            "runtime_mode": data.get("runtime_mode"),
            "source": path.relative_to(ROOT).as_posix(),
        }

missing_modules = [
    f"FORGE-INFRA-{number:03d}"
    for number in range(1, EXPECTED_MODULES + 1)
    if number not in modules
]

invalid_runtime_modes = [
    record["module"]
    for record in modules.values()
    if record["runtime_mode"] != EXPECTED_RUNTIME_MODE
]

invalid_statuses = [
    record["module"]
    for record in modules.values()
    if not isinstance(record["status"], str)
    or not record["status"].endswith("_READY")
]

consolidation_valid = (
    len(modules) == EXPECTED_MODULES
    and not missing_modules
    and not invalid_runtime_modes
    and not invalid_statuses
    and not errors
)

payload = {
    "module": MODULE,
    "status": STATUS,
    "expected_modules": EXPECTED_MODULES,
    "modules_discovered": len(modules),
    "missing_modules": missing_modules,
    "invalid_runtime_modes": invalid_runtime_modes,
    "invalid_statuses": invalid_statuses,
    "read_error_count": len(errors),
    "read_errors": errors,
    "consolidation_valid": consolidation_valid,
    "modules": [
        modules[number]
        for number in sorted(modules)
    ],
    "runtime_mode": EXPECTED_RUNTIME_MODE,
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":"),
)

integrity_hash = hashlib.sha256(
    canonical.encode("utf-8")
).hexdigest()

payload["integrity_hash"] = integrity_hash

report_path = RUNTIME_DIR / "forge_infrastructure_consolidation_051.json"
hash_path = RUNTIME_DIR / "forge_infrastructure_consolidation_051_hash.json"
ledger_path = RUNTIME_DIR / "forge_infrastructure_consolidation_051_ledger.jsonl"

report_path.write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()

hash_path.write_text(
    json.dumps(
        {
            "module": MODULE,
            "hash": final_hash,
        },
        indent=2,
        sort_keys=True,
    ) + "\n",
    encoding="utf-8",
)

with ledger_path.open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"expected_modules = {EXPECTED_MODULES}")
print(f"modules_discovered = {len(modules)}")
print(f"missing_module_count = {len(missing_modules)}")
print(f"invalid_runtime_mode_count = {len(invalid_runtime_modes)}")
print(f"invalid_status_count = {len(invalid_statuses)}")
print(f"read_error_count = {len(errors)}")
print(f"consolidation_valid = {consolidation_valid}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print(f"runtime_mode = {EXPECTED_RUNTIME_MODE}")
print(f"{MODULE} VERIFIED")

if not consolidation_valid:
    raise SystemExit(1)
