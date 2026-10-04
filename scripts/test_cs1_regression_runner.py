#!/usr/bin/env python3
"""Contract tests for the centralized CS1 regression runner."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile

from run_cs1_regressions import command_for_test, discover_tests


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_discovers_python_and_typescript_in_stable_order() -> None:
    with tempfile.TemporaryDirectory() as raw:
        scripts = Path(raw)
        for name in (
            "test_cs1_zeta.ts",
            "test_cs1_alpha.py",
            "test_cs1_beta.ts",
            "not_cs1.py",
        ):
            (scripts / name).write_text("", encoding="utf-8")

        discovered = [path.name for path in discover_tests(scripts)]
        assert discovered == [
            "test_cs1_alpha.py",
            "test_cs1_beta.ts",
            "test_cs1_zeta.ts",
        ], discovered


def test_fails_closed_on_unsupported_cs1_test_type() -> None:
    with tempfile.TemporaryDirectory() as raw:
        scripts = Path(raw)
        (scripts / "test_cs1_valid.py").write_text("", encoding="utf-8")
        (scripts / "test_cs1_unregistered.sh").write_text("", encoding="utf-8")
        try:
            discover_tests(scripts)
        except ValueError as exc:
            assert "unsupported CS1 regression" in str(exc)
        else:
            raise AssertionError("unsupported test type must fail closed")


def test_commands_are_runtime_explicit() -> None:
    py_command = command_for_test(Path("scripts/test_cs1_example.py"))
    ts_command = command_for_test(Path("scripts/test_cs1_example.ts"))
    assert py_command[1:] == ["scripts/test_cs1_example.py"], py_command
    assert Path(py_command[0]).name.startswith("python"), py_command
    assert ts_command == [
        "node",
        "--experimental-strip-types",
        "scripts/test_cs1_example.ts",
    ], ts_command


def test_both_ci_workflows_use_the_central_runner() -> None:
    for workflow in (
        REPO_ROOT / ".github/workflows/ci.yml",
        REPO_ROOT / ".github/workflows/ci-hosted-fallback.yml",
    ):
        text = workflow.read_text(encoding="utf-8")
        assert "python scripts/run_cs1_regressions.py" in text, workflow


def test_list_mode_does_not_execute_regressions() -> None:
    runner_source = (REPO_ROOT / "scripts/run_cs1_regressions.py").read_text(
        encoding="utf-8"
    )
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        scripts = root / "scripts"
        scripts.mkdir()
        (scripts / "run_cs1_regressions.py").write_text(
            runner_source, encoding="utf-8"
        )
        (scripts / "test_cs1_probe.py").write_text(
            "from pathlib import Path\nPath('executed.txt').write_text('ran', encoding='utf-8')\n",
            encoding="utf-8",
        )

        completed = subprocess.run(
            [sys.executable, "scripts/run_cs1_regressions.py", "--list"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 0, completed.stderr
        assert "scripts/test_cs1_probe.py" in completed.stdout, completed.stdout
        assert not (root / "executed.txt").exists(), (
            "--list must enumerate regressions without executing them"
        )


if __name__ == "__main__":
    tests = [
        test_discovers_python_and_typescript_in_stable_order,
        test_fails_closed_on_unsupported_cs1_test_type,
        test_commands_are_runtime_explicit,
        test_both_ci_workflows_use_the_central_runner,
        test_list_mode_does_not_execute_regressions,
    ]
    for test in tests:
        test()
    print(f"ok: {len(tests)} CS1 regression-runner tests")
