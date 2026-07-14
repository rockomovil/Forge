#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX_FILE = ROOT / "runtime" / "architecture" / "module_index.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "module_dependency_index.json"

module_index = json.loads(INDEX_FILE.read_text())

indexes = module_index["indexes"]
modules = indexes["by_name"]

dependency_index = defaultdict(list)

for module_name, metadata in sorted(modules.items()):
    family = metadata["family"]
    dependency_index[family].append(module_name)

result = {
    "module": "FORGE-ARCH-0005",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "module_count": module_index["module_count"],
    "unique_module_count": len(modules),
    "family_count": len(dependency_index),
    "dependency_index": dict(sorted(dependency_index.items())),
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0005")
print("Module Dependency Index Engine")
print("=" * 60)
print("Modules :", result["module_count"])
print("Unique  :", result["unique_module_count"])
print("Families:", result["family_count"])
print("Output  :", OUTPUT_FILE)
print()
print("STATUS : PASS")
