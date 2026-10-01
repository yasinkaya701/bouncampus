#!/usr/bin/env python3
from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_menu_demand():
    path = ROOT / "backend/app/decision/menu_demand.py"
    if not path.exists():
        raise AssertionError("menu-demand adjustment module missing")
    spec = importlib.util.spec_from_file_location("cs1_menu_demand", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CATALOG = [
    {"name": "Köfte", "popularity_score": 0.90},
    {"name": "Mercimek Çorbası", "popularity_score": 0.90},
    {"name": "Baklava", "popularity_score": 0.95},
    {"name": "Kuru Fasulye", "popularity_score": 0.68},
    {"name": "Bamya Çorbası", "popularity_score": 0.65},
]


def test_popular_menu_increases_and_low_popularity_menu_reduces_demand() -> None:
    mod = load_menu_demand()
    popular = mod.build_menu_demand_adjustment(
        {
            "main_dish": "Köfte",
            "soup": "Mercimek Çorbası",
            "options": ["Baklava"],
            "popularity_multiplier": 1.12,
        },
        CATALOG,
        official_menu=True,
    )
    low = mod.build_menu_demand_adjustment(
        {
            "main_dish": "Kuru Fasulye",
            "soup": "Bamya Çorbası",
            "popularity_multiplier": 0.92,
        },
        CATALOG,
        official_menu=True,
    )
    assert popular["factor"] > 1.0
    assert low["factor"] < 1.0
    assert popular["factor"] > low["factor"]
    assert mod.apply_menu_adjustment(1000, popular["factor"]) > 1000
    assert mod.apply_menu_adjustment(1000, low["factor"]) < 1000


def test_unverified_menu_source_is_neutral() -> None:
    mod = load_menu_demand()
    result = mod.build_menu_demand_adjustment(
        {"main_dish": "Köfte", "popularity_multiplier": 1.12},
        CATALOG,
        official_menu=False,
    )
    assert result["factor"] == 1.0
    assert result["provenance"] == "UNAVAILABLE"
    assert "MENU_SOURCE_NOT_VERIFIED_LIVE" in result["reason_codes"]


def test_unknown_official_menu_uses_bounded_source_heuristic() -> None:
    mod = load_menu_demand()
    result = mod.build_menu_demand_adjustment(
        {"main_dish": "Bilinmeyen Yemek", "popularity_multiplier": 9.0},
        CATALOG,
        official_menu=True,
    )
    assert result["factor"] == 1.12
    assert result["provenance"] == "POLICY_HEURISTIC_SOURCE"
    assert "SOURCE_MULTIPLIER_FALLBACK" in result["reason_codes"]


def test_food_api_exposes_non_actionable_planning_candidate() -> None:
    schema_path = ROOT / "backend/app/schemas.py"
    route_path = ROOT / "backend/app/routers/food.py"

    schema_tree = ast.parse(schema_path.read_text(encoding="utf-8"))
    forecast_class = next(
        node
        for node in schema_tree.body
        if isinstance(node, ast.ClassDef) and node.name == "FoodDemandForecast"
    )
    fields = {
        node.target.id
        for node in forecast_class.body
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
    }
    assert "planning_candidate_production" in fields
    assert "planning_candidate_semantics" in fields

    route_tree = ast.parse(route_path.read_text(encoding="utf-8"))
    forecast_calls = [
        node
        for node in ast.walk(route_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "FoodDemandForecast"
    ]
    assert forecast_calls, "FoodDemandForecast constructor missing from food route"
    keywords = {kw.arg: kw.value for kw in forecast_calls[0].keywords if kw.arg}
    candidate = keywords.get("planning_candidate_production")
    semantics = keywords.get("planning_candidate_semantics")
    assert isinstance(candidate, ast.Name) and candidate.id == "menu_adjusted_forecast"
    assert isinstance(semantics, ast.Constant)
    assert semantics.value == "ADVISORY_MODEL_ESTIMATE_NOT_AUTHORIZED_KITCHEN_ORDER"


def main() -> int:
    tests = [
        test_popular_menu_increases_and_low_popularity_menu_reduces_demand,
        test_unverified_menu_source_is_neutral,
        test_unknown_official_menu_uses_bounded_source_heuristic,
        test_food_api_exposes_non_actionable_planning_candidate,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} food menu-adjustment tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
