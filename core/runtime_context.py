#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import json
import platform

ROOT = Path(__file__).resolve().parents[1]

CONTEXT = ROOT / "runtime" / "context" / "runtime_context.json"

CONTEXT.parent.mkdir(parents=True, exist_ok=True)


class RuntimeContext:

    def __init__(self):
        self.state = {
            "generated_at": datetime.now(UTC).isoformat(),
            "forge_root": str(ROOT),
            "workspace": str(ROOT.parent),
            "platform": platform.system(),
            "platform_release": platform.release(),
            "python": platform.python_version(),
            "kernel": "Forge Kernel",
            "kernel_version": "0.1",
            "boot_mode": "BOOTSTRAP",
            "human_control": True,
            "autonomous_mode": False
        }

    def save(self):
        CONTEXT.write_text(
            json.dumps(
                self.state,
                indent=2,
                ensure_ascii=False
            )
        )

    def load(self):
        return json.loads(CONTEXT.read_text())


if __name__ == "__main__":

    ctx = RuntimeContext()

    ctx.save()

    runtime = ctx.load()

    print()
    print("Runtime Context")
    print("----------------")

    for k, v in runtime.items():
        print(f"{k:20}: {v}")

    print()
    print("Context file :", CONTEXT)
