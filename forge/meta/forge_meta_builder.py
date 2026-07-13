#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

AUTOMATION = ROOT / "forge" / "automation"
RUNTIME = ROOT / "runtime" / "atlas"
RUNTIME_META = ROOT / "runtime" / "meta"

SCRIPT_RE = re.compile(
    r"forge_knowledge_(\d+)_atlas_(.+)_engine\.py$"
)


@dataclass
class Module:

    id: int

    slug: str

    title: str

    status: str


def load_catalog(path: Path):

    with path.open(
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def automation_file(module):

    return (
        AUTOMATION /
        f"forge_knowledge_{module.id:03d}_atlas_{module.slug}_engine.py"
    )


def runtime_files(module):

    return {

        "runtime":
        RUNTIME /
        f"{module.slug}_{module.id:03d}.json",

        "hash":
        RUNTIME /
        f"{module.slug}_{module.id:03d}_hash.json",

        "ledger":
        RUNTIME /
        f"{module.slug}_{module.id:03d}_ledger.jsonl",
    }


def scan(modules):

    result = {}

    for m in modules:

        script = automation_file(m)

        files = runtime_files(m)

        if (
            script.exists()
            and
            all(
                p.exists()
                for p in files.values()
            )
        ):

            state = "COMPLETE"

        elif (
            script.exists()
            and
            any(
                p.exists()
                for p in files.values()
            )
        ):

            state = "PARTIAL"

        elif script.exists():

            state = "SCRIPT_ONLY"

        else:

            state = "MISSING"

        result[m.id] = {

            "state": state,

            "script": script,

            "runtime": files,

        }

    return result


def build(modules, scan_result, resume, overwrite):

    generated = []

    for m in modules:

        state = scan_result[m.id]["state"]

        if state == "COMPLETE":

            if resume:

                continue

            if not overwrite:

                raise SystemExit(
                    f"DESTINATION_EXISTS: {automation_file(m)}"
                )

        generated.append(m)

    return generated


def report(summary):

    RUNTIME_META.mkdir(
        parents=True,
        exist_ok=True
    )

    out = (
        RUNTIME_META /
        "forge_meta_builder_report.json"
    )

    out.write_text(

        json.dumps(
            summary,
            indent=2
        ),

        encoding="utf-8"

    )

    digest = hashlib.sha256(
        out.read_bytes()
    ).hexdigest()

    print()
    print(summary["status"])
    print(f"hash = {digest}")
    print()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--catalog",
        required=True
    )

    parser.add_argument(
        "--resume",
        action="store_true"
    )

    parser.add_argument(
        "--overwrite",
        action="store_true"
    )

    parser.add_argument(
        "--scan",
        action="store_true"
    )

    parser.add_argument(
        "--execute",
        action="store_true"
    )

    parser.add_argument(
        "--git-batch",
        action="store_true"
    )

    args = parser.parse_args()

    catalog = load_catalog(
        ROOT / args.catalog
    )

    modules = [

        Module(
            id=int(x["id"]),
            slug=x["slug"],
            title=x["title"],
            status=x["status"],
        )

        for x in catalog["modules"]

    ]

    state = scan(modules)

    complete = sum(
        s["state"] == "COMPLETE"
        for s in state.values()
    )

    partial = sum(
        s["state"] == "PARTIAL"
        for s in state.values()
    )

    script_only = sum(
        s["state"] == "SCRIPT_ONLY"
        for s in state.values()
    )

    missing = sum(
        s["state"] == "MISSING"
        for s in state.values()
    )

    summary = {

        "builder":
        "FORGE_META_BUILDER",

        "status":
        "FORGE_META_BUILDER_READY",

        "family":
        catalog["family"],

        "complete":
        complete,

        "partial":
        partial,

        "script_only":
        script_only,

        "missing":
        missing,

        "timestamp":
        datetime.now(
            timezone.utc
        ).isoformat(),

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY"

    }

    report(summary)

    if args.scan:

        print("SCAN COMPLETE")
        return

    todo = build(
        modules,
        state,
        args.resume,
        args.overwrite
    )

    print(
        f"TO_GENERATE = {len(todo)}"
    )

    if args.execute:

        for m in todo:

            subprocess.run(

                [

                    "python3",

                    str(
                        automation_file(m)
                    )

                ],

                cwd=ROOT,

                check=True

            )

    if args.git_batch:

        subprocess.run(
            ["git", "add", "."],
            cwd=ROOT,
            check=True
        )

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "FORGE-META-BUILDER Unified Engine Update"
            ],
            cwd=ROOT,
            check=True
        )

        subprocess.run(
            [
                "git",
                "push",
                "origin",
                "main"
            ],
            cwd=ROOT,
            check=True
        )


if __name__ == "__main__":
    main()
