# Public PMR data snapshots

These files preserve small public extracts for provenance/source-quality work. They are **not** service-level operational truth and must not be used as pilot/model labels.

## bogazici_food_waste_public_snapshot.csv

Sources:
- `S-BU-007` — 2024 Boğaziçi Impact campus food-waste page + official PDF.
- `S-BU-002` — 2025 Boğaziçi corporate-data campus food-waste page + linked workbook.

Each row is one published month. The snapshot preserves the university's published values without repair or interpolation.

### Columns

```text
source_id
year
month
total_food_waste_kg
delivered_to_istac_kg
waste_oil_kg
recycled_waste_oil_kg
source_url
retrieved_at
quality_flag
```

### 2025 semantic warning

The official 2025 table states that delivered-to-İSTAÇ amounts are included in total food-waste amounts, but:
- August: total = 1,502 kg; delivered = 3,550 kg.
- October: total = 1,334 kg; delivered = 4,850 kg.

Those rows are marked `SEMANTIC_RECONCILIATION_REQUIRED`.

Do not clamp, “correct”, normalize, or calculate recycling shares from these fields until the source owner clarifies their scope/period semantics.

### Forbidden inference

This snapshot does **not** provide:
- campus × meal-period `actual_served`;
- produced portions;
- edible production surplus;
- plate-waste causality;
- shortage / early-sellout;
- forecast error;
- a baseline/model target;
- pilot impact.

Its value is public context, provenance testing and a concrete source-quality question for PMR/data-owner interviews.
