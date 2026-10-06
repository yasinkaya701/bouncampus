# PMR Public Data Snapshots

## `bogazici_food_waste_public_snapshot.csv`

This is a small, auditable transcription of public monthly aggregate reporting discovered by the parallel IE PMR agent and reconciled into the canonical source IDs.

Sources:
- `S-BU-008` — 2024 Boğaziçi Impact food-waste page.
- `S-BU-002` / `S-BU-007` — 2025 current corporate-data page / linked raw workbook.

The CSV preserves the parallel agent's legacy source ID in a separate column for provenance.

### Non-negotiable limitations

This is **not**:
- campus × meal-period service truth;
- produced or served portions;
- edible surplus;
- plate waste;
- forecast error;
- pilot outcome;
- training truth for the decision model.

### Source-quality flags

The 2025 public rows for August and October have `delivered_to_istac_kg > total_food_waste_kg` in the transcribed source values and are marked `SEMANTIC_RECONCILIATION_REQUIRED`.

The 12 transcribed 2024 monthly total-food-waste rows sum to **50,994 kg**, while the inherited current-master registry records a published annual total of **50,993 kg**. Preserve both facts as a reconciliation question; do not silently alter one kilogram to force agreement.

Use this snapshot for provenance/data-quality tests and PMR questions about reporting semantics, not as operational labels.
