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

## Recommended reading order

1. Start with the Sustainability 2025 pack for the broad campus problem landscape and claim firewall.
2. Read the Food Operations Deep Dive before PMR, data requests, architecture or modeling around dining operations.
3. Read the Procurement & Contract pack before making cost, buyer, contractor-incentive or quantity-control claims.
4. Read the Türkiye procurement benchmark before beachhead, market-repeatability or cross-institution product-architecture work.
5. Check the Source Reconciliation Matrix before importing any numeric field into an application claim, dataset, KPI or model.

## How agents should consume a pack

1. Read the **agent-critical takeaways** and **claim firewall** first.
2. Use `fact_id` / `finding_id` references when creating downstream tasks or experiments.
3. Before promoting a number into `../EVIDENCE.md`, reopen the source, verify wording/date/units, and write a claim no broader than the source supports.
4. Route unknown workflow facts to PMR rather than filling them with assumptions.
5. Route quantitative/model implications to reproducible technical tests rather than presenting them as measured campus performance.
6. For dining data, preserve `source`, `year`, `unit`, `period`, `scope` and `counting_semantics`; use `UNKNOWN` rather than inferring missing semantics.
7. Never translate procurement contract value into food-waste savings unless the payable/accepted quantity semantics are verified.
8. Never extrapolate a purposive procurement sample into a national market size without an explicit market-sizing methodology and denominator.
