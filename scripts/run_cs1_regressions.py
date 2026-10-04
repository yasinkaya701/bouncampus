#!/usr/bin/env python3
"""Discover and execute CS1 regression suites deterministically.

Normal CS1 behavior tests live under ``scripts/`` and use the naming contract
``test_cs1_*.py`` or ``test_cs1_*.ts``. This runner is the single CI entrypoint
so feature PRs can add a regression without editing workflow files.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
SUPPORTED_SUFFIXES = {".py", ".ts"}
LEGACY_REGRESSIONS = ("test_food_decision_policy.py",)


def discover_test_files(scripts_dir: Path = SCRIPTS_DIR) -> list[Path]:
    """Return supported CS1 regression files in stable lexical order."""
    candidates = [
        path
        for path in scripts_dir.glob("test_cs1_*")
        if path.is_file() and path.suffix in SUPPORTED_SUFFIXES
    ]
    return sorted(candidates, key=lambda path: path.name)


def command_for_test(path: Path) -> list[str]:
    """Build the explicit interpreter command for one registered test file."""
    if path.suffix == ".py":
        return [sys.executable, str(path)]
    if path.suffix == ".ts":
        return ["node", str(path)]
    raise ValueError(f"unsupported CS1 regression suffix: {path.suffix or '<none>'}")


def regression_files(scripts_dir: Path = SCRIPTS_DIR) -> list[Path]:
    """Return normal CS1 suites plus explicitly retained legacy regressions."""
    files = discover_test_files(scripts_dir)
    for filename in LEGACY_REGRESSIONS:
        candidate = scripts_dir / filename
        if candidate.is_file() and candidate not in files:
            files.append(candidate)
    return sorted(files, key=lambda path: path.name)


def run_regressions(files: Sequence[Path]) -> int:
    """Execute every suite, stopping on first failure with visible provenance."""
    if not files:
        print("ERROR: no CS1 regression suites discovered", file=sys.stderr)
        return 2

    for path in files:
        command = command_for_test(path)
        try:
            relative = path.relative_to(ROOT)
        except ValueError:
            relative = path
        print(f"==> {relative}", flush=True)
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode != 0:
            print(
                f"FAIL {relative} (exit {completed.returncode})",
                file=sys.stderr,
                flush=True,
            )
            return completed.returncode or 1
        print(f"PASS {relative}", flush=True)

    print(f"PASS all {len(files)} CS1 regression suites", flush=True)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--list",
        action="store_true",
        help="list discovered regression suites without executing them",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = regression_files()
    if args.list:
        for path in files:
            print(path.relative_to(ROOT))
        return 0 if files else 2
    return run_regressions(files)


if __name__ == "__main__":
    raise SystemExit(main())
