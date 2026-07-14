#!/usr/bin/env python3

from pathlib import Path
from collections import deque
from datetime import datetime, UTC
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/architecture/architecture_dependency_graph.json").read_text()
)

INDEX = json.loads(
    (ROOT / "runtime/architecture/module_index.json").read_text()
)

G = GRAPH.get("graph", GRAPH)
edges = G.get("edges", [])

reverse = {}

def canon(x):
    if isinstance(x, dict):
        x = x.get("id") or x.get("name") or x.get("module")

    if not isinstance(x, str):
        return None

    if "::" in x:
        x = x.split("::", 1)[1]

    return x

for e in edges:

    src = canon(e.get("from") or e.get("source"))
    dst = canon(e.get("to") or e.get("target"))

    if src and dst:
        reverse.setdefault(dst, set()).add(src)

parser = argparse.ArgumentParser()
parser.add_argument("module")
args = parser.parse_args()

root = canon(args.module)

visited = {root}
queue = deque([root])

validation_plan = []

while queue:

    node = queue.popleft()

    for parent in sorted(reverse.get(node, [])):
        if parent not in visited:
            visited.add(parent)
            queue.append(parent)
            validation_plan.append(parent)

report = {
    "module": "FORGE-BUILD-0002",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "target_module": root,
    "validation_sequence": validation_plan,
    "validation_count": len(validation_plan),
    "index_module_count": INDEX["module_count"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/build/validation_plan.json"
OUT.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-BUILD-0002")
print("Validation Planner Engine")
print("=" * 60)
print("Target      :", root)
print("Validations :", len(validation_plan))
print("Output      :", OUT)
print()
print("STATUS : PASS")
