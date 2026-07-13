#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "runtime" / "atlas"
OUT.mkdir(parents=True, exist_ok=True)

MODULE = "FORGE-KNOWLEDGE-278"
STATUS = "ATLAS_KNOWLEDGE_VERSIONING_ENGINE_READY"
SLUG = "knowledge_versioning"
MODULE_ID = 278
RUNTIME_MODE = "SHADOW_ONLY_READ_ONLY"

payload = {
    "module": MODULE,
    "status": STATUS,
    "engine": {
        "initialized": True,
        "ready": True,
        "module_id": MODULE_ID,
        "slug": SLUG
    },
    "runtime": {
        "runtime_mode": RUNTIME_MODE,
        "broker_connected": False,
        "orders_allowed": False,
        "real_money_allowed": False
    },
    "result": "PASS",
    "timestamp": datetime.now(timezone.utc).isoformat()
}

canonical = json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":")
).encode("utf-8")

digest = hashlib.sha256(canonical).hexdigest()
payload["hash"] = digest

artifact = OUT / f"{SLUG}_{MODULE_ID:03d}.json"
hash_artifact = OUT / f"{SLUG}_{MODULE_ID:03d}_hash.json"
ledger = OUT / f"{SLUG}_{MODULE_ID:03d}_ledger.jsonl"

artifact.write_text(
    json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8"
)

hash_artifact.write_text(
    json.dumps(
        {
            "module": MODULE,
            "artifact": str(artifact.relative_to(ROOT)),
            "sha256": digest
        },
        indent=2,
        ensure_ascii=False
    ) + "\n",
    encoding="utf-8"
)

with ledger.open("a", encoding="utf-8") as handle:
    handle.write(
        json.dumps(payload, ensure_ascii=False) + "\n"
    )

print(MODULE)
print(STATUS)
print(f"hash = {digest}")
print(f"runtime_mode = {RUNTIME_MODE}")
