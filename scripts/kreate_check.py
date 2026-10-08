#!/usr/bin/env python3
"""Mechanical validation for the lightweight KREATE operating system.

Default mode is safe for day-to-day CI and validates structure/integrity without
pretending unfinished PMR is complete. `--submission` enables the stricter
October 8 application gate.
"""

from __future__ import annotations

import argparse
import json
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
ALLOWED_INTERVIEW_STATUSES = {"TODO", "OUTREACH", "SCHEDULED", "COMPLETED", "CANCELLED"}
ALLOWED_EVIDENCE_TYPES = {
    "PUBLIC_SOURCE",
    "INTERVIEW",
    "TECH_TEST",
    "REPO_ARTIFACT",
    "MODEL_RESULT",
}
ALLOWED_CONFIDENCE = {"LOW", "MEDIUM", "HIGH"}
ALLOWED_DECISIONS = {"KEEP", "MODIFY", "KILL"}
ALLOWED_CLAIM_LABELS = {
    "FACT",
    "PUBLIC SOURCE",
    "INTERVIEW EVIDENCE",
    "TECHNICAL TEST",
    "MODEL ESTIMATE",
    "POLICY HEURISTIC",
    "HYPOTHESIS",
    "UNKNOWN",
}
ALLOWED_CLAIM_STATUSES = {"DRAFT", "READY", "CUT"}

