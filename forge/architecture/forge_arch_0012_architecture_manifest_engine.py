#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX_FILE = ROOT / "runtime" / "architecture" / "module_index.json"
GRAPH_FILE = ROOT / "runtime" / "architecture" / "architecture_dependency_graph.json"
METRICS_FILE = ROOT / "runtime" / "architecture" / "architecture_metrics.json"
LOCK_FILE = ROOT / "runtime" / "architecture" / "architecture_lock.json"

OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_manifest.json"

index = json.loads(INDEX_FILE.read_text())
graph = json.loads(GRAPH_FILE.read_text())
metrics = json.loads(METRICS_FILE.read_text())
lock = json.loads(LOCK_FILE.read_text())

manifest = {
    "module": "FORGE-ARCH-0012",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),
    "artifacts": {
        "module_index": INDEX_FILE.name,
        "dependency_graph": GRAPH_FILE.name,
        "metrics": METRICS_FILE.name,
        "lock": LOCK_FILE.name,
    },
    "summary": {
        "module_count": index["module_count"],
        "unique_module_count": metrics["unique_module_count"],
        "family_count": index["family_count"],
        "node_count": graph["node_count"],
        "edge_count": graph["edge_count"],
        "locked": lock["architecture_locked"],
        "immutable": lock["immutable"],
    },
}

manifest["hash"] = hashlib.sha256(
    json.dumps(manifest, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(manifest, indent=2))

print("=" * 60)
print("FORGE-ARCH-0012")
print("Architecture Manifest Engine")
print("=" * 60)
print("Modules :", manifest["summary"]["module_count"])
print("Families:", manifest["summary"]["family_count"])
print("Nodes   :", manifest["summary"]["node_count"])
print("Edges   :", manifest["summary"]["edge_count"])
print("Locked  :", manifest["summary"]["locked"])
print("Output  :", OUTPUT_FILE)
print()
print("STATUS : PASS")
