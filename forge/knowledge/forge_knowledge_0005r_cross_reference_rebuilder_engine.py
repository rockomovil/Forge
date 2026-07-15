#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
from collections import defaultdict
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

GRAPH = json.loads(
    (ROOT / "runtime/architecture/architecture_dependency_graph_real.json").read_text()
)

INDEX = json.loads(
    (ROOT / "runtime/knowledge/knowledge_index.json").read_text()
)

modules = sorted(INDEX["indexes"]["by_name"].keys())

xref = {}

for m in modules:
    xref[m] = {
        "depends_on": [],
        "referenced_by": [],
        "same_family": [],
        "family": None
    }

#
# families
#

for family, mods in INDEX["indexes"]["by_family"].items():

    for m in mods:

        if m not in xref:
            continue

        xref[m]["family"] = family

        xref[m]["same_family"] = sorted(
            [
                x for x in mods
                if x != m
            ]
        )

#
# graph dependencies
#

for edge in GRAPH["edges"]:

    if edge["relation"] != "depends_on":
        continue

    src = edge["from"].replace("module::", "")
    dst = edge["to"].replace("module::", "")

    if src not in xref or dst not in xref:
        continue

    xref[src]["depends_on"].append(dst)
    xref[dst]["referenced_by"].append(src)

#
# normalize
#

for m in xref:

    xref[m]["depends_on"] = sorted(
        set(xref[m]["depends_on"])
    )

    xref[m]["referenced_by"] = sorted(
        set(xref[m]["referenced_by"])
    )

report = {
    "module": "FORGE-KNOWLEDGE-0005R",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "generated_at": datetime.now(UTC).isoformat(),

    "cross_references": xref,

    "modules": len(xref),

    "dependency_edges": sum(
        len(v["depends_on"])
        for v in xref.values()
    ),

    "reverse_edges": sum(
        len(v["referenced_by"])
        for v in xref.values()
    ),

    "source_graph_hash": GRAPH["hash"]
}

report["hash"] = hashlib.sha256(
    json.dumps(report, sort_keys=True).encode()
).hexdigest()

OUT = ROOT / "runtime/knowledge/knowledge_cross_reference.json"

OUT.write_text(
    json.dumps(report, indent=2)
)

print("=" * 60)
print("FORGE-KNOWLEDGE-0005R")
print("Cross Reference Rebuilder Engine")
print("=" * 60)
print("Modules          :", report["modules"])
print("Dependency Edges :", report["dependency_edges"])
print("Reverse Edges    :", report["reverse_edges"])
print("Output           :", OUT)
print()
print("STATUS : PASS")
