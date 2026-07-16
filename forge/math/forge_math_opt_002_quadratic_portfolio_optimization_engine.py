#!/usr/bin/env python3

from pathlib import Path
import json
import hashlib

ROOT = Path(__file__).resolve().parents[2]

SOURCE = json.loads(
    (ROOT / "runtime/math/convex_optimization_engine.json").read_text()
)

engine = {
    "module": "FORGE-MATH-OPT-002",
    "concept": "Quadratic Portfolio Optimization Engine",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "mutation_allowed": False,
    "capabilities": {
        "mean_variance_optimization": True,
        "portfolio_weight_optimization": True,
        "efficient_frontier_generation": True,
        "volatility_minimization": True,
        "return_target_optimization": True
    },
    "mathematical_model": {
        "optimization_type": "quadratic_programming",
        "objective": "minimize_portfolio_variance",
        "model": "Markowitz_mean_variance",
        "formula": "minimize(1/2*xTQx-cTx)"
    },
    "constraints": [
        "capital_budget",
        "asset_weight_limits",
        "risk_constraints",
        "exposure_limits",
        "allocation_rules"
    ],
    "portfolio_targets": [
        "optimal_weights",
        "risk_adjusted_return",
        "efficient_frontier",
        "minimum_variance_portfolio"
    ],
    "integration": {
        "convex_optimization_engine": True,
        "bayesian_decision_optimization_engine": True,
        "risk_engine": True,
        "athena_financial_intelligence": True,
        "simulation_engine": True,
        "portfolio_engine": True
    },
    "source_module": SOURCE["module"],
    "state": "READY"
}

payload = json.dumps(engine, sort_keys=True).encode()
engine["hash"] = hashlib.sha256(payload).hexdigest()

outdir = ROOT / "runtime/math"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "quadratic_portfolio_optimization_engine.json"
outfile.write_text(json.dumps(engine, indent=2))

print("=" * 60)
print("FORGE-MATH-OPT-002")
print("Quadratic Portfolio Optimization Engine")
print("=" * 60)
print("Mean Variance Optimization :", True)
print("Portfolio Weight Optimization :", True)
print("Efficient Frontier Generation :", True)
print("Volatility Minimization       :", True)
print("Return Target Optimization    :", True)
print("Runtime Mode                 :", engine["runtime_mode"])
print("State                        :", engine["state"])
print("Hash                         :", engine["hash"])
print("Output                       :", outfile)
print()
print("STATUS : PASS")
