#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

GENERATED = ROOT / "generated"
OUTDIR = GENERATED / "index"

OUTDIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIRS = [
    "python",
    "tests",
    "docs",
    "cli",
    "package",
    "dist",
    "release",
    "validation"
]

entries = []

print()
print("Artifact Index Backend")
print("----------------------")

for dirname in ARTIFACT_DIRS:

    folder = GENERATED / dirname

    if not folder.exists():
        continue

    for path in sorted(folder.rglob("*")):

        if not path.is_file():
            continue

        sha = hashlib.sha256(path.read_bytes()).hexdigest()

        record = {
            "category": dirname,
            "name": path.name,
            "relative_path": str(path.relative_to(ROOT)),
            "size": path.stat().st_size,
            "sha256": sha,
            "indexed": datetime.now(UTC).isoformat()
        }

        entries.append(record)

        print(path.relative_to(GENERATED))

index_file = OUTDIR / "artifact_index.json"

index_file.write_text(
    json.dumps(
        {
            "generated": datetime.now(UTC).isoformat(),
            "artifact_count": len(entries),
            "artifacts": entries
        },
        indent=4
    )
)

ledger = OUTDIR / "artifact_index.jsonl"

with ledger.open("w") as f:
    for entry in entries:
        f.write(json.dumps(entry) + "\n")

summary = OUTDIR / "artifact_index_summary.txt"

summary.write_text(
    "\n".join([
        f"Artifacts : {len(entries)}",
        f"Generated : {datetime.now(UTC).isoformat()}",
        "Status    : OK"
    ])
)

print()
print("Indexed :", len(entries))
print("Output  :", OUTDIR)

print()
print("STATUS : BLD0015_ARTIFACT_INDEX_BACKEND_READY")
