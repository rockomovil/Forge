#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

STATE_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_state.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_completion.json"

state = json.loads(STATE_FILE.read_text())

completed = (
    state["terminal_ready"]
    and state["immutable"]
    and state["locked"]
    and state["sealed"]
    and state["certified"]
)

result = {
    "module": "FORGE-ARCH-0040",
    "status": "PASS" if completed else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "architecture_terminal_completed": completed,
    "terminal_state": state["terminal_state"],
    "completed_at": datetime.now(UTC).isoformat(),
    "state_hash": state["hash"],
    "module_count": state["module_count"],
    "family_count": state["family_count"],
    "prefix_count": state["prefix_count"],
    "artifact_count": state["artifact_count"],
}

result["hash"] = hashlib.sha256(
    json.dumps(result, sort_keys=True).encode()
).hexdigest()

OUTPUT_FILE.write_text(json.dumps(result, indent=2))

print("=" * 60)
print("FORGE-ARCH-0040")
print("Architecture Terminal Completion Engine")
print("=" * 60)
print("Completed:", result["architecture_terminal_completed"])
print("State    :", result["terminal_state"])
print("Modules  :", result["module_count"])
print("Families :", result["family_count"])
print("Prefixes :", result["prefix_count"])
print("Artifacts:", result["artifact_count"])
print("Output   :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
