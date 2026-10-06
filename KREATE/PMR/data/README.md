# PMR Public Data Snapshots

This folder stores small, auditable public-data extracts used for PMR/source-quality reasoning. They are secondary/public context, not customer validation or service-level measured truth.

## `bogazici_food_waste_public_snapshot.csv`

### Sources

- 2024: `S-BU-007` — Boğaziçi Impact historical campus food-waste tracking.
- 2025: `S-BU-002` — current Boğaziçi corporate-data food-waste tracking page and linked official workbook.

### Semantics

Each row is one **published month**. Values are transcribed from university public reporting, not inferred from service-level operations.

Columns:
- `source_id`
- `year`
- `month`
- `total_food_waste_kg`
- `delivered_to_istac_kg`
- `source_url`
- `retrieved_at`
- `quality_flag`

### Non-negotiable limitations

This dataset is **not** campus × meal-period truth, produced portions, served portions, edible surplus, plate waste, forecast error, pilot outcome, or model-training truth.

### 2025 source-quality warning

The published 2025 table contains months where `delivered_to_istac_kg > total_food_waste_kg`, while the source page describes delivered waste as included in total waste. August and October are therefore marked `SEMANTIC_RECONCILIATION_REQUIRED`.

Preserve the published values. Do not clamp, recompute a “corrected” total, infer a recycling percentage, or treat the fields as an accounting identity until the source owner clarifies their semantics.

### Why preserve this snapshot

It supports provenance checks, cross-year context, interview questions about the reporting workflow, and a concrete demonstration that aggregate sustainability reporting is not the same artifact as `SERVICE_TRUTH_V1`.

It is not evidence that BOUNCAMPUS reduces food waste.
