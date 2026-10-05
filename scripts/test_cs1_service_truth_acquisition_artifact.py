#!/usr/bin/env python3
"""Contract tests for the #82 service-truth acquisition handoff artifact."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "KREATE/EXPERIMENTS/SERVICE_TRUTH_ACQUISITION_V1.json"


def load_contract():
    path = ROOT / "backend/app/decision/service_truth.py"
    spec = importlib.util.spec_from_file_location("service_truth", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_artifact() -> dict:
    assert ARTIFACT.exists(), f"missing acquisition artifact: {ARTIFACT.relative_to(ROOT)}"
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def test_artifact_is_explicitly_unverified_and_contains_no_fake_measured_rows() -> None:
    artifact = load_artifact()
    assert artifact["contract_version"] == "SERVICE_TRUTH_V1"
    assert artifact["artifact_status"] == "ACQUISITION_TEMPLATE_UNVERIFIED"
    assert artifact["measured_rows"] == []
    assert artifact["benchmark_eligible"] is False
    assert artifact["pilot_evidence_eligible"] is False
    assert "real measured" in artifact["claim_boundary"].lower()


def test_source_contract_is_structurally_complete_but_not_verified() -> None:
    artifact = load_artifact()
    contract = load_contract()
    result = contract.validate_service_truth_source_contract(artifact["field_provenance"])

    assert result["source_contract_complete"] is True
    assert result["source_contract_verified"] is False
    assert result["missing_source_contract_fields"] == []
    assert set(result["unverified_source_contract_fields"]) == set(
        artifact["field_provenance"]
    )


def test_every_required_field_has_an_operational_acquisition_question() -> None:
    artifact = load_artifact()
    contract = load_contract()
    questions = artifact["acquisition_questions"]

    assert set(contract.REQUIRED_SOURCE_CONTRACT_FIELDS).issubset(questions)
    for field in contract.REQUIRED_SOURCE_CONTRACT_FIELDS:
        question = questions[field]
        assert isinstance(question, str) and question.strip()
        assert "?" in question


def test_empty_template_fails_closed_if_accidentally_sent_to_dataset_admission() -> None:
    artifact = load_artifact()
    contract = load_contract()
    result = contract.validate_service_truth_dataset(artifact["measured_rows"])

    assert result["validation_status"] == "REJECTED"
    assert result["eligible_for_benchmark"] is False
    assert "INSUFFICIENT_CHRONOLOGICAL_SERVICES" in result["reason_codes"]


def test_hardware_candidates_remain_candidates_not_accepted_truth() -> None:
    artifact = load_artifact()
    candidates = artifact["candidate_measurement_paths"]

    assert candidates["produced_portions"]["status"] == "CANDIDATE_UNVERIFIED"
    assert candidates["actual_served"]["status"] == "CANDIDATE_UNVERIFIED"
    assert candidates["surplus_or_waste"]["status"] == "CANDIDATE_UNVERIFIED"
    assert "Production Count Node" in candidates["produced_portions"]["source"]
    assert "Serving Line Counter" in candidates["actual_served"]["source"]
    assert "TrayGate" in candidates["surplus_or_waste"]["source"]


def test_bucard_served_count_mapping_to_actual_served_stays_fail_closed() -> None:
    artifact = load_artifact()
    route = artifact["data_access_routes"]["served_count_bucard"]
    mapping = route["contract_mapping"]

    assert mapping["source_field"] == "served_count"
    assert mapping["target_field"] == "actual_served"
    assert mapping["status"] == "SEMANTIC_MAPPING_UNVERIFIED"
    assert "reconcil" in mapping["required_confirmation"].lower()
    assert "must not" in mapping["admission_rule"].lower()
    assert "actual_served" in mapping["admission_rule"]

    provenance = artifact["field_provenance"]["actual_served"]
    assert provenance["verification_status"] == "UNVERIFIED"
    assert "UNVERIFIED" in provenance["data_access_status"]

    requested_fields = {field.casefold() for field in route["minimum_requested_export_fields"]}
    banned_fragments = ("student", "person", "card", "transaction", "email", "phone")
    assert all(
        not any(fragment in field for fragment in banned_fragments)
        for field in requested_fields
    )


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service-truth acquisition artifact tests")
