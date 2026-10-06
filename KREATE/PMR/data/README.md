# PMR Public Data Snapshots

This folder stores small, auditable public-data extracts that are useful for PMR/data-source reasoning.

## `bogazici_food_waste_public_snapshot.csv`

### Sources

- 2024: `PMR-SRC-002` — Boğaziçi Impact campus food-waste tracking page.
- 2025: `PMR-SRC-001` — current Boğaziçi corporate-data campus food-waste tracking page / linked workbook.

### Semantics

Each row is one published month. Values are transcribed from the university's public reporting, not inferred from service-level activity.

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

This dataset is **not**:
- campus × meal-period service truth;
- produced portions;
- served portions;
- edible surplus;
- plate waste;
- forecast error;
- pilot outcome;
- training labels for the current decision model.

### 2025 source-quality warning

The public 2025 table contains multiple months where `delivered_to_istac_kg > total_food_waste_kg`, while the source text indicates delivered waste is included in total food waste.

The snapshot deliberately preserves the published values and marks those rows `SEMANTIC_RECONCILIATION_REQUIRED`.

Do not:
- clamp values;
- recompute a “corrected” total;
- infer a recycling percentage;
- treat this as an accounting identity;

until the source owner clarifies the field semantics.

### Why keep this snapshot

It is useful for:
- source-provenance tests;
- PMR questions about reporting workflow;
- cross-year context;
- demonstrating why aggregate sustainability reporting and service-level operational truth are different artifacts.

It is not evidence that BOUNCAMPUS reduces food waste.
