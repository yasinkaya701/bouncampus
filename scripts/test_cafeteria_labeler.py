#!/usr/bin/env python3
"""Focused regression tests for scripts/cafeteria_labeler.py.

Run from repository root:
    python scripts/test_cafeteria_labeler.py
"""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("cafeteria_labeler", ROOT / "scripts" / "cafeteria_labeler.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_official_registry_wins():
    registry = {
        MODULE.norm("Pirinç Pilavı"): {
            "canonical_name": "Pirinç Pilavı",
            "official_category": "SIDE_STARCH",
            "protein_class": "NONE",
            "diet_class": "PLANT_BASED_HEURISTIC",
            "kcal": "399",
            "portion_g": "",
            "ingredients": "Pirinç|Sıvıyağ|Tuz",
            "label_provenance": "OFFICIAL_DISH_PAGE",
        }
    }
    result = MODULE.label_dish("Pirinç Pilavı", registry)
    assert result["dish_role"] == "SIDE_STARCH"
    assert result["kcal"] == "399"
    assert result["label_provenance"] == "OFFICIAL_DISH_PAGE"
    assert result["label_confidence"] == "HIGH"


def test_explicit_vegan_not_collapsed_into_meat_keyword():
    result = MODULE.label_dish("Vegan Misket Köfte", {})
    assert result["diet_class"] == "VEGAN_EXPLICIT"
    assert result["dish_role"] == "MAIN_PLANT"
    assert result["protein_class"] == "PLANT_OTHER"


def test_name_only_plant_label_is_heuristic():
    result = MODULE.label_dish("Nohut Yemeği", {})
    assert result["protein_class"] == "LEGUME"
    assert result["diet_class"] == "PLANT_BASED_HEURISTIC"
    assert result["label_provenance"] == "NAME_RULE_HEURISTIC"
    assert result["label_confidence"] == "LOW"


def test_red_meat_proxy_is_not_measured_impact():
    result = MODULE.label_dish("Tas Kebabı", {})
    assert result["protein_class"] == "RED_MEAT"
    assert result["carbon_intensity_proxy"] == "VERY_HIGH_PROXY"
    assert result["label_provenance"] == "NAME_RULE_HEURISTIC"


def test_sugary_drink_proxy():
    assert MODULE.label_dish("Kola", {})["sugary_drink_proxy"] == "1"
    assert MODULE.label_dish("Ayran", {})["sugary_drink_proxy"] == "0"


def test_service_aggregation():
    labels = [
        MODULE.label_dish("Tas Kebabı", {}),
        MODULE.label_dish("Nohut Yemeği", {}),
        MODULE.label_dish("Pirinç Pilavı", {}),
        MODULE.label_dish("Kola", {}),
        MODULE.label_dish("Supangle", {}),
    ]
    agg = MODULE.aggregate_service(labels)
    assert agg["menu_item_count"] == "5"
    assert agg["has_red_meat_main"] == "1"
    assert agg["has_legume_option"] == "1"
    assert agg["sugary_drink_count"] == "1"
    assert agg["dessert_count"] == "1"
    assert agg["max_carbon_proxy_ordinal"] == "4"


def test_menu_signature_order_invariant():
    assert MODULE.service_signature(["A", "B", "C"]) == MODULE.service_signature(["C", "A", "B"])


def run():
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} cafeteria labeler tests")


if __name__ == "__main__":
    run()
