#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PYTHON_DIR = ROOT / "generated/python"
OUTDIR = ROOT / "generated/cli"

OUTDIR.mkdir(parents=True, exist_ok=True)

generated = 0

for module in sorted(PYTHON_DIR.glob("*.py")):

    name = module.stem

    outfile = OUTDIR / f"{name}_cli.py"

    code = f'''#!/usr/bin/env python3

import sys

from generated.python.{name} import *

def main():

    print("Running {name}")

if __name__ == "__main__":
    sys.exit(main())
'''

    outfile.write_text(code)
    outfile.chmod(0o755)

    generated += 1

print()
print("CLI Backend")
print("-----------")

for file in sorted(OUTDIR.glob("*.py")):
    print(file.name)

print()
print("Generated :", generated)
print("Output    :", OUTDIR)

print()
print("STATUS : BLD0010_CLI_BACKEND_READY")
