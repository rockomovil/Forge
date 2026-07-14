#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


class RegistryAPI:

    def __init__(self):

        self.root = Path(__file__).resolve().parents[3]
        self.runtime = self.root / "runtime" / "kernel"

    def load(self, filename: str) -> dict:

        return json.loads(
            (self.runtime / f"{filename}.json").read_text(
                encoding="utf-8"
            )
        )
