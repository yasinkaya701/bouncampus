#!/usr/bin/env python3
"""Local-only audit, causal backtest, fit, predict, and report for food-demand v2."""
from __future__ import annotations

import argparse
from datetime import date, datetime, time, timedelta
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid
from zoneinfo import ZoneInfo

# Disable TabPFN telemetry before optional model imports or initialization.
os.environ["TABPFN_DISABLE_TELEMETRY"] = "1"

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.models.food_demand_v2 import (  # noqa: E402
    ASSUMPTION,
    FittedFoodDemandV2,
    build_features,
    evaluate_predictions,
    fit,
    learn_simplex_weights,
    predict_as_of,
    prepare_snapshot,
    _SNAPSHOT_CACHE,
)

TZ = ZoneInfo("Europe/Istanbul")
DEFAULT_OUTPUT = ROOT / "backend/data/models/food-demand/v2"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_safe(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


def load_notices(path: Path | None) -> pd.DataFrame | None:
    if path is None:
        return None
    source = pd.read_csv(path).fillna({})
    # The source archive has published_date only, with no verified publication time.
    # Keep source hashes and review state, but do not infer service labels from text.
    if "source_html_sha256" in source:
        source["source_hash"] = source["source_html_sha256"]
    # Date-only publication evidence is made available at next local midnight.
    # The forecaster therefore excludes any notice published on the cutoff date.
    source["published_at"] = None
    source["effective_date"] = source.get("valid_from")
    source["campus"] = source.get("affected_campuses")
    source["meal"] = source.get("affected_meals")
    return source


def load_snapshot(data_path: Path, notices_path: Path | None, as_of: datetime):
    digest = sha256_file(data_path)
    return prepare_snapshot(data_path, as_of=as_of, notices=load_notices(notices_path), source_hash=digest), digest


def _model_direct(fitted, features):
    if fitted.model is None or features["history_n"] < 7:
        return None
    from app.models.food_demand_v2 import _candidate_matrix
    try:
        value = float(fitted.model.predict(_candidate_matrix([features], use_notices=bool(fitted.config.get("use_notices", True))))[0])
        if fitted.config.get("target_mode") == "residual_to_weekday_median":
            base = features["same_weekday_median"] if features["same_weekday_median"] is not None else features["recent_56_median"]
            if base is None:
                return None
            value += float(base)
        return max(0.0, value) if np.isfinite(value) else None
    except Exception:
        return None


def load_chronos2(checkpoint: str, device: str, allow_download: bool = False):
    """Load the public Chronos-2 checkpoint once; the pipeline runs locally."""
    try:
        import torch
        from chronos import Chronos2Pipeline
        torch.manual_seed(42)
        if Path(checkpoint).exists():
            model_path = checkpoint
        elif allow_download:
            model_path = checkpoint
        else:
            from huggingface_hub import snapshot_download
            model_path = snapshot_download(repo_id=checkpoint, local_files_only=True)
        pipeline = Chronos2Pipeline.from_pretrained(model_path, device_map=device, local_files_only=not allow_download)
        return pipeline, {"status": "READY", "checkpoint": checkpoint, "device": device, "library_version": getattr(__import__("chronos"), "__version__", "unknown"), "seed": 42}
    except Exception as exc:
        return None, {"status": f"UNAVAILABLE:{type(exc).__name__}:{str(exc)[:200]}", "checkpoint": checkpoint, "device": device}


def _calendar_covariates(day: date):
    return {
        "weekday": float(day.weekday()),
        "month": float(day.month),
        "day_of_year_sin": float(np.sin(2 * np.pi * day.timetuple().tm_yday / 366)),
        "day_of_year_cos": float(np.cos(2 * np.pi * day.timetuple().tm_yday / 366)),
    }


def chronos2_predictions(pipeline, snapshot, *, target_day, cutoff, groups, context_length):
    """Two-step daily Chronos-2 forecast from service-day D-2; return D (step two)."""
    if pipeline is None:
        return {}, "UNAVAILABLE"
    histories = []
    futures = []
    included = []
    target_day = pd.Timestamp(target_day).date()
    latest_available = target_day - timedelta(days=2)
    context_start = target_day - timedelta(days=context_length + 1)
    cache = _SNAPSHOT_CACHE.get(id(snapshot), {})
    group_rows = cache.get("group_rows", {})
    for campus, meal in groups:
        source = group_rows.get((campus, meal), [])
        window = [(day, value) for day, value in source if context_start <= day <= latest_available]
        grid = [context_start + timedelta(days=index) for index in range(context_length)]
        if len(window) != context_length or [day for day, _ in window] != grid:
            continue
        if any(value is None for _, value in window) or window[-1][0] != latest_available:
            continue
        item_id = f"{campus}::{meal}"
        for day, value in window:
            histories.append({"item_id": item_id, "timestamp": pd.Timestamp(day), "demand": float(value), **_calendar_covariates(day)})
        for step in (1, 2):
            day = target_day - timedelta(days=1) + timedelta(days=step - 1)
            futures.append({"item_id": item_id, "timestamp": pd.Timestamp(day), **_calendar_covariates(day)})
        included.append(item_id)
    if not histories:
        return {}, "INSUFFICIENT_CONTIGUOUS_HISTORY"
    past = pd.DataFrame(histories).sort_values(["item_id", "timestamp"])
    future = pd.DataFrame(futures).sort_values(["item_id", "timestamp"])
    try:
        forecasts = pipeline.predict_df(
            past,
            future_df=future,
            id_column="item_id",
            timestamp_column="timestamp",
            target="demand",
            quantile_levels=[0.5],
            context_length=context_length,
            cross_learning=True,
            freq="D",
        )
        selected = forecasts[forecasts["timestamp"].dt.date == target_day]
        values = {tuple(row.item_id.split("::", 1)): max(0.0, float(row.predictions)) for row in selected.itertuples(index=False) if np.isfinite(row.predictions)}
        return values, "SCORED" if values else "NO_VALID_FORECAST"
    except Exception as exc:
        return {}, f"FAILED:{type(exc).__name__}:{str(exc)[:180]}"


def workbook_plan_rows(workbooks: list[Path]) -> pd.DataFrame:
    """Read Planlanan rows solely as a labeled comparator; never as a feature."""
    rows = []
    for path in workbooks:
        excel = pd.ExcelFile(path)
        for sheet in excel.sheet_names:
            frame = pd.read_excel(path, sheet_name=sheet, header=None)
            dates = []
            for value in frame.iloc[0, 3:].tolist():
                parsed = pd.to_datetime(value, errors="coerce")
                dates.append(None if pd.isna(parsed) else parsed.date())
            meal = None
            campus = None
            for _, row in frame.iterrows():
                if pd.notna(row.iloc[0]) and str(row.iloc[0]).strip():
                    meal = str(row.iloc[0]).strip()
                if pd.notna(row.iloc[1]) and str(row.iloc[1]).strip():
                    campus = str(row.iloc[1]).strip()
                kind = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
                if kind.casefold() != "planlanan" or not meal or not campus:
                    continue
                for index, day in enumerate(dates, start=3):
                    if day is None or index >= len(row):
                        continue
                    try:
                        value = float(row.iloc[index])
                    except (TypeError, ValueError):
                        continue
                    if np.isfinite(value):
                        rows.append({"date": day, "campus": campus, "meal_raw": meal, "planned": value})
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    frame["meal"] = frame["meal_raw"].map(_normalize_meal)
    frame["campus"] = frame["campus"].map(_normalize_campus)
    return frame[["date", "campus", "meal", "planned"]].drop_duplicates(["date", "campus", "meal"])


def _normalize_campus(value: str) -> str:
    key = value.strip().casefold()
    aliases = {"sarıtepe": "Kilyos", "sarıtepe/kilyos": "Kilyos", "hisar kampüsü": "Hisar"}
    return aliases.get(key, value.strip())


def _normalize_meal(value: str) -> str:
    key = value.strip().casefold()
    aliases = {"öğle": "ÖĞLE", "ogle": "ÖĞLE", "akşam": "AKŞAM", "aksam": "AKŞAM", "kahvaltı": "KAHVALTI", "kahvalti": "KAHVALTI"}
    return aliases.get(key, value.strip().upper())


def _groups(snapshot: pd.DataFrame) -> list[tuple[str, str]]:
    return sorted(set(zip(snapshot["campus"].astype(str), snapshot["meal"].astype(str))))


def _day_actuals(snapshot: pd.DataFrame, target_day: date) -> dict[tuple[str, str], float | None]:
    day = snapshot[snapshot["date"] == target_day]
    return {(str(row.campus), str(row.meal)): (None if pd.isna(row.demand) else float(row.demand)) for row in day.itertuples(index=False)}


def _bootstrap_wape(actual, predicted, *, clusters=None, seed=42, samples=1000):
    valid = [(float(a), float(p), (clusters[index] if clusters is not None else index)) for index, (a, p) in enumerate(zip(actual, predicted)) if pd.notna(a) and pd.notna(p)]
    if not valid:
        return [None, None]
    rng = np.random.default_rng(seed)
    unique_clusters = list(dict.fromkeys(row[2] for row in valid))
    row_indices = {cluster: [i for i, row in enumerate(valid) if row[2] == cluster] for cluster in unique_clusters}
    a = np.asarray([row[0] for row in valid])
    p = np.asarray([row[1] for row in valid])
    values = []
    for _ in range(samples):
        sampled_clusters = rng.integers(0, len(unique_clusters), len(unique_clusters))
        idx = np.asarray([index for cluster_ix in sampled_clusters for index in row_indices[unique_clusters[cluster_ix]]], dtype=int)
        den = np.abs(a[idx]).sum()
        if den:
            values.append(np.abs(p[idx] - a[idx]).sum() / den * 100)
    return [float(np.percentile(values, 2.5)), float(np.percentile(values, 97.5))] if values else [None, None]


def run_backtest(snapshot: pd.DataFrame, *, warmup_days: int = 180, block_days: int = 28, iterations: int = 200, seed: int = 42, planned: pd.DataFrame | None = None, chronos_pipeline=None, chronos_status=None, tabpfn_status=None):
    dates = sorted(snapshot["date"].unique())
    if not dates:
        raise ValueError("no dated outcomes")
    first = dates[0] + timedelta(days=warmup_days)
    last = dates[-1]
    groups = _groups(snapshot)
    prediction_rows = []
    block_records = []
    prior_oof = []
    block_start = first
    block_number = 0
    chronos_forecast_counts = {length: 0 for length in (56, 112, 224)}
    chronos_status_counts = {length: {} for length in (56, 112, 224)}
    while block_start <= last:
        block_end = min(block_start + timedelta(days=block_days - 1), last)
        block_preds = []
        weekly_models = []
        fitted = None
        target_day = block_start
        while target_day <= block_end:
            if fitted is None or (target_day - block_start).days % 7 == 0:
                fit_cutoff = datetime.combine(target_day - timedelta(days=1), time(16), TZ)
                fitted = fit(snapshot, {"as_of": fit_cutoff, "iterations": iterations, "seed": seed, "min_training_rows": 20, "use_notices": True})
                residual_fitted = fit(snapshot, {"as_of": fit_cutoff, "iterations": iterations, "seed": seed, "min_training_rows": 20, "use_notices": True, "target_mode": "residual_to_weekday_median"})
                eligible_notices = any(
                    row.get("status") != "UNKNOWN"
                    and row.get("effective_date")
                    and row.get("campus") not in (None, "", np.nan)
                    and row.get("meal") not in (None, "", np.nan)
                    and any(row.get(key) is True for key in ("closure", "reservation_required", "package_meal", "hours_notice", "price_change"))
                    for row in snapshot.attrs.get("notice_rows", [])
                )
                ablated_notice_model = fit(snapshot, {"as_of": fit_cutoff, "iterations": iterations, "seed": seed, "min_training_rows": 20, "use_notices": False}) if eligible_notices else None
                weekly_models.append({"trained_through": fitted.trained_through, "training_rows": fitted.config.get("training_rows", 0), "candidate_status": {**fitted.candidate_status, **residual_fitted.candidate_status}})
            cutoff = datetime.combine(target_day - timedelta(days=1), time(16), TZ)
            actuals = _day_actuals(snapshot, target_day)
            chronos_predictions = {}
            chronos_status_by_context = {}
            for context_length in (56, 112, 224):
                values, candidate_status = chronos2_predictions(chronos_pipeline, snapshot, target_day=target_day, cutoff=cutoff, groups=groups, context_length=context_length)
                chronos_status_by_context[context_length] = candidate_status
                chronos_forecast_counts[context_length] += len(values)
                chronos_status_counts[context_length][candidate_status] = chronos_status_counts[context_length].get(candidate_status, 0) + 1
                chronos_predictions.update({(campus, meal, context_length): value for (campus, meal), value in values.items()})
            for campus, meal in groups:
                feature = build_features(snapshot, target_date=target_day, as_of=cutoff, campus=campus, meal=meal)
                baseline = feature["same_weekday_median"]
                if baseline is None:
                    baseline = feature["recent_56_median"]
                model_pred = _model_direct(fitted, feature)
                residual_pred = _model_direct(residual_fitted, feature)
                no_notice_pred = _model_direct(ablated_notice_model, feature) if ablated_notice_model is not None else None
                actual = actuals.get((campus, meal))
                row = {"date": target_day.isoformat(), "campus": campus, "meal": meal, "actual": actual, "baseline": baseline, "catboost": model_pred, "catboost_residual": residual_pred, "catboost_no_notice": no_notice_pred, "chronos2_ctx56": chronos_predictions.get((campus, meal, 56)), "chronos2_ctx112": chronos_predictions.get((campus, meal, 112)), "chronos2_ctx224": chronos_predictions.get((campus, meal, 224)), "plan_comparator": None, "block": block_number, "cutoff": cutoff.isoformat(), "status": "EVALUATED" if actual is not None else "MISSING_ACTUAL"}
                if planned is not None and not planned.empty:
                    match = planned[(planned["date"] == target_day) & (planned["campus"] == campus) & (planned["meal"] == meal)]
                    row["plan_comparator"] = float(match.iloc[0]["planned"]) if not match.empty else None
                block_preds.append(row)
            target_day += timedelta(days=1)
        # Learn weights only from earlier forward blocks. First block defaults to baseline.
        expert_names = ["baseline", "catboost", "catboost_residual", "catboost_no_notice", "chronos2_ctx56", "chronos2_ctx112", "chronos2_ctx224"]
        active_experts = [name for name in expert_names if any(row.get(name) is not None for row in prior_oof)]
        prior_valid = [row for row in prior_oof if row["actual"] is not None and active_experts and all(row.get(name) is not None for name in active_experts)]
        if prior_valid:
            weights = learn_simplex_weights([r["actual"] for r in prior_valid], {name: [r[name] for r in prior_valid] for name in active_experts})
        else:
            weights = {"baseline": 1.0}
        for row in block_preds:
            row["blend_weights"] = weights
            candidates = [(row.get(k), w) for k, w in weights.items()]
            if candidates and all(v is not None for v, _ in candidates):
                row["blend"] = sum(float(v) * float(w) for v, w in candidates)
            else:
                row["blend"] = row.get("baseline")
            prediction_rows.append(row)
        eligible = [r for r in block_preds if r["actual"] is not None]
        block_records.append({"block": block_number, "start": block_start.isoformat(), "end": block_end.isoformat(), "training_rows": fitted.config.get("training_rows", 0), "weekly_refits": weekly_models, "blend_weights": weights, "scored_rows": len(eligible)})
        prior_oof.extend(block_preds)
        block_number += 1
        block_start = block_end + timedelta(days=1)
    all_actual = [row["actual"] for row in prediction_rows]
    for row in prediction_rows:
        for context_length in (56, 112, 224):
            row[f"blend_chronos2_ctx{context_length}"] = None
    candidate_names = ["baseline", "catboost", "catboost_residual", "blend"]
    if any(row.get("catboost_no_notice") is not None for row in prediction_rows):
        candidate_names.append("catboost_no_notice")
    for context_length in (56, 112, 224):
        name = f"chronos2_ctx{context_length}"
        if any(row.get(name) is not None for row in prediction_rows):
            candidate_names.append(name)
    candidate_names = tuple(candidate_names)
    eligible_rows = [row for row in prediction_rows if row["actual"] is not None]
    common_rows = [
        row for row in prediction_rows
        if row["actual"] is not None and all(row.get(name) is not None for name in candidate_names)
    ]
    methods = {name: [row[name] for row in common_rows] for name in candidate_names}
    common_actual = [row["actual"] for row in common_rows]
    metrics = {name: evaluate_predictions(common_actual, values) for name, values in methods.items()}
    plan_rows = [row for row in prediction_rows if row["actual"] is not None and row.get("plan_comparator") is not None]
    plan_metrics = evaluate_predictions([row["actual"] for row in plan_rows], [row["plan_comparator"] for row in plan_rows]) if planned is not None else None
    details = {}
    for key in ("campus", "meal"):
        details[key] = {}
        for value in sorted({row[key] for row in common_rows}):
            subset = [row for row in common_rows if row[key] == value]
            details[key][value] = {name: evaluate_predictions([r["actual"] for r in subset], [r[name] for r in subset]) for name in methods}
    denominator = sum(abs(float(value)) for value in all_actual if value is not None)
    coverage = {name: float(sum(row.get(name) is not None and row["actual"] is not None for row in prediction_rows) / max(1, len(eligible_rows)) * 100) for name in candidate_names}
    eligible_support_metrics = {}
    for name in candidate_names:
        own_support_metrics = evaluate_predictions([r["actual"] for r in eligible_rows], [r.get(name) for r in eligible_rows])
        eligible_support_metrics[name] = {
            "eligible_actual_support_n": len(eligible_rows),
            "forecasted_actual_support_n": sum(row.get(name) is not None for row in eligible_rows),
            "coverage_pct": coverage[name],
            "metrics_on_forecasted_support": own_support_metrics,
            "complete_coverage_eligible": bool(eligible_rows) and coverage[name] == 100.0,
            "wape_5pct_threshold_met": own_support_metrics["wape_pct"] is not None and own_support_metrics["wape_pct"] <= 5.0,
        }
    ci = {name: _bootstrap_wape(common_actual, values, clusters=[row["date"] for row in common_rows], seed=seed + i) for i, (name, values) in enumerate(methods.items())}
    return {
        "design": {"warmup_days": warmup_days, "forward_block_days": block_days, "cutoff": "16:00 Europe/Istanbul on D-1", "historical_outcome_availability": ASSUMPTION, "fit_schedule": "weekly refits inside each 28-day forward evaluation block; daily features rebuilt at each 16:00 D-1 cutoff", "tuning": "CatBoost parameters fixed before this historical development run; no test-block tuning. Blend weights fitted from earlier causal out-of-fold blocks only"},
        "metrics": metrics,
        "common_candidate_support_n": len(common_rows),
        "eligible_actual_support": {"n": len(eligible_rows), "models": eligible_support_metrics},
        "five_percent_claim_eligible": False,
        "plan_comparator": {"metrics": plan_metrics, "support_n": len(plan_rows), "status": "UNVINTAGED_COMPARATOR_ONLY"} if planned is not None else {"metrics": None, "support_n": 0, "status": "NOT_PROVIDED"},
        "coverage_pct": coverage,
        "bootstrap_95pct_wape_interval": ci,
        "bootstrap_unit": "TARGET_DATE_CLUSTER" ,
        "by_group": details,
        "blocks": block_records,
        "predictions": prediction_rows,
        "wape_denominator": denominator,
        "valid_actual_rows": sum(value is not None for value in all_actual),
        "candidate_status": {"catboost_direct_mae": "FIT_CPU_PER_WEEK", "catboost_residual_to_weekday_median": "FIT_CPU_PER_WEEK", "catboost_no_notice_ablation": "FIT_CPU_PER_WEEK_IF_ELIGIBLE_NOTICE_FIELDS_EXIST", "residual_to_past_same_weekday_median": "BASELINE", "chronos_2": {**(chronos_status or {"status": "NOT_RUN"}), "scored_status": "SCORED" if any(chronos_forecast_counts.values()) else "NO_VALID_FORECASTS", "forecast_rows_by_context": chronos_forecast_counts, "status_counts_by_context": chronos_status_counts}, "tabpfn_ts_3_5": tabpfn_status or {"status": "NOT_RUN"}, "chronos_context_status_last_target": chronos_status_by_context if "chronos_status_by_context" in locals() else {}},
        "ablations": {"notices": {"status": "SCORED_CATBOOST_WITH_VS_WITHOUT_NOTICE_FIELDS" if "catboost_no_notice" in candidate_names else "NOT_RUN_NO_ELIGIBLE_NOTICE_FEATURES", "same_support_required": True}, "menu": "NOT_RUN_NO_MENU_PUBLICATION_VINTAGE", "weather": "NOT_RUN_NO_ARCHIVED_FORECAST_VINTAGE", "blend": "SCORED_CAUSAL_PRIOR_BLOCKS"},
    }


def _historical_training_rows_count(snapshot, cutoff):
    from app.models.food_demand_v2 import _historical_training_rows
    return _historical_training_rows(snapshot, as_of=cutoff)[0]


def write_run(output_root: Path, kind: str, data_hash: str):
    run_id = datetime.now(TZ).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8]
    run_dir = output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_id, run_dir


