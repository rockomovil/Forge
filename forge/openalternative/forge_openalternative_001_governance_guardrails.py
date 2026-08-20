#!/usr/bin/env python3
"""OPENALTERNATIVE-001 — fail-closed governance contracts for Forge/Galaxy."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable

RISK_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}

@dataclass(frozen=True)
class ExecutionContext:
    human_identity: str
    agent_identity: str
    department: str
    mission: str
    capability: str
    authorization: str | None = None
    risk_class: str = "LOW"
    execution_scope: tuple[str, ...] = ()
    audit_id: str = ""

@dataclass(frozen=True)
class AuthorizationDecision:
    decision: str
    reason: str
    one_shot: bool
    audit_required: bool = True

def authorize(ctx: ExecutionContext, *, channel: str, requested_persistence: bool = False) -> AuthorizationDecision:
    """Fail closed. Voice is not sufficient for HIGH/CRITICAL authority."""
    if ctx.risk_class not in RISK_ORDER:
        return AuthorizationDecision("DENY", "unknown_risk_class", True)
    if not ctx.human_identity or not ctx.agent_identity or not ctx.capability:
        return AuthorizationDecision("DENY", "incomplete_execution_context", True)
    if not ctx.authorization:
        return AuthorizationDecision("DENY", "authorization_unavailable", True)
    if RISK_ORDER[ctx.risk_class] >= RISK_ORDER["HIGH"] and channel == "voice":
        return AuthorizationDecision("DENY", "voice_channel_insufficient_for_high_risk", True)
    if requested_persistence and ctx.risk_class in {"HIGH", "CRITICAL"}:
        return AuthorizationDecision("DENY", "persistent_high_risk_grant_forbidden", True)
    return AuthorizationDecision("ALLOW", "authorized", not requested_persistence)

def monotonic_guard(decisions: Iterable[str]) -> str:
    """Any DENY dominates; lower layers cannot reopen a denial."""
    normalized = [d.upper() for d in decisions]
    if "DENY" in normalized:
        return "DENY"
    if "ASK" in normalized:
        return "ASK"
    if normalized and all(d == "ALLOW" for d in normalized):
        return "ALLOW"
    return "DENY"

def capability_subset(parent: set[str], child: set[str]) -> bool:
    """Delegation may only remove capabilities, never silently add them."""
    return child.issubset(parent)

def sandbox_gate(required: bool, available: bool) -> bool:
    """No silent sandbox degradation."""
    return (not required) or available

def serialize_context(ctx: ExecutionContext) -> dict:
    return asdict(ctx)

if __name__ == "__main__":
    sample = ExecutionContext(
        human_identity="human",
        agent_identity="forge-worker",
        department="forge",
        mission="shadow-validation",
        capability="write_proposal",
        authorization="explicit",
        risk_class="MEDIUM",
        execution_scope=("proposal-only",),
        audit_id="OPENALTERNATIVE-001",
    )
    assert authorize(sample, channel="ui").decision == "ALLOW"
    assert monotonic_guard(["ALLOW", "DENY", "ALLOW"]) == "DENY"
    assert capability_subset({"read", "write"}, {"read"})
    assert sandbox_gate(True, False) is False
    print("STATUS : PASS")
