#!/usr/bin/env python3
"""OPENALTERNATIVE-004 — human-output, session, visibility and interface guards."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class RewriteCriticalFacts:
    numbers: tuple[str, ...]
    commands: tuple[str, ...]
    warnings: tuple[str, ...]
    decisions: tuple[str, ...]

def rewrite_preserves_semantics(before: RewriteCriticalFacts, after: RewriteCriticalFacts) -> bool:
    return before == after

def bounded_autocorrection(attempts: int, max_attempts: int = 1) -> str:
    return "REWRITE" if attempts < max_attempts else "HUMAN_REVIEW"

def readability_not_correctness(readability_pass: bool, technical_pass: bool) -> bool:
    return readability_pass and technical_pass

def language_validated(language: str, validated_languages: set[str]) -> bool:
    return language.lower() in {x.lower() for x in validated_languages}

def post_cancel_output_valid(emitted_at_ms: int, cancelled_at_ms: int | None) -> bool:
    return cancelled_at_ms is None or emitted_at_ms <= cancelled_at_ms

def continuity_fallback_allowed(resume_succeeded: bool, reconstruction_verified: bool) -> bool:
    """Fresh silent fallback is forbidden; continuity requires successful resume or verified rebuild."""
    return resume_succeeded or reconstruction_verified

def output_visibility_record(*, generated: bool, streamed: bool, visible: bool, heard: bool, cancelled_remainder: bool) -> dict:
    return {
        "model_generated": generated,
        "model_streamed": streamed,
        "human_visible": visible,
        "human_heard": heard,
        "cancelled_remainder": cancelled_remainder,
    }

def remote_install_safe(*, downloaded: bool, hash_verified: bool, signature_verified: bool,
                        version_pinned: bool, approved: bool) -> bool:
    return all((downloaded, hash_verified, signature_verified, version_pinned, approved))

def human_interrupt_preemption(current_state: str, interrupt: bool) -> str:
    return "CANCELLED" if interrupt else current_state

if __name__ == "__main__":
    facts = RewriteCriticalFacts(("42",), ("pytest",), ("no live orders",), ("DENY",))
    assert rewrite_preserves_semantics(facts, facts)
    assert bounded_autocorrection(1) == "HUMAN_REVIEW"
    assert not continuity_fallback_allowed(False, False)
    assert not remote_install_safe(downloaded=True, hash_verified=False, signature_verified=False, version_pinned=True, approved=True)
    print("STATUS : PASS")
