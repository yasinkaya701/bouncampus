# PMR Knowledge Base

**Owner surface:** IE / Customer Discovery, with CS1/CS2/EE/EHB consumers  
**Updated:** 2026-10-06  
**Status:** canonical cumulative PMR research index. Secondary/public research is **not** Primary Market Research evidence.

This directory now reconciles multiple parallel PMR research agents into one appendable source layer instead of maintaining competing hubs.

## Canonical, appendable layer

Use these files for all new work:
1. [SOURCE_LIBRARY.md](SOURCE_LIBRARY.md) — human-readable cumulative source library.
2. [source_catalog.json](source_catalog.json) — machine-readable canonical registry using stable `S-*` IDs.
3. [CLAIM_SOURCE_MATRIX.md](CLAIM_SOURCE_MATRIX.md) — claim/hypothesis → secondary support → forbidden inference → exact PMR gap.
4. [ASSET_MANIFEST.md](ASSET_MANIFEST.md) — PDFs, XLSX/data, visuals, reuse status and provenance.
5. [AGENT_HANDOFF.md](AGENT_HANDOFF.md) — IE/EE/CS1/CS2/EHB handoff rules.
6. [data/README.md](data/README.md) and [data/bogazici_food_waste_public_snapshot.csv](data/bogazici_food_waste_public_snapshot.csv) — small auditable public-data snapshot with semantic warnings.
7. [SOURCE_ID_MIGRATION.md](SOURCE_ID_MIGRATION.md) — legacy registry reconciliation.

## Primary-research execution

- [HYPOTHESIS_FALSIFICATION_MATRIX.md](HYPOTHESIS_FALSIFICATION_MATRIX.md)
- [INTERVIEW_TEMPLATE.md](INTERVIEW_TEMPLATE.md)
- [INTERVIEW_TRACKER.md](INTERVIEW_TRACKER.md)

A completed interview/observation/operational artifact may become PMR evidence only through the repository evidence process. A source entry alone never does.

## Preserved 2026-10-06 snapshots

These already-merged artifacts are retained for provenance and should not be deleted:
- [PMR_KNOWLEDGE_BASE_2026-10-06.md](PMR_KNOWLEDGE_BASE_2026-10-06.md)
- [SOURCE_REGISTRY_2026-10-06.json](SOURCE_REGISTRY_2026-10-06.json)
- [ASSET_AND_MEDIA_INDEX_2026-10-06.md](ASSET_AND_MEDIA_INDEX_2026-10-06.md)

They are immutable historical snapshots. New sources go to `source_catalog.json`, not to another dated competing registry.

## Evidence firewall

| Class | Meaning | Can close PMR hypothesis? |
| --- | --- | --- |
| REAL_PMR | real interview/observation/operational artifact | Yes, with provenance |
| PUBLIC_OFFICIAL | official public source | No |
| ACADEMIC | external scholarly evidence | No |
| METHOD_REFERENCE | PMR/research methodology | No |
| VENDOR_CLAIM | vendor material/case study | No |
| REPO_SYNTHESIS | internal synthesis | No |

## Highest-value unresolved chain

```text
quantity owner
→ exact freeze point
→ signals actually available before freeze
→ current planning heuristic/system
→ surplus vs shortage consequence
→ settlement/economic beneficiary
→ service-level measurable truth
```

Secondary research is now strong enough to establish problem-mechanism plausibility and to kill weak novelty claims. It is **not** strong enough to identify the Boğaziçi/TEMAŞ decision owner, local waste causality, willingness to pay, or intervention impact.

## Current research consequences

- Generic “AI predicts cafeteria demand” is not a safe novelty claim: the academic literature is established and current vendors now market production forecasting.
- Calendar/weather/menu/history signals are not a moat; current university operations and literature already use these classes.
- Aggregate Boğaziçi waste reports show public problem-scale context but do not provide service-level produced/served/surplus/shortage truth.
- Plate waste, menu quality, taste, portion size and behavior are credible competing causes; H2 must remain falsifiable.
- Hardware/sensing is downstream of a proven missing decision-critical field.

## Contribution rule

Before adding a source:
1. search `source_catalog.json` by URL/DOI/title;
2. reuse the canonical `S-*` ID for the same artifact;
3. append a new ID only for a distinct/materially newer artifact;
4. preserve source class, access date, license/reuse note and limitations;
5. update the claim matrix only if a decision changes;
6. add PDFs/images/XLSX links to the asset manifest;
7. preserve contradictions and semantic anomalies;
8. never create `E-INT-*` from public research.

Relevant current research remains under [../RESEARCH/](../RESEARCH/), especially competitor red-team, cross-university repeatability, measurement standards, economic-buyer analysis and the highest-information-value queue.
