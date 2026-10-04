#!/usr/bin/env python3
"""Run every registered CS1 behavior regression deterministically.

Normal CS1 behavior tests register themselves by using the repository-level
`scripts/test_cs1_*` naming contract. Python and TypeScript are the only
supported runtimes; an unknown matching file fails closed instead of being
silently skipped.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


SUPPORTED_SUFFIXES = frozenset({".py", ".ts"})
LEGACY_EXTRAS = ("test_food_decision_policy.py",)


def discover_tests(scripts_dir: Path) -> list[Path]:
    """Return registered CS1 tests in stable lexical order."""

    matches = sorted(
        (path for path in scripts_dir.glob("test_cs1_*") if path.is_file()),
        key=lambda path: path.name,
    )
    unsupported = [path.name for path in matches if path.suffix not in SUPPORTED_SUFFIXES]
    if unsupported:
        raise ValueError(
            "unsupported CS1 regression file type(s): " + ", ".join(unsupported)
        )
    if not matches:
        raise RuntimeError(f"no CS1 regressions found in {scripts_dir}")
    return matches


def command_for_test(test_path: Path) -> list[str]:
    """Return the explicit runtime command for one registered test."""

    path_text = test_path.as_posix()
    if test_path.suffix == ".py":
        return [sys.executable, path_text]
    if test_path.suffix == ".ts":
        return ["node", "--experimental-strip-types", path_text]
    raise ValueError(f"unsupported CS1 regression: {test_path}")


def run_test(test_path: Path) -> None:
    command = command_for_test(test_path)
    print(f"==> {test_path.as_posix()}", flush=True)
    subprocess.run(command, check=True)


def main() -> int:
    scripts_dir = Path("scripts")
    tests = discover_tests(scripts_dir)
    for test_path in tests:
        run_test(test_path)

    for filename in LEGACY_EXTRAS:
        extra = scripts_dir / filename
        if extra.is_file():
            run_test(extra)

    print(f"ok: executed {len(tests)} registered CS1 regressions", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
