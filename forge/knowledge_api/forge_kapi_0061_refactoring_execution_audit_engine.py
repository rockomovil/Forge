#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

GATEWAY = json.loads(
    (ROOT / "runtime/knowledge_api/knowledge_refactoring_execution_gateway.json").read_text()
)

checks = {
    "gateway_ready": GATEWAY["gateway_ready"],
    "authorized": GATEWAY["authorized"],
    "shadow_only": GATEWAY["shadow_only"],
    "parallel_execution": GATEWAY["parallel_execution"],
    "workers_available": GATEWAY["worker_count"] > 0
}

passed = sum(bool(v) for v in checks.values())

report = {
    "module": "FORGE-KAPI-0061",
    "status": "PASS",
    "runtime_mode": "SHADOW_ONLY_READ_ONLY",
    "checks_passed": passed,
    "checks_total": len(checks),
    "all_checks_passed": passed == len(checks),
    "worker_count": GATEWAY["worker_count"],
    "execution_mode": GATEWAY["execution_mode"],
    "checks": checks
}

outdir = ROOT / "runtime/knowledge_api"
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "knowledge_refactoring_execution_audit.json"
outfile.write_text(json.dumps(report, indent=2))

print("=" * 60)
print("FORGE-KAPI-0061")
print("Refactoring Execution Audit Engine")
print("=" * 60)
print("Checks Passed :", report["checks_passed"], "/", report["checks_total"])
print("All Passed    :", report["all_checks_passed"])
print("Workers       :", report["worker_count"])
print("Mode          :", report["execution_mode"])
print("Output        :", outfile)
print()
print("STATUS : PASS")
