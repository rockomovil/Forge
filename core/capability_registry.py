#!/usr/bin/env python3

from pathlib import Path
import json
from datetime import datetime, UTC

REGISTRY = (
    Path(__file__).resolve().parents[1]
    / "runtime"
    / "capabilities"
    / "registry.json"
)

REGISTRY.parent.mkdir(parents=True, exist_ok=True)

if not REGISTRY.exists():
    REGISTRY.write_text("[]")


class CapabilityRegistry:

    def __init__(self):
        self._load()

    def _load(self):
        self.data = json.loads(REGISTRY.read_text())

    def _save(self):
        REGISTRY.write_text(
            json.dumps(
                self.data,
                indent=2,
                ensure_ascii=False
            )
        )

    def register(self,
                 capability_id,
                 name,
                 version,
                 stage):

        if any(c["id"] == capability_id for c in self.data):
            return False

        self.data.append(
            {
                "id": capability_id,
                "name": name,
                "version": version,
                "stage": stage,
                "status": "INSTALLED",
                "installed_at": datetime.now(UTC).isoformat()
            }
        )

        self.data.sort(key=lambda x: x["id"])
        self._save()
        return True

    def list(self):
        return self.data


if __name__ == "__main__":

    r = CapabilityRegistry()

    r.register(
        "F0001",
        "Capability Registry",
        "0.1",
        "Foundation"
    )

    print()

    print("Installed capabilities")

    print("----------------------")

    for c in r.list():
        print(
            f'{c["id"]:<8} {c["name"]}'
        )

    print()

    print("Capability count:", len(r.list()))
