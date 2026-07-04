#!/usr/bin/env python3

from pathlib import Path
import json
from datetime import datetime, UTC

REGISTRY = (
    Path(__file__).resolve().parents[1]
    / "runtime"
    / "services"
    / "registry.json"
)

REGISTRY.parent.mkdir(parents=True, exist_ok=True)

if not REGISTRY.exists():
    REGISTRY.write_text("[]")


class ServiceRegistry:

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

    def register(
        self,
        service_id,
        name,
        version,
        provider
    ):

        if any(s["id"] == service_id for s in self.data):
            return False

        self.data.append(
            {
                "id": service_id,
                "name": name,
                "version": version,
                "provider": provider,
                "status": "ACTIVE",
                "registered_at": datetime.now(UTC).isoformat()
            }
        )

        self.data.sort(key=lambda x: x["id"])
        self._save()

        return True

    def list(self):
        return self.data


if __name__ == "__main__":

    registry = ServiceRegistry()

    registry.register(
        "S0001",
        "Capability Registry Service",
        "0.1",
        "F0001"
    )

    registry.register(
        "S0002",
        "Service Registry Service",
        "0.1",
        "F0002"
    )

    print()
    print("Registered services")
    print("-------------------")

    for service in registry.list():
        print(
            f'{service["id"]:<8} {service["name"]} ({service["provider"]})'
        )

    print()
    print("Service count:", len(registry.list()))
