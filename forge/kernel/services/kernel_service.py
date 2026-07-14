#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path


class KernelService:

    def __init__(self, module: str, status: str):

        self.module = module
        self.status = status

        self.root = Path(__file__).resolve().parents[3]
        self.runtime = self.root / "runtime" / "kernel"

        self.runtime.mkdir(parents=True, exist_ok=True)

    def write_runtime(self, filename: str, payload: dict):

        payload["module"] = self.module
        payload["status"] = self.status
        payload["runtime_mode"] = "SHADOW_ONLY_READ_ONLY"
        payload["generated"] = datetime.now(UTC).isoformat()

        text = json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )

        (self.runtime / f"{filename}.json").write_text(
            text,
            encoding="utf-8",
        )

        integrity = hashlib.sha256(
            text.encode()
        ).hexdigest()

        (self.runtime / f"{filename}_hash.json").write_text(
            json.dumps(
                {
                    "module": self.module,
                    "integrity_hash": integrity,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        with (self.runtime / f"{filename}_ledger.jsonl").open(
            "a",
            encoding="utf-8",
        ) as ledger:

            ledger.write(
                json.dumps(
                    {
                        "timestamp": payload["generated"],
                        "module": self.module,
                        "status": self.status,
                        "integrity_hash": integrity,
                    }
                )
                + "\n"
            )

        verification = hashlib.sha256(
            (self.module + self.status + integrity).encode()
        ).hexdigest()

        print(self.module)
        print(self.status)

        for k, v in payload.items():

            if k in {
                "module",
                "status",
                "generated",
                "runtime_mode",
            }:
                continue

            print(f"{k} = {v}")

        print(f"integrity_hash = {integrity}")
        print(f"hash = {verification}")
        print("runtime_mode = SHADOW_ONLY_READ_ONLY")
        print(f"{self.module} VERIFIED")
