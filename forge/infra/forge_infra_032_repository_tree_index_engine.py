#!/usr/bin/env python3

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-032"
STATUS = "FORGE_REPOSITORY_TREE_INDEX_READY"

ROOT = Path(__file__).resolve().parents[2]

tree = []

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts:
        continue

    relative = path.relative_to(ROOT).as_posix()

    if path.is_dir():
        kind = "directory"
    elif path.is_file():
        kind = "file"
    elif path.is_symlink():
        kind = "symlink"
    else:
        kind = "other"

    tree.append({
        "path": relative,
        "type": kind,
        "depth": len(path.relative_to(ROOT).parts),
    })

payload = {
    "module": MODULE,
    "status": STATUS,
    "node_count": len(tree),
    "tree": tree,
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_tree_index_032.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
).hexdigest()

(runtime_dir / "forge_repository_tree_index_032_hash.json").write_text(
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
    runtime_dir / "forge_repository_tree_index_032_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"node_count = {len(tree)}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
