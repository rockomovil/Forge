#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

INDEX = ROOT / "generated/index/artifact_index.json"
OUTDIR = ROOT / "generated/dependencies"

OUTDIR.mkdir(parents=True, exist_ok=True)

if not INDEX.exists():
    raise SystemExit("ERROR: Execute BLD-0015 first.")

index = json.loads(INDEX.read_text())

dependencies = []

for artifact in index["artifacts"]:

    rel = artifact["relative_path"]

    if rel.startswith("python/"):
        stage = "python"

    elif rel.startswith("tests/"):
        stage = "tests"

    elif rel.startswith("docs/"):
        stage = "documentation"

    elif rel.startswith("cli/"):
        stage = "cli"

    elif rel.startswith("package/"):
        stage = "package"

    elif rel.startswith("dist/"):
        stage = "distribution"

    elif rel.startswith("release/"):
        stage = "release"

    elif rel.startswith("validation/"):
        stage = "validation"

    else:
        stage = "unknown"

    dependencies.append({
        "artifact": artifact["name"],
        "stage": stage,
        "sha256": artifact["sha256"]
    })

dependency_graph = {
    "generated": datetime.now(UTC).isoformat(),
    "artifact_count": len(dependencies),
    "dependencies": dependencies
}

dependency_graph["graph_sha256"] = hashlib.sha256(
    json.dumps(dependency_graph, sort_keys=True).encode()
).hexdigest()

(OUTDIR / "dependency_graph.json").write_text(
    json.dumps(dependency_graph, indent=4)
)

with (OUTDIR / "dependency_graph.jsonl").open("w") as f:
    for dep in dependencies:
        f.write(json.dumps(dep) + "\n")

with (OUTDIR / "dependency_summary.txt").open("w") as f:
    f.write(f"Dependencies : {len(dependencies)}\n")
    f.write(f"Generated    : {dependency_graph['generated']}\n")
    f.write(f"SHA256       : {dependency_graph['graph_sha256']}\n")

print()
print("Dependency Backend")
print("------------------")

for dep in dependencies:
    print(f"{dep['stage']:<15}{dep['artifact']}")

print()
print("Dependencies :", len(dependencies))
print("Output       :", OUTDIR)

print()
print("STATUS : BLD0017_DEPENDENCY_BACKEND_READY")
