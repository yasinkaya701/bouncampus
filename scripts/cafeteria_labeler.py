#!/usr/bin/env python3
"""Label Boğaziçi cafeteria menu records with reproducible, provenance-aware features.

Stdlib-only on purpose so research data preparation does not need the frontend or ML stack.
The labeler prefers exact official registry records and falls back to conservative name rules.
Heuristic dietary/allergen labels are never promoted to official facts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Mapping


DISH_COLUMNS = [f"dish_{i}" for i in range(1, 9)]

BEVERAGE_WORDS = (
    "ayran", "kola", "gazoz", "limonata", "ice tea", "soğuk çay", "soda",
    "meyve suyu", "meyveli içecek", "kefir", "komposto",
)
DESSERT_WORDS = (
    "tatlı", "puding", "muhallebi", "supangle", "baklava", "kadayıf",
    "şöbiyet", "şekerpare", "profiterol", "cheesecake", "sütlaç", "trileçe",
    "magnolia", "kazandibi", "tiramisu", "brownie", "pasta", "lokma",
    "tulumba", "höşmerim", "güllaç", "ekler",
)
STARCH_WORDS = (
    "pilav", "makarna", "spagetti", "erişte", "kuskus", "börek", "patates",
)
SALAD_WORDS = ("salata", "coleslaw", "piyaz", "kısır", "tabule", "tarator", "ezme", "haydari")
FRUIT_WORDS = ("meyve", "kavun", "karpuz", "elma", "armut", "portakal", "mandalina")
LEGUME_WORDS = ("nohut", "mercimek", "fasulye", "barbunya", "börülce")
POULTRY_WORDS = ("tavuk", "piliç", "hindi", "kanat")
FISH_WORDS = ("balık", "mezgit", "palamut", "somon", "hamsi", "levrek")
RED_MEAT_WORDS = (
    "dana", "kuzu", "etli", "et döner", "et sote", "gulaş", "kebap", "kebabı",
    "köfte", "kavurma", "beef", "ciğer", "yahni", "iskender", "alinazik",
)
EXPLICIT_VEGAN_WORDS = ("vegan",)
EXPLICIT_VEGETARIAN_WORDS = ("etsiz", "zy.", "zeytinyağlı")
SUGARY_DRINK_WORDS = ("kola", "gazoz", "ice tea", "soğuk çay", "limonata", "meyve suyu", "meyveli içecek")


def norm(value: str) -> str:
    value = (value or "").strip().lower()
    value = value.replace("ı", "i").replace("İ", "i")
    value = re.sub(r"\s+", " ", value)
    return value


def has_any(text: str, words: Iterable[str]) -> bool:
    n = norm(text)
    return any(norm(word) in n for word in words)


def load_registry(path: Path) -> Dict[str, Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return {norm(row["canonical_name"]): row for row in rows if row.get("canonical_name")}


def infer_name_labels(name: str) -> Dict[str, str]:
    n = norm(name)
    role = "UNKNOWN"
    protein = "UNKNOWN"
    diet = "UNKNOWN"

    if "çorba" in n:
        role = "SOUP"
    elif has_any(n, BEVERAGE_WORDS):
        role = "BEVERAGE"
    elif has_any(n, DESSERT_WORDS):
        role = "DESSERT"
    elif has_any(n, FRUIT_WORDS) and not has_any(n, DESSERT_WORDS):
        role = "FRUIT"
    elif has_any(n, SALAD_WORDS):
        role = "SALAD_COLD"
    elif has_any(n, STARCH_WORDS):
        role = "SIDE_STARCH"

    if has_any(n, FISH_WORDS):
        protein = "FISH"
        diet = "ANIMAL_BASED"
        if role == "UNKNOWN":
            role = "MAIN_ANIMAL"
    elif has_any(n, POULTRY_WORDS):
        protein = "POULTRY"
        diet = "ANIMAL_BASED"
        if role == "UNKNOWN":
            role = "MAIN_ANIMAL"
    elif has_any(n, RED_MEAT_WORDS):
        protein = "RED_MEAT"
        diet = "ANIMAL_BASED"
        if role == "UNKNOWN":
            role = "MAIN_ANIMAL"
    elif has_any(n, LEGUME_WORDS):
        protein = "LEGUME"
        if role == "UNKNOWN":
            role = "MAIN_PLANT"
        diet = "PLANT_BASED_HEURISTIC"

    if has_any(n, EXPLICIT_VEGAN_WORDS):
        diet = "VEGAN_EXPLICIT"
        if role in ("UNKNOWN", "MAIN_ANIMAL"):
            role = "MAIN_PLANT"
        if protein in ("UNKNOWN", "RED_MEAT", "POULTRY", "FISH"):
            protein = "PLANT_OTHER"
    elif has_any(n, EXPLICIT_VEGETARIAN_WORDS) and diet == "UNKNOWN":
        diet = "VEGETARIAN_EXPLICIT"
        if role == "UNKNOWN":
            role = "MAIN_PLANT"

    # Generic animal-looking mains that escaped specific protein classification.
    if role == "UNKNOWN" and any(token in n for token in ("mantı", "pizza", "hamburger", "cordon bleu")):
        role = "MAIN_ANIMAL"

    return {
        "dish_role": role,
        "protein_class": protein,
        "diet_class": diet,
        "label_provenance": "NAME_RULE_HEURISTIC",
        "label_confidence": "LOW",
    }


def carbon_proxy(protein_class: str) -> str:
    if protein_class == "RED_MEAT":
        return "VERY_HIGH_PROXY"
    if protein_class == "MIXED_ANIMAL":
        return "HIGH_PROXY"
    if protein_class in {"POULTRY", "FISH", "DAIRY_DOMINANT"}:
        return "MEDIUM_PROXY"
    if protein_class in {"LEGUME", "PLANT_OTHER", "NONE"}:
        return "LOW_PROXY"
    return "UNKNOWN"


def label_dish(name: str, registry: Mapping[str, Mapping[str, str]]) -> Dict[str, str]:
    base = infer_name_labels(name)
    official = registry.get(norm(name))
    if official:
        # Official values win only when populated. Exact ingredient/allergen fields remain as stored.
        for source, target in (
            ("official_category", "dish_role"),
            ("protein_class", "protein_class"),
            ("diet_class", "diet_class"),
        ):
            if official.get(source):
                base[target] = official[source]
        base["label_provenance"] = official.get("label_provenance") or "OFFICIAL_DISH_PAGE"
        base["label_confidence"] = "HIGH" if base["label_provenance"] == "OFFICIAL_DISH_PAGE" else "MEDIUM"

    base["canonical_name"] = official.get("canonical_name", name.strip()) if official else name.strip()
    base["kcal"] = official.get("kcal", "") if official else ""
    base["portion_g"] = official.get("portion_g", "") if official else ""
    base["ingredients"] = official.get("ingredients", "") if official else ""
    base["carbon_intensity_proxy"] = carbon_proxy(base["protein_class"])
    base["sugary_drink_proxy"] = "1" if has_any(name, SUGARY_DRINK_WORDS) else "0"
    base["popularity_status"] = "UNOBSERVED"
    return base


def service_signature(items: List[str]) -> str:
    canonical = "|".join(sorted(norm(item) for item in items if item.strip()))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def aggregate_service(labels: List[Dict[str, str]]) -> Dict[str, str]:
    roles = Counter(item["dish_role"] for item in labels)
    proteins = Counter(item["protein_class"] for item in labels)
    diets = Counter(item["diet_class"] for item in labels)
    known_kcal = [float(item["kcal"]) for item in labels if item.get("kcal")]
    known_portions = [float(item["portion_g"]) for item in labels if item.get("portion_g")]

    ordinal = {"UNKNOWN": 0, "LOW_PROXY": 1, "MEDIUM_PROXY": 2, "HIGH_PROXY": 3, "VERY_HIGH_PROXY": 4}
    max_carbon = max((ordinal[item["carbon_intensity_proxy"]] for item in labels), default=0)

    return {
        "menu_item_count": str(len(labels)),
        "has_red_meat_main": str(int(proteins["RED_MEAT"] > 0)),
        "has_poultry_main": str(int(proteins["POULTRY"] > 0)),
        "has_fish_main": str(int(proteins["FISH"] > 0)),
        "has_explicit_vegan_option": str(int(diets["VEGAN_EXPLICIT"] > 0)),
        "has_legume_option": str(int(proteins["LEGUME"] > 0)),
        "dessert_count": str(roles["DESSERT"]),
        "sugary_drink_count": str(sum(int(item["sugary_drink_proxy"]) for item in labels)),
        "starch_option_count": str(roles["SIDE_STARCH"]),
        "vegetable_option_count": str(roles["SIDE_VEGETABLE"] + roles["MAIN_PLANT"] + roles["SALAD_COLD"]),
        "mean_known_kcal": f"{sum(known_kcal) / len(known_kcal):.2f}" if known_kcal else "",
        "known_kcal_coverage": f"{len(known_kcal) / len(labels):.4f}" if labels else "0.0000",
        "mean_known_portion_g": f"{sum(known_portions) / len(known_portions):.2f}" if known_portions else "",
        "known_portion_coverage": f"{len(known_portions) / len(labels):.4f}" if labels else "0.0000",
        "max_carbon_proxy_ordinal": str(max_carbon),
    }


def process(menu_csv: Path, registry_csv: Path, dish_output: Path, service_output: Path) -> None:
    registry = load_registry(registry_csv)
    with menu_csv.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    dish_rows: List[Dict[str, str]] = []
    service_rows: List[Dict[str, str]] = []

    for row in rows:
        service_items = [row.get(col, "").strip() for col in DISH_COLUMNS if row.get(col, "").strip()]
        labels = []
        for position, item in enumerate(service_items, start=1):
            labeled = label_dish(item, registry)
            labels.append(labeled)
            dish_rows.append({
                "service_date": row.get("service_date", ""),
                "service_type": row.get("service_type", ""),
                "position": str(position),
                "raw_name": item,
                **labeled,
            })

        agg = aggregate_service(labels)
        service_rows.append({
            "service_date": row.get("service_date", ""),
            "weekday_tr": row.get("weekday_tr", ""),
            "service_type": row.get("service_type", ""),
            "menu_signature": service_signature(service_items),
            "menu_text_canonical": " | ".join(item["canonical_name"] for item in labels),
            **agg,
            "source_url": row.get("source_url", ""),
            "truth_class": row.get("truth_class", ""),
        })

    dish_output.parent.mkdir(parents=True, exist_ok=True)
    service_output.parent.mkdir(parents=True, exist_ok=True)

    dish_fields = [
        "service_date", "service_type", "position", "raw_name", "canonical_name", "dish_role",
        "protein_class", "diet_class", "kcal", "portion_g", "ingredients",
        "carbon_intensity_proxy", "sugary_drink_proxy", "popularity_status",
        "label_provenance", "label_confidence",
    ]
    with dish_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=dish_fields)
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in dish_fields} for row in dish_rows)

    service_fields = [
        "service_date", "weekday_tr", "service_type", "menu_signature", "menu_text_canonical",
        "menu_item_count", "has_red_meat_main", "has_poultry_main", "has_fish_main",
        "has_explicit_vegan_option", "has_legume_option", "dessert_count", "sugary_drink_count",
        "starch_option_count", "vegetable_option_count", "mean_known_kcal", "known_kcal_coverage",
        "mean_known_portion_g", "known_portion_coverage", "max_carbon_proxy_ordinal",
        "source_url", "truth_class",
    ]
    with service_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=service_fields)
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in service_fields} for row in service_rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--menu-csv", type=Path, required=True)
    parser.add_argument("--registry", type=Path, default=Path("research/cafeteria/official_dish_registry_seed.csv"))
    parser.add_argument("--dish-output", type=Path, required=True)
    parser.add_argument("--service-output", type=Path, required=True)
    args = parser.parse_args()
    process(args.menu_csv, args.registry, args.dish_output, args.service_output)


if __name__ == "__main__":
    main()
