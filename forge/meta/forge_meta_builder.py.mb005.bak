#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

AUTOMATION = ROOT / "forge" / "automation"
RUNTIME = ROOT / "runtime" / "atlas"
RUNTIME_META = ROOT / "runtime" / "meta"


@dataclass
class Module:
    id: int
    slug: str
    title: str
    status: str


def load_catalog(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def script_path(m: Module):
    return AUTOMATION / (
        f"forge_knowledge_{m.id:03d}_atlas_{m.slug}_engine.py"
    )


def runtime_paths(m: Module):
    return [
        RUNTIME / f"{m.slug}_{m.id:03d}.json",
        RUNTIME / f"{m.slug}_{m.id:03d}_hash.json",
        RUNTIME / f"{m.slug}_{m.id:03d}_ledger.jsonl",
    ]


def scan_module(m: Module):

    script = script_path(m)

    runtime = runtime_paths(m)

    if script.exists() and all(x.exists() for x in runtime):
        return "COMPLETE"

    if script.exists() and any(x.exists() for x in runtime):
        return "PARTIAL"

    if script.exists():
        return "SCRIPT_ONLY"

    return "MISSING"


def find_template(modules):

    for m in reversed(modules):

        if script_path(m).exists():

            return m

    raise RuntimeError("NO_TEMPLATE_AVAILABLE")


def render(template: str, src: Module, dst: Module):

    text = template

    replacements = [

        (
            f"FORGE-KNOWLEDGE-{src.id:03d}",
            f"FORGE-KNOWLEDGE-{dst.id:03d}"
        ),

        (
            src.status,
            dst.status
        ),

        (
            src.title,
            dst.title
        ),

        (
            src.title.lower(),
            dst.title.lower()
        ),

        (
            src.slug,
            dst.slug
        ),

        (
            f"_{src.id:03d}",
            f"_{dst.id:03d}"
        )

    ]

    for a, b in replacements:

        text = text.replace(a, b)

    return text


def generate(template_module, target):

    template_file = script_path(template_module)

    text = template_file.read_text(
        encoding="utf-8"
    )

    out = script_path(target)

    out.write_text(

        render(
            text,
            template_module,
            target
        ),

        encoding="utf-8"

    )

    out.chmod(0o755)

    return out


def validate_runtime(module):

    return all(
        p.exists()
        for p in runtime_paths(module)
    )


def execute(module):

    subprocess.run(

        [
            "python3",
            str(script_path(module))
        ],

        cwd=ROOT,
        check=True

    )


def main():

    ap = argparse.ArgumentParser()

    ap.add_argument(
        "--catalog",
        required=True
    )

    ap.add_argument(
        "--resume",
        action="store_true"
    )

    ap.add_argument(
        "--execute",
        action="store_true"
    )

    ap.add_argument(
        "--scan",
        action="store_true"
    )

    args = ap.parse_args()

    catalog = load_catalog(
        ROOT / args.catalog
    )

    modules = [

        Module(

            int(x["id"]),

            x["slug"],

            x["title"],

            x["status"]

        )

        for x in catalog["modules"]

    ]

    template = find_template(modules)

    summary = {
        "COMPLETE":0,
        "PARTIAL":0,
        "SCRIPT_ONLY":0,
        "MISSING":0
    }

    todo = []

    for m in modules:

        state = scan_module(m)

        summary[state]+=1

        if state!="COMPLETE":

            todo.append(m)

    digest = hashlib.sha256(

        json.dumps(
            summary,
            sort_keys=True
        ).encode()

    ).hexdigest()

    print()
    print("FORGE_META_BUILDER_005_READY")
    print(f"hash = {digest}")
    print()

    print(summary)

    if args.scan:
        return

    generated=[]

    for m in todo:

        print(f"GENERATING {m.id}")

        generate(
            template,
            m
        )

        generated.append(m)

        if args.execute:

            execute(m)

            if not validate_runtime(m):

                raise RuntimeError(
                    f"Runtime validation failed {m.id}"
                )

    report={

        "status":
        "FORGE_META_BUILDER_005_READY",

        "generated":
        [m.id for m in generated],

        "count":
        len(generated),

        "timestamp":
        datetime.now(
            timezone.utc
        ).isoformat(),

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY"

    }

    RUNTIME_META.mkdir(
        parents=True,
        exist_ok=True
    )

    (
        RUNTIME_META /
        "forge_meta_builder_report.json"
    ).write_text(

        json.dumps(
            report,
            indent=2
        ),

        encoding="utf-8"

    )


if __name__ == "__main__":
    main()
