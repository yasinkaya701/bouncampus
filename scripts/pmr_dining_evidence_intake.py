#!/usr/bin/env python3
"""Fail-closed PMR intake validator for dining primary-evidence packets P1-P5."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PACKETS = {"P1", "P2", "P3", "P4", "P5"}
REQUIRED_COMMON = {
    "packet_id",
    "artifact_id",
    "source_owner_role",
    "acquired_at",
    "authoritative_status",
    "native_grain",
    "redaction_status",
    "source_reference",
}
ALLOWED_AUTHORITY = {"SOURCE_OWNER", "AUTHORITATIVE_RECORD", "PUBLIC_PRIMARY"}
ALLOWED_REDACTION = {"ORIGINAL", "REDACTED"}

PACKET_REQUIRED = {
    "P1": {"source_report_id", "reported_field_name", "report_generated_at", "correction_finality_status"},
    "P2": {"reported_event_definition", "correction_rule", "second_meal_rule", "package_meal_rule", "finality_rule"},
    "P3": {"ikn", "work_item_count", "work_item_labels_status", "payment_clause_status"},
    "P4": {"period", "control_record_ref", "hakedis_record_ref", "payable_quantity_field", "reconciliation_status"},
    "P5": {"initial_quantity_owner", "latest_reversible_time_status", "revision_rule_status", "authoritative_record_rule_status"},
}

FORBIDDEN_PROMOTIONS = {
    "P1": {"actual_served", "payable_quantity", "savings"},
    "P2": {"payable_quantity", "savings"},
    "P3": {"actual_served", "payable_quantity", "savings"},
    "P4": {"actual_served", "savings"},
    "P5": {"actual_served", "payable_quantity", "savings"},
}


def _present(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def validate(doc: Any) -> dict[str, Any]:
    reasons: list[str] = []
    if not isinstance(doc, dict):
        return {"status": "REJECTED", "reason_codes": ["PACKAGE_MUST_BE_OBJECT"], "promotions": []}

    packet = doc.get("packet_id")
    if packet not in PACKETS:
        reasons.append("UNKNOWN_PACKET_ID")

    for field in sorted(REQUIRED_COMMON):
        if not _present(doc.get(field)):
            reasons.append(f"MISSING_{field.upper()}")

    if doc.get("authoritative_status") not in ALLOWED_AUTHORITY:
        reasons.append("INVALID_AUTHORITATIVE_STATUS")
    if doc.get("redaction_status") not in ALLOWED_REDACTION:
        reasons.append("INVALID_REDACTION_STATUS")

    if packet in PACKETS:
        for field in sorted(PACKET_REQUIRED[packet]):
            if not _present(doc.get(field)):
                reasons.append(f"MISSING_{field.upper()}")

    requested = set(doc.get("requested_promotions", [])) if isinstance(doc.get("requested_promotions", []), list) else set()
    if packet in PACKETS:
        bad = sorted(requested & FORBIDDEN_PROMOTIONS[packet])
        reasons.extend(f"FORBIDDEN_PROMOTION_{x.upper()}" for x in bad)

    # P2 may promote actual_served only with an explicit authoritative served-field mapping.
    if packet == "P2" and "actual_served" in requested:
        if not _present(doc.get("authoritative_served_field")):
            reasons.append("ACTUAL_SERVED_REQUIRES_AUTHORITATIVE_FIELD")
        if doc.get("served_field_finality") != "FINAL_RECONCILED":
            reasons.append("ACTUAL_SERVED_REQUIRES_FINAL_RECONCILED")

    # P4 may promote payable quantity only when the join and reconciliation are explicit.
    if packet == "P4" and "payable_quantity" in requested:
        if doc.get("reconciliation_status") != "SOURCE_OWNER_CONFIRMED":
            reasons.append("PAYABLE_REQUIRES_SOURCE_OWNER_RECONCILIATION")
        if not _present(doc.get("joins_to_service_slice")):
            reasons.append("PAYABLE_REQUIRES_SERVICE_SLICE_JOIN")

    status = "ACCEPTED" if not reasons else "REJECTED"
    return {
        "status": status,
        "packet_id": packet,
        "artifact_id": doc.get("artifact_id"),
        "reason_codes": reasons,
        "promotions": sorted(requested) if status == "ACCEPTED" else [],
        "handoff": {
            "cs1_service_truth_candidate": bool(status == "ACCEPTED" and packet == "P2" and "actual_served" in requested),
            "payable_semantics_confirmed": bool(status == "ACCEPTED" and packet == "P4" and "payable_quantity" in requested),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    args = parser.parse_args()
    try:
        doc = json.loads(args.artifact.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        print(json.dumps({"status": "REJECTED", "reason_codes": ["INVALID_JSON_OR_READ_ERROR"], "promotions": []}))
        return 2
    result = validate(doc)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "ACCEPTED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
