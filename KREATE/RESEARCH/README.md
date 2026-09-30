# KREATE Research Packs

This directory contains secondary/public-source research prepared for KREATE agents. It is a shared **research layer**, not the evidence registry and not PMR.

## Claim boundary

- Nothing in this directory counts as `INTERVIEW EVIDENCE` or customer validation.
- Official university pages and reports may become `PUBLIC_SOURCE` evidence only after a domain owner narrows the claim and promotes it into `../EVIDENCE.md`.
- Academic papers are benchmarks and design references. A result from another university does **not** prove the same mechanism exists at Boğaziçi.
- Apparent inconsistencies in source data are preserved as caveats; agents must not silently repair them.
- Model or scenario implications derived from these sources remain `HYPOTHESIS`, `POLICY_HEURISTIC`, or `MODEL ESTIMATE` until separately validated.
- Procurement samples in this directory are **not** TAM/SAM/SOM unless a separate systematic market-sizing method explicitly establishes that scope.
- Contract clauses from another university are **sector precedents, not Boğaziçi contract facts**.
- Global climate/food-waste statistics are context, **not local conversion factors or measured Boğaziçi impact**.
- Public professional contact information is for role routing only; it is **not interview evidence, endorsement, availability or permission for repeated outreach**.
- Policy/ranking pressure is market context, **not willingness-to-pay evidence or a guaranteed score/compliance outcome**.
- Vendor claims and case-study percentages are competitive context, **not neutral evidence or expected BOUNCAMPUS impact**.
- National university counts are ecosystem context, **not addressable-customer counts or TAM without segmentation evidence**.
- Reservation practices at other universities are sector precedents, **not evidence that Boğaziçi should use the same mechanism in normal-term service**.

## Available packs

| Pack | Purpose | Machine-readable companion |
| --- | --- | --- |
| [Boğaziçi Sustainability 2025](./BOGAZICI_SUSTAINABILITY_2025.md) | Deep secondary research from Boğaziçi sustainability/SDG sources plus peer-reviewed institutional-dining literature; includes food, water, energy, transport, data-quality caveats, PMR questions and role-specific handoffs. | [`bogazici_sustainability_2025.json`](./bogazici_sustainability_2025.json) |
| [Boğaziçi Food Operations Deep Dive](./BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md) | Decision/governance map for central production, contractor controls, BUCampus menu voting, BUCard/QR candidate signals, service regimes, packaged service, pilot data requests and CS1 model-design rules. | [`bogazici_food_operations_deep_dive.json`](./bogazici_food_operations_deep_dive.json) |
| [Boğaziçi Food Procurement & Contract Research](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md) | Current 2026–2027 unit-price dining procurement, quantities, contractor, capacity requirement, cancelled predecessor, contract-semantics unknowns and PMR/data questions. | [`bogazici_food_procurement_2026_2027.json`](./bogazici_food_procurement_2026_2027.json) |
| [Türkiye Public-University Dining Procurement Benchmark](./TURKIYE_UNIVERSITY_DINING_PROCUREMENT_BENCHMARK.md) | Cross-university 2026 procurement sample testing whether the buyer/quantity/contract workflow repeats beyond Boğaziçi; covers SKS buyer pattern, on-site vs transported service, meal/channel segmentation and candidate beachhead refinement. | [`turkiye_university_dining_procurement_benchmark.json`](./turkiye_university_dining_procurement_benchmark.json) |
| [Türkiye University Dining Contract Decision Precedents](./TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md) | KİK-backed precedents showing historical-demand quantity heuristics, contractor forecast responsibility, smart-card/actual-consumption settlement, excess/shortage risk and historical-preference menu-mix adjustment. | [`turkiye_dining_contract_decision_precedents.json`](./turkiye_dining_contract_decision_precedents.json) |
| [Türkiye Dining Reservation Signals](./TURKIYE_DINING_RESERVATION_SIGNALS.md) | Multi-university examples of reservation/intent systems used to plan meals and reduce waste/shortages; compares passive forecast, reservation and hybrid residual-uncertainty approaches, including Boğaziçi's 2026 special-service reservation precedent. | — |
| [Türkiye Zero-Waste & Campus Food-Waste Measurement Context](./TURKIYE_ZERO_WASTE_CAMPUS_MEASUREMENT_CONTEXT.md) | Official Türkiye Zero Waste and UNEP context translated into pilot KPI hierarchy, measurement boundary and anti-greenwashing rules for food-waste/climate claims. | [`turkiye_zero_waste_campus_measurement_context.json`](./turkiye_zero_waste_campus_measurement_context.json) |
| [Boğaziçi PMR Target Map](./BOGAZICI_PMR_TARGET_MAP.md) | Public role-routing map for Food Services, current contractor, BİD data owner, sustainability/Zero Waste measurement owner, SKS escalation and operational-data support; includes question ownership and recommended interview sequence. | [`bogazici_pmr_target_map.json`](./bogazici_pmr_target_map.json) |
| [Boğaziçi Source Reconciliation Matrix](./BOGAZICI_SOURCE_RECONCILIATION.md) | Cross-source data-quality control: capacity, beneficiary, serving, packaged-meal, food-waste/İSTAÇ and service-regime semantics that agents must reconcile before joining metrics or training models. | See the `source_conflicts` section of [`bogazici_food_operations_deep_dive.json`](./bogazici_food_operations_deep_dive.json). |
| [Türkiye Policy, Ranking & Institutional Pull](./TURKIYE_POLICY_RANKING_PULL.md) | YÖK, public-building energy policy, Climate Law, UI GreenMetric 2026 Governance & Digitalization, Türkiye benchmark campuses and safe why-now language. | — |
| [Metric Provenance & Verification](./METRIC_PROVENANCE_AND_VERIFICATION.md) | Cross-domain event/provenance model, food-pilot data contract, decision records, water/energy governance implications and verification levels. | — |
| [Academic Decision Intelligence](./ACADEMIC_DECISION_INTELLIGENCE.md) | Peer-reviewed synthesis connecting food-waste causality, forecasting, smart-campus decision processes, measurement and model design. | — |
| [Competitor & Substitute Landscape](./COMPETITOR_SUBSTITUTE_LANDSCAPE.md) | Türkiye-first comparison of Emissary Campus, Winnow, Leanpath, BMS/BEMS, in-house dashboards and manual/reporting substitutes; converts overlap into differentiation and PMR questions. | — |
| [Türkiye Market Segmentation & Beachhead](./MARKET_SEGMENTATION_AND_BEACHHEAD.md) | Decision-structure, measurement-maturity and sustainability-maturity segmentation; ideal pilot criteria, validation gates and market-sizing rules. | — |
| [Agent Next Actions](./AGENT_NEXT_ACTIONS.md) | Role-specific execution handoff for IE, EE, CS1, CS2, frontend and backend agents, including kill/modify conditions. | — |

