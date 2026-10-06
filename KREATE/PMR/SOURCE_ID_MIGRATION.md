# PMR Source-ID Reconciliation

**Updated:** 2026-10-06

Parallel PMR agents created useful registries with different source-ID schemes. Their snapshots remain provenance, but **all new work appends to `source_catalog.json` using canonical `S-*` IDs**.

## Registry status

| Registry | Status |
| --- | --- |
| `source_catalog.json` | **CANONICAL / APPEND HERE** |
| `SOURCE_REGISTRY_2026-10-06.json` | immutable master snapshot |
| PR #315 `source_catalog.json` | unique sources/data salvaged |
| PR #320 `source_registry.json` | unique sources salvaged |

## Common aliases

| Legacy | Canonical |
| --- | --- |
| SRC-METHOD-DE-PMR-2019 / PMR-SRC-007 | S-PMR-001 |
| SRC-BOUN-FOODWASTE-2025 / PMR-SRC-001 | S-BU-002 |
| SRC-BOUN-FOODWASTE-2025-XLSX | S-BU-007 |
| SRC-BOUN-FOODWASTE-2024 / PMR-SRC-002 | S-BU-008 |
| PMR-SRC-003 | S-BU-001 |
| PMR-SRC-004 | S-BU-004 |
| PMR-SRC-005 | S-BU-006 |
| PMR-SRC-006 | S-BU-005 |
| SRC-BOUN-SUSTAINABLE-FOOD | S-BU-009 |
| SRC-BOUN-MENU-SURVEY | S-BU-010 |
| SRC-BOUN-DINING-CONTROL | S-BU-011 |
| SRC-BOUN-SDG2-2024-PDF | S-BU-012 |
| SRC-UNEP-FWI-2024 / PMR-SRC-008 | S-MEAS-001 |
| SRC-FLW-STANDARD / PMR-SRC-009 | S-MEAS-002 |
| SRC-FLW-OVERVIEW-PDF | S-MEAS-004 |
| PMR-SRC-011 | S-MEAS-005 |
| PMR-SRC-013 | S-ACAD-002 |
| PMR-SRC-014 / SRC-ACADEMIC-TURKER-2025 | S-ACAD-005 |
| PMR-SRC-015 | S-ACAD-004 |
| PMR-SRC-016 | S-ACAD-007 |
| PMR-SRC-017 | S-ACAD-008 |
| PMR-SRC-018 | S-ACAD-009 |
| PMR-SRC-019 | S-ACAD-010 |
| PMR-SRC-020 | S-TR-001 |
| PMR-SRC-021 | S-TR-002 |
| PMR-SRC-022 | S-TR-005 |
| PMR-SRC-023 | S-COMP-005 |
| PMR-SRC-024 | S-COMP-002 |
| PMR-SRC-025 | S-COMP-006 |
| PMR-SRC-026 | S-COMP-004 |
| SRC-BU-003 | S-BU-013 |
| SRC-BU-004 | S-BU-014 |
| SRC-MEAS-004 | S-MEAS-008 |
| SRC-MEAS-005 | S-MEAS-009 |
| SRC-ACAD-006 | S-ACAD-011 |
| SRC-ACAD-007 | S-ACAD-012 |
| SRC-ACAD-008 | S-ACAD-013 |
| SRC-ACAD-009 | S-ACAD-014 |
| SRC-ACAD-010 | S-ACAD-015 |
| SRC-TGT-002…007 | S-TR-006…011 |
| SRC-PRIV-001…004 | S-PRIV-001…004 |

Deduplicate by DOI/canonical URL/title, not by a legacy ID. If a legacy record is richer, enrich the canonical record instead of reviving the old identifier.
