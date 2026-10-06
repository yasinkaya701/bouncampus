# Secondary Research Index for PMR

**Updated:** 2026-10-06  
**Status:** source-backed PMR preparation; **not** customer validation.

This document compresses the source registry into decision-relevant findings and interview pressure. Every external statement should trace to a stable \`SRC-*\` ID in [SOURCE_REGISTRY.json](./SOURCE_REGISTRY.json).

## Executive synthesis

The current evidence justifies continuing to test institutional dining as a beachhead, but it does **not** validate the product-market thesis.

What public/academic evidence establishes:

- Boğaziçi has a real, officially reported food-waste baseline and multi-campus dining operation (\`SRC-BU-001\`, \`SRC-BU-002\`).
- Some relevant signals/workflows exist publicly, including advance menus, an academic calendar, and at least one bounded reservation workflow (\`SRC-BU-004\`, \`SRC-BU-005\`, \`SRC-BU-006\`).
- Demand forecasting, reservation/no-show uncertainty, batch sizing and food-waste measurement are real institutional-foodservice problem classes in external literature (\`SRC-ACA-001\`–\`SRC-ACA-004\`).
- Policy/ranking context rewards documented sustainability governance, waste action and digitalization (\`SRC-POL-001\`, \`SRC-STD-001\`).

What remains unknown and must be closed by real PMR/artifacts:

- the actual quantity/production decision owner;
- exact freeze point and batch flexibility;
- the last real over/under-production incident and its cause;
- whether the published waste is materially reachable by a quantity decision;
- shortage consequences and safety-buffer behavior;
- settlement/hakediş basis and who captures savings;
- service-level data ownership, semantics, retention and exportability;
- operator trust/adoption conditions;
- economic buyer, veto path and purchasing criteria;
- repeatability at a second institution.

## Boğaziçi public fact boundary

### Official food-waste baseline

\`SRC-BU-002\` reports **48,251 kg** total food waste for 2025 and provides monthly aggregate values. It also reports public dining-hall capacity/service context.

Use it for:

- problem existence and scale context;
- sanity checks;
- selecting periods for follow-up questions;
- deciding what additional granularity is needed.

Do **not** use it for:

- service-level labels;
- campus×meal causal attribution;
- a forecast-training target;
- proof that overproduction is the root cause;
- a claimed intervention effect.

The derived snapshot is stored at [data/bogazici_food_waste_2025_official.csv](./data/bogazici_food_waste_2025_official.csv). It is explicitly aggregate public context, not \`SERVICE_TRUTH_V1\`.

### Public dining scale

\`SRC-BU-001\` reports six dining halls and approximately 6,000 daily meals, plus package-meal and feedback-program context.

This helps size the operating surface but cannot be expanded into fabricated service rows or demand distributions.

### Candidate pre-service signals

- menus: \`SRC-BU-004\`;
- academic calendar: \`SRC-BU-006\`;
- bounded Kilyos reservation example: \`SRC-BU-005\`.

These are candidate **inputs** only. A historical feature is admissible for backtesting only if the exact snapshot can be shown to have existed by the decision cutoff. Reservation is intent, not served demand.

## H1–H6 evidence pressure

| PMR hypothesis | Secondary evidence that informs it | What would support it in PMR | What would reject/modify it |
| --- | --- | --- | --- |
| **H1 — reachable production control point** | Centralized preparation context (\`SRC-BU-003\`); one bounded reservation workflow (\`SRC-BU-005\`) | Last-service account naming quantity owner, timing, revision rights and freeze point | Quantity is fixed outside a reachable workflow, or the real decision is batch/allocation/portioning instead |
| **H2 — material actionable mismatch** | Official waste exists (\`SRC-BU-002\`); forecasting is plausible externally (\`SRC-ACA-001\`, \`SRC-ACA-003\`) | Repeated concrete incidents linking forecast/quantity choice to avoidable unserved surplus or shortage | Waste is dominated by prep loss, plate waste, menu/quality, safety discard or another cause |
| **H3 — asymmetric shortage risk** | Reservation/show-no-show and waste-vs-shortage modeling exists externally (\`SRC-ACA-002\`) | Concrete shortage and surplus incidents plus deliberate buffer behavior | No meaningful shortage penalty/buffer, or rapid replenishment makes it irrelevant |
| **H4 — data/measurement feasibility** | Candidate public inputs + measurement standards (\`SRC-BU-004\`–\`006\`, \`SRC-MEAS-001\`) | Real owner/export semantics for planned, produced, served, surplus/waste and timing | Export unavailable, semantics unreconcilable, privacy burden excessive, or outcome cannot be measured |
| **H5 — persona/authority** | Public org structure helps identify interview routes but not authority | Independent accounts converge on a role/person with action/approval rights | Authority is fragmented across parties with no usable service-time actor |
| **H6 — workflow adoption** | External practice shows forecasting/batching can be operational tools (\`SRC-ACA-003\`) | Operators describe existing revision behavior, trust criteria, acceptable workload and approval gates | Recommendation arrives too late, adds unacceptable burden/risk, or current workflow is already sufficient |

The detailed neutral prompts and support/reject criteria live in [HYPOTHESIS_FALSIFICATION_MATRIX.md](./HYPOTHESIS_FALSIFICATION_MATRIX.md).

## The most valuable next interview sequence

1. **Food Services / SKS operations owner**  
   Resolve who owns quantity, last concrete mismatch, freeze time, revision rights, shortage/surplus consequences and who owns the records.

2. **Contractor / central-kitchen local operations**  
   Resolve the actual production heuristic, batch process, ingredient/cooking commitment, campus allocation, over/under-production response and operational economics.

3. **BUCard / BİD aggregate-data owner + SKS semantic owner**  
   Resolve #292: whether privacy-preserving campus×meal-period×service-date reports exist, how retries/refunds/categories are reconciled, when a report becomes final, and whether stable report IDs/timestamps can be preserved.

4. **Waste/sustainability measurement owner**  
   Resolve the published waste boundary, generation-vs-collection timing, stage split, authoritative internal record and acceptable pilot outcome metric.

5. **Procurement/contract/hakediş owner**  
   Resolve settlement quantity, incentive ownership, economic buyer and veto path.

6. **Second institution with comparable workflow**  
   Test whether the same problem, language, user and deployment motion repeat. Include at least one contrasting governance/procurement archetype to avoid Boğaziçi-only overfitting.

## Data contract pressure

Issue **#292** owns institutional acquisition. Issue **#82** owns CS1 admission.

The minimum useful grain is one real row per:

\`campus_id × meal_period × service_date\`

Candidate outcome/reconciliation fields:

- reported served/passage count with original semantics;
- \`produced_portions\`;
- accepted \`actual_surplus_portions\` and/or \`waste_kg\`;
- \`shortage_or_early_sellout\`;
- stable source record ID;
- report/finalization timestamp.

Candidate decision-time fields:

- decision cutoff;
- operator/status-quo quantity estimate + timestamp/version;
- reservation count only where that workflow is proven;
- menu snapshot;
- academic-calendar snapshot;
- archived forecast snapshot if weather was actually used;
- known special events.

Never rename a passage/transaction count to \`actual_served\` before source-owner reconciliation. Never train on unreconciled outcomes.

## Measurement implication

Current master already contains [FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md](../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md).

The PMR implication is simple:

\`\`\`text
existing trustworthy operational record
→ direct weighing/manual record where simplest
→ automated sensing only for a decision-critical missing field
→ validate any sensor against physical ground truth
→ preserve method, stage, units, timing and provenance
\`\`\`

A sophisticated sensor with unclear semantics is weaker evidence than a disciplined low-burden manual protocol.

## Market / buyer pressure

National and international sustainability context (\`SRC-POL-001\`, \`SRC-STD-001\`) can support a **why-now** story. It cannot establish purchasing intent.

The buying question remains empirical:

> If unnecessary production falls without increasing shortages, whose operational or financial outcome improves, who can authorize change, and who can pay or mandate the tool?

Do not collapse end user, beneficiary, data owner, approver and economic buyer into one persona without PMR.

## Academic evidence — correct use

### \`SRC-ACA-001\` — catering demand forecasting

Use: benchmark architecture and proof that the problem class can be modeled with real catering data.

Do not transfer its reported performance/waste-reduction results to Boğaziçi.

### \`SRC-ACA-002\` — university subsidy/reservation uncertainty

Use: prompts about reservation intent, no-shows, shortage penalty and decision under uncertainty.

Do not assume Boğaziçi has the same reservation coverage or economics.

### \`SRC-ACA-003\` — university foodservice practices

Use: external support for asking about demand forecasting, smaller batches and measurement barriers.

Do not infer that Boğaziçi follows the same practice distribution.

### \`SRC-ACA-004\` — educational food-waste review

Use: enforce multi-causal diagnosis and waste-stage separation.

Do not let the existence of forecasting literature crowd out menu, portion, preparation, food-safety or plate-waste causes.

## Negative knowledge is part of the database

Record these as first-class constraints:

- public annual/monthly waste ≠ production-caused waste;
- public aggregate dining counts ≠ service truth;
- reservation ≠ served demand;
- source URL existence ≠ team data access;
- vendor capability claim ≠ actual deployed workflow;
- academic result ≠ transferable model impact;
- policy/ranking context ≠ willingness to buy;
- synthetic/demo CSV ≠ measured pilot evidence;
- planned interview ≠ \`REAL_PMR\`.

## Existing branch research — reuse policy

Two historical branches contain substantial work:

- \`research/kreate-deep-pmr-market-20261004\`;
- \`agent/campus-data-geo/bogazici-pmr-target-map\`.

They are intentionally **not** wholesale merged because their ancestry is stale. Useful claims must be reverified against current sources/current master and recut into the canonical PMR hub.

Two current-master draft hub branches were also found on 2026-10-06:

- \`agent/ie/pmr-research-hub-20261006\`;
- \`research/pmr-knowledge-base-20261006\`.

Their strongest evidence-firewall/contribution ideas were consumed into this consolidated current-master implementation rather than duplicated independently.

## Cross-role work queue

**IE**
- execute the interview sequence;
- update tracker only from real outreach/scheduling/completion;
- preserve contradictions and referrals;
- own #292 institutional access.

**CS1**
- consume #292 only after provenance/semantic checks;
- use \`scripts/cs1_service_truth_artifact_intake.py\`;
- compare transparent baseline before richer modeling;
- fail closed on post-cutoff or unverified fields.

**CS2**
- use this hub for source traceability and claim-boundary checks;
- keep public sources distinct from \`INTERVIEW EVIDENCE\`;
- update application only when narrow claims meet the evidence gate.

**EE**
- use measurement standards to define a prospective, stage-specific physical truth boundary.

**EHB**
- build/validate hardware only for a measurement gap that remains after existing records and lower-burden methods are tested.

## Stop rule

Further web research has diminishing value unless it directly closes one of:

- decision owner/freeze;
- waste-stage causality;
- shortage asymmetry;
- contract economics;
- current planning stack;
- service-level data ownership/semantics;
- persona purchasing criteria;
- second-site repeatability;
- current incumbent capability;
- measurement/privacy constraints.

Everything else yields to real PMR.
