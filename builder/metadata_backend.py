#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

INDEX = ROOT / "generated/index/artifact_index.json"
OUTDIR = ROOT / "generated/metadata"

OUTDIR.mkdir(parents=True, exist_ok=True)

if not INDEX.exists():
    raise SystemExit("ERROR: artifact_index.json missing. Execute BLD-0015 first.")

index = json.loads(INDEX.read_text())

artifacts = index["artifacts"]

categories = {}

for item in artifacts:
    categories[item["category"]] = categories.get(item["category"], 0) + 1

payload = {
    "forge_version": "1.0.0",
    "generated": datetime.now(UTC).isoformat(),
    "artifact_count": len(artifacts),
    "categories": categories,
    "index_file": str(INDEX.relative_to(ROOT))
}

payload["metadata_sha256"] = hashlib.sha256(
    json.dumps(payload, sort_keys=True).encode()
).hexdigest()

metadata = OUTDIR / "forge_metadata.json"
metadata.write_text(json.dumps(payload, indent=4))

ledger = OUTDIR / "forge_metadata_ledger.jsonl"

with ledger.open("w") as f:
    f.write(json.dumps(payload) + "\n")

summary = OUTDIR / "forge_metadata_summary.txt"
summary.write_text(
    "\n".join([
        "FORGE METADATA",
        f"Artifacts : {payload['artifact_count']}",
        f"Categories: {len(categories)}",
        f"Generated : {payload['generated']}",
        f"SHA256    : {payload['metadata_sha256']}"
    ])
)

print()
print("Metadata Backend")
print("----------------")

for category in sorted(categories):
    print(f"{category:<12} {categories[category]}")

print()
print("Artifacts :", payload["artifact_count"])
print("Categories:", len(categories))
print("Output    :", OUTDIR)

print()
print("STATUS : BLD0016_METADATA_BACKEND_READY")
