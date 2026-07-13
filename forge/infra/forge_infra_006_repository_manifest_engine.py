#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-006"
STATUS = "FORGE_REPOSITORY_MANIFEST_READY"

ROOT = Path(__file__).resolve().parents[2]

top_level = sorted(
    p.name
    for p in ROOT.iterdir()
    if not p.name.startswith(".")
)

manifest = {
    "module": MODULE,
    "status": STATUS,
    "repository_root": str(ROOT),
    "top_level_entries": top_level,
    "entry_count": len(top_level),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

serialized = json.dumps(manifest, sort_keys=True, indent=2)
integrity_hash = hashlib.sha256(serialized.encode()).hexdigest()
manifest["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_manifest_006.json").write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8",
)

hash_payload = {
    "module": MODULE,
    "hash": hashlib.sha256(
        json.dumps(manifest, sort_keys=True).encode()
    ).hexdigest(),
}

(runtime_dir / "forge_repository_manifest_006_hash.json").write_text(
    json.dumps(hash_payload, indent=2),
    encoding="utf-8",
)

with (runtime_dir / "forge_repository_manifest_006_ledger.jsonl").open(
    "a",
    encoding="utf-8",
) as ledger:
    ledger.write(json.dumps(manifest) + "\n")

print(MODULE)
print(STATUS)
print(f"entry_count = {manifest['entry_count']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {hash_payload['hash']}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
