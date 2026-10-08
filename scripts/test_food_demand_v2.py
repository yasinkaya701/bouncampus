"""Focused causal and missingness checks for the shadow food-demand v2."""
from __future__ import annotations

from datetime import date, datetime
import json
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.models.food_demand_v2 import (
    build_features,
    evaluate_predictions,
    predict_as_of,
    prepare_snapshot,
)

TZ = ZoneInfo("Europe/Istanbul")


def fixture_rows():
    rows = []
    for day, demand in [("2026-03-01", 10), ("2026-03-02", 12), ("2026-03-03", 0), ("2026-03-04", None)]:
        rows.append({"date": day, "campus": "Hisar", "meal": "DINNER", "demand": demand})
    rows.extend([
        {"date": "2026-03-01", "campus": "Anadolu Hisarı", "meal": "DINNER", "demand": 4},
        {"date": "2026-03-02", "campus": "Hisar", "meal": "LUNCH", "demand": 20},
    ])
    return pd.DataFrame(rows)


def test_cutoff_excludes_d_minus_1_actual_and_later_notice():
    as_of = datetime(2026, 3, 4, 16, tzinfo=TZ)
    target = date(2026, 3, 5)
    snapshot = prepare_snapshot(fixture_rows(), as_of=as_of)
    features = build_features(snapshot, target_date=target, as_of=as_of, campus="Hisar", meal="DINNER")
    assert features["history_max_service_date"] == "2026-03-03"

    changed = fixture_rows()
    changed.loc[changed["date"] == "2026-03-04", "demand"] = 99999
    changed_snapshot = prepare_snapshot(changed, as_of=as_of)
    changed_features = build_features(changed_snapshot, target_date=target, as_of=as_of, campus="Hisar", meal="DINNER")
    assert features == changed_features


def test_missing_actual_is_not_zero_and_future_cutoff_may_use_known_zero():
    as_of = datetime(2026, 3, 4, 16, tzinfo=TZ)
    snapshot = prepare_snapshot(fixture_rows(), as_of=as_of)
    assert snapshot.loc[(snapshot.date == date(2026, 3, 3)) & (snapshot.campus == "Hisar") & (snapshot.meal == "DINNER"), "demand"].iloc[0] == 0
    assert pd.isna(snapshot.loc[(snapshot.date == date(2026, 3, 4)) & (snapshot.campus == "Hisar") & (snapshot.meal == "DINNER"), "demand"].iloc[0])


def test_unknown_group_is_unavailable_not_zero():
    as_of = datetime(2026, 3, 4, 16, tzinfo=TZ)
    snapshot = prepare_snapshot(fixture_rows(), as_of=as_of)
    predictions = predict_as_of(snapshot, cutoff=as_of, target_date=date(2026, 3, 5), groups=[("Unknown", "DINNER")])
    assert len(predictions) == 1
    assert predictions[0]["prediction"] is None
    assert predictions[0]["status"] == "INSUFFICIENT_DATA"


def test_hisar_and_anadolu_hisari_are_distinct_and_planned_is_not_a_feature():
    as_of = datetime(2026, 3, 4, 16, tzinfo=TZ)
    rows = fixture_rows().assign(planned=1_000_000)
    snapshot = prepare_snapshot(rows, as_of=as_of)
    hisar = build_features(snapshot, target_date=date(2026, 3, 5), as_of=as_of, campus="Hisar", meal="DINNER")
    anadolu = build_features(snapshot, target_date=date(2026, 3, 5), as_of=as_of, campus="Anadolu Hisarı", meal="DINNER")
    assert hisar["recent_56_median"] != anadolu["recent_56_median"]
    assert "planned" not in hisar


def test_notice_requires_publication_timestamp_before_cutoff():
    as_of = datetime(2026, 3, 4, 16, tzinfo=TZ)
    notices = pd.DataFrame([
        {"campus": "Hisar", "meal": "DINNER", "effective_date": "2026-03-05", "published_at": None, "closure": True},
        {"campus": "Hisar", "meal": "DINNER", "effective_date": "2026-03-05", "published_at": "2026-03-04T17:00:00+03:00", "closure": True},
    ])
    snapshot = prepare_snapshot(fixture_rows(), as_of=as_of, notices=notices)
    features = build_features(snapshot, target_date=date(2026, 3, 5), as_of=as_of, campus="Hisar", meal="DINNER")
    assert features["notice_status"] == "UNKNOWN"
    assert features["closure"] is None


def test_metrics_align_support_and_handle_zero_denominator():
    result = evaluate_predictions([10, None, 0], [12, 99, 5])
    assert result["n"] == 2
    assert result["mae"] == 3.5
    assert result["wape_pct"] == 70
    assert evaluate_predictions([0], [0])["wape_pct"] is None


def test_date_only_notice_is_available_next_midnight_and_keeps_provenance_hash():
    as_of = datetime(2026, 3, 4, 16, tzinfo=TZ)
    notices = pd.DataFrame([
        {
            "published_date": "2026-03-03",
            "valid_from": "2026-03-05",
            "valid_to": "2026-03-06",
            "review_status": "UNREVIEWED",
            "title": "Yemek hizmeti",
            "notice_text": "Yemek hizmeti verilmeyecektir.",
            "source_html_sha256": "a" * 64,
        }
    ])
    snapshot = prepare_snapshot(fixture_rows(), as_of=as_of, notices=notices)
    features = build_features(snapshot, target_date=date(2026, 3, 5), as_of=as_of, campus="Hisar", meal="DINNER")
    assert features["notice_status"] == "RULE_EXTRACTED_UNREVIEWED"
    assert features["closure"] is True
    assert features["notice_source_hashes"] == ["a" * 64]


