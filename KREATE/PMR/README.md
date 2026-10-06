# PMR Research Hub

**Owner:** IE — Customer Discovery & Market  
**Updated:** 2026-10-06  
**Scope:** cumulative source, data, methodology, and falsification context for BOUNCAMPUS Primary Market Research.

This directory is the shared PMR research source-of-truth for the current institutional-dining wedge.

> **Evidence boundary:** public sources, academic literature, standards, vendor materials, and public datasets are **secondary research**. They can establish context, mechanism plausibility, measurement practice, alternatives, and falsification pressure. They do **not** become `INTERVIEW EVIDENCE`, pilot evidence, measured Boğaziçi service truth, willingness-to-pay evidence, or proof of live data access.

## Start here

- [SOURCE_CATALOG.md](./SOURCE_CATALOG.md) — curated human-readable source register.
- [source_catalog.json](./source_catalog.json) — machine-readable source register for agents/scripts.
- [PMR_RESEARCH_SYNTHESIS_2026-10-06.md](./PMR_RESEARCH_SYNTHESIS_2026-10-06.md) — current implications for H1–H6.
- [PDF_VISUAL_INDEX.md](./PDF_VISUAL_INDEX.md) — canonical PDF/spreadsheet/visual links.
- [data/README.md](./data/README.md) — dataset semantics and quality warnings.
- [data/bogazici_food_waste_public_snapshot.csv](./data/bogazici_food_waste_public_snapshot.csv) — verbatim public monthly snapshot.
- [HYPOTHESIS_FALSIFICATION_MATRIX.md](./HYPOTHESIS_FALSIFICATION_MATRIX.md) — interview hypotheses.
- [INTERVIEW_TEMPLATE.md](./INTERVIEW_TEMPLATE.md) — real-interview record template.
- [INTERVIEW_TRACKER.md](./INTERVIEW_TRACKER.md) — distributed PMR tracker.

## Stable source-ID contract

Use `PMR-SRC-###`. IDs are immutable. Never reuse an ID for a different source.

For every source record preserve:

```text
id
title
source_kind
publisher
publication_or_update_date
canonical_url
direct_assets
doi_or_identifier
geographic_scope
pmr_hypotheses
role_consumers
decision_use
limitations
last_checked
verification_status
```

### Deduplication

1. Deduplicate academic papers by DOI before title.
2. Prefer the primary publisher / institution URL over mirrors.
3. Keep a landing page and a direct PDF/download URL as assets of the **same** source ID.
4. Vendor case studies remain `VENDOR_CLAIM`; do not duplicate their outcome number into a separate “evidence” source.
5. If a source changes materially, preserve the old source ID and add a new version/source ID rather than silently changing semantics.

## Role collaboration

| Role | What to consume from this hub | What it must return |
| --- | --- | --- |
| IE | interview targets, hypotheses, contrary evidence, buyer/workflow questions | real PMR records + narrow `E-INT-*` evidence only after interviews |
| CS1 | data-source inventory, semantics, decision-time availability, quality warnings | admitted source contract, benchmark-safe dataset artifacts, fail-closed semantics |
| CS2 | competitor reality, claim boundaries, beachhead repeatability, evidence strength | application/product claims that retain source class and limitation |
| EE | measurement standards, waste-stage definitions, physical ground-truth options | measurement boundary, calibration/uncertainty plan, field evidence when real |
| EHB | only measurement requirements that survive EE/PMR gates | device implementation evidence; no promotion of public sources to bench/field evidence |

### Active coordination

- PMR hub work: GitHub issue **#309**.
- CS1 service-level dining truth acquisition: GitHub issue **#82**.
- CS2 current-master evidence/acquisition recut: `KREATE/RESEARCH/CS2_CURRENT_MASTER_RECUT_2026-10-06.md`.

## Research stop rule

Secondary research is useful only when it does at least one of these:

- identifies a higher-value interview target;
- resolves or sharpens a hypothesis;
- exposes a contradictory mechanism;
- establishes an authoritative measurement/data rule;
- clarifies procurement/incentives;
- identifies a current incumbent/alternative;
- provides a source artifact needed for source admission or pilot design.

Otherwise, spend the next unit of effort on real PMR.
