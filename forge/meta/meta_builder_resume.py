#!/usr/bin/env python3

from pathlib import Path
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
AUTOMATION = ROOT / "forge" / "automation"

PATTERN = re.compile(
    r"forge_knowledge_(\d+)_atlas_(.+)_engine\.py$"
)


def load_catalog(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def existing_modules():
    found = {}

    for file in AUTOMATION.glob("forge_knowledge_*_atlas_*_engine.py"):
        m = PATTERN.match(file.name)
        if m:
            found[int(m.group(1))] = file

    return found


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--catalog", required=True)

    parser.add_argument(
        "--mode",
        choices=[
            "safe",
            "resume",
            "skip",
            "overwrite"
        ],
        default="safe"
    )

    args = parser.parse_args()

    catalog = load_catalog(ROOT / args.catalog)

    modules = catalog["modules"]

    existing = existing_modules()

    print()
    print("FORGE META BUILDER 002")
    print("----------------------")
    print()

    generated = []

    skipped = []

    start = None

    for m in modules:

        idx = int(m["id"])

        if idx in existing:

            if args.mode == "safe":

                print(f"EXISTS  {idx}")

                sys.exit(1)

            elif args.mode == "skip":

                skipped.append(idx)

                continue

            elif args.mode == "resume":

                skipped.append(idx)

                continue

        if start is None:
            start = idx

        generated.append(idx)

    print(f"MODE            : {args.mode}")

    print(f"FIRST NEW       : {start}")

    print(f"SKIPPED         : {len(skipped)}")

    print(f"TO GENERATE     : {len(generated)}")

    if skipped:
        print()
        print("Skipped:")

        print(skipped)

    if generated:
        print()
        print("Generate:")

        print(generated)


if __name__ == "__main__":
    main()

