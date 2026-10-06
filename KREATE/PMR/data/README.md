# Public PMR data snapshots

This folder preserves small public extracts for provenance and source-quality work. These files are **not** service-level operational truth and must not be used as pilot/model labels.

## `bogazici_food_waste_public_snapshot.csv`

Sources:
- `S-BU-009` — 2024 Boğaziçi Impact campus food-waste page + official PDF.
- `S-BU-002` — 2025 Boğaziçi corporate-data campus food-waste page + linked official XLSX.

Each row is one published month. Values are transcribed without repair, interpolation or semantic normalization.

### 2024 published-total mismatch

The 12 published 2024 monthly `Total Food Waste` rows sum to **50,994 kg**, while the same official page/PDF prints an annual total of **50,993 kg**. Preserve both as published; do not alter a month to force the printed annual total.

### 2025 semantic mismatch

The official page states delivered-to-İSTAÇ quantities are included in total food-waste values, but:
- August: total = **1,502 kg**; delivered = **3,550 kg**.
- October: total = **1,334 kg**; delivered = **4,850 kg**.

Those rows are marked `SEMANTIC_RECONCILIATION_REQUIRED`.

Do not clamp, “correct”, recompute recycling shares, or promote the fields to operational truth until the source owner clarifies their scope/period semantics.

### Forbidden inference

This snapshot does **not** provide:
- campus × meal-period `actual_served`;
- produced portions;
- edible production surplus;
- plate-waste causality;
- shortage / early sellout;
- forecast error;
- model labels;
- pilot impact.

Its purpose is public context, reproducible provenance and concrete data-owner reconciliation questions.
