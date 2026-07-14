#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, UTC
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

STATE_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_sovereign_state.json"
OUTPUT_FILE = ROOT / "runtime" / "architecture" / "architecture_terminal_sovereign_certified_state.json"

state = json.loads(STATE_FILE.read_text())

ready = state["terminal_sovereign_ready"]

result = {
    "module": "FORGE-ARCH-0048",
    "status": "PASS" if ready else "FAIL",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "terminal_sovereign_certified_state": ready,
    "state": "ULTIMATE_TERMINAL_SOVEREIGN_CERTIFIED_STATE",
    "immutable": state["immutable"],
    "sealed": state["sealed"],
    "locked": state["locked"],
    "certified": state["certified"],
    "completed": state["completed"],
    "certified_at": datetime.now(UTC).isoformat(),
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
print("FORGE-ARCH-0048")
print("Architecture Terminal Sovereign Certified State Engine")
print("=" * 60)
print("Certified :", result["terminal_sovereign_certified_state"])
print("State     :", result["state"])
print("Modules   :", result["module_count"])
print("Families  :", result["family_count"])
print("Prefixes  :", result["prefix_count"])
print("Artifacts :", result["artifact_count"])
print("Output    :", OUTPUT_FILE)
print()
print("STATUS :", result["status"])
