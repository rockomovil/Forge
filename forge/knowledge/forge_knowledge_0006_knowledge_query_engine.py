#!/usr/bin/env python3

from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]

INDEX = json.loads(
    (ROOT / "runtime/knowledge/knowledge_index.json").read_text()
)

XREF = json.loads(
    (ROOT / "runtime/knowledge/knowledge_cross_reference.json").read_text()
)

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--module")
group.add_argument("--family")
group.add_argument("--depends")
group.add_argument("--referenced-by")
group.add_argument("--search")

args = parser.parse_args()

modules = INDEX["indexes"]["by_module"]
families = INDEX["indexes"]["by_family"]
xref = XREF["cross_references"]

print("=" * 60)
print("FORGE-KNOWLEDGE-0006")
print("Knowledge Query Engine")
print("=" * 60)

if args.module:

    m = args.module

    if m not in modules:
        print("Module not found.")
        raise SystemExit(1)

    print("MODULE\n")

    print(json.dumps(modules[m], indent=2))

elif args.family:

    fam = args.family

    mods = families.get(fam, [])

    print(f"FAMILY : {fam}")
    print(f"COUNT  : {len(mods)}\n")

    for m in sorted(mods):
        print(m)

elif args.depends:

    m = args.depends

    if m not in xref:
        print("Module not found.")
        raise SystemExit(1)

    print(f"DEPENDENCIES : {m}\n")

    deps = xref[m]["depends_on"]

    if not deps:
        print("None")
    else:
        for d in deps:
            print(d)

elif args.referenced_by:

    m = args.referenced_by

    if m not in xref:
        print("Module not found.")
        raise SystemExit(1)

    print(f"REFERENCED BY : {m}\n")

    refs = xref[m]["referenced_by"]

    if not refs:
        print("None")
    else:
        for r in refs:
            print(r)

elif args.search:

    q = args.search.lower()

    matches = []

    for m in modules:

        if q in m.lower():
            matches.append(m)

    print(f"SEARCH : {q}")
    print(f"MATCHES: {len(matches)}\n")

    for m in sorted(matches):
        print(m)

print()
print("STATUS : PASS")