def cmd_audit(args):
    data_path = Path(args.data)
    as_of = datetime.now(TZ).replace(hour=16, minute=0, second=0, microsecond=0)
    snapshot, digest = load_snapshot(data_path, Path(args.notices) if args.notices else None, as_of)
    notices = load_notices(Path(args.notices)) if args.notices else None
    notice_rows = snapshot.attrs.get("notice_rows", [])
    notice_categories = ("closure", "reservation_required", "package_meal", "hours_notice", "price_change")
    notice_features = {
        "rows": len(notice_rows),
        "source_date_only_availability": "NEXT_LOCAL_MIDNIGHT_ASSUMPTION",
        "positive_rule_extracted_unreviewed": sum(row.get("status") == "RULE_EXTRACTED_UNREVIEWED" for row in notice_rows),
        "source_hashes_present": sum(bool(row.get("source_hash")) for row in notice_rows),
        "validity_windows_present": sum(bool(row.get("effective_date")) for row in notice_rows),
        "campus_scopes_present": sum(row.get("campus") is not None and pd.notna(row.get("campus")) and bool(str(row.get("campus")).strip()) for row in notice_rows),
        "meal_scopes_present": sum(row.get("meal") is not None and pd.notna(row.get("meal")) and bool(str(row.get("meal")).strip()) for row in notice_rows),
        "eligible_for_forecast_features": sum(row.get("status") != "UNKNOWN" and bool(row.get("effective_date")) and row.get("campus") is not None and pd.notna(row.get("campus")) and row.get("meal") is not None and pd.notna(row.get("meal")) for row in notice_rows),
        "positive_fields_by_category": {key: sum(row.get(key) is True for row in notice_rows) for key in notice_categories},
        "unknown_fields_by_category": {key: sum(row.get(key) is None for row in notice_rows) for key in notice_categories},
    }
    result = {
        "dataset_sha256": digest,
        "rows": int(len(snapshot)),
        "date_min": min(snapshot.date).isoformat(),
        "date_max": max(snapshot.date).isoformat(),
        "groups": int(snapshot.groupby(["campus", "meal"]).ngroups),
        "explicit_zero_rows": int((snapshot.demand == 0).sum()),
        "missing_demand_rows": int(snapshot.demand.isna().sum()),
        "campuses": sorted(snapshot.campus.astype(str).unique().tolist()),
        "meals": sorted(snapshot.meal.astype(str).unique().tolist()),
        "target_provenance": "SOURCE_WORKBOOK_CONTAINS_PLAN_AND_REALIZED_ROWS; NORMALIZED_TARGET_IS_REALIZED_ROW_CLASS_NOT_INDEPENDENTLY_ATTESTED",
        "historical_availability": ASSUMPTION,
        "notices": notice_features,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_backtest(args):
    data_path = Path(args.data)
    start = min(pd.to_datetime(pd.read_csv(data_path, usecols=["date"])["date"]).dt.date)
    as_of = datetime.combine(start + timedelta(days=args.warmup_days + 1), time(16), TZ)
    snapshot, digest = load_snapshot(data_path, Path(args.notices) if args.notices else None, as_of)
    planned = workbook_plan_rows([Path(path) for path in args.plan_workbook]) if args.plan_workbook else None
    device = "mps" if args.chronos_device == "auto" and __import__("torch").backends.mps.is_available() else ("cuda" if args.chronos_device == "auto" and __import__("torch").cuda.is_available() else ("cpu" if args.chronos_device == "auto" else args.chronos_device))
    chronos_pipeline, chronos_status = load_chronos2(args.chronos_checkpoint, device, allow_download=args.allow_chronos_download) if args.run_chronos2 else (None, {"status": "NOT_RUN_BY_REQUEST"})
    tabpfn_status = {
        "status": "NOT_RUN_LICENSE_AND_CHECKPOINT_UNAVAILABLE",
        "package": "tabpfn-time-series==1.3.0",
        "package_installed_in_optional_local_venv": (DEFAULT_OUTPUT / "tabpfn-ts-venv").exists(),
        "mode": "TabPFNMode.LOCAL",
        "telemetry": "TABPFN_DISABLE_TELEMETRY=1",
        "checkpoint": "tabpfn-v3.5-20260909.safetensors",
        "checkpoint_present": (Path.home() / "Library/Caches/tabpfn/tabpfn-v3.5-20260909.safetensors").exists(),
        "inference_attempted": False,
        "reason": "LOCAL constructor API verified; checkpoint absent from local cache and upstream requires prior license acceptance. No terms accepted and no inference attempted.",
    }
    result = run_backtest(snapshot, warmup_days=args.warmup_days, block_days=args.block_days, iterations=args.iterations, seed=args.seed, planned=planned, chronos_pipeline=chronos_pipeline, chronos_status=chronos_status, tabpfn_status=tabpfn_status)
    run_id, run_dir = write_run(Path(args.output), "backtest", digest)
    manifest = {"run_id": run_id, "run_type": "historical_development_backtest", "dataset_sha256": digest, "source_path_label": Path(args.data).name, "generated_at": datetime.now(TZ).isoformat(), "target_scope": "OFFLINE_DEVELOPMENT_ONLY", "realized_demand_claim": "Normalized target rows correspond to workbook 'Gerçekleşen' fields as inspected, but independently verified operational provenance remains NOT_ATTESTED.", "prospective_5pct_gate": "NOT_EVALUATED_NO_56_DAY_PROSPECTIVE_WINDOW", "result": {k: v for k, v in result.items() if k != "predictions"}}
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    pd.DataFrame(result["predictions"]).to_csv(run_dir / "predictions.csv", index=False)
    print(json.dumps({"run_id": run_id, "output_dir": str(run_dir), "metrics": result["metrics"], "coverage_pct": result["coverage_pct"], "common_candidate_support_n": result["common_candidate_support_n"], "plan_comparator": result["plan_comparator"], "bootstrap_95pct_wape_interval": result["bootstrap_95pct_wape_interval"], "block_count": len(result["blocks"])}, ensure_ascii=False, indent=2))


def cmd_fit(args):
    data_path = Path(args.data)
    as_of = datetime.fromisoformat(args.cutoff)
    snapshot, digest = load_snapshot(data_path, Path(args.notices) if args.notices else None, as_of)
    fitted = fit(snapshot, {"as_of": as_of, "iterations": args.iterations, "seed": args.seed, "target_mode": args.target_mode})
    fitted.config["source_dataset_sha256"] = digest
    run_id, run_dir = write_run(Path(args.output), "fit", digest)
    manifest = {"artifact_schema_version": 1, "run_id": run_id, "model_version": fitted.model_version, "candidate_id": fitted.config.get("candidate_id"), "target_mode": fitted.config.get("target_mode", "direct"), "dataset_sha256": digest, "data_version": fitted.data_version, "trained_through": fitted.trained_through, "feature_names": fitted.feature_names, "config": _json_safe(fitted.config), "model_file": "catboost.cbm" if fitted.model is not None else None, "candidate_status": fitted.candidate_status, "historical_availability_assumption": ASSUMPTION, "scope": "SHADOW_ONLY_NOT_PROMOTED"}
    if fitted.model is not None:
        fitted.model.save_model(str(run_dir / "catboost.cbm"))
    (run_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"run_id": run_id, "output_dir": str(run_dir), "manifest": manifest}, ensure_ascii=False, indent=2))


