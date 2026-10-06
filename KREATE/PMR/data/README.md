# PMR Public Data Snapshots

## `bogazici_food_waste_public_snapshot.csv`

A small auditable transcription of public aggregate reporting discovered by a parallel IE PMR agent and reconciled to canonical IDs.

Sources:
- `S-BU-008` — 2024 Boğaziçi Impact food-waste page.
- `S-BU-002` / `S-BU-007` — 2025 corporate-data page / linked raw workbook.

This is **not** campus × meal-period truth, produced/served portions, edible surplus, plate waste, forecast error, pilot outcome, or model-training truth.

### Source-quality warnings

- 2025 August and October retain published rows where `delivered_to_istac_kg > total_food_waste_kg`; they are flagged `SEMANTIC_RECONCILIATION_REQUIRED`.
- The 12 transcribed 2024 monthly totals sum to **50,994 kg** while the inherited master snapshot records a published annual total of **50,993 kg**. Preserve the mismatch as a source-owner question; do not silently force agreement.

Use this snapshot for provenance/data-quality tests and PMR questions about reporting semantics only.
