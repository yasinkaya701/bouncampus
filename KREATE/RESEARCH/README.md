# KREATE Research Packs

This directory contains secondary/public-source research prepared for KREATE agents. It is a shared **research layer**, not the evidence registry and not PMR.

## Claim boundary

- Nothing in this directory counts as `INTERVIEW EVIDENCE` or customer validation.
- Official university pages and reports may become `PUBLIC_SOURCE` evidence only after a domain owner narrows the claim and promotes it into `../EVIDENCE.md`.
- Academic papers are benchmarks and design references. A result from another university does **not** prove the same mechanism exists at Boğaziçi.
- Apparent inconsistencies in source data are preserved as caveats; agents must not silently repair them.
- Model or scenario implications derived from these sources remain `HYPOTHESIS`, `POLICY_HEURISTIC`, or `MODEL ESTIMATE` until separately validated.
- Procurement samples in this directory are **not** TAM/SAM/SOM unless a separate systematic market-sizing method explicitly establishes that scope.

## Start here — agent routing

| If you are working on… | Read first | Then |
| --- | --- | --- |
| Any role / choosing next work | [Campus Decision Surface Atlas](./CAMPUS_DECISION_SURFACE_ATLAS.md) | [Agent Next Actions](./AGENT_NEXT_ACTIONS.md) |
| Data access / system ownership | [Boğaziçi Data & System Ownership Map](./BOGAZICI_DATA_SYSTEM_OWNERSHIP_MAP.md) | [Metric Provenance & Verification](./METRIC_PROVENANCE_AND_VERIFICATION.md) |
| PMR / dining owner discovery | [Boğaziçi PMR Pre-Interview Evidence Pack](./BOGAZICI_PMR_PREINTERVIEW_EVIDENCE_PACK.md) | Food Operations + Procurement packs |
| CS1 dining model | [Food Operations Deep Dive](./BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md) | Academic Decision Intelligence + Metric Provenance |
| Classroom allocation | [Classroom Allocation & Occupancy](./BOGAZICI_CLASSROOM_ALLOCATION_AND_OCCUPANCY.md) | Atlas + machine-readable classroom map |
| Shuttle scheduling | [Shuttle Operations & Demand](./BOGAZICI_SHUTTLE_OPERATIONS_AND_DEMAND.md) | Atlas + machine-readable shuttle map |
| Water / energy expansion | [Campus Decision Surface Atlas](./CAMPUS_DECISION_SURFACE_ATLAS.md) | Sustainability 2025 + Metric Provenance |
| Pitch / market context | [Market Segmentation & Beachhead](./MARKET_SEGMENTATION_AND_BEACHHEAD.md) | Policy/Ranking + Competitor Landscape |

## Available packs

