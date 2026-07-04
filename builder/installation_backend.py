#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]

REGISTRY = ROOT / "generated/registry/forge_registry.json"
INSTALL_DIR = ROOT / "generated/install"

INSTALL_DIR.mkdir(parents=True, exist_ok=True)

if not REGISTRY.exists():
    raise SystemExit("ERROR: Execute BLD-0018 first.")

registry = json.loads(REGISTRY.read_text())

installed = []
installed_names = set()

print()
print("Installation Backend")
print("--------------------")

for artifact in registry["artifacts"]:

    # Solo instalar artefactos publicados
    if artifact["category"] != "release":
        continue

    # Instalar únicamente paquetes .tar.gz
    if Path(artifact["name"]).suffixes != [".tar", ".gz"]:
        continue

    source = ROOT / artifact["relative_path"]

    if not source.exists():
        continue

    # Evitar duplicados
    if source.name in installed_names:
        continue

    installed_names.add(source.name)

    target = INSTALL_DIR / source.name

    shutil.copy2(source, target)

    sha256 = hashlib.sha256(target.read_bytes()).hexdigest()

    installed.append(
        {
            "artifact": target.name,
            "relative_path": artifact["relative_path"],
            "size": target.stat().st_size,
            "sha256": sha256,
            "installed": datetime.now(UTC).isoformat(),
        }
    )

    print(target.name)

manifest = {
    "generated": datetime.now(UTC).isoformat(),
    "installed_count": len(installed),
    "artifacts": installed,
}

manifest["installation_sha256"] = hashlib.sha256(
    json.dumps(manifest, sort_keys=True).encode()
).hexdigest()

(INSTALL_DIR / "installation_manifest.json").write_text(
    json.dumps(manifest, indent=4)
)

with (INSTALL_DIR / "installation_manifest.jsonl").open("w") as f:
    for item in installed:
        f.write(json.dumps(item) + "\n")

(INSTALL_DIR / "installation_summary.txt").write_text(
f"""FORGE INSTALLATION

Installed : {manifest['installed_count']}
Generated : {manifest['generated']}
SHA256    : {manifest['installation_sha256']}
"""
)

print()
print("Installed :", manifest["installed_count"])
print("Output    :", INSTALL_DIR)

print()
print("STATUS : BLD0019_INSTALLATION_BACKEND_READY")
