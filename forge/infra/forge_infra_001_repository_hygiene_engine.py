#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "runtime/infra"


def sha256(path: Path):

    h = hashlib.sha256()

    with path.open("rb") as f:

        while chunk := f.read(65536):

            h.update(chunk)

    return h.hexdigest()


removed = []

for p in ROOT.rglob("__pycache__"):

    if p.is_dir():

        for f in p.rglob("*"):

            if f.is_file():

                removed.append(
                    str(f.relative_to(ROOT))
                )

                f.unlink()

        p.rmdir()

pyc = []

for f in ROOT.rglob("*.pyc"):

    if f.exists():

        pyc.append(
            str(f.relative_to(ROOT))
        )

        f.unlink()

gitignore = ROOT / ".gitignore"

existing = []

if gitignore.exists():

    existing = gitignore.read_text().splitlines()

required = [

    "__pycache__/",
    "*.pyc",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".coverage",
]

changed = False

for item in required:

    if item not in existing:

        existing.append(item)

        changed = True

if changed or not gitignore.exists():

    gitignore.write_text(
        "\n".join(existing) + "\n"
    )

payload = {

    "infra":
    "FORGE-INFRA-001",

    "status":
    "FORGE_REPOSITORY_HYGIENE_READY",

    "runtime_mode":
    "SHADOW_ONLY_READ_ONLY",

    "pycache_removed":
    len(removed),

    "pyc_removed":
    len(pyc),

    "gitignore_rules":
    required,

    "generated":
    datetime.now(
        timezone.utc
    ).isoformat()

}

payload["integrity_hash"] = hashlib.sha256(

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

report = OUT / "forge_repository_hygiene_001.json"

report.write_text(
    json.dumps(
        payload,
        indent=2
    ) + "\n"
)

digest = sha256(report)

(OUT / "forge_repository_hygiene_001_hash.json").write_text(

    json.dumps({

        "artifact":
        str(report.relative_to(ROOT)),

        "sha256":
        digest

    }, indent=2) + "\n"

)

with (
    OUT /
    "forge_repository_hygiene_001_ledger.jsonl"
).open("a") as f:

    f.write(
        json.dumps(payload) + "\n"
    )

print("FORGE-INFRA-001")
print("FORGE_REPOSITORY_HYGIENE_READY")
print(f"pycache_removed = {payload['pycache_removed']}")
print(f"pyc_removed = {payload['pyc_removed']}")
print(f"integrity_hash = {payload['integrity_hash']}")
print(f"hash = {digest}")
print("runtime_mode = SHADOW_ONLY_READ_ONLY")
