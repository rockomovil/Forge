#!/usr/bin/env python3
"""OPENALTERNATIVE-006 — certification gate for the technology-intake wave."""
from __future__ import annotations
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "forge" / "openalternative"
REGISTRY = ROOT / "runtime" / "openalternative" / "technology_intake_registry.json"
MODULES = [
    "forge_openalternative_001_governance_guardrails.py",
    "forge_openalternative_002_orchestration_contracts.py",
    "forge_openalternative_003_research_auditors.py",
    "forge_openalternative_004_human_interface_contracts.py",
    "forge_openalternative_005_capability_registry.py",
]

def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = mod
    spec.loader.exec_module(mod)
    return mod

def certify() -> dict:
    registry = json.loads(REGISTRY.read_text())
    assert registry["runtime_mode"] == "SHADOW_ONLY_READ_ONLY"
    assert registry["canonical_mutation_allowed"] is False
    assert registry["worker_activation_allowed"] is False
    assert registry["orders_allowed"] is False
    assert registry["real_money_allowed"] is False
    assert len(registry["sources"]) >= 8

    g, o, r, h, c = [load(BASE / name) for name in MODULES]

    ctx = g.ExecutionContext("human","worker","forge","audit","write_proposal","explicit","MEDIUM",("proposal-only",),"cert")
    checks = {
        "fail_closed_authorization": g.authorize(ctx, channel="ui").decision == "ALLOW",
        "monotonic_deny": g.monotonic_guard(["ALLOW","DENY","ALLOW"]) == "DENY",
        "capability_contraction": g.capability_subset({"read","write"},{"read"}),
        "sandbox_fail_closed": g.sandbox_gate(True, False) is False,
        "lease_enforcement": o.diff_within_lease(["galaxy/risk/a.py"],["galaxy/risk/**"]),
        "lease_escape_blocked": not o.diff_within_lease(["broker/a.py"],["galaxy/risk/**"]),
        "human_wait_not_stall": o.classify_wait(True,999999,10) == "WAITING_PERMISSION",
        "bounded_recovery": o.bounded_recovery(1) == "ESCALATE",
        "signal_time_parity": not r.signal_execution_time_valid(True,5,5),
        "future_extrema_blocked": not r.future_extrema_sizing_guard(True,False,False),
        "smoother_live_blocked": not r.filter_smoother_causality_guard("RTS",True),
        "failed_evidence_not_canonical": not r.narrative_override_guard(False,"CANONICAL"),
        "numerical_parity": r.independent_method_parity([1.0,1.00001],0.001),
        "rng_provenance": r.rng_provenance_valid({"generator":"x","seed":1,"stream_id":"a","model_version":"1","parameters":{},"sample_count":1}),
        "rewrite_bounded": h.bounded_autocorrection(1) == "HUMAN_REVIEW",
        "no_silent_continuity": not h.continuity_fallback_allowed(False,False),
        "remote_pipe_blocked": not h.remote_install_safe(downloaded=True,hash_verified=False,signature_verified=False,version_pinned=True,approved=True),
        "no_fake_capabilities": c.no_fake_capability_advertisement({"read"},{"read","write"}),
        "signed_package_gate": not c.signed_package_valid(signature_ok=False,hash_ok=True,compatible=True,permissions_declared=True),
    }
    passed = sum(checks.values())
    return {
        "module": "OPENALTERNATIVE-006",
        "runtime_mode": registry["runtime_mode"],
        "checks": checks,
        "passed": passed,
        "total": len(checks),
        "status": "PASS" if passed == len(checks) else "FAIL",
        "live_activation": False,
    }

if __name__ == "__main__":
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)
