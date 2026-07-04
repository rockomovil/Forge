#!/usr/bin/env python3
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()

IN_DIR = ROOT / "architecture_registry"
OUT_DIR = ROOT / "architecture_graph"

INPUT = IN_DIR / "architecture_registry.json"

GRAPH_JSON = OUT_DIR / "architecture_dependency_graph.json"
SCHEMA_JSON = OUT_DIR / "architecture_dependency_graph.schema.json"
INDEX_JSON = OUT_DIR / "architecture_dependency_index.json"
TOPO_JSON = OUT_DIR / "architecture_topological_order.json"
MANIFEST_JSON = OUT_DIR / "architecture_graph_manifest.json"
LEDGER_JSONL = OUT_DIR / "architecture_graph_ledger.jsonl"
SUMMARY_TXT = OUT_DIR / "architecture_graph_summary.txt"
VERSION_JSON = OUT_DIR / "architecture_graph_version.json"

STATUS = "ARC0003_ARCHITECTURE_DEPENDENCY_GRAPH_READY"

def sha256_obj(obj):
    data = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def load_json(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing canonical input: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def collect_components(registry):
    candidates = []

    for key in ("components", "registry", "architecture_components", "items", "nodes"):
        value = registry.get(key)
        if isinstance(value, list):
            candidates = value
            break
        if isinstance(value, dict):
            candidates = list(value.values())
            break

    if not candidates:
        candidates = [
            {
                "id": "architecture_root",
                "name": "Architecture Root",
                "type": "root",
                "depends_on": []
            }
        ]

    components = {}
    for i, item in enumerate(candidates, start=1):
        if not isinstance(item, dict):
            continue

        cid = (
            item.get("id")
            or item.get("component_id")
            or item.get("name")
            or f"component_{i:04d}"
        )

        cid = str(cid)

        deps = (
            item.get("depends_on")
            or item.get("dependencies")
            or item.get("requires")
            or []
        )

        if isinstance(deps, str):
            deps = [deps]
        if not isinstance(deps, list):
            deps = []

        components[cid] = {
            "id": cid,
            "name": item.get("name", cid),
            "type": item.get("type", "component"),
            "depends_on": [str(d) for d in deps],
            "source": item
        }

    return components

def validate_dependencies(components):
    missing = []
    for cid, comp in components.items():
        for dep in comp["depends_on"]:
            if dep not in components:
                missing.append({"component": cid, "missing_dependency": dep})
    return missing

def topological_sort(components):
    graph = {cid: set(comp["depends_on"]) for cid, comp in components.items()}
    result = []

    while graph:
        ready = sorted([node for node, deps in graph.items() if not deps])
        if not ready:
            return None, sorted(graph.keys())

        for node in ready:
            result.append(node)
            graph.pop(node)
            for deps in graph.values():
                deps.discard(node)

    return result, []

def main():
    print("======================================================")
    print(" FORGE")
    print(" ARC-0003 - ARCHITECTURE DEPENDENCY GRAPH")
    print("======================================================")
    print()
    print("Running Architecture Dependency Graph...")
    print()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    registry = load_json(INPUT)
    input_hash = sha256_obj(registry)

    components = collect_components(registry)
    missing = validate_dependencies(components)
    topo, cycles = topological_sort(components)

    all_checks_passed = not missing and not cycles and topo is not None

    nodes = [
        {
            "id": cid,
            "name": comp["name"],
            "type": comp["type"]
        }
        for cid, comp in sorted(components.items())
    ]

    edges = []
    for cid, comp in sorted(components.items()):
        for dep in comp["depends_on"]:
            edges.append({
                "from": dep,
                "to": cid,
                "relation": "dependency"
            })

    graph = {
        "module": "ARC-0003",
        "name": "Architecture Dependency Graph",
        "status": STATUS if all_checks_passed else "ARC0003_ARCHITECTURE_DEPENDENCY_GRAPH_FAILED",
        "canonical_input": str(INPUT),
        "canonical_output": str(GRAPH_JSON),
        "input_hash": input_hash,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "cycle_count": len(cycles),
        "missing_dependency_count": len(missing),
        "all_checks_passed": all_checks_passed,
        "nodes": nodes,
        "edges": edges,
        "missing_dependencies": missing,
        "cycles": cycles,
        "topological_order": topo or [],
        "runtime_mode": "SHADOW_ONLY_READ_ONLY",
        "mutation_allowed": False,
        "delete_allowed": False,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

    graph["graph_hash"] = sha256_obj(graph)

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Forge ARC-0003 Architecture Dependency Graph",
        "type": "object",
        "required": [
            "module",
            "status",
            "canonical_input",
            "canonical_output",
            "node_count",
            "edge_count",
            "all_checks_passed",
            "nodes",
            "edges",
            "topological_order",
            "graph_hash"
        ],
        "properties": {
            "module": {"const": "ARC-0003"},
            "status": {"type": "string"},
            "node_count": {"type": "integer"},
            "edge_count": {"type": "integer"},
            "all_checks_passed": {"type": "boolean"},
            "nodes": {"type": "array"},
            "edges": {"type": "array"},
            "topological_order": {"type": "array"},
            "graph_hash": {"type": "string"}
        }
    }

    index = {
        "module": "ARC-0003",
        "index_name": "architecture_dependency_index",
        "component_count": len(nodes),
        "dependency_count": len(edges),
        "components": {node["id"]: node for node in nodes},
        "dependencies": edges,
        "hash": sha256_obj({"nodes": nodes, "edges": edges})
    }

    topo_obj = {
        "module": "ARC-0003",
        "topological_order": topo or [],
        "count": len(topo or []),
        "valid": all_checks_passed,
        "hash": sha256_obj(topo or [])
    }

    version = {
        "module": "ARC-0003",
        "version": "1.0.0",
        "status": STATUS if all_checks_passed else "FAILED",
        "canonical_input_hash": input_hash,
        "canonical_output_hash": graph["graph_hash"]
    }

    manifest = {
        "module": "ARC-0003",
        "name": "Architecture Dependency Graph",
        "status": STATUS if all_checks_passed else "FAILED",
        "generated_files": [
            GRAPH_JSON.name,
            SCHEMA_JSON.name,
            INDEX_JSON.name,
            TOPO_JSON.name,
            MANIFEST_JSON.name,
            LEDGER_JSONL.name,
            SUMMARY_TXT.name,
            VERSION_JSON.name
        ],
        "canonical_input": str(INPUT),
        "canonical_output": str(GRAPH_JSON),
        "all_checks_passed": all_checks_passed,
        "hash": sha256_obj(graph)
    }

    write_json(GRAPH_JSON, graph)
    write_json(SCHEMA_JSON, schema)
    write_json(INDEX_JSON, index)
    write_json(TOPO_JSON, topo_obj)
    write_json(MANIFEST_JSON, manifest)
    write_json(VERSION_JSON, version)

    ledger_entry = {
        "module": "ARC-0003",
        "status": manifest["status"],
        "canonical_input": str(INPUT),
        "canonical_output": str(GRAPH_JSON),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "all_checks_passed": all_checks_passed,
        "hash": manifest["hash"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    LEDGER_JSONL.write_text(json.dumps(ledger_entry, sort_keys=True) + "\n", encoding="utf-8")

    SUMMARY_TXT.write_text(
        "\n".join([
            "Architecture Dependency Graph",
            "-----------------------------",
            f"nodes               {len(nodes)}",
            f"edges               {len(edges)}",
            f"missing_dependencies {len(missing)}",
            f"cycles              {len(cycles)}",
            f"all_checks_passed   {all_checks_passed}",
            f"status              {manifest['status']}",
            ""
        ]),
        encoding="utf-8"
    )

    print("Architecture Dependency Graph")
    print("-----------------------------")
    for file in manifest["generated_files"]:
        print(file)
    print()
    print(f"Generated : {len(manifest['generated_files'])}")
    print(f"Output    : {OUT_DIR}")
    print()

    if not all_checks_passed:
        print("STATUS : ARC0003_ARCHITECTURE_DEPENDENCY_GRAPH_FAILED")
        raise SystemExit(1)

    print(f"STATUS : {STATUS}")
    print()
    print(f"STATUS : {STATUS}")

if __name__ == "__main__":
    main()
