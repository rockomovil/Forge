#!/usr/bin/env python3

from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]

idx = json.loads(
    (ROOT/"runtime/architecture/module_index.json").read_text()
)

parser = argparse.ArgumentParser()
parser.add_argument("query")
args = parser.parse_args()

q = args.query.lower()

matches = []

for name, meta in idx["indexes"]["by_name"].items():

    if (
        q in name.lower()
        or q in meta["relative_path"].lower()
        or q in meta["family"].lower()
    ):
        matches.append((name, meta))

print("="*60)
print("FORGE-ARCH-QUERY-0004")
print("Architecture Fuzzy Query Engine")
print("="*60)
print("Query :", args.query)
print("Matches:", len(matches))
print()

for name, meta in sorted(matches):
    print(name)
    print("  Family :", meta["family"])
    print("  Path   :", meta["relative_path"])
    print("  Size   :", meta["size_bytes"])
    print()
