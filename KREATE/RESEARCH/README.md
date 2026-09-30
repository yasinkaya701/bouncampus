# KREATE Research Packs

This directory contains secondary/public-source research prepared for KREATE agents. It is a shared **research layer**, not the evidence registry and not PMR.

## Claim boundary

- Nothing in this directory counts as `INTERVIEW EVIDENCE` or customer validation.
- Official university pages and reports may become `PUBLIC_SOURCE` evidence only after a domain owner narrows the claim and promotes it into `../EVIDENCE.md`.
- Academic papers are benchmarks and design references. A result from another university does **not** prove the same mechanism exists at Boğaziçi.
- Apparent inconsistencies in source data are preserved as caveats; agents must not silently repair them.
- Model or scenario implications derived from these sources remain `HYPOTHESIS`, `POLICY_HEURISTIC`, or `MODEL ESTIMATE` until separately validated.
- Procurement samples in this directory are **not** TAM/SAM/SOM unless a separate systematic market-sizing method explicitly establishes that scope.

## Available packs

| Pack | Purpose | Machine-readable companion |
| --- | --- | --- |
| [Boğaziçi Sustainability 2025](./BOGAZICI_SUSTAINABILITY_2025.md) | Deep secondary research from Boğaziçi sustainability/SDG sources plus peer-reviewed institutional-dining literature; includes food, water, energy, transport, data-quality caveats, PMR questions and role-specific handoffs. | [`bogazici_sustainability_2025.json`](./bogazici_sustainability_2025.json) |
| [Boğaziçi Food Operations Deep Dive](./BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md) | Decision/governance map for central production, contractor controls, BUCampus menu voting, BUCard/QR candidate signals, service regimes, packaged service, pilot data requests and CS1 model-design rules. | [`bogazici_food_operations_deep_dive.json`](./bogazici_food_operations_deep_dive.json) |
| [Boğaziçi Food Procurement & Contract Research](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md) | Current 2026–2027 unit-price dining procurement, quantities, contractor, capacity requirement, cancelled predecessor, contract-semantics unknowns and PMR/data questions. | [`bogazici_food_procurement_2026_2027.json`](./bogazici_food_procurement_2026_2027.json) |
| [Türkiye Public-University Dining Procurement Benchmark](./TURKIYE_UNIVERSITY_DINING_PROCUREMENT_BENCHMARK.md) | Cross-university 2026 procurement sample testing whether the buyer/quantity/contract workflow repeats beyond Boğaziçi; covers SKS buyer pattern, on-site vs transported service, meal/channel segmentation and candidate beachhead refinement. | [`turkiye_university_dining_procurement_benchmark.json`](./turkiye_university_dining_procurement_benchmark.json) |
| [Boğaziçi Source Reconciliation Matrix](./BOGAZICI_SOURCE_RECONCILIATION.md) | Cross-source data-quality control: capacity, beneficiary, serving, packaged-meal, food-waste/İSTAÇ and service-regime semantics that agents must reconcile before joining metrics or training models. | See the `source_conflicts` section of [`bogazici_food_operations_deep_dive.json`](./bogazici_food_operations_deep_dive.json). |
| [Türkiye Policy, Ranking & Institutional Pull](./TURKIYE_POLICY_RANKING_PULL.md) | YÖK, public-building energy policy, Climate Law, UI GreenMetric 2026 Governance & Digitalization, Türkiye benchmark campuses and safe why-now language. | — |
| [Metric Provenance & Verification](./METRIC_PROVENANCE_AND_VERIFICATION.md) | Cross-domain event/provenance model, food-pilot data contract, decision records, water/energy governance implications and verification levels. | — |
| [Academic Decision Intelligence](./ACADEMIC_DECISION_INTELLIGENCE.md) | Peer-reviewed synthesis connecting food-waste causality, forecasting, smart-campus decision processes, measurement and model design. | — |
| [Agent Next Actions](./AGENT_NEXT_ACTIONS.md) | Role-specific execution handoff for IE, EE, CS1, CS2, frontend and backend agents, including kill/modify conditions. | — |

## Recommended reading order

### Any new agent

1. Start with [Agent Next Actions](./AGENT_NEXT_ACTIONS.md) for the current research-to-execution handoff.
2. Read [Boğaziçi Sustainability 2025](./BOGAZICI_SUSTAINABILITY_2025.md) for the broad campus baseline and claim firewall.
3. Check [Boğaziçi Source Reconciliation Matrix](./BOGAZICI_SOURCE_RECONCILIATION.md) before using numeric fields.

### Dining / PMR / model work

4. Read the [Food Operations Deep Dive](./BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md).
5. Read the [Procurement & Contract](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md) pack before making cost, buyer, contractor-incentive or quantity-control claims.
6. Read the [Türkiye dining procurement benchmark](./TURKIYE_UNIVERSITY_DINING_PROCUREMENT_BENCHMARK.md) before beachhead or cross-institution architecture work.
7. Use [Academic Decision Intelligence](./ACADEMIC_DECISION_INTELLIGENCE.md) for CS1/EE method choices, not for Boğaziçi impact claims.

### Platform / expansion / pitch strategy

8. Use [Türkiye Policy, Ranking & Institutional Pull](./TURKIYE_POLICY_RANKING_PULL.md) for safe why-now and market-context claims.
9. Read [Metric Provenance & Verification](./METRIC_PROVENANCE_AND_VERIFICATION.md) before defining durable schemas or cross-domain resource modules.

## How agents should consume a pack

1. Read the **agent-critical takeaways** and **claim firewall** first.
2. Use `fact_id` / `finding_id` references when creating downstream tasks or experiments where available.
3. Before promoting a number into `../EVIDENCE.md`, reopen the source, verify wording/date/units, and write a claim no broader than the source supports.
4. Route unknown workflow facts to PMR rather than filling them with assumptions.
5. Route quantitative/model implications to reproducible technical tests rather than presenting them as measured campus performance.
6. For dining data, preserve `source`, `year`, `unit`, `period`, `scope` and `counting_semantics`; use `UNKNOWN` rather than inferring missing semantics.
7. Never translate procurement contract value into food-waste savings unless the payable/accepted quantity semantics are verified.
8. Never extrapolate a purposive procurement sample into a national market size without an explicit market-sizing methodology and denominator.
9. Treat policy and sustainability rankings as market/context pressure, not proof of willingness to pay.
10. Treat external academic intervention effects as design references, never as BOUNCAMPUS or Boğaziçi measured outcomes.

## Current cross-pack synthesis

```text
PUBLIC FACT:
Boğaziçi already has sustainability measurement/governance and reports 48,251 kg food waste for 2025.

RESEARCH INFERENCE:
A first-time monitoring/dashboard pitch is weak for a mature campus.

HYPOTHESIS:
Demand mismatch materially contributes to avoidable dining waste and the production decision is reachable.

PMR JOB:
Find the real decision owner, timing, constraints, current data, failure cost and intervention authority.

TECH JOB:
Start with a simple baseline, preserve uncertainty/human approval, and verify outcomes against service-level guardrails.

PLATFORM DIRECTION IF VALIDATED:
Observe -> Reconcile -> Predict -> Diagnose -> Recommend -> Human Act -> Verify.
```
