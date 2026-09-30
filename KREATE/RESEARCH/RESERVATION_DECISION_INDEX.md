# Reservation & Dining Decision Workstream Index

**Research date:** 2026-10-01  
**Purpose:** Entry point for agents working specifically on Boğaziçi dining intent, decision rights, reservation/no-show uncertainty, accepted operational truth and the first falsifiable pilot.  
**Status:** Secondary/public-source research + proposed pilot method. Not PMR, not pilot evidence, not a measured outcome.

## Read in this order

1. [`BOGAZICI_DEMAND_CONTROL_SURFACES.md`](./BOGAZICI_DEMAND_CONTROL_SURFACES.md) — what Boğaziçi has publicly demonstrated: reservation, cancellation/no-show commitment, service-regime switching, BUCard/QR access, menu intent and formal control roles.
2. [`BOGAZICI_FOOD_GOVERNANCE_DECISION_RIGHTS.md`](./BOGAZICI_FOOD_GOVERNANCE_DECISION_RIGHTS.md) — production-planning/reporting obligations and the unresolved role graph across Food Services, TEMAŞ, Control Organisation, BİD/BUCard and sustainability governance.
3. [`BOGAZICI_SOURCE_RECONCILIATION.md`](./BOGAZICI_SOURCE_RECONCILIATION.md) — semantic firewall: reservation ≠ served ≠ user charge ≠ accepted service ≠ contractor settlement; historic rules ≠ current policy.
4. [`BOGAZICI_PMR_TARGET_MAP.md`](./BOGAZICI_PMR_TARGET_MAP.md) — who to interview, in what order, and which narrow question each role owns.
5. [`PILOT_RESERVATION_RECONCILIATION_PROTOCOL.md`](./PILOT_RESERVATION_RECONCILIATION_PROTOCOL.md) — event reconciliation → transparent baselines → residual model only if justified → shadow/advisory pilot.
6. [`bogazici_dining_decision_graph.json`](./bogazici_dining_decision_graph.json) — machine-readable facts, sources, roles, signals, decisions, unknowns, pilot gates and falsifiers.
7. [`AGENT_NEXT_ACTIONS.md`](./AGENT_NEXT_ACTIONS.md) — role-specific execution handoff for IE, EE, CS1, CS2, backend and frontend.

## Existing packs that must also be respected

This workstream does **not** replace the parallel research already merged into the CS2 role branch. Before economic, privacy or contract claims, also read:

- [`BOGAZICI_CONTRACT_SEMANTICS_EVIDENCE_MAP.md`](./BOGAZICI_CONTRACT_SEMANTICS_EVIDENCE_MAP.md)
- [`BOGAZICI_2024_2025_CONTRACT_PRECEDENT.md`](./BOGAZICI_2024_2025_CONTRACT_PRECEDENT.md)
- [`BOGAZICI_DINING_INCENTIVE_SUBSIDY_MAP.md`](./BOGAZICI_DINING_INCENTIVE_SUBSIDY_MAP.md)
- [`BOGAZICI_DINING_PRIVACY_DATA_MINIMIZATION.md`](./BOGAZICI_DINING_PRIVACY_DATA_MINIMIZATION.md)
- [`BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md)
- [`TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md`](./TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md)
- [`TURKIYE_DINING_RESERVATION_SIGNALS.md`](./TURKIYE_DINING_RESERVATION_SIGNALS.md)

## Current decision thesis

```text
not:
"use AI to predict cafeteria traffic"

but:
identify existing intent / history / contract / service signals
→ reconcile their event semantics
→ find a decision that remains uncertain and reachable before freeze
→ compare the cheapest transparent policy against current practice
→ add residual modeling only if it earns its complexity
→ keep human approval
→ measure accepted service + surplus/shortage/waste prospectively
→ promote only traceable evidence
```

## Current P0 unknowns

1. Who sets normal-term production quantity, campus allocation and service mode?
2. What is each action's exact freeze time?
3. Is reservation available/used in normal term, and what residual no-show/walk-in uncertainty remains?
4. Can historic reservation/cancellation/service events be exported as source-owner aggregates?
5. Which record does the Control Organisation accept as operational truth?
6. Which quantity drives current TEMAŞ hakediş/payment?
7. Which source systems produce the current governance-required `produced / consumed / discarded` monthly report?
8. What share of addressable waste is pre-consumer surplus versus preparation/plate waste?
9. Who captures financial/operational benefit from a better decision?

## Hard gates

Do not build complex ML unless:

- event semantics reconcile;
- a meaningful residual uncertainty exists after reservation/current heuristic;
- a real action is adjustable before freeze;
- a simple baseline is beaten out-of-sample on decision utility;
- shortage/food-access guardrails remain acceptable;
- the data path can be implemented with aggregate/minimized data;
- an operator can approve/override and outcomes can be verified.

Failure at a gate means change the control point or stop — not add model complexity.
