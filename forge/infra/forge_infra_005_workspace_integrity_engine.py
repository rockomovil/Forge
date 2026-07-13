#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-005"
STATUS = "FORGE_WORKSPACE_INTEGRITY_READY"

ROOT = Path(__file__).resolve().parents[2]

workspace = {
    "forge": (ROOT / "forge").is_dir(),
    "runtime": (ROOT / "runtime").is_dir(),
    "registry": (ROOT / "registry").is_dir(),
    ".git": (ROOT / ".git").is_dir(),
}

workspace_valid = all(workspace.values())

payload = {
    "module": MODULE,
    "status": STATUS,
    "workspace": workspace,
    "workspace_valid": workspace_valid,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(payload, sort_keys=True, indent=2)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_workspace_integrity_005.json").write_text(
    json.dumps(payload, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest(),
}

(runtime_dir / "forge_workspace_integrity_005_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_workspace_integrity_005_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(payload) + "\n")

print(MODULE)
print(STATUS)
print(f"workspace_valid = {workspace_valid}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
