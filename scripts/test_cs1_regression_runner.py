#!/usr/bin/env python3
"""Contract tests for deterministic CS1 regression discovery/execution."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "run_cs1_regressions.py"

if not RUNNER_PATH.exists():
    raise AssertionError("scripts/run_cs1_regressions.py must exist")

spec = importlib.util.spec_from_file_location("run_cs1_regressions", RUNNER_PATH)
assert spec is not None and spec.loader is not None
runner = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = runner
spec.loader.exec_module(runner)

with tempfile.TemporaryDirectory() as tmp:
    scripts_dir = Path(tmp)
    (scripts_dir / "test_cs1_zeta.py").write_text("print('py')\n", encoding="utf-8")
    (scripts_dir / "test_cs1_alpha.ts").write_text("console.log('ts');\n", encoding="utf-8")
    (scripts_dir / "test_cs1_notes.txt").write_text("ignore\n", encoding="utf-8")
    (scripts_dir / "other_test.py").write_text("ignore\n", encoding="utf-8")

    discovered = runner.discover_test_files(scripts_dir)
    assert [path.name for path in discovered] == ["test_cs1_alpha.ts", "test_cs1_zeta.py"]

python_command = runner.command_for_test(Path("scripts/test_cs1_example.py"))
assert python_command[0] == sys.executable
assert python_command[-1].endswith("test_cs1_example.py")

node_command = runner.command_for_test(Path("scripts/test_cs1_example.ts"))
assert node_command[0] == "node"
assert node_command[-1].endswith("test_cs1_example.ts")

try:
    runner.command_for_test(Path("scripts/test_cs1_example.txt"))
except ValueError as exc:
    assert "unsupported CS1 regression suffix" in str(exc)
else:
    raise AssertionError("unsupported suffix must fail closed")

print("PASS CS1 regression runner contract")
