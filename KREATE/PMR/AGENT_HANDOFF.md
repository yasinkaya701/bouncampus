# PMR Cross-Agent Handoff

**Updated:** 2026-10-06  
**Canonical coordination surface:** this PMR directory.

## What was consolidated

This knowledge base intentionally combines:
- current master research;
- source-level re-verification from public/academic materials;
- useful additive discoveries from older agent branches;
- explicit claim/PMR boundaries.

Two older branches were found with substantial PMR material:
- `agent/campus-data-geo/bogazici-pmr-target-map`
- `research/kreate-deep-pmr-market-20261004`

Both are materially stale relative to current master. Their useful additive ideas are being **selectively salvaged**, not wholesale merged. Shared KREATE policy/evidence files from stale branches must never overwrite newer master state.

## Single append point

Agents should treat:
- [source_catalog.json](source_catalog.json) as the machine-readable registry;
- [SOURCE_LIBRARY.md](SOURCE_LIBRARY.md) as the human index;
- [CLAIM_SOURCE_MATRIX.md](CLAIM_SOURCE_MATRIX.md) as the reasoning firewall;
- [ASSET_MANIFEST.md](ASSET_MANIFEST.md) as the PDF/image/data provenance layer.

Do not create another standalone source dump if the material fits this schema.

## Role handoffs

### IE — Customer Discovery & Market

P0:
1. identify the real Boğaziçi/TEMAŞ quantity owner;
2. establish exact decision/freeze time;
3. obtain recent surplus and shortage incidents;
4. establish current planning heuristic/system;
5. map contract/economic beneficiary;
6. get referral to the real source owner for service-level truth.

Create real interview records from [INTERVIEW_TEMPLATE.md](INTERVIEW_TEMPLATE.md). A scheduled contact is not evidence.

### EE — Physical Systems & Measurement

Consume:
- S-MEAS-001/002/003;
- H2/H4 rows in the claim matrix.

Deliver:
- stage-separated measurement boundary;
- direct-weighing minimum protocol where feasible;
- calibration/quality metadata;
- only propose TrayGate/sensors for a proven missing decision-critical field.

Do not convert camera pixels/volume to mass without measured calibration.

### CS1 — Decision Intelligence

Consume:
- S-BU-004/005/006;
- S-TR-001/002/003;
- S-ACAD-001…006;
- service-level data contract from issue #82.

Sequence:
```text
operator/current heuristic
→ reproducible naive baseline
→ leakage-safe calendar/menu/context ablations
→ richer model only if it clears decision-loss gate
```

Every historical feature must prove it existed before the service decision cutoff. Optimize decision utility with shortage/surplus asymmetry, not only RMSE.

### CS2 — Product Strategy / Application

Consume:
- competitor sources S-COMP-001…004;
- the full claim-source matrix.

Do not claim:
- first AI food-waste platform;
- nobody forecasts kitchen demand;
- competitors only measure waste;
- first Türkiye campus sustainability/evidence platform;
- public Boğaziçi waste totals prove overproduction;
- literature effect sizes are expected project results.

Safe narrative is a **specific unresolved operational control-point hypothesis** pending PMR.

### EHB / hardware

Do not let hardware outrank PMR. Hardware work is justified only by a demonstrated measurement/control gap that existing operational data cannot satisfy.

## Highest-information shared queue

| Priority | Unknown | Changes which workstreams? |
| ---: | --- | --- |
| P0 | quantity owner + freeze point | IE, CS1, CS2, EE |
| P1 | waste-stage causality | IE, EE, CS1, CS2 |
| P2 | shortage asymmetry / safety buffer | IE, CS1, CS2 |
| P3 | contract economics / beneficiary | IE, CS2 |
| P4 | current planning stack | IE, CS1, CS2 |
| P5 | service-level data availability | IE, CS1, EE |
| P6 | persona purchasing criteria | IE, CS2 |
| P7 | second-site same-product test | IE, CS2 |
| P8 | technical model lift | CS1, only after P0–P5 |
| P9 | automated sensing lift | EE/EHB, only after measurement gap is proven |

## Collaboration rule

When another agent finds a source:
1. check for an existing stable source ID;
2. append/update source metadata without deleting contrary evidence;
3. state exactly which hypothesis/decision it changes;
4. add asset provenance if there is a PDF/image/data file;
5. hand off only the actionable delta to another role.

When another agent performs an interview or obtains operational data:
- do **not** merely add it to this secondary-source catalog;
- create the primary record, preserve provenance, and promote only supported/contradicted claims through the evidence system.

## Current decision consequence

The research base is now strong enough that more generic browsing has low information value. New secondary research should be prioritized only if it:
- identifies a new high-value interview target;
- reveals authoritative contract mechanics;
- kills or materially narrows a novelty claim;
- resolves measurement/privacy/legal constraints;
- identifies a directly relevant current incumbent.

Otherwise, effort should move to real PMR.


## Parallel PMR hub convergence — 2026-10-06

Multiple agents created PMR registries in the same execution window. Convergence rule:
- `source_catalog.json` + `SOURCE_LIBRARY.md` are the canonical append targets.
- Dated master registries remain immutable provenance snapshots.
- Unique source/data/assets from PR #315 and PR #320 are salvaged under canonical `S-*` IDs.
- Do not merge a duplicate registry wholesale after its unique sources have been migrated.
- Preserve source anomalies and contradictions; do not normalize them into fake operational truth.