EVIDENCE_PREFIX_TYPE = {
    "PUB": "PUBLIC_SOURCE",
    "INT": "INTERVIEW",
    "TECH": "TECH_TEST",
    "REP": "REPO_ARTIFACT",
    "MODEL": "MODEL_RESULT",
}
CLAIM_LABEL_REQUIRED_EVIDENCE_TYPE = {
    "PUBLIC SOURCE": "PUBLIC_SOURCE",
    "INTERVIEW EVIDENCE": "INTERVIEW",
    "TECHNICAL TEST": "TECH_TEST",
    "MODEL ESTIMATE": "MODEL_RESULT",
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

APPLICATION_HEADINGS = [
    "Team — 20%",
    "Problem — 20%",
    "Beachhead Market — 10%",
    "Persona — 10%",
    "Primary Market Research — 40%",
    "Submission claim ledger",
    "Final claim sign-off",
]

REQUIRED_ISSUE_FIELD_IDS = {
    "why",
    "owner",
    "workstream",
    "priority",
    "dependency",
    "deliverable",
    "acceptance",
    "evidence",
    "kill",
    "deadline",
    "reviewer",
}

BANNED_SLOP_TERMS = {
    "revolutionary",
    "groundbreaking",
    "transformative",
    "seamless",
    "cutting-edge",
    "unique",
    "real-time",
    "ai-powered",
}

EVIDENCE_ID_RE = re.compile(r"\bE-(?:PUB|INT|TECH|REP|MODEL)-\d{3}\b")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def strip_md(text: str) -> str:
    return text.replace("`", "").replace("**", "").strip()


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def extract_evidence_ids(text: str) -> list[str]:
    return EVIDENCE_ID_RE.findall(strip_md(text))


def is_placeholder(text: str) -> bool:
    value = strip_md(text).strip()
    return not value or value in {"—", "-"} or value.upper().startswith("TODO")


def section_has_content(markdown: str, heading: str) -> bool:
    lines = markdown.splitlines()
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", flags=re.IGNORECASE)
    for index, line in enumerate(lines):
        if not pattern.match(line.strip()):
            continue
        for following in lines[index + 1 :]:
            stripped = following.strip()
            if stripped.startswith("## "):
                return False
            if stripped and not stripped.startswith("<!--"):
                return True
        return False
    return False


def check_required_files(errors: list[str]) -> None:
    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")


def parse_evidence_registry(errors: list[str], submission: bool) -> dict[str, dict[str, str]]:
    path = "KREATE/EVIDENCE.md"
    if not (ROOT / path).is_file():
        return {}

    evidence: dict[str, dict[str, str]] = {}
    for line_number, line in enumerate(read(path).splitlines(), start=1):
        if not re.match(r"^\|\s*E-(?:PUB|INT|TECH|REP|MODEL)-\d{3}\s*\|", line):
            continue
        row = cells(line)
        if len(row) != 8:
            errors.append(f"{path}:{line_number}: malformed evidence row; expected 8 columns")
            continue
        evidence_id, evidence_type, claim, source, date, owner, confidence, notes = row
        evidence_id = strip_md(evidence_id)
        evidence_type = strip_md(evidence_type)
        confidence = strip_md(confidence)

        if evidence_id in evidence:
            errors.append(f"{path}:{line_number}: duplicate evidence ID {evidence_id}")
            continue
        if evidence_type not in ALLOWED_EVIDENCE_TYPES:
            errors.append(f"{path}:{line_number}: invalid evidence type {evidence_type!r}")
        if confidence not in ALLOWED_CONFIDENCE:
            errors.append(f"{path}:{line_number}: invalid confidence {confidence!r}")

        prefix = evidence_id.split("-")[1]
        expected_type = EVIDENCE_PREFIX_TYPE.get(prefix)
        if expected_type and evidence_type != expected_type:
            errors.append(
                f"{path}:{line_number}: {evidence_id} prefix requires type {expected_type}, found {evidence_type}"
            )
        if is_placeholder(claim) or is_placeholder(source) or is_placeholder(owner):
            errors.append(f"{path}:{line_number}: evidence rows require claim, source/artifact, and owner")
        if evidence_type == "INTERVIEW" and "TODO" in strip_md(date).upper():
            errors.append(f"{path}:{line_number}: interview evidence cannot have a TODO date")

        evidence[evidence_id] = {
            "type": evidence_type,
            "claim": strip_md(claim),
            "source": strip_md(source),
            "date": strip_md(date),
            "owner": strip_md(owner),
            "confidence": confidence,
            "notes": strip_md(notes),
        }

    if submission and "E-PUB-001" in evidence and "TODO" in evidence["E-PUB-001"]["date"].upper():
        errors.append("submission gate: E-PUB-001 still requires human re-verification/date before submission")
    return evidence


def check_interview_tracker(
    errors: list[str], evidence: dict[str, dict[str, str]], submission: bool
) -> None:
    path = "KREATE/PMR/INTERVIEW_TRACKER.md"
    if not (ROOT / path).is_file():
        return

    rows: dict[str, list[str]] = {}
    for line_number, line in enumerate(read(path).splitlines(), start=1):
        if not re.match(r"^\|\s*(?:IE|EE|CS1|CS2)-\d{2}\s*\|", line):
            continue
        row = cells(line)
        if len(row) != 11:
            errors.append(f"{path}:{line_number}: malformed tracker row; expected 11 columns")
            continue
        interview_id = strip_md(row[0])
        if interview_id in rows:
            errors.append(f"{path}:{line_number}: duplicate interview slot {interview_id}")
            continue
        rows[interview_id] = row

        lead = strip_md(row[1])
        expected_lead = interview_id.split("-")[0]
        if lead != expected_lead:
            errors.append(f"{path}:{line_number}: {interview_id} must be led by {expected_lead}, found {lead}")

        status = strip_md(row[5]).upper()
        if status not in ALLOWED_INTERVIEW_STATUSES:
            errors.append(f"{path}:{line_number}: invalid interview status {status!r}")
            continue
        if status == "SCHEDULED" and is_placeholder(row[6]):
            errors.append(f"{path}:{line_number}: SCHEDULED requires a scheduled date/time")
        if status == "COMPLETED":
            for index, label in ((2, "note-taker"), (3, "stakeholder type"), (4, "organization type"), (7, "completed date")):
                if is_placeholder(row[index]):
                    errors.append(f"{path}:{line_number}: COMPLETED requires {label}")

            evidence_cell = strip_md(row[8])
            if is_placeholder(evidence_cell):
                errors.append(
                    f"{path}:{line_number}: COMPLETED requires E-INT evidence IDs or 'NONE — no promotable claim'"
                )
            elif not evidence_cell.upper().startswith("NONE"):
                linked_ids = extract_evidence_ids(evidence_cell)
                if not linked_ids:
                    errors.append(f"{path}:{line_number}: completed interview evidence link has no valid evidence ID")
                for evidence_id in linked_ids:
                    item = evidence.get(evidence_id)
                    if item is None:
                        errors.append(f"{path}:{line_number}: unknown linked evidence ID {evidence_id}")
                    elif item["type"] != "INTERVIEW":
                        errors.append(
                            f"{path}:{line_number}: completed interview must link INTERVIEW evidence, {evidence_id} is {item['type']}"
                        )

    found = set(rows)
    if found != EXPECTED_INTERVIEW_IDS:
        missing = sorted(EXPECTED_INTERVIEW_IDS - found)
        extra = sorted(found - EXPECTED_INTERVIEW_IDS)
        errors.append(
            f"interview tracker slots mismatch: expected 16 exact slots; missing={missing}, extra={extra}"
        )

    if submission:
        completed = sum(1 for row in rows.values() if strip_md(row[5]).upper() == "COMPLETED")
        if completed < 12:
            errors.append(f"submission gate: hard minimum is 12 completed interviews; found {completed}")


def check_assumptions(errors: list[str], evidence: dict[str, dict[str, str]]) -> None:
    path = "KREATE/ASSUMPTIONS.md"
    if not (ROOT / path).is_file():
        return
    for line_number, line in enumerate(read(path).splitlines(), start=1):
        if not re.match(r"^\|\s*H-\d+\s*\|", line):
            continue
        row = cells(line)
        if len(row) != 9:
            errors.append(f"{path}:{line_number}: malformed assumption row; expected 9 columns")
            continue
        status = strip_md(row[5]).upper()
        if status not in ALLOWED_ASSUMPTION_STATUSES:
            errors.append(f"{path}:{line_number}: invalid status {status!r}")
            continue
        referenced = extract_evidence_ids(row[4])
        for evidence_id in referenced:
            if evidence_id not in evidence:
                errors.append(f"{path}:{line_number}: unknown evidence ID {evidence_id}")
        if status in {"SUPPORTED", "REJECTED", "CONFLICTING"} and not referenced:
            errors.append(f"{path}:{line_number}: {status} requires traceable evidence IDs")


def check_decisions(errors: list[str], evidence: dict[str, dict[str, str]]) -> None:
    path = "KREATE/DECISIONS.md"
    if not (ROOT / path).is_file():
        return
    seen: set[str] = set()
    for line_number, line in enumerate(read(path).splitlines(), start=1):
        if not re.match(r"^\|\s*D-\d+\s*\|", line):
            continue
        row = cells(line)
        if len(row) != 8:
            errors.append(f"{path}:{line_number}: malformed decision row; expected 8 columns")
            continue
        decision_id = strip_md(row[0])
        if decision_id in seen:
            errors.append(f"{path}:{line_number}: duplicate decision ID {decision_id}")
        seen.add(decision_id)
        outcome = strip_md(row[6]).upper()
        if outcome not in ALLOWED_DECISIONS:
            errors.append(f"{path}:{line_number}: invalid decision outcome {outcome!r}")
        for evidence_id in extract_evidence_ids(row[3]):
            if evidence_id not in evidence:
                errors.append(f"{path}:{line_number}: unknown evidence ID {evidence_id}")


def check_claim_ledger(
    errors: list[str], warnings: list[str], evidence: dict[str, dict[str, str]], submission: bool
) -> None:
    path = "KREATE/APPLICATION_RUBRIC.md"
    if not (ROOT / path).is_file():
        return

    claim_rows: list[list[str]] = []
    seen: set[str] = set()
    for line_number, line in enumerate(read(path).splitlines(), start=1):
        if not re.match(r"^\|\s*C-\d{3}\s*\|", line):
            continue
        row = cells(line)
        if len(row) != 8:
            errors.append(f"{path}:{line_number}: malformed claim-ledger row; expected 8 columns")
            continue
        claim_rows.append(row)
        claim_id = strip_md(row[0])
        if claim_id in seen:
            errors.append(f"{path}:{line_number}: duplicate claim ID {claim_id}")
        seen.add(claim_id)

        label = strip_md(row[2]).upper()
        status = strip_md(row[6]).upper()
        if label not in ALLOWED_CLAIM_LABELS:
            errors.append(f"{path}:{line_number}: invalid claim label {label!r}")
        if status not in ALLOWED_CLAIM_STATUSES:
            errors.append(f"{path}:{line_number}: invalid claim status {status!r}")
            continue

        referenced = extract_evidence_ids(row[3])
        for evidence_id in referenced:
            if evidence_id not in evidence:
                errors.append(f"{path}:{line_number}: claim references unknown evidence ID {evidence_id}")

        if status == "READY":
            for index, field_name in ((1, "claim"), (4, "domain owner"), (5, "human reviewer")):
                if is_placeholder(row[index]):
                    errors.append(f"{path}:{line_number}: READY requires non-placeholder {field_name}")
            if label not in {"HYPOTHESIS", "UNKNOWN", "POLICY HEURISTIC"} and not referenced:
                errors.append(f"{path}:{line_number}: READY {label} claim requires evidence IDs")
            required_type = CLAIM_LABEL_REQUIRED_EVIDENCE_TYPE.get(label)
            if required_type and referenced:
                actual_types = {evidence[eid]["type"] for eid in referenced if eid in evidence}
                if required_type not in actual_types:
                    errors.append(
                        f"{path}:{line_number}: {label} requires at least one {required_type} evidence item"
                    )
            lowered = strip_md(row[1]).lower()
            terms = sorted(term for term in BANNED_SLOP_TERMS if term in lowered)
            if terms:
                warnings.append(
                    f"{path}:{line_number}: READY claim contains anti-slop term(s) {terms}; human reviewer must justify or rewrite"
                )

    if submission:
        if not claim_rows:
            errors.append("submission gate: claim ledger has no material application claims")
            return
        draft_ids = [strip_md(row[0]) for row in claim_rows if strip_md(row[6]).upper() == "DRAFT"]
        if draft_ids:
            errors.append(f"submission gate: claim ledger still contains DRAFT rows: {draft_ids}")
        if not any(strip_md(row[6]).upper() == "READY" for row in claim_rows):
            errors.append("submission gate: claim ledger has no READY claims")


def check_template_headings(errors: list[str]) -> None:
    checks = {
        "KREATE/PMR/INTERVIEW_TEMPLATE.md": INTERVIEW_TEMPLATE_HEADINGS,
        "KREATE/EXPERIMENTS/EXPERIMENT_TEMPLATE.md": EXPERIMENT_HEADINGS,
        "KREATE/APPLICATION_RUBRIC.md": APPLICATION_HEADINGS,
    }
    for path, headings in checks.items():
        if not (ROOT / path).is_file():
            continue
        content = read(path)
        for heading in headings:
            if not section_has_content(content, heading):
                errors.append(f"{path}: missing or empty mandatory heading: {heading}")


def check_local_markdown_links(errors: list[str]) -> None:
    kreate_root = ROOT / "KREATE"
    if not kreate_root.is_dir():
        return
    for file_path in kreate_root.rglob("*.md"):
        content = file_path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_RE.findall(content):
            target = target.strip().strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            resolved = (file_path.parent / clean).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{file_path.relative_to(ROOT)}: local link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{file_path.relative_to(ROOT)}: broken local link: {target}")


def check_github_templates(errors: list[str]) -> None:
    issue_path = ".github/ISSUE_TEMPLATE/kreate-task.yml"
    if (ROOT / issue_path).is_file():
        found_ids = set(re.findall(r"^\s+id:\s*([A-Za-z0-9_-]+)\s*$", read(issue_path), flags=re.MULTILINE))
        missing = sorted(REQUIRED_ISSUE_FIELD_IDS - found_ids)
        if missing:
            errors.append(f"{issue_path}: missing required fields {missing}")

    pr_path = ".github/PULL_REQUEST_TEMPLATE.md"
    if (ROOT / pr_path).is_file():
        content = read(pr_path).lower()
        for phrase in ("ai-generated", "human reviewer", "no fabricated", "known limitations", "evidence ids / artifacts"):
            if phrase not in content:
                errors.append(f"{pr_path}: missing KREATE review gate phrase {phrase!r}")


def check_food_decision_integrity(errors: list[str]) -> None:
    """Protect the CS1 truth boundary in every active food-decision surface."""

    required_paths = [
        "backend/app/decision/food_policy.py",
        "backend/app/decision/baselines.py",
        "backend/app/routers/food.py",
        "backend/app/routers/dashboard.py",
        "backend/app/routers/actions.py",
        "backend/app/optimizers/food_optimizer.py",
        "backend/app/models/food_demand.py",
        "backend/app/schemas.py",
        "frontend/src/lib/food-waste.ts",
        "frontend/src/app/api/v1/food/route.ts",
        "frontend/src/app/api/v1/food/pilot-score/route.ts",
        "scripts/cs1_baseline_benchmark.py",
    ]
    for path in required_paths:
        if not (ROOT / path).is_file():
            errors.append(f"food decision integrity: missing required CS1 artifact {path}")
    if any(not (ROOT / path).is_file() for path in required_paths):
        return

    backend_policy = read("backend/app/decision/food_policy.py")
    frontend_policy = read("frontend/src/lib/food-waste.ts")
    backend_route = read("backend/app/routers/food.py")
    dashboard_route = read("backend/app/routers/dashboard.py")
    actions_route = read("backend/app/routers/actions.py")
    optimizer = read("backend/app/optimizers/food_optimizer.py")
    schemas = read("backend/app/schemas.py")
    food_schema = schemas.split("class FoodDemandForecast", 1)[-1].split("class ActionItem", 1)[0]
    next_route = read("frontend/src/app/api/v1/food/route.ts")
    pilot_route = read("frontend/src/app/api/v1/food/pilot-score/route.ts")
    benchmark = read("scripts/cs1_baseline_benchmark.py")

    forbidden_food_terms = ("potential_waste_saved_kg", "waste_reduction", "cost_saved_tl")
    for path, content in (
        ("backend/app/routers/food.py", backend_route),
        ("backend/app/optimizers/food_optimizer.py", optimizer),
        ("backend/app/schemas.py::FoodDemandForecast", food_schema),
    ):
        for term in forbidden_food_terms:
            if term in content:
                errors.append(f"food decision integrity: unsupported pre-pilot field {term!r} found in {path}")

    dashboard_forbidden = ("food_waste_saved_kg", "food_waste_avoided_kg=40.0", "base_meals * 1.15")
    for term in dashboard_forbidden:
        if term in dashboard_route:
            errors.append(f"food decision integrity: legacy food-impact claim {term!r} found in dashboard")
    action_forbidden = ("Pre-portion 1,420", "impact_value=48.0", 'impact_unit="kg"')
    for term in action_forbidden:
        if term in actions_route:
            errors.append(f"food decision integrity: legacy food-impact claim {term!r} found in actions route")

    for marker in ("food_waste_avoided_kg=None", 'food_waste_impact_status="UNMEASURED"'):
        if marker not in dashboard_route:
            errors.append(f"food decision integrity: dashboard missing unmeasured-impact marker {marker!r}")
    for path, content in (("dashboard", dashboard_route), ("actions", actions_route)):
        for marker in ("MODEL_ESTIMATE", "POLICY_HEURISTIC", "automatic kitchen dispatch"):
            if marker.lower() not in content.lower():
                errors.append(f"food decision integrity: {path} surface missing {marker!r}")

    backend_markers = (
        "POLICY_HEURISTIC",
        "MODEL_ESTIMATE",
        "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL",
        "NOT_CALIBRATED",
        "operator_approval_required",
        "automatic_kitchen_dispatch",
        "WITHHOLD",
        "PILOT_READY",
    )
    for marker in backend_markers:
        if marker not in backend_policy:
            errors.append(f"food decision integrity: backend policy missing {marker!r}")

    frontend_markers = (
        "POLICY_HEURISTIC",
        "MODEL_ESTIMATE",
        "PLANNING_RANGE_NOT_CALIBRATED_INTERVAL",
        "NOT_CALIBRATED",
        "operatorApprovalRequired",
        "autoDispatchAllowed",
        "abstained",
    )
    for marker in frontend_markers:
        if marker not in frontend_policy:
            errors.append(f"food decision integrity: frontend policy missing {marker!r}")

    for marker in (
        "humanApprovalRequired",
        "automaticKitchenDispatch",
        "forbiddenUntilMeasured",
        "decisionAssessment",
        "READY_FOR_MEASURED_DATA",
    ):
        if marker not in next_route:
            errors.append(f"food decision integrity: Next food API missing truth-boundary marker {marker!r}")

    for marker in ("dataQualityPassed", "promotableAsGeneralizedClimateImpact", "false"):
        if marker not in pilot_route:
            errors.append(f"food decision integrity: pilot evidence gate missing {marker!r}")

    if "OFFLINE_BENCHMARK_ONLY" not in benchmark or "TECH_TEST" not in benchmark:
        errors.append("food decision integrity: baseline benchmark must remain scoped to TECH_TEST/OFFLINE_BENCHMARK_ONLY")
    if "food-waste" not in next_route.lower() and "food waste" not in next_route.lower():
        errors.append("food decision integrity: food API lost explicit food-waste claim boundary context")



def check_pmr_source_integrity(errors: list[str]) -> None:
    """Keep PMR source IDs unique and acquisition-tracker routes resolvable."""

    catalog_path = "KREATE/PMR/source_catalog.json"
    tracker_path = "KREATE/PMR/ie_acquisition_tracker.json"
    if not (ROOT / catalog_path).is_file() or not (ROOT / tracker_path).is_file():
        return

    try:
        catalog = json.loads(read(catalog_path))
    except json.JSONDecodeError as exc:
        errors.append(f"{catalog_path}: invalid JSON: {exc}")
        return
    try:
        tracker = json.loads(read(tracker_path))
    except json.JSONDecodeError as exc:
        errors.append(f"{tracker_path}: invalid JSON: {exc}")
        return

    sources = catalog.get("sources")
    if not isinstance(sources, list):
        errors.append(f"{catalog_path}: top-level 'sources' must be a list")
        return

    source_ids: list[str] = []
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"{catalog_path}: sources[{index}] must be an object")
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id.strip():
            errors.append(f"{catalog_path}: sources[{index}] has missing/invalid id")
            continue
        source_ids.append(source_id)

    seen: set[str] = set()
    duplicate_ids: set[str] = set()
    for source_id in source_ids:
        if source_id in seen:
            duplicate_ids.add(source_id)
        seen.add(source_id)
    if duplicate_ids:
        errors.append(f"{catalog_path}: duplicate source IDs: {sorted(duplicate_ids)}")

    workstreams = tracker.get("workstreams")
    if not isinstance(workstreams, list):
        errors.append(f"{tracker_path}: top-level 'workstreams' must be a list")
        return

    known_ids = set(source_ids)
    for index, workstream in enumerate(workstreams):
        if not isinstance(workstream, dict):
            errors.append(f"{tracker_path}: workstreams[{index}] must be an object")
            continue
        issue = workstream.get("issue", "?")
        routes = workstream.get("routes", [])
        if not isinstance(routes, list):
            errors.append(f"{tracker_path}: issue {issue} routes must be a list")
            continue
        for route in routes:
            if not isinstance(route, str) or not route.strip():
                errors.append(f"{tracker_path}: issue {issue} has invalid route reference {route!r}")
            elif route not in known_ids:
                errors.append(f"{tracker_path}: issue {issue} references unknown source ID {route}")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--submission",
        action="store_true",
        help="enforce the final application gate (12+ completed PMR interviews, verified public source, no draft claims)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    warnings: list[str] = []

    check_required_files(errors)
    evidence = parse_evidence_registry(errors, args.submission)
    check_interview_tracker(errors, evidence, args.submission)
    check_assumptions(errors, evidence)
    check_decisions(errors, evidence)
    check_claim_ledger(errors, warnings, evidence, args.submission)
    check_template_headings(errors)
    check_local_markdown_links(errors)
    check_github_templates(errors)
    check_pmr_source_integrity(errors)
    check_food_decision_integrity(errors)

    mode = "SUBMISSION" if args.submission else "CI"
    if warnings:
        print(f"KREATE {mode} warnings:")
        for warning in warnings:
            print(f"- {warning}")

    if errors:
        print(f"KREATE {mode} validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"KREATE {mode} validation PASSED")
    print("- required operating files present")
    print("- evidence IDs/types/confidence and cross-references are mechanically consistent")
    print("- 16 exact interview slots and tracker state rules are valid")
    print("- assumption and decision states are valid")
    print("- claim-ledger labels/evidence/reviewer gates are valid")
    print("- mandatory template/application headings are present and non-empty")
    print("- local KREATE markdown links resolve")
    print("- GitHub task/PR anti-slop review gates are present")
    print("- PMR source IDs are unique and IE acquisition routes resolve")
    print("- food decision policy, abstention, provenance, baseline scope, active-surface firewall, and pilot evidence gates are intact")
    if args.submission:
        print("- hard minimum PMR count and final submission gates are satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
