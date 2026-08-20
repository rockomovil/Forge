#!/usr/bin/env python3
"""OPENALTERNATIVE-002 — task-DAG, path-lease, worker and merge contracts."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Iterable

TERMINAL = {"DONE", "FAILED", "CANCELLED"}
WORKER_STATES = {
    "CREATED", "STARTING", "WORKING", "WAITING_PERMISSION", "BLOCKED",
    "REVIEW", "DONE", "FAILED", "STALE", "TERMINATED"
}

@dataclass
class Task:
    task_id: str
    dependencies: set[str] = field(default_factory=set)
    leased_paths: tuple[str, ...] = ()
    state: str = "CREATED"
    revision: int = 0

def ready(task: Task, task_states: dict[str, str]) -> bool:
    return task.state in {"CREATED", "BLOCKED"} and all(task_states.get(d) == "DONE" for d in task.dependencies)

def dependency_delete_safe(task: Task, deleted_id: str) -> bool:
    """Removing a dependency never auto-promotes a dependent task."""
    return deleted_id not in task.dependencies

def cas_update(task: Task, expected_revision: int, new_state: str) -> bool:
    if expected_revision != task.revision or new_state not in WORKER_STATES:
        return False
    task.state = new_state
    task.revision += 1
    return True

def _parts(pattern: str) -> tuple[str, ...]:
    return PurePosixPath(pattern.replace("**", "")).parts

def paths_overlap(a: str, b: str) -> bool:
    pa, pb = _parts(a), _parts(b)
    n = min(len(pa), len(pb))
    return pa[:n] == pb[:n]

def leases_conflict(existing: Iterable[tuple[str, str]], candidate_paths: Iterable[str], holder: str) -> list[str]:
    conflicts = []
    for other_holder, existing_path in existing:
        if other_holder == holder:
            continue
        for candidate in candidate_paths:
            if paths_overlap(existing_path, candidate):
                conflicts.append(f"{other_holder}:{existing_path}<->{candidate}")
    return conflicts

def diff_within_lease(changed_paths: Iterable[str], leased_paths: Iterable[str]) -> bool:
    leases = tuple(leased_paths)
    return all(any(paths_overlap(changed, lease) for lease in leases) for changed in changed_paths)

def merge_gate(*, task_pass: bool, dependencies_pass: bool, global_regression_pass: bool,
               architecture_pass: bool, security_pass: bool, constitution_pass: bool,
               provenance_pass: bool, conflict_free: bool) -> bool:
    return all((
        task_pass, dependencies_pass, global_regression_pass, architecture_pass,
        security_pass, constitution_pass, provenance_pass, conflict_free
    ))

def classify_wait(awaiting_human: bool, elapsed_ms: int, stall_ms: int) -> str:
    if awaiting_human:
        return "WAITING_PERMISSION"
    return "STALE" if elapsed_ms > stall_ms else "WORKING"

def bounded_recovery(attempts: int, max_attempts: int = 1) -> str:
    return "RETRY" if attempts < max_attempts else "ESCALATE"

def delegation_depth_allowed(depth: int, max_depth: int) -> bool:
    return 0 <= depth <= max_depth

if __name__ == "__main__":
    assert paths_overlap("galaxy/risk/a.py", "galaxy/risk/**")
    assert not paths_overlap("broker/a.py", "galaxy/risk/**")
    assert diff_within_lease(["galaxy/risk/a.py"], ["galaxy/risk/**"])
    assert not diff_within_lease(["broker/a.py"], ["galaxy/risk/**"])
    assert classify_wait(True, 999999, 1000) == "WAITING_PERMISSION"
    assert bounded_recovery(1) == "ESCALATE"
    print("STATUS : PASS")
