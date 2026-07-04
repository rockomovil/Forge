#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import json

EVENT_LOG = (
    Path(__file__).resolve().parents[1]
    / "runtime"
    / "events"
    / "events.jsonl"
)

EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)


class EventBus:

    def publish(self,
                event_type,
                source,
                payload=None):

        if payload is None:
            payload = {}

        event = {
            "timestamp": datetime.now(UTC).isoformat(),
            "event": event_type,
            "source": source,
            "payload": payload
        }

        with EVENT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False))
            f.write("\n")

        return event

    def history(self):

        if not EVENT_LOG.exists():
            return []

        events = []

        with EVENT_LOG.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if line:
                    events.append(json.loads(line))

        return events


if __name__ == "__main__":

    bus = EventBus()

    bus.publish(
        "SYSTEM_BOOT",
        "F0003",
        {
            "kernel":"Forge",
            "version":"0.1"
        }
    )

    bus.publish(
        "SERVICE_STARTED",
        "F0002",
        {
            "service":"Service Registry"
        }
    )

    bus.publish(
        "CAPABILITY_READY",
        "F0001",
        {
            "capability":"Capability Registry"
        }
    )

    print()
    print("Event History")
    print("-------------")

    for e in bus.history():
        print(
            f'{e["timestamp"]} | {e["event"]} | {e["source"]}'
        )

    print()
    print("Total events:", len(bus.history()))