## Recommended reading order

### Any new agent

1. Read [Agent Next Actions](./AGENT_NEXT_ACTIONS.md) for the current research-to-execution handoff and falsification conditions.
2. Read the [Sustainability 2025](./BOGAZICI_SUSTAINABILITY_2025.md) pack for the broad campus problem landscape and claim firewall.
3. Check the [Source Reconciliation Matrix](./BOGAZICI_SOURCE_RECONCILIATION.md) before importing any numeric field into a claim, dataset, KPI or model.

### Dining / PMR / model work

4. Read the [Food Operations Deep Dive](./BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md) before PMR, data requests, architecture or modeling around dining operations.
5. Read the [Procurement & Contract](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md) pack before making Boğaziçi-specific cost, buyer, contractor-incentive or quantity-control claims.
6. Read the [Türkiye procurement benchmark](./TURKIYE_UNIVERSITY_DINING_PROCUREMENT_BENCHMARK.md) before beachhead, market-repeatability or cross-institution product-architecture work.
7. Read the [Contract Decision Precedents](./TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md) before designing PMR around quantity ownership, hakediş, excess/shortage incentives, current heuristics or menu-mix decisions.
8. Read [Türkiye Dining Reservation Signals](./TURKIYE_DINING_RESERVATION_SIGNALS.md) before treating ML forecasting as the default intervention; compare reservation/intent, passive forecast and hybrid strategies.
9. Read the [Zero-Waste Measurement Context](./TURKIYE_ZERO_WASTE_CAMPUS_MEASUREMENT_CONTEXT.md) before defining pilot waste KPIs, climate/resource conversions or application impact language.
10. Use the [PMR Target Map](./BOGAZICI_PMR_TARGET_MAP.md) to route each unresolved question to the smallest relevant owner set; do not shotgun generic outreach.
11. Use [Academic Decision Intelligence](./ACADEMIC_DECISION_INTELLIGENCE.md) for model/measurement/interview method choices, never as a Boğaziçi impact claim.

