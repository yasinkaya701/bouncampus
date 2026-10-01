#!/usr/bin/env python3
"""Run the CS1 campus-operations regression suite with one deterministic command.

The default suite is dependency-light and exercises the decision policies directly.
Use ``--with-api`` in an environment with backend FastAPI/Pydantic dependencies to
also execute the orchestration-router regression.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

POLICY_TESTS = (
    "scripts/test_cs1_campus_state.py",
    "scripts/test_cs1_source_health.py",
    "scripts/test_cs1_shuttle_policy.py",
    "scripts/test_cs1_classroom_policy.py",
    "scripts/test_cs1_food_ops_policy.py",
    "scripts/test_cs1_building_energy_policy.py",
    "scripts/test_cs1_space_activation_policy.py",
    "scripts/test_cs1_shared_capacity_policy.py",
    "scripts/test_cs1_campus_portfolio.py",
    "scripts/test_cs1_cross_contract.py",
    "scripts/test_cs1_decision_intelligence.py",
    "scripts/test_cs1_method_eligibility.py",
    "scripts/test_food_decision_policy.py",
)

API_TESTS = (
    "scripts/test_cs1_campus_ops_router.py",
)


def run_one(relative_path: str) -> tuple[bool, str]:
    path = ROOT / relative_path
    if not path.is_file():
        return False, f"MISSING {relative_path}"

    process = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    stdout = process.stdout.strip()
    stderr = process.stderr.strip()
    detail = stdout or stderr or f"exit={process.returncode}"
    if process.returncode != 0 and stdout and stderr:
        detail = f"{stdout}\n{stderr}"
    return process.returncode == 0, detail


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--with-api",
        action="store_true",
        help="also run FastAPI orchestration tests (requires backend dependencies)",
    )
    args = parser.parse_args()

    selected = [*POLICY_TESTS, *(API_TESTS if args.with_api else ())]
    failures: list[str] = []
    for relative_path in selected:
        ok, detail = run_one(relative_path)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {relative_path}: {detail}")
        if not ok:
            failures.append(relative_path)

    if failures:
        print(f"CS1 regression suite failed: {len(failures)}/{len(selected)}")
        for item in failures:
            print(f" - {item}")
        return 1

    print(f"CS1 regression suite passed: {len(selected)}/{len(selected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
