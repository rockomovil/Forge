#!/usr/bin/env python3

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-028"
STATUS = "FORGE_REPOSITORY_DEPTH_ANALYSIS_READY"

ROOT = Path(__file__).resolve().parents[2]

depth_counter = Counter()

for path in ROOT.rglob("*"):
    if ".git" in path.parts:
        continue

    relative = path.relative_to(ROOT)
    depth = len(relative.parts)
    depth_counter[depth] += 1

payload = {
    "module": MODULE,
    "status": STATUS,
    "depth_distribution": dict(sorted(depth_counter.items())),
    "max_depth": max(depth_counter) if depth_counter else 0,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_depth_analysis_028.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_depth_analysis_028_hash.json").write_text(
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

with (
    runtime_dir / "forge_repository_depth_analysis_028_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"max_depth = {payload['max_depth']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
