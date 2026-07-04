#!/usr/bin/env python3

from pathlib import Path
import tarfile
import hashlib

ROOT = Path(__file__).resolve().parents[1]

PACKAGE_DIR = ROOT / "generated/package"
DIST_DIR = ROOT / "generated/dist"

DIST_DIR.mkdir(parents=True, exist_ok=True)

generated = 0

for package in sorted(PACKAGE_DIR.iterdir()):

    if not package.is_dir():
        continue

    archive = DIST_DIR / f"{package.name}.tar.gz"

    with tarfile.open(archive, "w:gz") as tar:
        tar.add(package, arcname=package.name)

    sha256 = hashlib.sha256()

    with archive.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            sha256.update(chunk)

    (DIST_DIR / f"{package.name}.sha256").write_text(
        sha256.hexdigest() + "\n"
    )

    generated += 1

print()
print("Distribution Backend")
print("--------------------")

for file in sorted(DIST_DIR.glob("*.tar.gz")):
    print(file.name)

print()
print("Generated :", generated)
print("Output    :", DIST_DIR)

print()
print("STATUS : BLD0012_DISTRIBUTION_BACKEND_READY")
