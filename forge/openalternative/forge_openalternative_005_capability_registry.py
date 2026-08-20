#!/usr/bin/env python3
"""OPENALTERNATIVE-005 — capability/agent/plugin manifests and reversible lifecycle."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Capability:
    capability_id: str
    input_schema: str
    output_schema: str
    permissions: frozenset[str]
    side_effect_level: str
    risk_class: str
    proposal_only: bool
    version: str

@dataclass
class AgentDefinition:
    agent_id: str
    provider: str
    capabilities: set[str] = field(default_factory=set)
    permissions: set[str] = field(default_factory=set)
    department: str = ""
    trust_level: str = "UNTRUSTED"
    health: str = "UNKNOWN"

class CapabilityRegistry:
    def __init__(self) -> None:
        self._caps: dict[str, Capability] = {}
    def mount(self, cap: Capability) -> None:
        if cap.capability_id in self._caps:
            raise ValueError("duplicate capability")
        self._caps[cap.capability_id] = cap
    def unmount(self, capability_id: str) -> None:
        self._caps.pop(capability_id, None)
    def get(self, capability_id: str) -> Capability:
        return self._caps[capability_id]
    def list_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._caps))

def no_fake_capability_advertisement(advertised: set[str], executable: set[str]) -> bool:
    return advertised.issubset(executable)

def integration_version_valid(tested_version: str, runtime_version: str) -> bool:
    return tested_version == runtime_version

def signed_package_valid(*, signature_ok: bool, hash_ok: bool, compatible: bool, permissions_declared: bool) -> bool:
    return all((signature_ok, hash_ok, compatible, permissions_declared))

if __name__ == "__main__":
    reg = CapabilityRegistry()
    reg.mount(Capability("read_repo", "json", "json", frozenset({"repo:read"}), "NONE", "LOW", False, "1"))
    assert reg.list_ids() == ("read_repo",)
    reg.unmount("read_repo")
    assert not reg.list_ids()
    print("STATUS : PASS")
