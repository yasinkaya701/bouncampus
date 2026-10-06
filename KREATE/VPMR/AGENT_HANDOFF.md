# VPMR Agent Handoff & Collaboration Contract

**Owner lane:** IE / Customer Discovery & Market, with shared consumption by EE/EHB, CS1 and CS2.

## Current branch policy

The durable IE branch was fast-forwarded to current master before this VPMR work. New research is being built from a current base rather than reviving the old IE history.

Do not wholesale-merge stale research branches into current master. They contain valuable evidence, but also old shared-file states and superseded product assumptions.

## Existing agent research to reuse

### Deep PMR / market archive

Branch: `research/kreate-deep-pmr-market-20261004`

High-value artifacts:

- `KREATE/RESEARCH/DEEP_PMR_MARKET_SYNTHESIS_2026-10-04.md`
- `KREATE/RESEARCH/ACADEMIC_DEMAND_MODELING_EVIDENCE_2026-10-04.md`
- `KREATE/RESEARCH/BOGAZICI_*_2026-10-04.md`
- `KREATE/RESEARCH/COMPETITOR_CAPABILITY_MATRIX_2026-10-04.md`
- `KREATE/RESEARCH/PILOT_MEASUREMENT_AND_EVIDENCE_STANDARD_2026-10-04.md`
- `KREATE/PMR/HYPOTHESIS_FALSIFICATION_MATRIX.md`
- `KREATE/PMR/TARGET_ROLE_MAP_2026-10-04.md`

Action: recut only still-valid source-backed findings into VPMR; do not import old shared files wholesale.

### Evidence/method archive

Branch: `research/kreate-evidence-20261005`

High-value artifacts:

- `KREATE/RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md`
- `KREATE/RESEARCH/HIGHEST_INFORMATION_VALUE_QUEUE_2026-10-05.md`
- `KREATE/PMR/HYPOTHESIS_FALSIFICATION_MATRIX.md`

### Contractor/GTM archive

Branch: `research/kreate-contractor-gtm-clean-20261005`

High-value artifacts:

- `KREATE/RESEARCH/CONTRACTOR_LED_GTM_EVIDENCE_2026-10-05.md`
- `KREATE/RESEARCH/TEMAS_PUBLIC_PAIN_AND_PMR_ROLE_MAP_2026-10-05.md`

Boundary: public company information prioritizes interview targets; it is not an interview, endorsement or buying signal.

### Boğaziçi operations / PMR map archive

Branch: `agent/campus-data-geo/bogazici-pmr-target-map`

High-value artifacts:

- `KREATE/RESEARCH/BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md`
- `KREATE/RESEARCH/BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`
- `KREATE/RESEARCH/BOGAZICI_PMR_TARGET_MAP.md`
- `KREATE/RESEARCH/TURKIYE_UNIVERSITY_DINING_PROCUREMENT_BENCHMARK.md`
- related JSON source artifacts.

### CS1 cafeteria data archive

Branch: `agent/decision-intelligence/cafeteria-data-research`

High-value artifacts:

- `docs/research/cs1-cafeteria-recommendation-data.md`
- `research/cafeteria/source_manifest.csv`
- `research/cafeteria/model_feature_contract.csv`
- `research/cafeteria/private_export_request_schema.csv`

Boundary: historical generated/seed data remain sandbox-only unless current source-admission rules prove otherwise.

### Current CS2 truth boundary

Current master artifact:

- `KREATE/RESEARCH/CS2_CURRENT_MASTER_RECUT_2026-10-06.md`

Treat this as the current product/evidence integration boundary: semantic reconciliation, reachable pre-freeze decision, transparent baseline first, residual modeling only if earned, human approval, prospective measurement, evidence promotion.

## Division of work

| Role | VPMR contribution | Must not do |
| --- | --- | --- |
| IE | PMR targets, workflow/persona/buyer questions, source registry, market repeatability | turn public research into fake PMR |
| EE/EHB | measurement methods, calibration, sensor/physical feasibility, field protocol | upgrade datasheet/simulation to bench evidence |
| CS1 | data contracts, source admission, leakage-safe features, baselines, evaluation semantics | train on aggregate/synthetic rows as measured truth |
| CS2 | evidence synthesis, claim traceability, application wording, kill/modify gates | weaken current truth boundary for narrative convenience |

## Stable source-ID protocol

New sources use `VPMR-SRC-NNN`. Do not reuse an ID for a different source. Source updates should either:

- add an `updated_at`/snapshot field if semantics are unchanged; or
- create a successor ID when content/meaning materially changes.

Machine-readable registry and Markdown registry must stay semantically aligned.

## Dedupe rule

Before adding a source:

1. search `KREATE/VPMR/source_registry.json` by canonical URL;
2. check existing archive artifacts listed above;
3. prefer publisher/official source over a mirror;
4. if a mirror contains unique contract text, label it as a mirror and seek an official primary source;
5. add only the delta that changes a decision, interview question, measurement plan or evidence boundary.

## Handoff note format

Every agent adding research should leave a compact note:

- source IDs added/updated;
- hypothesis/decision affected;
- new PMR question or technical gate;
- contradictions found;
- verification status;
- whether an application claim should remain `UNKNOWN`, `HYPOTHESIS`, or can be supported by a public-source evidence row after human review.

## Merge safety

Prefer additive files inside `KREATE/VPMR/` to reduce collisions. Shared files such as `KREATE/EVIDENCE.md`, `KREATE/APPLICATION_RUBRIC.md`, `.agents/**` or root policy files require the broader repository coordination/validation rules in `AGENTS.md`.

## Immediate next agent tasks

1. IE: conduct/record decision-owner + freeze-time PMR using `PMR_GUIDE.md`.
2. IE/CS2: re-verify any public source that will enter final application copy and promote only the narrow claim needed.
3. CS1: bind any acquired service export to the current service-truth admission contract; do not infer semantics from field names.
4. EE/EHB: turn the measurement standards into the lowest-burden prospective field protocol for the chosen waste stage.
5. IE/CS2: test one second institutional site/contractor project before claiming cross-site repeatability.
