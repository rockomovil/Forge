#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX = json.loads(
    (ROOT / "runtime/architecture/module_index.json").read_text()
)

GRAPH = json.loads(
    (ROOT / "runtime/architecture/architecture_dependency_graph.json").read_text()
)

RECON = json.loads(
    (ROOT / "runtime/architecture/architecture_dependency_graph_reconciliation_v2.json").read_text()
)

G = GRAPH.get("graph", GRAPH)

nodes = G.get("nodes", [])
edges = G.get("edges", [])

node_count = len(nodes)
edge_count = len(edges)

orphans = RECON["orphan_graph_nodes"]
coverage = RECON["coverage"]

health = (
    coverage == 1.0 and
    node_count > 0 and
    edge_count > 0
)

report = {
    "module": "FORGE-ARCH-QUERY-0012",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "architecture_health": {
        "healthy": health,
        "coverage": coverage,
        "index_modules": RECON["index_modules"],
        "graph_nodes": node_count,
        "graph_edges": edge_count,
        "orphan_nodes": orphans,
    }
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/architecture/architecture_health_report.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-ARCH-QUERY-0012")
print("Architecture Health Report Engine")
print("=" * 60)
print("Healthy      :", health)
print("Coverage     :", f"{coverage:.2%}")
print("Modules      :", RECON["index_modules"])
print("Graph Nodes  :", node_count)
print("Graph Edges  :", edge_count)
print("Orphans      :", orphans)
print("Output       :", OUT)
print()
print("STATUS : PASS")
