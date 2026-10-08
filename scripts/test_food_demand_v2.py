"""Focused causal and missingness checks for the shadow food-demand v2."""
from __future__ import annotations

from datetime import date, datetime
import json
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.models.food_demand_v2 import (
    FittedFoodDemandV2,
    build_features,
    evaluate_predictions,
    fit,
    predict_as_of,
    prepare_snapshot,
)
from scripts.food_demand_v2 import _available_prior_oof, _fitted_reproducibility_metadata, _load_chronos_request, chronos2_predictions, load_notices, tabpfn_ts_predictions, load_tabpfn_ts

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
            "campus": "Hisar",
            "meal": "DINNER",
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
            "campus": "Hisar",
            "meal": "DINNER",
            "review_status": "UNREVIEWED",
            "title": "Yemek hizmeti",
            "notice_text": "Yemek hizmeti verilmeyecektir.",
            "source_html_sha256": "b" * 64,
        },
        {
            "published_date": "2026-03-03",
            "valid_from": "2026-03-02",
            "valid_to": "2026-03-04",
            "campus": "Hisar",
            "meal": "DINNER",
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


def test_cross_campus_features_ignore_campuses_first_seen_after_cutoff():
    as_of = datetime(2026, 3, 9, 16, tzinfo=TZ)
    base = fixture_rows()
    with_future_campus = pd.concat([base, pd.DataFrame([{
        "date": "2026-03-10", "campus": "Future Campus", "meal": "DINNER", "demand": 999,
    }])], ignore_index=True)
    before = prepare_snapshot(base, as_of=as_of)
    after = prepare_snapshot(with_future_campus, as_of=as_of)
    a = build_features(before, target_date=date(2026, 3, 10), as_of=as_of, campus="Hisar", meal="DINNER")
    b = build_features(after, target_date=date(2026, 3, 10), as_of=as_of, campus="Hisar", meal="DINNER")
    assert {key: a[key] for key in a if key.startswith("cross_campus_")} == {key: b[key] for key in b if key.startswith("cross_campus_")}
    pred_a = predict_as_of(before, cutoff=as_of, target_date=date(2026, 3, 10), groups=[("Hisar", "DINNER")])[0]
    pred_b = predict_as_of(after, cutoff=as_of, target_date=date(2026, 3, 10), groups=[("Hisar", "DINNER")])[0]
    assert pred_a["prediction"] == pred_b["prediction"]
    assert pred_a["input_data_version"] == pred_b["input_data_version"]


def test_prior_oof_excludes_previous_block_final_day_label_until_available():
    rows = [
        {"date": "2026-03-02", "actual": 10, "baseline": 9},
        {"date": "2026-03-03", "actual": 20, "baseline": 18},
    ]
    # The next block forecasts 2026-03-04 at the 2026-03-03 16:00 cutoff.
    kept = _available_prior_oof(rows, datetime(2026, 3, 3, 16, tzinfo=TZ))
    assert [row["date"] for row in kept] == ["2026-03-02"]


def test_prediction_rejects_future_trained_fitted_object():
    fitted = FittedFoodDemandV2(
        model=object(), feature_names=[], config={}, trained_through="2026-03-03",
        data_version="train-hash", fit_cutoff="2026-03-05T16:00:00+03:00",
    )
    snapshot = prepare_snapshot(fixture_rows(), as_of=datetime(2026, 3, 4, 16, tzinfo=TZ))
    with pytest.raises(ValueError, match="model cutoff is later"):
        predict_as_of(snapshot, cutoff=datetime(2026, 3, 4, 16, tzinfo=TZ), target_date=date(2026, 3, 5), groups=[("Hisar", "DINNER")], fitted=fitted)


def test_prediction_rejects_training_label_not_yet_available_at_cutoff():
    fitted = FittedFoodDemandV2(
        model=object(), feature_names=[], config={}, trained_through="2026-03-04",
        data_version="train-hash", fit_cutoff="2026-03-03T16:00:00+03:00",
    )
    snapshot = prepare_snapshot(fixture_rows(), as_of=datetime(2026, 3, 4, 16, tzinfo=TZ))
    with pytest.raises(ValueError, match="training label unavailable"):
        predict_as_of(snapshot, cutoff=datetime(2026, 3, 4, 16, tzinfo=TZ), target_date=date(2026, 3, 5), groups=[("Hisar", "DINNER")], fitted=fitted)


def test_sparse_history_residual_fit_keeps_features_and_labels_aligned():
    start = date(2026, 1, 1)
    day_indexes = list(range(61)) + [140]
    rows = pd.DataFrame([
        {"date": (start + pd.Timedelta(days=index)).isoformat(), "campus": "Hisar", "meal": "ÖĞLE", "demand": 100 + index * index * 0.01 + (index % 7) * 3}
        for index in day_indexes
    ])
    cutoff = datetime.combine(start + pd.Timedelta(days=162), datetime.min.time().replace(hour=16), TZ)
    snapshot = prepare_snapshot(rows, as_of=cutoff)
    fitted = fit(snapshot, {"as_of": cutoff, "iterations": 2, "min_training_rows": 1, "target_mode": "residual_to_weekday_median"})
    assert fitted.config["training_rows"] == 5
    assert fitted.candidate_status["catboost_residual_to_weekday_median"] == "FIT_CPU"
    metadata = _fitted_reproducibility_metadata(fitted)
    assert metadata["model_artifact_sha256"]
    assert metadata["fit_config_sha256"]
    assert metadata["data_version_sha256"] == fitted.data_version
    assert metadata["runner_sha256"] and metadata["model_code_sha256"]


def test_failed_catboost_fit_returns_no_model_and_explicit_candidate_status(monkeypatch):
    from types import SimpleNamespace

    class FailingCatBoost:
        def __init__(self, **kwargs):
            pass

        def fit(self, *args, **kwargs):
            raise RuntimeError("synthetic injected fit failure")

    monkeypatch.setitem(sys.modules, "catboost", SimpleNamespace(CatBoostRegressor=FailingCatBoost))
    start = date(2026, 1, 1)
    rows = pd.DataFrame([
        {"date": (start + pd.Timedelta(days=index)).isoformat(), "campus": "Hisar", "meal": "ÖĞLE", "demand": 100 + index}
        for index in range(60)
    ])
    cutoff = datetime.combine(start + pd.Timedelta(days=61), datetime.min.time().replace(hour=16), TZ)
    snapshot = prepare_snapshot(rows, as_of=cutoff)
    fitted = fit(snapshot, {"as_of": cutoff, "min_training_rows": 1})
    assert fitted.model is None
    assert fitted.candidate_status["catboost_direct_mae"].startswith("FAILED:RuntimeError:synthetic injected fit failure")


def test_notice_loader_preserves_canonical_fields_and_positive_labels_require_food_scope(tmp_path):
    path = tmp_path / "notices.csv"
    pd.DataFrame([{
        "published_at": "2026-03-03T10:00:00+03:00", "published_date": "2026-03-04",
        "effective_date": "2026-03-05", "valid_from": "2026-03-06", "valid_to": "2026-03-06",
        "campus": "Hisar", "affected_campuses": "Güney", "meal": "ÖĞLE", "affected_meals": "AKŞAM",
        "source_hash": "canonical-hash", "source_html_sha256": "alias-hash", "review_status": "UNREVIEWED",
        "title": "Yemek hizmeti", "notice_text": "Yemek hizmeti verilmeyecektir.",
    }]).to_csv(path, index=False)
    loaded = load_notices(path)
    assert loaded.loc[0, "published_at"] == "2026-03-03T10:00:00+03:00"
    assert loaded.loc[0, "effective_date"] == "2026-03-05"
    assert loaded.loc[0, "campus"] == "Hisar"
    assert loaded.loc[0, "meal"] == "ÖĞLE"
    assert loaded.loc[0, "source_hash"] == "canonical-hash"
    snapshot = prepare_snapshot(fixture_rows(), as_of=datetime(2026, 3, 4, 16, tzinfo=TZ), notices=loaded)
    feature = build_features(snapshot, target_date=date(2026, 3, 5), as_of=datetime(2026, 3, 4, 16, tzinfo=TZ), campus="Hisar", meal="ÖĞLE")
    assert feature["closure"] is True
    assert feature["notice_source_hashes"] == ["canonical-hash"]


def test_unscoped_kiosk_closure_is_unknown_but_explicit_global_food_scope_is_allowed():
    as_of = datetime(2026, 3, 4, 16, tzinfo=TZ)
    notices = pd.DataFrame([
        {"published_at": "2026-03-03T10:00:00+03:00", "effective_date": "2026-03-05", "title": "Kiosk", "notice_text": "Kiosk kapalıdır."},
        {"published_at": "2026-03-03T10:00:00+03:00", "effective_date": "2026-03-05", "campus": "all campuses", "meal": "all meals", "title": "Yemek", "notice_text": "Yemek hizmeti verilmeyecektir."},
    ])
    snapshot = prepare_snapshot(fixture_rows(), as_of=as_of, notices=notices)
    feature = build_features(snapshot, target_date=date(2026, 3, 5), as_of=as_of, campus="Hisar", meal="DINNER")
    assert feature["closure"] is True
    assert feature["notice_status"] == "RULE_EXTRACTED_UNREVIEWED"
    unscoped_only = prepare_snapshot(fixture_rows(), as_of=as_of, notices=notices.iloc[[0]])
    unknown = build_features(unscoped_only, target_date=date(2026, 3, 5), as_of=as_of, campus="Hisar", meal="DINNER")
    assert unknown["closure"] is None
    assert unknown["notice_status"] == "UNKNOWN"


def test_no_chronos_path_does_not_import_torch(monkeypatch):
    import builtins
    from types import SimpleNamespace

    original_import = builtins.__import__
    def guarded_import(name, *args, **kwargs):
        if name == "torch":
            raise AssertionError("torch should not be imported when Chronos is disabled")
        return original_import(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", guarded_import)
    pipeline, status = _load_chronos_request(SimpleNamespace(run_chronos2=False))
    assert pipeline is None
    assert status["status"] == "NOT_RUN_BY_REQUEST"


def test_chronos_requests_two_step_horizon_and_selects_target_day():
    class FakePipeline:
        def predict_df(self, context, *, future_df, id_column, timestamp_column, target, prediction_length, quantile_levels, context_length, cross_learning, freq):
            assert prediction_length == 2
            assert len(future_df) == 2
            assert future_df[timestamp_column].dt.date.tolist() == [date(2026, 3, 4), date(2026, 3, 5)]
            return pd.DataFrame({
                id_column: ["Hisar::DINNER", "Hisar::DINNER"],
                timestamp_column: future_df[timestamp_column].tolist(),
                "predictions": [10.0, 12.0],
            })

    rows = pd.DataFrame([
        {"date": f"2026-03-0{day}", "campus": "Hisar", "meal": "DINNER", "demand": float(day * 10)}
        for day in (1, 2, 3)
    ])
    cutoff = datetime(2026, 3, 4, 16, tzinfo=TZ)
    snapshot = prepare_snapshot(rows, as_of=cutoff)
    predictions, status = chronos2_predictions(
        FakePipeline(), snapshot, target_day=date(2026, 3, 5), cutoff=cutoff,
        groups=[("Hisar", "DINNER")], context_length=2,
    )
    assert status == "SCORED"
    assert predictions == {("Hisar", "DINNER"): 12.0}


def test_tabpfn_local_adapter_selects_second_day_and_never_passes_d_minus_1_actual():
    class FakePipeline:
        def predict_df(self, context_df, *, future_df, quantiles):
            assert quantiles == [0.5]
            assert context_df.timestamp.max().date() == date(2026, 3, 3)
            assert future_df.timestamp.dt.date.tolist() == [date(2026, 3, 4), date(2026, 3, 5)]
            return pd.DataFrame({
                "item_id": ["Hisar::DINNER", "Hisar::DINNER"],
                "timestamp": future_df.timestamp.tolist(),
                "target": [100.0, 120.0],
            })

    rows = pd.DataFrame([
        {"date": f"2026-03-{day:02d}", "campus": "Hisar", "meal": "DINNER", "demand": float(day * 10)}
        for day in range(1, 5)
    ])
    cutoff = datetime(2026, 3, 4, 16, tzinfo=TZ)
    snapshot = prepare_snapshot(rows, as_of=cutoff)
    predictions, status = tabpfn_ts_predictions(
        FakePipeline(), snapshot, target_day=date(2026, 3, 5), cutoff=cutoff,
        groups=[("Hisar", "DINNER")], context_length=2,
    )
    assert status == "SCORED"
    assert predictions == {("Hisar", "DINNER"): 120.0}


def test_tabpfn_loader_does_not_import_or_download_without_explicit_checkpoint(tmp_path, monkeypatch):
    import builtins
    original_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name == "tabpfn_time_series":
            raise AssertionError("optional TabPFN package must not load without local checkpoint")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    pipeline, status = load_tabpfn_ts(tmp_path / "missing.safetensors")
    assert pipeline is None
    assert status["status"] == "NOT_RUN_CHECKPOINT_ABSENT"
    assert status["inference_attempted"] is False
    assert status["telemetry"] == "disabled"


def test_chronos_auto_device_dependency_failure_is_nonfatal(monkeypatch):
    import builtins
    from types import SimpleNamespace
    original_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name == "torch":
            raise ImportError("test torch unavailable")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    pipeline, status = _load_chronos_request(SimpleNamespace(
        run_chronos2=True, chronos_device="auto", chronos_checkpoint="amazon/chronos-2",
        allow_chronos_download=False, chronos_revision=None,
    ))
    assert pipeline is None
    assert status["status"].startswith("UNAVAILABLE:ImportError:")


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
    assert fit_payload["manifest"]["artifact_schema_version"] == 2
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
    with (model_dir / "catboost.cbm").open("ab") as handle:
        handle.write(b"tamper")
    rejected = subprocess.run(
        [
            sys.executable, str(script), "predict", "--data", str(data_path), "--cutoff", cutoff,
            "--target", "2026-05-01", "--group", "Hisar/ÖĞLE", "--model-dir", str(model_dir),
        ],
        capture_output=True,
        text=True,
    )
    assert rejected.returncode != 0
    assert "SHA-256 verification failed" in rejected.stderr
