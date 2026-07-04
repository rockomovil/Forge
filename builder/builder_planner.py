#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import json

ROOT = Path(__file__).resolve().parents[1]

ORDERS = ROOT / "runtime/builder/work_orders.json"
PLAN   = ROOT / "runtime/builder/execution_plan.json"

if not ORDERS.exists():
    print("ERROR: work_orders.json not found")
    raise SystemExit(1)

orders = json.loads(ORDERS.read_text())

plan = {
    "generated_at": datetime.now(UTC).isoformat(),
    "planner": "BLD-0002",
    "orders": []
}

for index, order in enumerate(orders, start=1):

    plan["orders"].append({

        "step": index,

        "order_id": order["id"],

        "title": order["title"],

        "status": "PLANNED",

        "depends_on": [],

        "estimated_phase": "GENERATOR"

    })

PLAN.write_text(
    json.dumps(
        plan,
        indent=2,
        ensure_ascii=False
    )
)

print()
print("Execution Plan")
print("----------------")

for item in plan["orders"]:

    print(
        f'Step {item["step"]} -> {item["order_id"]} -> {item["title"]}'
    )

print()
print("Planned Orders :", len(plan["orders"]))
print("Execution Plan :", PLAN)

