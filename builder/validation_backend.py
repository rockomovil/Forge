#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json
import tarfile

ROOT = Path(__file__).resolve().parents[1]

RELEASE_DIR = ROOT / "generated/release"
OUTDIR = ROOT / "generated/validation"

OUTDIR.mkdir(parents=True, exist_ok=True)

validated = 0
passed = 0
failed = 0

print()
print("Validation Backend")
print("------------------")

for archive in sorted(RELEASE_DIR.glob("*.tar.gz")):

    ok = True
    errors = []

    try:
        with tarfile.open(archive, "r:gz") as tar:
            members = tar.getmembers()

        if len(members) == 0:
            ok = False
            errors.append("archive empty")

    except Exception as e:
        ok = False
        errors.append(str(e))

    sha256 = hashlib.sha256(archive.read_bytes()).hexdigest()

    report = {
        "artifact": archive.name,
        "timestamp": datetime.now(UTC).isoformat(),
        "size": archive.stat().st_size,
        "sha256": sha256,
        "valid": ok,
        "errors": errors
    }

    outfile = OUTDIR / f"{archive.stem}_validation.json"
    outfile.write_text(json.dumps(report, indent=4))

    print(archive.name)

    validated += 1

    if ok:
        passed += 1
    else:
        failed += 1

print()
print("Validated :", validated)
print("Passed    :", passed)
print("Failed    :", failed)
print("Output    :", OUTDIR)

print()
print("STATUS : BLD0014_VALIDATION_BACKEND_READY")
