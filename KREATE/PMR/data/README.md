# Public PMR data snapshots

These files preserve small public extracts for provenance and source-quality work. They are **not** service-level operational truth and must not be used as pilot/model labels.

## bogazici_food_waste_public_snapshot.csv

Sources:
- `S-BU-011` — 2024 Boğaziçi Impact campus food-waste page + official PDF.
- `S-BU-002` — 2025 Boğaziçi corporate-data campus food-waste page + linked workbook.

Each row is one published month. Values are preserved without repair or interpolation.

### 2024 published-total warning

The 12 published 2024 monthly `Total Food Waste` rows sum to **50,994 kg**, while the same official page/PDF prints **50,993 kg** for the year. Preserve both facts; do not alter a month to force the printed total.

### 2025 semantic warning

The official page states delivered-to-İSTAÇ amounts are included in total food-waste amounts, but:
- August: total 1,502 kg vs delivered 3,550 kg.
- October: total 1,334 kg vs delivered 4,850 kg.

Those rows are marked `SEMANTIC_RECONCILIATION_REQUIRED`. Do not clamp, normalize or calculate recycling shares until the source owner clarifies scope/period semantics.

### Forbidden inference

The snapshot does not provide campus × meal-period served truth, produced portions, edible surplus, plate-waste causality, shortage, forecast error or pilot impact. It is public context + a concrete source-quality/reconciliation artifact.