def cmd_predict(args):
    data_path = Path(args.data)
    cutoff = datetime.fromisoformat(args.cutoff)
    snapshot, digest = load_snapshot(data_path, Path(args.notices) if args.notices else None, cutoff)
    groups = [tuple(item.split("/", 1)) for item in args.group]
    fitted = None
    model_status = {"status": "BASELINE_ONLY_NO_MODEL_DIR"}
    if args.model_dir:
        model_dir = Path(args.model_dir)
        manifest_path = model_dir / "manifest.json"
        if not manifest_path.is_file():
            raise FileNotFoundError(f"model artifact manifest not found: {manifest_path}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("artifact_schema_version") != 1:
            raise ValueError(f"unsupported model artifact schema: {manifest.get('artifact_schema_version')!r}")
        model_filename = manifest.get("model_file")
        if not model_filename:
            raise ValueError(f"model artifact has no trained model file; candidate status={manifest.get('candidate_status')}")
        model_path = model_dir / model_filename
        if not model_path.is_file():
            raise FileNotFoundError(f"trained model file not found: {model_path}")
        if manifest.get("target_mode") not in {"direct", "residual_to_weekday_median"}:
            raise ValueError(f"unsupported serialized target mode: {manifest.get('target_mode')!r}")
        from catboost import CatBoostRegressor
        model = CatBoostRegressor()
        try:
            model.load_model(str(model_path))
        except Exception as exc:
            raise ValueError(f"failed to load trained candidate from {model_path}: {type(exc).__name__}: {exc}") from exc
        fitted = FittedFoodDemandV2(
            model=model,
            feature_names=manifest.get("feature_names", []),
            config=manifest.get("config", {"target_mode": manifest["target_mode"], "candidate_id": manifest.get("candidate_id"), "use_notices": True}),
            trained_through=manifest.get("trained_through", "UNKNOWN"),
            data_version=manifest.get("data_version", manifest.get("dataset_sha256", "UNKNOWN")),
            model_version=manifest.get("model_version", "unknown"),
            candidate_status=manifest.get("candidate_status"),
        )
        model_status = {"status": "LOADED_LOCAL_MODEL", "model_dir": str(model_dir), "candidate_id": manifest.get("candidate_id"), "model_version": fitted.model_version, "training_dataset_sha256": manifest.get("dataset_sha256"), "trained_through": fitted.trained_through, "target_mode": manifest.get("target_mode")}
    predictions = predict_as_of(snapshot, cutoff=cutoff, target_date=date.fromisoformat(args.target), groups=groups, fitted=fitted)
    print(json.dumps({"dataset_sha256": digest, "model_status": model_status, "prediction_ledger": predictions}, ensure_ascii=False, indent=2))


def cmd_report(args):
    path = Path(args.run) / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("audit", "backtest", "fit", "predict"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--data", required=True, help="local normalized dated demand CSV")
        cmd.add_argument("--notices", help="local official notice CSV; admitted only with explicit timestamp/review fields")
        cmd.add_argument("--output", default=str(DEFAULT_OUTPUT))
        if name == "audit":
            cmd.set_defaults(func=cmd_audit)
        elif name == "backtest":
            cmd.add_argument("--warmup-days", type=int, default=180)
            cmd.add_argument("--block-days", type=int, default=28)
            cmd.add_argument("--iterations", type=int, default=200)
            cmd.add_argument("--seed", type=int, default=42)
            cmd.add_argument("--plan-workbook", action="append", default=[], help="optional workbook(s), Planlanan rows only as comparator")
            cmd.add_argument("--chronos-checkpoint", default="amazon/chronos-2")
            cmd.add_argument("--chronos-device", choices=["auto", "mps", "cuda", "cpu"], default="auto")
            cmd.add_argument("--allow-chronos-download", action="store_true", help="download only the public checkpoint; all inference remains local")
            cmd.add_argument("--no-chronos2", dest="run_chronos2", action="store_false")
            cmd.set_defaults(run_chronos2=True)
            cmd.set_defaults(func=cmd_backtest)
        elif name == "fit":
            cmd.add_argument("--cutoff", required=True)
            cmd.add_argument("--iterations", type=int, default=350)
            cmd.add_argument("--seed", type=int, default=42)
            cmd.add_argument("--target-mode", choices=["direct", "residual_to_weekday_median"], default="direct")
            cmd.set_defaults(func=cmd_fit)
        else:
            cmd.add_argument("--cutoff", required=True)
            cmd.add_argument("--target", required=True)
            cmd.add_argument("--group", action="append", default=[], help="campus/meal; repeat per group")
            cmd.add_argument("--model-dir", help="local fit run directory containing manifest.json and catboost.cbm; omitted means baseline only")
            cmd.set_defaults(func=cmd_predict)
    report = sub.add_parser("report")
    report.add_argument("--run", required=True)
    report.set_defaults(func=cmd_report)
    return root


if __name__ == "__main__":
    arguments = parser().parse_args()
    arguments.func(arguments)
