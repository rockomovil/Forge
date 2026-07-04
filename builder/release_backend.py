#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]

DIST = ROOT / "generated/dist"
OUT = ROOT / "generated/release"

OUT.mkdir(parents=True, exist_ok=True)

generated = 0

print()
print("Release Backend")
print("---------------")

for archive in sorted(DIST.glob("*.tar.gz")):

    target = OUT / archive.name
    shutil.copy2(archive, target)

    sha256 = hashlib.sha256(target.read_bytes()).hexdigest()

    manifest = {
        "artifact": archive.name,
        "sha256": sha256,
        "size": target.stat().st_size,
        "generated": datetime.now(UTC).isoformat()
    }

    (OUT / f"{archive.stem}.json").write_text(
        json.dumps(manifest, indent=4)
    )

    print(archive.name)

    generated += 1

print()
print("Generated :", generated)
print("Output    :", OUT)

print()
print("STATUS : BLD0013_RELEASE_BACKEND_READY")