### Platform / expansion / market-context work

12. Read [Türkiye Policy, Ranking & Institutional Pull](./TURKIYE_POLICY_RANKING_PULL.md) for safe why-now context and national benchmark signals.
13. Read [Competitor & Substitute Landscape](./COMPETITOR_SUBSTITUTE_LANDSCAPE.md) before claiming novelty, designing broad platform features or writing competitor analysis.
14. Read [Türkiye Market Segmentation & Beachhead](./MARKET_SEGMENTATION_AND_BEACHHEAD.md) before TAM/SAM/SOM work, external PMR sampling or beachhead claims.
15. Read [Metric Provenance & Verification](./METRIC_PROVENANCE_AND_VERIFICATION.md) before defining durable cross-domain schemas, water/energy expansion or evidence export surfaces.

## How agents should consume a pack

1. Read the **agent-critical takeaways** and **claim firewall** first.
2. Use `fact_id` / `finding_id` / `case_id` / `target_id` references when creating downstream tasks or experiments.
3. Before promoting a number into `../EVIDENCE.md`, reopen the source, verify wording/date/units, and write a claim no broader than the source supports.
4. Route unknown workflow facts to PMR rather than filling them with assumptions.
5. Route quantitative/model implications to reproducible technical tests rather than presenting them as measured campus performance.
6. For dining data, preserve `source`, `year`, `unit`, `period`, `scope` and `counting_semantics`; use `UNKNOWN` rather than inferring missing semantics.
7. Never translate procurement contract value into food-waste savings unless the payable/accepted quantity semantics are verified.
8. Never extrapolate a purposive procurement sample into a national market size without an explicit market-sizing methodology and denominator.
9. Never copy another university's contract clause into a Boğaziçi claim; use precedents only to sharpen the exact question that Boğaziçi PMR/contract verification must answer.
10. Never convert global food-waste GHG/resource statistics into local saved CO2e/water without measured physical change, a documented conversion method and explicit `MODEL ESTIMATE` labeling.
11. A contact, scheduled call or unanswered outreach is not PMR evidence; only completed conversation artifacts can enter the interview evidence pipeline.
12. Treat policy and sustainability rankings as **context pressure**, not proof that a university will buy BOUNCAMPUS or that implementation guarantees ranking points.
13. Treat external academic intervention effects as **design references**, not expected or measured Boğaziçi effects.
14. Preserve event-time, reporting-period and measurement-stage semantics; if two values cannot be safely reconciled, represent the conflict rather than silently cleaning it.
15. Verify competitor capabilities directly before claiming a gap; vendor marketing claims and case-study savings are not neutral performance evidence.
16. Do not turn a national institution count into an addressable market count before decision/workflow segmentation and buying-path evidence exist.
17. Do not defend ML as the intervention if reservation/intent or a simple operational rule removes the uncertainty more cheaply and reliably.

## Current cross-pack synthesis

```text
PUBLIC FACT:
Boğaziçi already has sustainability measurement/governance and reports 48,251 kg food waste for 2025.

MARKET FACT:
Türkiye already has sustainability platforms, food-waste specialists, BMS/BEMS, in-house tools and reservation-based demand signals.

RESEARCH INFERENCE:
A first-time monitoring/dashboard/reporting pitch is weak; provenance alone is not a moat; ML forecasting is not automatically the best control mechanism.

HYPOTHESIS:
A material residual dining-demand/production decision remains unsolved after current tools/signals and can be improved before the freeze point.

PMR JOB:
Find the real decision owner, timing, constraints, current data/signals, reservation practices, consequences, current workaround and incumbent tools.

TECH JOB:
Compare simple baseline + reservation/intent + contextual forecast strategies; preserve uncertainty/human approval; verify outcomes against service-level guardrails.

BEACHHEAD GATE:
Repeated pain + reachable control point + measurable outcome + current-tool gap + incentive alignment + pilot feasibility + repeatability.

PLATFORM DIRECTION IF VALIDATED:
Observe -> Reconcile -> Predict/Infer Intent -> Diagnose -> Recommend -> Human Act -> Verify.
```