| Pack | Purpose | Machine-readable companion |
| --- | --- | --- |
| [Campus Decision Surface Atlas](./CAMPUS_DECISION_SURFACE_ATLAS.md) | Cross-domain owner/decision/data/falsifier map covering dining, classroom allocation, shuttle scheduling, water and energy; keeps dining as P0 while identifying adjacent P1 decision modules. | [`campus_decision_surface_atlas.json`](./campus_decision_surface_atlas.json) |
| [Boğaziçi Data & System Ownership Map](./BOGAZICI_DATA_SYSTEM_OWNERSHIP_MAP.md) | Cross-domain routing for BUIS/ÖBİKAS, classroom scheduling, BUCampus, BUCard, shuttle, Wi-Fi, water and energy; separates service support, data stewardship, business ownership and access authority. | [`bogazici_data_system_ownership_map.json`](./bogazici_data_system_ownership_map.json) |
| [Boğaziçi PMR Pre-Interview Evidence Pack](./BOGAZICI_PMR_PREINTERVIEW_EVIDENCE_PACK.md) | Converts strongest current public-source dining findings into interview routing, falsifiers, exact questions and stop-browsing boundaries. | [`bogazici_pmr_preinterview_evidence_pack.json`](./bogazici_pmr_preinterview_evidence_pack.json) |
| [Boğaziçi Classroom Allocation & Occupancy](./BOGAZICI_CLASSROOM_ALLOCATION_AND_OCCUPANCY.md) | Maps the classroom scheduling owner, 2025 room-capacity inventory, data semantics, optimization baselines, occupancy caveats and PMR falsifiers. | [`bogazici_classroom_decision_map.json`](./bogazici_classroom_decision_map.json) |
| [Boğaziçi Shuttle Operations & Demand](./BOGAZICI_SHUTTLE_OPERATIONS_AND_DEMAND.md) | Maps public route/timetable surfaces, aggregate shuttle signals, candidate demand/scheduling model, baselines and operator PMR questions. | [`bogazici_shuttle_decision_map.json`](./bogazici_shuttle_decision_map.json) |
| [Boğaziçi Sustainability 2025](./BOGAZICI_SUSTAINABILITY_2025.md) | Deep secondary research from Boğaziçi sustainability/SDG sources plus peer-reviewed institutional-dining literature; includes food, water, energy, transport, data-quality caveats, PMR questions and role-specific handoffs. | [`bogazici_sustainability_2025.json`](./bogazici_sustainability_2025.json) |
| [Boğaziçi Food Operations Deep Dive](./BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md) | Decision/governance map for central production, contractor controls, BUCampus menu voting, BUCard/QR candidate signals, service regimes, packaged service, pilot data requests and CS1 model-design rules. | [`bogazici_food_operations_deep_dive.json`](./bogazici_food_operations_deep_dive.json) |
| [Boğaziçi Food Procurement & Contract Research](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md) | Current 2026–2027 unit-price dining procurement, quantities, contractor, capacity requirement, cancelled predecessor, contract-semantics unknowns and PMR/data questions. | [`bogazici_food_procurement_2026_2027.json`](./bogazici_food_procurement_2026_2027.json) |
| [Boğaziçi PMR Target Map](./BOGAZICI_PMR_TARGET_MAP.md) | Public contact/role routing for Food Services, contractor, BİD, waste and escalation owners; routing only, not interview evidence. | [`bogazici_pmr_target_map.json`](./bogazici_pmr_target_map.json) |
| [Türkiye Public-University Dining Procurement Benchmark](./TURKIYE_UNIVERSITY_DINING_PROCUREMENT_BENCHMARK.md) | Cross-university 2026 procurement sample testing whether the buyer/quantity/contract workflow repeats beyond Boğaziçi. | [`turkiye_university_dining_procurement_benchmark.json`](./turkiye_university_dining_procurement_benchmark.json) |
| [Türkiye Dining Contract Decision Precedents](./TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md) | Contract precedents for call-off, acceptance, penalty and operational decision semantics; precedents only, never silently transferred to Boğaziçi. | [`turkiye_dining_contract_decision_precedents.json`](./turkiye_dining_contract_decision_precedents.json) |
| [Türkiye Dining Reservation Signals](./TURKIYE_DINING_RESERVATION_SIGNALS.md) | Reservation/intent mechanisms used elsewhere and the questions they create for Boğaziçi demand planning. | — |
| [Boğaziçi Source Reconciliation Matrix](./BOGAZICI_SOURCE_RECONCILIATION.md) | Cross-source data-quality control for capacity, beneficiary, serving, packaged-meal, food-waste/İSTAÇ and service-regime semantics. | See source-conflict sections in existing JSON packs. |
| [Türkiye Policy, Ranking & Institutional Pull](./TURKIYE_POLICY_RANKING_PULL.md) | YÖK, public-building energy policy, Climate Law, UI GreenMetric 2026 Governance & Digitalization, Türkiye benchmark campuses and safe why-now language. | — |
| [Türkiye Zero-Waste Campus Measurement Context](./TURKIYE_ZERO_WASTE_CAMPUS_MEASUREMENT_CONTEXT.md) | National zero-waste/campus measurement context and safe measurement-governance implications. | [`turkiye_zero_waste_campus_measurement_context.json`](./turkiye_zero_waste_campus_measurement_context.json) |
| [Metric Provenance & Verification](./METRIC_PROVENANCE_AND_VERIFICATION.md) | Cross-domain event/provenance model, food-pilot data contract, decision records, water/energy governance implications and verification levels. | — |
| [Academic Decision Intelligence](./ACADEMIC_DECISION_INTELLIGENCE.md) | Peer-reviewed synthesis connecting food-waste causality, forecasting, smart-campus decision processes, measurement and model design. | — |
| [Competitor / Substitute Landscape](./COMPETITOR_SUBSTITUTE_LANDSCAPE.md) | Existing sustainability, food-waste, BMS/BEMS and in-house substitutes; use after the decision gap is understood. | — |
| [Market Segmentation & Beachhead](./MARKET_SEGMENTATION_AND_BEACHHEAD.md) | Beachhead logic and market segmentation grounded in current research boundaries. | — |
| [Agent Next Actions](./AGENT_NEXT_ACTIONS.md) | Role-specific execution handoff for IE, EE, CS1, CS2, frontend and backend agents, including kill/modify conditions. | — |

## Recommended reading order

### Any new agent

