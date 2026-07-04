#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import json

ROOT = Path(__file__).resolve().parents[1]

QUEUE = ROOT / "runtime" / "builder" / "work_orders.json"

QUEUE.parent.mkdir(parents=True, exist_ok=True)

if not QUEUE.exists():
    QUEUE.write_text("[]")


class BuilderCore:

    def __init__(self):
        self.orders = json.loads(QUEUE.read_text())

    def save(self):
        QUEUE.write_text(
            json.dumps(
                self.orders,
                indent=2,
                ensure_ascii=False
            )
        )

    def create_order(
        self,
        order_id,
        title,
        category
    ):

        self.orders.append(
            {
                "id": order_id,
                "title": title,
                "category": category,
                "status": "PENDING",
                "created_at": datetime.now(UTC).isoformat()
            }
        )

        self.save()

    def show(self):

        print()
        print("Builder Work Orders")
        print("-------------------")

        for order in self.orders:

            print(
                f'{order["id"]:<12} {order["status"]:<10} {order["title"]}'
            )

        print()
        print("Total Orders:", len(self.orders))


builder = BuilderCore()

if len(builder.orders) == 0:

    builder.create_order(
        "WO-000001",
        "Create Module Generator",
        "Builder"
    )

builder.show()
