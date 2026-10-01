#!/usr/bin/env python3
"""Build a frequency-ranked manual review queue for unresolved cafeteria dish labels.

The goal is active labeling: review the most frequent unresolved dishes first, enrich the
official registry when a source is found, rerun the labeler, and watch heuristic coverage fall.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("cafeteria_labeler", ROOT / "scripts" / "cafeteria_labeler.py")
LABELER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(LABELER)


def iter_dishes(menu_paths: Iterable[Path]):
    for path in menu_paths:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                for column in LABELER.DISH_COLUMNS:
                    value = (row.get(column) or "").strip()
                    if value:
                        yield path.name, value


def build_queue(menu_paths: Iterable[Path], registry_path: Path):
    registry = LABELER.load_registry(registry_path)
    counts: Counter[str] = Counter()
    display: Dict[str, str] = {}
    sources: Dict[str, set[str]] = {}

    for source_file, raw_name in iter_dishes(menu_paths):
        key = LABELER.norm(raw_name)
        counts[key] += 1
        display.setdefault(key, raw_name)
        sources.setdefault(key, set()).add(source_file)

    output = []
    for key, frequency in counts.most_common():
        raw_name = display[key]
        labeled = LABELER.label_dish(raw_name, registry)
        is_official = key in registry
        needs_review = (
            not is_official
            or labeled["dish_role"] == "UNKNOWN"
            or labeled["protein_class"] == "UNKNOWN"
            or labeled["diet_class"] == "UNKNOWN"
        )
        if not needs_review:
            continue

        reasons = []
        if not is_official:
            reasons.append("NO_OFFICIAL_REGISTRY_MATCH")
        if labeled["dish_role"] == "UNKNOWN":
            reasons.append("UNKNOWN_ROLE")
        if labeled["protein_class"] == "UNKNOWN":
            reasons.append("UNKNOWN_PROTEIN")
        if labeled["diet_class"] == "UNKNOWN":
            reasons.append("UNKNOWN_DIET")

        output.append({
            "raw_name": raw_name,
            "frequency": str(frequency),
            "suggested_role": labeled["dish_role"],
            "suggested_protein": labeled["protein_class"],
            "suggested_diet": labeled["diet_class"],
            "current_provenance": labeled["label_provenance"],
            "review_reasons": "|".join(reasons),
            "source_files": "|".join(sorted(sources[key])),
            "review_status": "OPEN",
            "review_note": "",
            "verified_source_url": "",
        })
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("menu_csv", nargs="+", type=Path)
    parser.add_argument("--registry", type=Path, default=ROOT / "research/cafeteria/official_dish_registry_seed.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "research/cafeteria/manual_label_queue.csv")
    args = parser.parse_args()

    rows = build_queue(args.menu_csv, args.registry)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "raw_name", "frequency", "suggested_role", "suggested_protein", "suggested_diet",
        "current_provenance", "review_reasons", "source_files", "review_status",
        "review_note", "verified_source_url",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"WROTE: {len(rows)} unresolved/heuristic dish labels -> {args.output}")


if __name__ == "__main__":
    main()
