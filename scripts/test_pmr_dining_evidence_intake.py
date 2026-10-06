#!/usr/bin/env python3
import importlib.util
from pathlib import Path

PATH = Path(__file__).with_name("pmr_dining_evidence_intake.py")
spec = importlib.util.spec_from_file_location("pmr_dining_evidence_intake", PATH)
m = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(m)


def base(packet):
    return {
        "packet_id": packet,
        "artifact_id": "A-1",
        "source_owner_role": "owner",
        "acquired_at": "2026-10-06",
        "authoritative_status": "SOURCE_OWNER",
        "native_grain": "service_date x campus x meal_period",
        "redaction_status": "REDACTED",
        "source_reference": "ref",
        "requested_promotions": [],
    }


def test_p1_cannot_promote_actual_served():
    d = base("P1")
    d.update(source_report_id="R", reported_field_name="passage_count", report_generated_at="t", correction_finality_status="UNKNOWN")
    d["requested_promotions"] = ["actual_served"]
    r = m.validate(d)
    assert r["status"] == "REJECTED"
    assert "FORBIDDEN_PROMOTION_ACTUAL_SERVED" in r["reason_codes"]


def test_p2_actual_served_requires_reconciled_authoritative_field():
    d = base("P2")
    d.update(
        reported_event_definition="one finalized served event",
        correction_rule="documented",
        second_meal_rule="documented",
        package_meal_rule="documented",
        finality_rule="documented",
        authoritative_served_field="served_count",
        served_field_finality="FINAL_RECONCILED",
    )
    d["requested_promotions"] = ["actual_served"]
    r = m.validate(d)
    assert r["status"] == "ACCEPTED"
    assert r["handoff"]["cs1_service_truth_candidate"] is True


def test_p4_payable_requires_join_and_owner_reconciliation():
    d = base("P4")
    d.update(
        period="2026-09",
        control_record_ref="C",
        hakedis_record_ref="H",
        payable_quantity_field="accepted_qty",
        reconciliation_status="SOURCE_OWNER_CONFIRMED",
        joins_to_service_slice="2026-09-01|north|lunch",
    )
    d["requested_promotions"] = ["payable_quantity"]
    r = m.validate(d)
    assert r["status"] == "ACCEPTED"
    assert r["handoff"]["payable_semantics_confirmed"] is True


def test_p3_cannot_promote_savings():
    d = base("P3")
    d.update(ikn="2025/1727143", work_item_count=15, work_item_labels_status="AUTHORITATIVE", payment_clause_status="AUTHORITATIVE")
    d["requested_promotions"] = ["savings"]
    assert m.validate(d)["status"] == "REJECTED"


if __name__ == "__main__":
    test_p1_cannot_promote_actual_served()
    test_p2_actual_served_requires_reconciled_authoritative_field()
    test_p4_payable_requires_join_and_owner_reconciliation()
    test_p3_cannot_promote_savings()
    print("ok")
