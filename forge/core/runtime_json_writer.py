#!/usr/bin/env python3
"""
FORGE-CORE-0001
Runtime JSON Writer

Common utility for Forge engines.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class RuntimeJsonWriter:

    @staticmethod
    def write(path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

    @staticmethod
    def read(path: Path) -> Any:
        return json.loads(
            path.read_text(encoding="utf-8")
        )


if __name__ == "__main__":
    print("FORGE-CORE-0001 READY")
