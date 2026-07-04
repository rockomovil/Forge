#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import json

ROOT = Path(__file__).resolve().parents[1]

PARSED = ROOT / "runtime" / "builder" / "parsed_specifications.json"
ARCH   = ROOT / "runtime" / "architecture" / "architecture_registry.json"
GRAPH  = ROOT / "runtime" / "dependencies" / "dependency_graph.json"
OUT    = ROOT / "runtime" / "builder" / "validated_specifications.json"

if not PARSED.exists():
    raise SystemExit("ERROR: parsed_specifications.json missing")

if not ARCH.exists():
    raise SystemExit("ERROR: architecture_registry.json missing")

if not GRAPH.exists():
    raise SystemExit("ERROR: dependency_graph.json missing")

parsed = json.loads(PARSED.read_text())
arch = json.loads(ARCH.read_text())
graph = json.loads(GRAPH.read_text())

known_nodes = {n["id"] for n in graph["nodes"]}

allowed_architectures = {
    arch["architecture"]["style"],
    "Clean",
    "Onion",
    "Hexagonal",
    "Hybrid"
}

validated = {
    "generated_at": datetime.now(UTC).isoformat(),
    "validator": "BLD-0004",
    "specifications": []
}

for spec in parsed["specifications"]:

    checks = {
        "id_present": bool(spec.get("id")),
        "name_present": bool(spec.get("name")),
        "type_present": bool(spec.get("type")),
        "architecture_allowed": spec.get("architecture") in allowed_architectures,
        "dependencies_declared": isinstance(spec.get("dependencies"), list),
        "dependencies_known_or_external": all(
            dep in known_nodes or dep.startswith(("KRN-", "BLD-", "CMD-", "ARC-", "HRM-", "ATL-", "PRJ-", "MOD-"))
            for dep in spec.get("dependencies", [])
        ),
        "no_self_dependency": spec.get("id") not in spec.get("dependencies", []),
    }

    passed = sum(1 for v in checks.values() if v)
    total = len(checks)

    status = "VALID" if passed == total else "INVALID"

    validated["specifications"].append({
        "id": spec["id"],
        "name": spec["name"],
        "status": status,
        "checks": checks,
        "passed": passed,
        "total": total,
        "score": round(passed / total, 6)
    })

OUT.write_text(json.dumps(validated, indent=2, ensure_ascii=False))

print()
print("Architecture Validation")
print("-----------------------")

for item in validated["specifications"]:
    print(
        f'{item["id"]:<12} {item["status"]:<8} '
        f'{item["passed"]}/{item["total"]} score={item["score"]}'
    )

print()
print("Output:", OUT)

invalid = [x for x in validated["specifications"] if x["status"] != "VALID"]

if invalid:
    print()
    print("STATUS : BLD0004_ARCHITECTURE_VALIDATION_FAILED")
    raise SystemExit(1)

print()
print("STATUS : BLD0004_ARCHITECTURE_VALIDATOR_READY")
