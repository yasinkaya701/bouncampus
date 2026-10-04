#!/usr/bin/env python3
"""Discover and execute every registered CS1 behavior regression deterministically.

Normal CS1 behavior tests register themselves with the repository-level
``scripts/test_cs1_*`` naming contract. Python and TypeScript are the only
supported runtimes. Any other matching file fails closed instead of being
silently skipped.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
SUPPORTED_SUFFIXES = frozenset({".py", ".ts"})
LEGACY_REGRESSIONS = ("test_food_decision_policy.py",)


def discover_tests(scripts_dir: Path = SCRIPTS_DIR) -> list[Path]:
    """Return registered CS1 tests in stable order, rejecting unknown runtimes."""

    matches = sorted(
        (path for path in scripts_dir.glob("test_cs1_*") if path.is_file()),
        key=lambda path: path.name,
    )
    unsupported = [path.name for path in matches if path.suffix not in SUPPORTED_SUFFIXES]
    if unsupported:
        raise ValueError(
            "unsupported CS1 regression file type(s): " + ", ".join(unsupported)
        )
    return matches


def discover_test_files(scripts_dir: Path = SCRIPTS_DIR) -> list[Path]:
    """Compatibility alias for the dedicated CS1 gate contract."""

    return discover_tests(scripts_dir)


def regression_files(scripts_dir: Path = SCRIPTS_DIR) -> list[Path]:
    """Return normal CS1 suites plus explicitly retained legacy regressions."""

    files = discover_tests(scripts_dir)
    for filename in LEGACY_REGRESSIONS:
        candidate = scripts_dir / filename
        if candidate.is_file() and candidate not in files:
            files.append(candidate)
    return sorted(files, key=lambda path: path.name)


def command_for_test(test_path: Path) -> list[str]:
    """Return the explicit runtime command for one registered test."""

    path_text = str(test_path)
    if test_path.suffix == ".py":
        return [sys.executable, path_text]
    if test_path.suffix == ".ts":
        return ["node", "--experimental-strip-types", path_text]
    raise ValueError(f"unsupported CS1 regression: {test_path}")


def display_path(test_path: Path) -> Path:
    try:
        return test_path.relative_to(ROOT)
    except ValueError:
        return test_path


def run_regressions(files: Sequence[Path]) -> int:
    """Execute every suite, stopping on first failure with visible provenance."""

    if not files:
        print("ERROR: no CS1 regression suites discovered", file=sys.stderr)
        return 2

    for test_path in files:
        shown = display_path(test_path)
        print(f"==> {shown}", flush=True)
        completed = subprocess.run(
            command_for_test(test_path),
            cwd=ROOT,
            check=False,
        )
        if completed.returncode != 0:
            print(
                f"FAIL {shown} (exit {completed.returncode})",
                file=sys.stderr,
                flush=True,
            )
            return completed.returncode or 1
        print(f"PASS {shown}", flush=True)

    print(f"PASS all {len(files)} CS1 regression suites", flush=True)
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--list",
        action="store_true",
        help="list discovered regression suites without executing them",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    files = regression_files()
    if args.list:
        if not files:
            print("ERROR: no CS1 regression suites discovered", file=sys.stderr)
            return 2
        for test_path in files:
            print(display_path(test_path))
        return 0
    return run_regressions(files)


if __name__ == "__main__":
    raise SystemExit(main())
