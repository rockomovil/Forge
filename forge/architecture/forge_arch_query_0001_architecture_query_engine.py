#!/usr/bin/env python3

from pathlib import Path
import json
import argparse

ROOT = Path(__file__).resolve().parents[2]

REGISTRY = ROOT / "runtime" / "architecture" / "architecture_registry_export.json"

db = json.loads(REGISTRY.read_text())
index = db["registry"]["by_name"]

parser = argparse.ArgumentParser()
parser.add_argument("query", help="Module name or substring")
args = parser.parse_args()

q = args.query.lower()

matches = []

for name, meta in sorted(index.items()):
    if q in name.lower():
        matches.append({
            "name": name,
            "family": meta["family"],
            "path": meta["relative_path"],
            "size": meta["size_bytes"],
        })

print("=" * 60)
print("FORGE-ARCH-QUERY-0001")
print("Architecture Query Engine")
print("=" * 60)
print("Query   :", args.query)
print("Matches :", len(matches))
print()

for m in matches:
    print(f'{m["name"]}')
    print(f'  Family : {m["family"]}')
    print(f'  Path   : {m["path"]}')
    print(f'  Size   : {m["size"]}')
    print()

