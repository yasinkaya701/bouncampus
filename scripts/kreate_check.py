#!/usr/bin/env python3
"""Mechanical validation for the lightweight KREATE operating system."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "KREATE/README.md",
    "KREATE/STATUS.md",
    "KREATE/ASSUMPTIONS.md",
    "KREATE/EVIDENCE.md",
    "KREATE/PMR/INTERVIEW_TEMPLATE.md",
    "KREATE/PMR/INTERVIEW_TRACKER.md",
    "KREATE/DECISIONS.md",
    "KREATE/EXPERIMENTS/EXPERIMENT_TEMPLATE.md",
    "KREATE/FEATURES.md",
    "KREATE/APPLICATION_RUBRIC.md",
    ".github/ISSUE_TEMPLATE/kreate-task.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
]

ALLOWED_ASSUMPTION_STATUSES = {
    "UNKNOWN",
    "TESTING",
    "SUPPORTED",
    "REJECTED",
    "CONFLICTING",
}

EXPECTED_INTERVIEW_IDS = {
    *(f"IE-{i:02d}" for i in range(1, 5)),
    *(f"EE-{i:02d}" for i in range(1, 5)),
    *(f"CS1-{i:02d}" for i in range(1, 5)),
    *(f"CS2-{i:02d}" for i in range(1, 5)),
}

INTERVIEW_TEMPLATE_HEADINGS = [
    "Interview metadata",
    "Screener",
    "Hypotheses tested",
    "Last concrete incident / story",
    "Current workflow",
    "Decision owner",
    "Data used / available",
    "Failure / risk",
    "Workaround",
    "Exact quotes",
    "Objections",
    "Referral",
    "Evidence IDs created",
    "What changed in our assumptions / product",
    "Follow-up",
]

EXPERIMENT_HEADINGS = [
    "QUESTION",
    "HYPOTHESIS",
    "WHY IT MATTERS",
    "OWNER",
    "TIMEBOX",
    "METHOD",
    "INPUTS",
    "SUCCESS CONDITION",
    "FAILURE CONDITION",
    "RAW EVIDENCE LOCATION",
    "RESULT",
    "DECISION: KEEP / MODIFY / KILL",
    "LIMITATIONS",
    "NEXT STEP",
]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def check_required_files(errors: list[str]) -> None:
    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")


def check_interview_slots(errors: list[str]) -> None:
    path = "KREATE/PMR/INTERVIEW_TRACKER.md"
    if not (ROOT / path).is_file():
        return
    content = read(path)
    found = set(re.findall(r"^\|\s*((?:IE|EE|CS1|CS2)-\d{2})\s*\|", content, flags=re.MULTILINE))
    if found != EXPECTED_INTERVIEW_IDS:
        missing = sorted(EXPECTED_INTERVIEW_IDS - found)
        extra = sorted(found - EXPECTED_INTERVIEW_IDS)
        errors.append(
            f"interview tracker slots mismatch: expected 16 exact slots; missing={missing}, extra={extra}"
        )


def check_assumption_statuses(errors: list[str]) -> None:
    path = "KREATE/ASSUMPTIONS.md"
    if not (ROOT / path).is_file():
        return
    for line_number, line in enumerate(read(path).splitlines(), start=1):
        if not re.match(r"^\|\s*H-\d+\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 9:
            errors.append(f"{path}:{line_number}: malformed assumption row")
            continue
        status = cells[5]
        if status not in ALLOWED_ASSUMPTION_STATUSES:
            errors.append(
                f"{path}:{line_number}: invalid status {status!r}; allowed={sorted(ALLOWED_ASSUMPTION_STATUSES)}"
            )


def section_has_content(markdown: str, heading: str) -> bool:
    lines = markdown.splitlines()
    heading_index = None
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", flags=re.IGNORECASE)
    for index, line in enumerate(lines):
        if pattern.match(line.strip()):
            heading_index = index
            break
    if heading_index is None:
        return False
    for line in lines[heading_index + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if stripped and not stripped.startswith("<!--"):
            return True
    return False


def check_template_headings(errors: list[str]) -> None:
    checks = {
        "KREATE/PMR/INTERVIEW_TEMPLATE.md": INTERVIEW_TEMPLATE_HEADINGS,
        "KREATE/EXPERIMENTS/EXPERIMENT_TEMPLATE.md": EXPERIMENT_HEADINGS,
    }
    for path, headings in checks.items():
        if not (ROOT / path).is_file():
            continue
        content = read(path)
        for heading in headings:
            if not section_has_content(content, heading):
                errors.append(f"{path}: missing or empty mandatory heading: {heading}")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_interview_slots(errors)
    check_assumption_statuses(errors)
    check_template_headings(errors)

    if errors:
        print("KREATE validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("KREATE validation PASSED")
    print("- required files present")
    print("- 16 exact interview TODO slots present")
    print("- assumption statuses valid")
    print("- mandatory template headings present and non-empty")
    return 0


if __name__ == "__main__":
    sys.exit(main())
