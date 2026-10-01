#!/usr/bin/env python3
"""Expand normalized 8-slot standard cafeteria menus into item-level rows.

The monthly Boğaziçi menu layout preserves a stable semantic order:
1 soup, 2 main, 3 vegetarian/vegan, 4-5 sides, 6-8 selectable items.
We retain that official section role separately from finer heuristic/registry labels.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("cafeteria_labeler", ROOT / "scripts" / "cafeteria_labeler.py")
LABELER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(LABELER)

POSITION_ROLE = {
    1: "SOUP_SECTION",
    2: "MAIN_SECTION",
    3: "VEGETARIAN_VEGAN_SECTION",
    4: "SIDE_SECTION",
    5: "SIDE_SECTION",
    6: "SELECTABLE_SECTION",
    7: "SELECTABLE_SECTION",
    8: "SELECTABLE_SECTION",
}


def expand(menu_csv: Path, registry_csv: Path):
    registry = LABELER.load_registry(registry_csv)
    rows = []
    with menu_csv.open(newline="", encoding="utf-8-sig") as handle:
        for service in csv.DictReader(handle):
            for position, column in enumerate(LABELER.DISH_COLUMNS, start=1):
                raw_name = (service.get(column) or "").strip()
                if not raw_name:
                    continue
                labels = LABELER.label_dish(raw_name, registry)
                rows.append({
                    "service_date": service.get("service_date", ""),
                    "weekday_tr": service.get("weekday_tr", ""),
                    "service_type": service.get("service_type", ""),
                    "position": str(position),
                    "official_menu_role": POSITION_ROLE[position],
                    "official_role_provenance": "OFFICIAL_MENU_ROLE",
                    "raw_name": raw_name,
                    "canonical_name": labels["canonical_name"],
                    "fine_dish_role": labels["dish_role"],
                    "protein_class": labels["protein_class"],
                    "diet_class": labels["diet_class"],
                    "kcal": labels["kcal"],
                    "portion_g": labels["portion_g"],
                    "carbon_intensity_proxy": labels["carbon_intensity_proxy"],
                    "fine_label_provenance": labels["label_provenance"],
                    "fine_label_confidence": labels["label_confidence"],
                    "source_url": service.get("source_url", ""),
                    "truth_class": service.get("truth_class", ""),
                })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--menu-csv", type=Path, required=True)
    parser.add_argument("--registry", type=Path, default=ROOT / "research/cafeteria/official_dish_registry_seed.csv")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = expand(args.menu_csv, args.registry)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "service_date", "weekday_tr", "service_type", "position", "official_menu_role",
        "official_role_provenance", "raw_name", "canonical_name", "fine_dish_role",
        "protein_class", "diet_class", "kcal", "portion_g", "carbon_intensity_proxy",
        "fine_label_provenance", "fine_label_confidence", "source_url", "truth_class",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"WROTE: {len(rows)} item exposures -> {args.output}")


if __name__ == "__main__":
    main()
