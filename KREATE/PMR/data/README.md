# PMR Public Data Snapshots

This folder stores small, auditable public-data extracts for PMR/source-quality reasoning. They are secondary/public context, not customer validation or service-level measured truth.

## `bogazici_food_waste_public_snapshot.csv`

Sources:
- 2024: `S-BU-009` — Boğaziçi Impact historical food-waste tracking.
- 2025: `S-BU-002` — current corporate-data food-waste page and official XLSX.

Each row is one published month. The file is **not** campus × meal-period truth, produced/served portions, edible surplus, plate waste, forecast error, pilot outcome or model-training truth.

The 2025 source displays months where `delivered_to_istac_kg > total_food_waste_kg` while describing delivered waste as included in total. August and October are therefore marked `SEMANTIC_RECONCILIATION_REQUIRED`.

Preserve the published values. Do not clamp/recompute a “corrected” total or infer an accounting identity until the source owner clarifies field semantics through the institutional acquisition/reconciliation path (#292).

Use this snapshot for provenance checks, cross-year context and interview questions about reporting semantics—not for impact claims.
