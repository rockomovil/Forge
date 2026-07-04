#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

INDEX = ROOT / "generated/index/artifact_index.json"
META = ROOT / "generated/metadata/forge_metadata.json"
DEPS = ROOT / "generated/dependencies/dependency_graph.json"

OUT = ROOT / "generated/registry"
OUT.mkdir(parents=True, exist_ok=True)

for required in (INDEX, META, DEPS):
    if not required.exists():
        raise SystemExit(f"ERROR: missing {required.name}")

index = json.loads(INDEX.read_text())
metadata = json.loads(META.read_text())
dependencies = json.loads(DEPS.read_text())

registry = {
    "forge_registry_version": "1.0.0",
    "generated": datetime.now(UTC).isoformat(),
    "artifact_count": index["artifact_count"],
    "category_count": len(metadata["categories"]),
    "dependency_count": dependencies["artifact_count"],
    "metadata_sha256": metadata["metadata_sha256"],
    "dependency_sha256": dependencies["graph_sha256"],
    "artifacts": index["artifacts"]
}

registry["registry_sha256"] = hashlib.sha256(
    json.dumps(registry, sort_keys=True).encode()
).hexdigest()

(REG := OUT / "forge_registry.json").write_text(
    json.dumps(registry, indent=4)
)

with (OUT / "forge_registry.jsonl").open("w") as f:
    for artifact in registry["artifacts"]:
        f.write(json.dumps(artifact) + "\n")

(OUT / "forge_registry_summary.txt").write_text(
f"""FORGE REGISTRY

Artifacts   : {registry['artifact_count']}
Categories  : {registry['category_count']}
Dependencies: {registry['dependency_count']}

Generated   : {registry['generated']}
SHA256      : {registry['registry_sha256']}
"""
)

print()
print("Registry Backend")
print("----------------")

for category in sorted(metadata["categories"]):
    print(f"{category:<12} {metadata['categories'][category]}")

print()
print("Artifacts    :", registry["artifact_count"])
print("Dependencies :", registry["dependency_count"])
print("Output       :", OUT)

print()
print("STATUS : BLD0018_REGISTRY_BACKEND_READY")
