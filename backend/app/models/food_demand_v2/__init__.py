"""Causal, shadow-only cafeteria demand forecasting primitives.

Historical service rows are treated as available at 12:00 on the following day.
This is an explicit, unverified backtest assumption. Features are rebuilt from raw
outcomes; precomputed lags and unvintaged menu, calendar, notice, and weather fields
are deliberately ignored.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
import hashlib
import json
import math
from typing import Any, Iterable, Mapping, Sequence
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

TZ = ZoneInfo("Europe/Istanbul")
CUTOFF_HOUR = 16
ASSUMPTION = "ASSUMED_NEXT_DAY_12_LOCAL"
MODEL_VERSION = "food-demand-v2.0.0"
_SNAPSHOT_CACHE: dict[int, dict[str, Any]] = {}


@dataclass
class FittedFoodDemandV2:
    model: Any
    feature_names: list[str]
    config: dict[str, Any]
    trained_through: str
    data_version: str
    model_version: str = MODEL_VERSION
    candidate_status: dict[str, str] | None = None
    fit_cutoff: str | None = None


def _local_datetime(value: datetime | str) -> datetime:
    result = pd.Timestamp(value).to_pydatetime()
    if result.tzinfo is None:
        result = result.replace(tzinfo=TZ)
    return result.astimezone(TZ)


def _service_available_by(service_day: date, cutoff: datetime) -> bool:
    available = datetime.combine(service_day + timedelta(days=1), time(12), TZ)
    return available <= cutoff


def _asof_snapshot_digest(snapshot: pd.DataFrame, cutoff: datetime) -> str:
    available = snapshot[snapshot["date"].map(lambda day: _service_available_by(day, cutoff)).astype(bool)].reset_index(drop=True)
    return hashlib.sha256(pd.util.hash_pandas_object(available, index=False).values.tobytes()).hexdigest()


def _float_or_none(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (list, tuple, set)):
        return bool(value)
    try:
        return not bool(pd.isna(value))
    except (TypeError, ValueError):
        return True


def _notice_scope_matches(scope: Any, requested: str) -> bool:
    if not _has_value(scope):
        return False
    if isinstance(scope, (list, tuple, set)):
        values = [str(item).strip() for item in scope]
    else:
        raw = str(scope).strip()
        if raw == "*":
            return True
        values = [part.strip() for part in raw.replace(";", ",").split(",")]
    return any(value == requested for value in values)


def prepare_snapshot(
    rows: pd.DataFrame | str,
    *,
    as_of: datetime | str,
    notices: pd.DataFrame | None = None,
    source_hash: str | None = None,
) -> pd.DataFrame:
    """Normalize only dated outcome fields and explicitly published notice fields."""
    frame = pd.read_csv(rows) if isinstance(rows, (str, __import__("pathlib").Path)) else rows.copy()
    required = {"date", "campus", "meal", "demand"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"snapshot missing required columns: {sorted(missing)}")
    frame = frame[["date", "campus", "meal", "demand"]].copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce").dt.date
    frame["campus"] = frame["campus"].astype("string").str.strip()
    frame["meal"] = frame["meal"].astype("string").str.strip()
    frame["demand"] = pd.to_numeric(frame["demand"], errors="coerce")
    frame.loc[~np.isfinite(frame["demand"].fillna(0)), "demand"] = np.nan
    frame = frame.dropna(subset=["date", "campus", "meal"])
    if frame.duplicated(["date", "campus", "meal"]).any():
        raise ValueError("snapshot contains duplicate date/campus/meal rows")
    frame = frame.sort_values(["date", "campus", "meal"]).reset_index(drop=True)
    frame.attrs["as_of"] = _local_datetime(as_of).isoformat()
    frame.attrs["historical_availability_assumption"] = ASSUMPTION
    frame.attrs["source_hash"] = source_hash
    frame.attrs["notice_rows"] = _prepare_notices(notices)
    group_rows: dict[tuple[str, str], list[tuple[date, float | None]]] = {}
    campus_first_seen: dict[str, date] = {}
    for key, group in frame.groupby(["campus", "meal"], sort=False):
        group_rows[(str(key[0]), str(key[1]))] = [
            (row.date, None if pd.isna(row.demand) else float(row.demand))
            for row in group.itertuples(index=False)
        ]
        campus_name = str(key[0])
        first_seen = min(group["date"])
        campus_first_seen[campus_name] = min(campus_first_seen.get(campus_name, first_seen), first_seen)
    meal_daily: dict[str, dict[date, tuple[float, int]]] = {}
    observed = frame[frame["demand"].notna()]
    for meal, group in observed.groupby("meal", sort=False):
        daily = group.groupby("date", sort=False).agg(total=("demand", "sum"), coverage=("campus", "nunique"))
        meal_daily[str(meal)] = {day: (float(row.total), int(row.coverage)) for day, row in daily.iterrows()}
    _SNAPSHOT_CACHE[id(frame)] = {
        "group_rows": group_rows,
        "meal_daily": meal_daily,
        "campus_count": int(frame["campus"].nunique()),
        "campus_first_seen": campus_first_seen,
    }
    return frame


def _scope_text(value: Any) -> str:
    if not _has_value(value):
        return ""
    return " ".join(str(value or "").casefold().replace("’", "'").split())


def _is_explicit_all_campuses(value: Any, text: str) -> bool:
    scope = _scope_text(value)
    return scope in {"*", "all", "all campuses", "tüm kampüsler", "tum kampusler", "bütün kampüsler", "butun kampusler"} or any(
        phrase in text for phrase in ("tüm kampüslerde", "tum kampuslerde", "bütün kampüslerde", "butun kampuslerde")
    )


def _is_explicit_all_meals(value: Any, text: str) -> bool:
    scope = _scope_text(value)
    return scope in {"*", "all", "all meals", "tüm öğünler", "tum ogunler", "bütün öğünler", "butun ogunler"} or any(
        phrase in text for phrase in ("tüm öğünlerde", "tum ogunlerde", "bütün öğünlerde", "butun ogunlerde", "tüm yemek servislerinde")
    )


def _has_food_service_context(text: str) -> bool:
    return any(term in text for term in ("yemek", "yemekhane", "kafeterya", "lokanta", "öğle yemeği", "ogle yemegi", "akşam yemeği", "aksam yemegi"))


def _notice_rule_labels(row: Mapping[str, Any], *, scoped: bool) -> dict[str, bool | None]:
    text = " ".join(str(row.get(key)) for key in ("title", "notice_text") if _has_value(row.get(key))).casefold()
    if not scoped or not _has_food_service_context(text):
        return {key: None for key in ("closure", "reservation_required", "package_meal", "hours_notice", "price_change")}
    explicit_closure = any(phrase in text for phrase in (
        "yemek hizmeti verilmeyecektir", "yemek hizmeti verilmeyecek", "yemekhane hizmeti verilmeyecektir",
        "yemekhane kapalı olacaktır", "yemekhane kapali olacaktir", "yemekhane kapalıdır", "yemekhane kapalidir",
        "kafeterya kapalı olacaktır", "kafeterya kapali olacaktir", "yemek servisi yapılmayacaktır", "yemek servisi yapilmayacaktir",
    ))
    reservation = "rezervasyon" in text and any(phrase in text for phrase in (
        "rezervasyon zorunlu", "rezervasyon gerekmektedir", "rezervasyon yaptırılması gerekmektedir",
        "rezervasyon yaptirilmasi gerekmektedir", "rezervasyon şart", "rezervasyon sart",
    ))
    package_meal = "paket yemek" in text or "paket olarak yemek" in text
    hours_notice = "saat" in text and any(word in text for word in ("hizmet", "yemekhane", "kiosk", "büfe", "bufe"))
    price_change = "ücret" in text and any(word in text for word in ("güncellen", "artış", "değiş", "fiyat"))
    return {
        "closure": True if explicit_closure else None,
        "reservation_required": True if reservation else None,
        "package_meal": True if package_meal else None,
        "hours_notice": True if hours_notice else None,
        "price_change": True if price_change else None,
    }


def _prepare_notices(notices: pd.DataFrame | None) -> list[dict[str, Any]]:
    if notices is None:
        return []
    prepared: list[dict[str, Any]] = []
    for row in notices.to_dict(orient="records"):
        published = row.get("published_at") if _has_value(row.get("published_at")) else row.get("available_at")
        if not _has_value(published):
            published = row.get("published_date")
        if _has_value(published) and len(str(published).strip()) == 10:
            # Date-only source: conservatively available from the next local midnight.
            day = pd.Timestamp(published).date()
            published = datetime.combine(day + timedelta(days=1), time(0), TZ).isoformat()
        effective = row.get("effective_date") if _has_value(row.get("effective_date")) else row.get("valid_from")
        text = " ".join(str(row.get(key)) for key in ("title", "notice_text") if _has_value(row.get(key))).casefold()
        campus = row.get("campus") if _has_value(row.get("campus")) else row.get("affected_campuses")
        meal = row.get("meal") if _has_value(row.get("meal")) else row.get("affected_meals")
        if _is_explicit_all_campuses(campus, text):
            campus = "*"
        if _is_explicit_all_meals(meal, text):
            meal = "*"
        scope_resolved = _has_value(campus) and _has_value(meal)
        item: dict[str, Any] = {
            "campus": campus,
            "meal": meal,
            "effective_date": str(effective)[:10] if _has_value(effective) else None,
            "valid_to": str(row.get("valid_to"))[:10] if _has_value(row.get("valid_to")) else None,
            "published_at": None,
            "closure": None,
            "reservation_required": None,
            "package_meal": None,
            "hours_notice": None,
            "price_change": None,
            "source_hash": row.get("source_hash") if _has_value(row.get("source_hash")) else row.get("source_html_sha256"),
            "status": "UNKNOWN",
        }
        if _has_value(published):
            try:
                item["published_at"] = _local_datetime(str(published)).isoformat()
                labels = _notice_rule_labels(row, scoped=scope_resolved)
                if str(row.get("review_status", "")).upper() == "REVIEWED" and scope_resolved and _has_food_service_context(text):
                    for key in ("closure", "reservation_required", "package_meal", "hours_notice", "price_change"):
                        value = row.get(key)
                        if value is not None and pd.notna(value) and bool(value):
                            item[key] = True
                    item["status"] = "REVIEWED_EXPLICIT_FIELDS"
                else:
                    item.update(labels)
                    if any(item[key] is True for key in ("closure", "reservation_required", "package_meal", "hours_notice", "price_change")):
                        item["status"] = "RULE_EXTRACTED_UNREVIEWED"
            except (TypeError, ValueError):
                pass
        prepared.append(item)
    return prepared

def _known_history(snapshot: pd.DataFrame, *, cutoff: datetime, campus: str, meal: str) -> pd.DataFrame:
    cache = _SNAPSHOT_CACHE.get(id(snapshot), {})
    rows = cache.get("group_rows", {}).get((campus, meal), [])
    latest_available_service = cutoff.date() - timedelta(days=1)
    return [(day, value) for day, value in rows if day <= latest_available_service and value is not None]


def build_features(
    snapshot: pd.DataFrame,
    *,
    target_date: date | str,
    as_of: datetime | str,
    campus: str,
    meal: str,
) -> dict[str, Any]:
    """Build only information available at the specified local forecast cutoff."""
    cutoff = _local_datetime(as_of)
    target = pd.Timestamp(target_date).date()
    if cutoff.hour != CUTOFF_HOUR or cutoff.minute != 0:
        raise ValueError("forecast cutoff must be exactly 16:00 Europe/Istanbul")
    if cutoff.date() != target - timedelta(days=1):
        raise ValueError("cutoff must be on D-1 for the requested target date")
    history = _known_history(snapshot, cutoff=cutoff, campus=campus, meal=meal)
    recent_56 = [(day, value) for day, value in history if (target - day).days <= 56]
    same_weekday = [(day, value) for day, value in recent_56 if day.weekday() == target.weekday()]
    by_day = dict(history)
    cache = _SNAPSHOT_CACHE.get(id(snapshot), {})
    latest_available_service = cutoff.date() - timedelta(days=1)
    expected_campuses = sum(first_seen <= latest_available_service for first_seen in cache.get("campus_first_seen", {}).values())
    meal_daily = cache.get("meal_daily", {}).get(meal, {})
    cross_lags = {}
    for lag in (7, 14, 28):
        lag_day = target - timedelta(days=lag)
        row = meal_daily.get(lag_day)
        if row is not None and lag_day > cutoff.date() - timedelta(days=1):
            row = None
        full = row is not None and row[1] == expected_campuses
        cross_lags[f"cross_campus_total_lag_{lag}"] = row[0] if full else None
        cross_lags[f"cross_campus_coverage_lag_{lag}"] = float(row[1] / expected_campuses) if row is not None and expected_campuses else 0.0
    same_weekday_median = float(np.median([value for _, value in same_weekday])) if same_weekday else None
    recent_median = float(np.median([value for _, value in recent_56])) if recent_56 else None
    features: dict[str, Any] = {
        "campus": campus,
        "meal": meal,
        "weekday": target.weekday(),
        "month": target.month,
        "day_of_year_sin": math.sin(2 * math.pi * target.timetuple().tm_yday / 366),
        "day_of_year_cos": math.cos(2 * math.pi * target.timetuple().tm_yday / 366),
        "same_weekday_median": same_weekday_median,
        "same_weekday_n": int(len(same_weekday)),
        "recent_56_median": recent_median,
        "recent_56_n": int(len(recent_56)),
        "lag_7": by_day.get(target - timedelta(days=7)),
        "lag_14": by_day.get(target - timedelta(days=14)),
        "lag_28": by_day.get(target - timedelta(days=28)),
        **cross_lags,
        "history_n": int(len(history)),
        "history_max_service_date": max(day for day, _ in history).isoformat() if history else None,
        "menu_status": "UNKNOWN_UNVINTAGED",
        "calendar_status": "UNKNOWN_UNVINTAGED",
        "weather_status": "UNKNOWN_NO_FORECAST_VINTAGE",
        "notice_status": "UNKNOWN",
        "closure": None,
        "reservation_required": None,
        "package_meal": None,
        "hours_notice": None,
        "price_change": None,
    }
    matching: list[dict[str, Any]] = []
    for notice in snapshot.attrs.get("notice_rows", []):
        effective_from = notice.get("effective_date")
        effective_to = notice.get("valid_to") or effective_from
        if not effective_from or not (effective_from <= target.isoformat() <= effective_to):
            continue
        if not _notice_scope_matches(notice.get("campus"), campus) or not _notice_scope_matches(notice.get("meal"), meal):
            continue
        published = notice.get("published_at")
        if published is None or _local_datetime(published) > cutoff:
            continue
        if notice.get("status") in {"REVIEWED_EXPLICIT_FIELDS", "RULE_EXTRACTED_UNREVIEWED"}:
            matching.append(notice)
    if matching:
        features["notice_status"] = "RULE_EXTRACTED_UNREVIEWED" if any(n.get("status") == "RULE_EXTRACTED_UNREVIEWED" for n in matching) else "REVIEWED_EXPLICIT_FIELDS"
        features["notice_source_hashes"] = [row.get("source_hash") for row in matching if row.get("source_hash")]
        for key in ("closure", "reservation_required", "package_meal", "hours_notice", "price_change"):
            values = [row[key] for row in matching if row.get(key) is not None]
            if values:
                features[key] = values[-1]
    return features


def _candidate_matrix(features: Sequence[Mapping[str, Any]], *, use_notices: bool = True) -> pd.DataFrame:
    columns = ["campus", "meal", "weekday", "month", "day_of_year_sin", "day_of_year_cos", "same_weekday_median", "same_weekday_n", "recent_56_median", "recent_56_n", "lag_7", "lag_14", "lag_28", "cross_campus_total_lag_7", "cross_campus_coverage_lag_7", "cross_campus_total_lag_14", "cross_campus_coverage_lag_14", "cross_campus_total_lag_28", "cross_campus_coverage_lag_28", "closure", "reservation_required", "package_meal", "hours_notice", "price_change"]
    notice_columns = {"closure", "reservation_required", "package_meal", "hours_notice", "price_change"}
    matrix = pd.DataFrame([
        {key: (item.get(key) if use_notices or key not in notice_columns else None) for key in columns}
        for item in features
    ], columns=columns)
    for key in ("campus", "meal"):
        matrix[key] = matrix[key].fillna("UNKNOWN").astype(str)
    for key in columns:
        if key not in ("campus", "meal"):
            matrix[key] = pd.to_numeric(matrix[key], errors="coerce")
    return matrix


def _historical_training_rows(snapshot: pd.DataFrame, *, as_of: datetime) -> tuple[list[dict[str, Any]], list[float]]:
    train_features: list[dict[str, Any]] = []
    labels: list[float] = []
    available = snapshot[snapshot["date"].map(lambda day: _service_available_by(day, as_of)).astype(bool) & snapshot["demand"].notna()]
    if available.empty:
        return train_features, labels
    first_day = min(snapshot["date"])
    for row in available.itertuples(index=False):
        target_day = row.date
        cutoff = datetime.combine(target_day - timedelta(days=1), time(CUTOFF_HOUR), TZ)
        if target_day - first_day < timedelta(days=56):
            continue
        feature = build_features(snapshot, target_date=target_day, as_of=cutoff, campus=row.campus, meal=row.meal)
        if feature["history_n"] < 1:
            continue
        feature["_target_service_date"] = target_day.isoformat()
        train_features.append(feature)
        labels.append(float(row.demand))
    return train_features, labels


def fit(snapshot: pd.DataFrame, config: Mapping[str, Any] | None = None) -> FittedFoodDemandV2:
    """Fit pooled direct-MAE CatBoost on leakage-safe historical features."""
    config = dict(config or {})
    cutoff = _local_datetime(config.get("as_of", snapshot.attrs.get("as_of")))
    train_x, train_y = _historical_training_rows(snapshot, as_of=cutoff)
    target_mode = str(config.get("target_mode", "direct"))
    if target_mode not in {"direct", "residual_to_weekday_median"}:
        raise ValueError(f"unsupported target_mode: {target_mode}")
    if target_mode == "residual_to_weekday_median":
        eligible_training_rows = [
            (feature, actual)
            for feature, actual in zip(train_x, train_y)
            if feature["same_weekday_median"] is not None or feature["recent_56_median"] is not None
        ]
        train_x = [feature for feature, _ in eligible_training_rows]
        train_y = [actual for _, actual in eligible_training_rows]
    labels = train_y if target_mode == "direct" else [
        float(actual) - float(feature["same_weekday_median"] if feature["same_weekday_median"] is not None else feature["recent_56_median"])
        for feature, actual in zip(train_x, train_y)
    ]
    candidate_id = "catboost_direct_mae" if target_mode == "direct" else "catboost_residual_to_weekday_median"
    candidate_status = {candidate_id: "PENDING", "chronos_2": "UNAVAILABLE_NOT_RUN", "tabpfn_ts_3_5": "UNAVAILABLE_NOT_RUN"}
    model = None
    matrix = _candidate_matrix(train_x, use_notices=bool(config.get("use_notices", True)))
    if len(labels) < int(config.get("min_training_rows", 20)):
        candidate_status[candidate_id] = f"FAILED:INSUFFICIENT_TRAINING_ROWS:{len(labels)}"
    else:
        try:
            from catboost import CatBoostRegressor
            model = CatBoostRegressor(
                loss_function="MAE",
                iterations=int(config.get("iterations", 350)),
                depth=int(config.get("depth", 7)),
                learning_rate=float(config.get("learning_rate", 0.05)),
                random_seed=int(config.get("seed", 42)),
                verbose=False,
                allow_writing_files=False,
                task_type="CPU",
            )
            model.fit(matrix, np.asarray(labels), cat_features=["campus", "meal"])
            candidate_status[candidate_id] = "FIT_CPU"
        except ImportError as exc:
            model = None
            candidate_status[candidate_id] = f"FAILED:CATBOOST_UNAVAILABLE:{str(exc)[:180]}"
        except Exception as exc:
            model = None
            candidate_status[candidate_id] = f"FAILED:{type(exc).__name__}:{str(exc)[:180]}"
    dataset_digest = _asof_snapshot_digest(snapshot, cutoff)
    trained_dates = [feature["_target_service_date"] for feature in train_x]
    return FittedFoodDemandV2(
        model=model,
        feature_names=list(matrix.columns),
        config={**config, "loss": "MAE", "target_mode": target_mode, "candidate_id": candidate_id, "training_rows": len(labels), "historical_availability_assumption": ASSUMPTION},
        trained_through=max(trained_dates, default="UNKNOWN"),
        data_version=dataset_digest,
        candidate_status=candidate_status,
        fit_cutoff=cutoff.isoformat(),
    )


def predict_as_of(
    snapshot: pd.DataFrame,
    *,
    cutoff: datetime | str,
    target_date: date | str,
    groups: Iterable[tuple[str, str]],
    fitted: FittedFoodDemandV2 | None = None,
) -> list[dict[str, Any]]:
    """Create an auditable prediction ledger; missing history remains unavailable."""
    cutoff_dt = _local_datetime(cutoff)
    target = pd.Timestamp(target_date).date()
    if fitted is not None:
        validate_fitted_timing(fitted, cutoff_dt)
    inference_data_version = _asof_snapshot_digest(snapshot, cutoff_dt)
    rows = []
    for campus, meal in groups:
        features = build_features(snapshot, target_date=target, as_of=cutoff_dt, campus=campus, meal=meal)
        baseline = features["same_weekday_median"] if features["same_weekday_median"] is not None else features["recent_56_median"]
        prediction: float | None = None
        model_id = "past_same_weekday_median"
        status = "BASELINE_ONLY" if baseline is not None else "INSUFFICIENT_DATA"
        if fitted is not None and fitted.model is not None and features["history_n"] >= 7:
            try:
                value = float(fitted.model.predict(_candidate_matrix([features], use_notices=bool(fitted.config.get("use_notices", True))))[0])
                if fitted.config.get("target_mode") == "residual_to_weekday_median":
                    base = features["same_weekday_median"] if features["same_weekday_median"] is not None else features["recent_56_median"]
                    if base is None:
                        raise ValueError("no causal baseline for residual candidate")
                    value += float(base)
                if math.isfinite(value):
                    prediction = max(0.0, value)
                    model_id = fitted.config.get("candidate_id", "catboost_direct_mae")
                    status = "MODEL_ESTIMATE"
            except Exception as exc:
                status = f"MODEL_FAILED:{type(exc).__name__}"
        if prediction is None and baseline is not None:
            prediction = max(0.0, float(baseline))
        rows.append({
            "target_date": target.isoformat(),
            "campus": campus,
            "meal": meal,
            "cutoff": cutoff_dt.isoformat(),
            "prediction": prediction,
            "model_id": model_id,
            "model_version": fitted.model_version if fitted else "baseline-v2",
            "data_version": fitted.data_version if fitted else inference_data_version,
            "input_data_version": inference_data_version,
            "data_coverage": {"history_rows": features["history_n"], "same_weekday_rows": features["same_weekday_n"], "history_max_service_date": features["history_max_service_date"]},
            "source_assumption": ASSUMPTION,
            "status": status,
        })
    return rows


def validate_fitted_timing(fitted: FittedFoodDemandV2, cutoff: datetime | str) -> None:
    cutoff_dt = _local_datetime(cutoff)
    if fitted.fit_cutoff is None:
        raise ValueError("fitted model is missing its fit cutoff metadata")
    if _local_datetime(fitted.fit_cutoff) > cutoff_dt:
        raise ValueError("fitted model cutoff is later than prediction cutoff")
    try:
        latest_training_day = date.fromisoformat(fitted.trained_through)
    except (TypeError, ValueError) as exc:
        raise ValueError("fitted model is missing a valid latest training label date") from exc
    if not _service_available_by(latest_training_day, cutoff_dt):
        raise ValueError("fitted model includes a training label unavailable by prediction cutoff")


def evaluate_predictions(actual: Sequence[float | int | None], predicted: Sequence[float | int | None]) -> dict[str, Any]:
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")
    pairs = [(float(a), float(p)) for a, p in zip(actual, predicted) if _float_or_none(a) is not None and _float_or_none(p) is not None]
    if not pairs:
        return {"n": 0, "mae": None, "wape_pct": None, "bias": None, "coverage_pct": 0.0}
    errors = [p - a for a, p in pairs]
    denominator = sum(abs(a) for a, _ in pairs)
    return {
        "n": len(pairs),
        "mae": float(np.mean(np.abs(errors))),
        "wape_pct": None if denominator == 0 else float(np.sum(np.abs(errors)) / denominator * 100),
        "bias": float(np.mean(errors)),
        "coverage_pct": float(len(pairs) / max(1, len(actual)) * 100),
    }


def learn_simplex_weights(actual: Sequence[float], prediction_columns: Mapping[str, Sequence[float]]) -> dict[str, float]:
    """Fit a nonnegative sum-to-one MAE blend on prior causal OOF predictions."""
    names = list(prediction_columns)
    if not names:
        return {}
    matrix = np.asarray([prediction_columns[name] for name in names], dtype=float).T
    target = np.asarray(actual, dtype=float)
    if matrix.shape[0] != len(target) or matrix.shape[0] == 0:
        return {name: (1.0 if index == 0 else 0.0) for index, name in enumerate(names)}
    try:
        from scipy.optimize import minimize
        result = minimize(lambda w: np.mean(np.abs(matrix @ w - target)), np.full(len(names), 1 / len(names)), method="SLSQP", bounds=[(0, 1)] * len(names), constraints=[{"type": "eq", "fun": lambda w: np.sum(w) - 1}], options={"maxiter": 500, "ftol": 1e-10})
        weights = result.x if result.success else np.eye(1, len(names), 0).reshape(-1)
    except Exception:
        weights = np.eye(1, len(names), 0).reshape(-1)
    return {name: float(weight) for name, weight in zip(names, weights)}


__all__ = ["ASSUMPTION", "FittedFoodDemandV2", "build_features", "evaluate_predictions", "fit", "learn_simplex_weights", "predict_as_of", "prepare_snapshot"]
