#!/usr/bin/env python3

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MODULE = "FORGE-INFRA-025"
STATUS = "FORGE_REPOSITORY_FILE_CLASSIFICATION_READY"

ROOT = Path(__file__).resolve().parents[2]

categories = Counter()

TEXT_EXTENSIONS = {
    ".py", ".json", ".jsonl", ".md", ".txt", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".sh", ".bash", ".ps1",
    ".csv", ".xml", ".html", ".css", ".js", ".ts", ".sql"
}

for path in sorted(ROOT.rglob("*")):
    if ".git" in path.parts or not path.is_file():
        continue

    ext = path.suffix.lower()

    if ext in TEXT_EXTENSIONS:
        categories["text"] += 1
    elif ext == "":
        categories["no_extension"] += 1
    else:
        categories["other"] += 1

payload = {
    "module": MODULE,
    "status": STATUS,
    "classification": dict(categories),
    "total_files": sum(categories.values()),
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
integrity_hash = hashlib.sha256(canonical.encode()).hexdigest()
payload["integrity_hash"] = integrity_hash

runtime_dir = ROOT / "runtime" / "infra"
runtime_dir.mkdir(parents=True, exist_ok=True)

(runtime_dir / "forge_repository_file_classification_025.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

final_hash = hashlib.sha256(
    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

(runtime_dir / "forge_repository_file_classification_025_hash.json").write_text(
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
    runtime_dir / "forge_repository_file_classification_025_ledger.jsonl"
).open("a", encoding="utf-8") as ledger:
    ledger.write(json.dumps(payload, sort_keys=True) + "\n")

print(MODULE)
print(STATUS)
print(f"text = {categories['text']}")
print(f"other = {categories['other']}")
print(f"no_extension = {categories['no_extension']}")
print(f"total_files = {payload['total_files']}")
print(f"integrity_hash = {integrity_hash}")
print(f"hash = {final_hash}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
print(f"{MODULE} VERIFIED")