def test_notice_published_on_cutoff_date_or_outside_valid_window_stays_unknown():
    as_of = datetime(2026, 3, 4, 16, tzinfo=TZ)
    notices = pd.DataFrame([
        {
            "published_date": "2026-03-04",
            "valid_from": "2026-03-05",
            "valid_to": "2026-03-05",
            "review_status": "UNREVIEWED",
            "title": "Yemek hizmeti",
            "notice_text": "Yemek hizmeti verilmeyecektir.",
            "source_html_sha256": "b" * 64,
        },
        {
            "published_date": "2026-03-03",
            "valid_from": "2026-03-02",
            "valid_to": "2026-03-04",
            "review_status": "UNREVIEWED",
            "title": "Yemek hizmeti",
            "notice_text": "Yemek hizmeti verilmeyecektir.",
            "source_html_sha256": "c" * 64,
        },
    ])
    snapshot = prepare_snapshot(fixture_rows(), as_of=as_of, notices=notices)
    features = build_features(snapshot, target_date=date(2026, 3, 5), as_of=as_of, campus="Hisar", meal="DINNER")
    assert features["notice_status"] == "UNKNOWN"
    assert features["closure"] is None


def test_cross_campus_total_is_missing_when_campus_coverage_is_partial():
    as_of = datetime(2026, 3, 9, 16, tzinfo=TZ)
    snapshot = prepare_snapshot(fixture_rows(), as_of=as_of)
    features = build_features(snapshot, target_date=date(2026, 3, 10), as_of=as_of, campus="Hisar", meal="DINNER")
    assert features["cross_campus_coverage_lag_7"] == 0.5
    assert features["cross_campus_total_lag_7"] is None


def test_source_outage_returns_unavailable_ledger_rows():
    as_of = datetime(2026, 3, 4, 16, tzinfo=TZ)
    empty = pd.DataFrame(columns=["date", "campus", "meal", "demand"])
    snapshot = prepare_snapshot(empty, as_of=as_of)
    rows = predict_as_of(snapshot, cutoff=as_of, target_date=date(2026, 3, 5), groups=[("Hisar", "DINNER")])
    assert rows[0]["prediction"] is None
    assert rows[0]["status"] == "INSUFFICIENT_DATA"
    assert rows[0]["data_coverage"]["history_rows"] == 0


def test_blend_weights_are_nonnegative_and_sum_to_one():
    from app.models.food_demand_v2 import learn_simplex_weights

    weights = learn_simplex_weights([10, 20, 30], {"low": [9, 21, 29], "high": [15, 15, 15]})
    assert all(value >= 0 for value in weights.values())
    assert abs(sum(weights.values()) - 1) < 1e-6


def test_explicit_zero_same_weekday_baseline_is_preserved():
    as_of = datetime(2026, 3, 10, 16, tzinfo=TZ)
    rows = pd.DataFrame([
        {"date": "2026-03-04", "campus": "Hisar", "meal": "DINNER", "demand": 0},
        {"date": "2026-03-09", "campus": "Hisar", "meal": "DINNER", "demand": 20},
    ])
    snapshot = prepare_snapshot(rows, as_of=as_of)
    prediction = predict_as_of(snapshot, cutoff=as_of, target_date=date(2026, 3, 11), groups=[("Hisar", "DINNER")])[0]
    assert prediction["prediction"] == 0


def test_cli_fit_predict_loads_saved_candidate_and_metadata(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    script = repo / "scripts" / "food_demand_v2.py"
    data_path = tmp_path / "demand.csv"
    output_dir = tmp_path / "runs"
    start = date(2026, 1, 1)
    rows = pd.DataFrame([
        {
            "date": (start + pd.Timedelta(days=index)).isoformat(),
            "campus": "Hisar",
            "meal": "ÖĞLE",
            "demand": 100 + (index % 7) * 3,
        }
        for index in range(120)
    ])
    rows.to_csv(data_path, index=False)
    cutoff = "2026-04-30T16:00:00+03:00"
    fit_result = subprocess.run(
        [sys.executable, str(script), "fit", "--data", str(data_path), "--output", str(output_dir), "--cutoff", cutoff, "--iterations", "5"],
        check=True,
        capture_output=True,
        text=True,
    )
    fit_payload = json.loads(fit_result.stdout)
    model_dir = Path(fit_payload["output_dir"])
    assert (model_dir / "catboost.cbm").is_file()
    assert fit_payload["manifest"]["artifact_schema_version"] == 1
    assert fit_payload["manifest"]["target_mode"] == "direct"

    predict_result = subprocess.run(
        [
            sys.executable, str(script), "predict", "--data", str(data_path), "--cutoff", cutoff,
            "--target", "2026-05-01", "--group", "Hisar/ÖĞLE", "--model-dir", str(model_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    predict_payload = json.loads(predict_result.stdout)
    assert predict_payload["model_status"]["status"] == "LOADED_LOCAL_MODEL"
    assert predict_payload["model_status"]["target_mode"] == "direct"
    assert predict_payload["prediction_ledger"][0]["model_id"] == "catboost_direct_mae"
    assert predict_payload["prediction_ledger"][0]["status"] == "MODEL_ESTIMATE"
