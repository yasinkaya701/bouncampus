#!/usr/bin/env python3
"""Contract tests for CS1 service-truth source ownership/provenance manifests."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_contract():
    path = ROOT / "backend/app/decision/service_truth.py"
    spec = importlib.util.spec_from_file_location("service_truth", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_contract(*, verification_status: str = "UNVERIFIED") -> dict:
    def entry(owner: str, source_system: str, availability_semantics: str) -> dict:
        return {
            "owner": owner,
            "source_system": source_system,
            "availability_semantics": availability_semantics,
            "verification_status": verification_status,
        }

    return {
        "actual_served": entry(
            "DINING_OPERATIONS_OWNER_TO_BE_CONFIRMED",
            "SERVICE_RECONCILIATION_EXPORT_TO_BE_CONFIRMED",
            "POST_SERVICE_RECONCILED",
        ),
        "produced_portions": entry(
            "DINING_OPERATIONS_OWNER_TO_BE_CONFIRMED",
            "PRODUCTION_RECORD_TO_BE_CONFIRMED",
            "POST_PRODUCTION_RECORDED",
        ),
        "surplus_or_waste": entry(
            "DINING_OPERATIONS_OWNER_TO_BE_CONFIRMED",
            "SURPLUS_OR_WASTE_RECORD_TO_BE_CONFIRMED",
            "POST_SERVICE_MEASURED",
        ),
        "shortage_or_early_sellout": entry(
            "DINING_OPERATIONS_OWNER_TO_BE_CONFIRMED",
            "SERVICE_STATUS_RECORD_TO_BE_CONFIRMED",
            "POST_SERVICE_RECORDED",
        ),
        "operator_status_quo_quantity": entry(
            "DINING_OPERATIONS_OWNER_TO_BE_CONFIRMED",
            "OPERATOR_PLAN_TO_BE_CONFIRMED",
            "MUST_EXIST_BY_DECISION_CUTOFF",
        ),
        "menu": entry(
            "OFFICIAL_DINING_MENU",
            "OFFICIAL_MENU_SNAPSHOT",
            "MUST_EXIST_BY_DECISION_CUTOFF",
        ),
        "academic_calendar": entry(
            "OFFICIAL_ACADEMIC_CALENDAR",
            "OFFICIAL_CALENDAR_SNAPSHOT",
            "MUST_EXIST_BY_DECISION_CUTOFF",
        ),
        "weather_forecast": entry(
            "ARCHIVED_FORECAST_PROVIDER_TO_BE_CONFIRMED",
            "HISTORICAL_FORECAST_SNAPSHOT_TO_BE_CONFIRMED",
            "FORECAST_MUST_HAVE_BEEN_AVAILABLE_BY_DECISION_CUTOFF",
        ),
    }


def test_source_contract_hash_is_deterministic_and_verification_is_separate() -> None:
    contract = load_contract()
    manifest = source_contract()
    first = contract.validate_service_truth_source_contract(manifest)
    second = contract.validate_service_truth_source_contract(
        dict(reversed(list(manifest.items())))
    )

    assert first["source_contract_complete"] is True
    assert first["source_contract_verified"] is False
    assert first["source_contract_sha256"] == second["source_contract_sha256"]
    assert len(first["source_contract_sha256"]) == 64
    assert set(first["unverified_source_contract_fields"]) == set(manifest)
    assert first["missing_source_contract_fields"] == []
    assert first["incomplete_source_contract_fields"] == []

    verified = contract.validate_service_truth_source_contract(
        source_contract(verification_status="VERIFIED")
    )
    assert verified["source_contract_complete"] is True
    assert verified["source_contract_verified"] is True
    assert verified["unverified_source_contract_fields"] == []


def test_missing_or_incomplete_source_ownership_stays_explicit() -> None:
    contract = load_contract()
    manifest = source_contract()
    del manifest["actual_served"]
    manifest["menu"]["owner"] = ""

    result = contract.validate_service_truth_source_contract(manifest)

    assert result["source_contract_complete"] is False
    assert result["source_contract_verified"] is False
    assert "actual_served" in result["missing_source_contract_fields"]
    assert "menu" in result["incomplete_source_contract_fields"]
    assert "actual_served" not in manifest
    assert manifest["menu"]["owner"] == ""


def test_optional_source_entries_are_validated_without_becoming_globally_required() -> None:
    contract = load_contract()
    manifest = source_contract(verification_status="VERIFIED")
    manifest["special_events"] = {
        "owner": "OFFICIAL_EVENTS_OWNER",
        "source_system": "HISTORICAL_EVENTS_SNAPSHOT",
        "availability_semantics": "EVENT_MUST_HAVE_BEEN_KNOWN_BY_DECISION_CUTOFF",
        "verification_status": "VERIFIED",
    }
    accepted = contract.validate_service_truth_source_contract(manifest)
    assert accepted["source_contract_complete"] is True
    assert accepted["source_contract_verified"] is True

    manifest["special_events"]["source_system"] = ""
    rejected = contract.validate_service_truth_source_contract(manifest)
    assert rejected["source_contract_complete"] is False
    assert "special_events" in rejected["incomplete_source_contract_fields"]


def test_weather_forecast_is_not_a_globally_required_source_contract_field() -> None:
    contract = load_contract()
    manifest = source_contract(verification_status="VERIFIED")
    del manifest["weather_forecast"]

    result = contract.validate_service_truth_source_contract(manifest)

    assert result["source_contract_complete"] is True
    assert result["source_contract_verified"] is True
    assert "weather_forecast" not in result["missing_source_contract_fields"]
    assert "weather_forecast" not in result["required_source_contract_fields"]


if __name__ == "__main__":
    tests = [name for name in globals() if name.startswith("test_")]
    for name in tests:
        globals()[name]()
    print(f"ok: {len(tests)} service source-contract tests")
