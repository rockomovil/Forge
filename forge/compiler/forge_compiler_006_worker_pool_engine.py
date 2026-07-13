#!/usr/bin/env python3

from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_SCHEDULE = ROOT / \
    "runtime/compiler/forge_parallel_build_schedule_001.json"

OUT = ROOT / "runtime/compiler"


def load_schedule(path: Path):

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def module_script(module_id: int) -> Path:

    pattern = f"forge_knowledge_{module_id:03d}_*.py"

    matches = list(
        (ROOT / "forge/automation").glob(pattern)
    )

    if len(matches) != 1:
        raise RuntimeError(
            f"SCRIPT_NOT_FOUND[{module_id}]"
        )

    return matches[0]


def worker(module_id: int):

    script = module_script(module_id)

    start = time.time()

    result = subprocess.run(

        [
            sys.executable,
            str(script)
        ],

        cwd=ROOT,

        capture_output=True,

        text=True

    )

    elapsed = round(
        time.time() - start,
        3
    )

    return {

        "module": module_id,

        "script":
        str(script.relative_to(ROOT)),

        "returncode":
        result.returncode,

        "elapsed":
        elapsed,

        "stdout":
        result.stdout.strip(),

        "stderr":
        result.stderr.strip()

    }


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(

        "--schedule",

        default=str(
            DEFAULT_SCHEDULE.relative_to(ROOT)
        )

    )

    parser.add_argument(

        "--workers",

        type=int,

        default=max(
            2,
            os.cpu_count() or 2
        )

    )

    args = parser.parse_args()

    schedule = load_schedule(
        ROOT / args.schedule
    )

    report = []

    level_reports = []

    total_start = time.time()

    for level_id, level in enumerate(

        schedule["levels"],

        start=1

    ):

        print()

        print(
            f"LEVEL {level_id}"
        )

        print(level)

        with cf.ThreadPoolExecutor(

            max_workers=args.workers

        ) as pool:

            futures = {

                pool.submit(
                    worker,
                    module
                ): module

                for module in level

            }

            completed = []

            for future in cf.as_completed(futures):

                result = future.result()

                completed.append(result)

                report.append(result)

                print(

                    f"PASS {result['module']:03d}"

                    if result["returncode"] == 0

                    else

                    f"FAIL {result['module']:03d}"

                )

        level_reports.append({

            "level":
            level_id,

            "modules":
            level,

            "results":
            completed

        })

    elapsed = round(
        time.time() - total_start,
        3
    )

    payload = {

        "compiler":
        "FORGE-COMPILER-006",

        "status":
        "FORGE_WORKER_POOL_READY",

        "runtime_mode":
        "SHADOW_ONLY_READ_ONLY",

        "cpu_count":
        os.cpu_count(),

        "workers":
        args.workers,

        "levels":
        len(level_reports),

        "modules":
        len(report),

        "elapsed":
        elapsed,

        "generated":
        datetime.now(
            timezone.utc
        ).isoformat(),

        "results":
        level_reports

    }

    payload["execution_hash"] = hashlib.sha256(

        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        ).encode()

    ).hexdigest()

    OUT.mkdir(
        parents=True,
        exist_ok=True
    )

    report_file = OUT / \
        "forge_worker_pool_report_001.json"

    report_file.write_text(

        json.dumps(
            payload,
            indent=2
        ) + "\n"

    )

    digest = hashlib.sha256(
        report_file.read_bytes()
    ).hexdigest()

    (OUT /
     "forge_worker_pool_report_001_hash.json").write_text(

        json.dumps(
            {
                "artifact":
                str(report_file.relative_to(ROOT)),
                "sha256":
                digest
            },
            indent=2
        ) + "\n"

    )

    with (
        OUT /
        "forge_worker_pool_report_001_ledger.jsonl"
    ).open("a") as f:

        f.write(
            json.dumps(payload) + "\n"
        )

    print()
    print("FORGE-COMPILER-006")
    print("FORGE_WORKER_POOL_READY")
    print(f"workers = {args.workers}")
    print(f"modules = {len(report)}")
    print(f"levels = {len(level_reports)}")
    print(f"elapsed = {elapsed}")
    print(f"execution_hash = {payload['execution_hash']}")
    print(f"hash = {digest}")
    print("runtime_mode = SHADOW_ONLY_READ_ONLY")


if __name__ == "__main__":
    main()
