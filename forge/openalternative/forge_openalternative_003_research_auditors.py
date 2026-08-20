#!/usr/bin/env python3
"""OPENALTERNATIVE-003 — causal, arithmetic, numerical and research guards."""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class MetricContract:
    name: str
    annualization: str
    sign_convention: str
    units: str
    benchmark: str | None = None

def condition_satisfiable(kind: str, lhs: float, rhs: float) -> bool:
    if kind == ">": return lhs > rhs
    if kind == "<": return lhs < rhs
    if kind == ">=": return lhs >= rhs
    if kind == "<=": return lhs <= rhs
    if kind == "==": return lhs == rhs
    raise ValueError("unsupported comparator")

def self_referential_sigma_condition_impossible(sigma: float) -> bool:
    """z > z+sigma and z < z-sigma are impossible for sigma>0."""
    return sigma > 0

def signal_execution_time_valid(signal_uses_close_t: bool, execution_bar: int, signal_bar: int, justified_same_bar: bool=False) -> bool:
    if signal_uses_close_t and execution_bar == signal_bar and not justified_same_bar:
        return False
    return execution_bar >= signal_bar

def future_extrema_sizing_guard(uses_future_max: bool, uses_future_min: bool, uses_future_vol: bool) -> bool:
    return not any((uses_future_max, uses_future_min, uses_future_vol))

def forward_slice_write_guard(read_end_index: int, decision_index: int) -> bool:
    return read_end_index <= decision_index

def filter_smoother_causality_guard(mode: str, live: bool) -> bool:
    return not (live and mode.upper() in {"RTS", "SMOOTHER", "BACKWARD_SMOOTHER"})

def narrative_override_guard(test_passed: bool, claim_status: str) -> bool:
    """A failed statistical test cannot be promoted to VERIFIED/CANONICAL."""
    if not test_passed and claim_status.upper() in {"VERIFIED", "CANONICAL"}:
        return False
    return True

def metric_semantics_valid(contract: MetricContract) -> bool:
    return bool(contract.name and contract.annualization and contract.sign_convention and contract.units)

def rng_provenance_valid(record: dict) -> bool:
    return all(k in record for k in ("generator", "seed", "stream_id", "model_version", "parameters", "sample_count"))

def parameter_defaults_valid(defaults: dict[str, float], validators: dict[str, tuple[float|None, float|None]]) -> bool:
    for key, value in defaults.items():
        if key not in validators:
            continue
        lo, hi = validators[key]
        if lo is not None and value < lo: return False
        if hi is not None and value > hi: return False
    return True

def convergence_contract(values: Iterable[float], tolerance: float) -> bool:
    vals = list(values)
    if len(vals) < 2 or tolerance < 0:
        return False
    return abs(vals[-1] - vals[-2]) <= tolerance

def independent_method_parity(values: Iterable[float], tolerance: float) -> bool:
    vals = list(values)
    if not vals or not all(math.isfinite(x) for x in vals):
        return False
    return max(vals) - min(vals) <= tolerance

def warning_suppression_guard(all_warnings_suppressed: bool, critical_financial_path: bool) -> bool:
    return not (all_warnings_suppressed and critical_financial_path)

def train_live_parity(train_fields: set[str], live_fields: set[str]) -> bool:
    return train_fields.issubset(live_fields)

def configuration_space_conformance(results: dict[str, bool]) -> bool:
    return bool(results) and all(results.values())

def cache_state_equivalence(cached: Iterable[float], cold: Iterable[float], tolerance: float) -> bool:
    a, b = list(cached), list(cold)
    return len(a) == len(b) and all(abs(x-y) <= tolerance for x, y in zip(a,b))

def input_channel_dropout_stress(base_score: float, ablations: dict[str, float], max_drop: float) -> dict[str, bool]:
    return {name: (base_score - score) <= max_drop for name, score in ablations.items()}

if __name__ == "__main__":
    assert self_referential_sigma_condition_impossible(1.0)
    assert not signal_execution_time_valid(True, 10, 10)
    assert future_extrema_sizing_guard(False, False, False)
    assert not filter_smoother_causality_guard("RTS", live=True)
    assert narrative_override_guard(False, "HYPOTHESIS")
    assert independent_method_parity([10.0, 10.0001], 0.001)
    print("STATUS : PASS")