1. [Campus Decision Surface Atlas](./CAMPUS_DECISION_SURFACE_ATLAS.md) — understand the P0/P1/P2 decision hierarchy.
2. [Boğaziçi Data & System Ownership Map](./BOGAZICI_DATA_SYSTEM_OWNERSHIP_MAP.md) — identify business/technical/data/access owners before requesting data.
3. [Agent Next Actions](./AGENT_NEXT_ACTIONS.md) — map research into role-specific execution.
4. [Boğaziçi Sustainability 2025](./BOGAZICI_SUSTAINABILITY_2025.md) — broad campus baseline and claim firewall.
5. [Boğaziçi Source Reconciliation Matrix](./BOGAZICI_SOURCE_RECONCILIATION.md) — numeric/data-quality constraints.

### Dining / PMR / model work

6. [Boğaziçi PMR Pre-Interview Evidence Pack](./BOGAZICI_PMR_PREINTERVIEW_EVIDENCE_PACK.md).
7. [Food Operations Deep Dive](./BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md).
8. [Procurement & Contract](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md).
9. [Türkiye dining procurement benchmark](./TURKIYE_UNIVERSITY_DINING_PROCUREMENT_BENCHMARK.md).
10. [Academic Decision Intelligence](./ACADEMIC_DECISION_INTELLIGENCE.md).

### Classroom / mobility adjacency

11. [Classroom Allocation & Occupancy](./BOGAZICI_CLASSROOM_ALLOCATION_AND_OCCUPANCY.md).
12. [Shuttle Operations & Demand](./BOGAZICI_SHUTTLE_OPERATIONS_AND_DEMAND.md).
13. Return to the [Campus Decision Surface Atlas](./CAMPUS_DECISION_SURFACE_ATLAS.md) before building either module; both are **P1 hypotheses**, not validated pivots.

### Platform / expansion / pitch strategy

14. [Türkiye Policy, Ranking & Institutional Pull](./TURKIYE_POLICY_RANKING_PULL.md).
15. [Metric Provenance & Verification](./METRIC_PROVENANCE_AND_VERIFICATION.md).
16. [Market Segmentation & Beachhead](./MARKET_SEGMENTATION_AND_BEACHHEAD.md).

## How agents should consume a pack

1. Read **agent-critical takeaways** and **claim firewall** first.
2. Use `fact_id` / `finding_id` references when creating downstream tasks or experiments where available.
3. Before promoting a number into `../EVIDENCE.md`, reopen the source, verify wording/date/units, and write a claim no broader than the source supports.
4. Route unknown workflow facts to PMR rather than filling them with assumptions.
5. Route quantitative/model implications to reproducible technical tests rather than presenting them as measured campus performance.
6. Preserve `source`, `year`, `unit`, `period`, `scope` and `counting_semantics`; use `UNKNOWN` rather than inferring missing semantics.
7. Never translate procurement contract value into food-waste savings unless payable/accepted quantity semantics are verified.
8. Never extrapolate a purposive procurement sample into a national market size without an explicit denominator and method.
9. Treat policy and sustainability rankings as context pressure, not proof of willingness to pay.
10. Treat external academic intervention effects as design references, never as Boğaziçi/BOUNCAMPUS measured outcomes.
11. For classroom work, preserve `quota`, `registered`, `attendance`, `room_capacity`, and `estimated_occupancy` as distinct fields.
12. For shuttle work, preserve `scheduled_departure`, `actual_departure`, `capacity`, `boarded`, `queue/left_behind`, and `estimated_demand` as distinct fields.
13. Before requesting data, distinguish `business_owner`, `technical_owner`, `semantic_validator`, and `access_authority`; never infer data access from a public service listing.
14. Prefer a transparent baseline and owner-review loop before complex ML or autonomous control.

## Current cross-pack synthesis

```text
PUBLIC FACT:
Boğaziçi already has mature sustainability governance, a reported 48,251 kg 2025 food-waste stream,
a centrally owned classroom-scheduling workflow, and a public multi-campus shuttle network.

RESEARCH INFERENCE:
A generic dashboard or digital-twin pitch is weak. The stronger reusable unit is a real operational decision with an owner, deadline, constraints and measurable outcome.

P0 HYPOTHESIS:
Dining demand mismatch materially contributes to avoidable waste and production quantity is reachable.

P1 HYPOTHESES:
Classroom allocation may contain costly capacity/movement/rework trade-offs.
Shuttle departures may contain peak imbalance that can be improved with class-transition + ridership context.

PMR JOB:
Find the owner, timing, constraints, current workaround, data semantics and failure cost before deep implementation.

TECH JOB:
Baseline first -> recommendation -> human approval -> measured outcome -> verification.

PLATFORM DIRECTION IF VALIDATED:
Observe -> Reconcile -> Decision Context -> Predict/Optimize -> Recommend -> Human Act -> Verify.
```
