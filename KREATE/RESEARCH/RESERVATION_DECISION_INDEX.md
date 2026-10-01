# Reservation & Dining Decision Workstream Index

**Research date:** 2026-10-01  
**Purpose:** Entry point for agents working specifically on Boğaziçi dining intent, decision rights, digital reporting, reservation/no-show uncertainty, accepted operational truth, evidence acquisition and the first falsifiable pilot.  
**Status:** Secondary/public-source research + proposed acquisition/pilot methods. Not PMR, not pilot evidence, not a measured outcome.

## Read in this order

1. [`BOGAZICI_DEMAND_CONTROL_SURFACES.md`](./BOGAZICI_DEMAND_CONTROL_SURFACES.md) — what Boğaziçi has publicly demonstrated: reservation, cancellation/no-show commitment, service-regime switching, BUCard/QR access, menu intent and formal control roles.
2. [`BOGAZICI_FOOD_GOVERNANCE_DECISION_RIGHTS.md`](./BOGAZICI_FOOD_GOVERNANCE_DECISION_RIGHTS.md) — production-planning/reporting obligations and the unresolved role graph across Food Services, TEMAŞ, Control Organisation, BİD/BUCard and sustainability governance.
3. [`BOGAZICI_DINING_DIGITAL_REPORTING_SURFACES.md`](./BOGAZICI_DINING_DIGITAL_REPORTING_SURFACES.md) — 2025 BİD evidence for the BUCard dining real-time report, daily passage reports, packaged-meal reporting and package-service mobile surfaces; reframes data acquisition around existing aggregate reports rather than raw logs. Machine-readable companion: [`bogazici_dining_digital_reporting_surfaces.json`](./bogazici_dining_digital_reporting_surfaces.json).
4. [`BOGAZICI_SOURCE_RECONCILIATION.md`](./BOGAZICI_SOURCE_RECONCILIATION.md) — semantic firewall: reservation ≠ passage ≠ served ≠ user charge ≠ accepted service ≠ contractor settlement; historic rules ≠ current policy.
5. [`BOGAZICI_PMR_TARGET_MAP.md`](./BOGAZICI_PMR_TARGET_MAP.md) — who to interview, in what order, and which narrow question each role owns.
6. [`BOGAZICI_EVIDENCE_ACQUISITION_PLAYBOOK.md`](./BOGAZICI_EVIDENCE_ACQUISITION_PLAYBOOK.md) — when public research must stop and which minimum artifact/aggregate field should be acquired from Food Services, TEMAŞ, Control, Tahakkuk, Procurement, BİD or reporting owners.
7. [`bogazici_evidence_acquisition_queue.json`](./bogazici_evidence_acquisition_queue.json) — machine-readable `EA-01...EA-06` acquisition tasks, owners, exact minimum requests, privacy exclusions, downstream gates and stop conditions.
8. [`PILOT_RESERVATION_RECONCILIATION_PROTOCOL.md`](./PILOT_RESERVATION_RECONCILIATION_PROTOCOL.md) — event reconciliation → transparent baselines → residual model only if justified → shadow/advisory pilot.
9. [`bogazici_dining_decision_graph.json`](./bogazici_dining_decision_graph.json) — machine-readable facts, sources, roles, signals, decisions, unknowns, pilot gates and falsifiers.
10. [`AGENT_NEXT_ACTIONS.md`](./AGENT_NEXT_ACTIONS.md) — role-specific execution handoff for IE, EE, CS1, CS2, backend and frontend.

## Existing packs that must also be respected

This workstream does **not** replace the parallel research already merged into the CS2 role branch. Before economic, privacy, contract or causal claims, also read:

- [`BOGAZICI_CONTRACT_SEMANTICS_EVIDENCE_MAP.md`](./BOGAZICI_CONTRACT_SEMANTICS_EVIDENCE_MAP.md)
- [`BOGAZICI_2024_2025_CONTRACT_PRECEDENT.md`](./BOGAZICI_2024_2025_CONTRACT_PRECEDENT.md)
- [`BOGAZICI_DINING_INCENTIVE_SUBSIDY_MAP.md`](./BOGAZICI_DINING_INCENTIVE_SUBSIDY_MAP.md)
- [`BOGAZICI_DINING_PRIVACY_DATA_MINIMIZATION.md`](./BOGAZICI_DINING_PRIVACY_DATA_MINIMIZATION.md)
- [`BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md)
- [`TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md`](./TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md)
- [`TURKIYE_DINING_RESERVATION_SIGNALS.md`](./TURKIYE_DINING_RESERVATION_SIGNALS.md)
- [`FOOD_WASTE_PILOT_PROTOCOL_RED_TEAM.md`](./FOOD_WASTE_PILOT_PROTOCOL_RED_TEAM.md)
- [`BOGAZICI_PROCUREMENT_COST_DENOMINATOR_WARNING.md`](./BOGAZICI_PROCUREMENT_COST_DENOMINATOR_WARNING.md)

## Current decision thesis

```text
not:
"use AI to predict cafeteria traffic"

but:
identify existing intent / history / contract / service / report signals
→ reconcile their event semantics
→ find a decision that remains uncertain and reachable before freeze
→ reuse the smallest existing aggregate institutional report when possible
→ acquire the minimum authoritative evidence object for unresolved semantics
→ compare the cheapest transparent policy against current practice
→ add residual modeling only if it earns its complexity
→ keep human approval
→ measure accepted service + surplus/shortage/waste prospectively
→ promote only traceable evidence
```

## New digital-reporting evidence

The 2025 BİD activity report publicly documents:

- a **BUCard dining real-time report page** with packaged-meal-count enhancements;
- **daily passage reports** enhanced with packaged-meal information;
- a personnel meal report with a breakfast field;
- BUCard mobile use at dining halls and packaged-meal distribution points;
- a packaged-meal sales mobile application.

This does **not** mean the team has report access, API access, historical retention or a validated ground-truth field.

Correct next question:

```text
What does the existing report count,
which dimensions/export already exist,
who uses it,
and what decision can still change when the report is available?
```

The first BİD request should therefore be the existing report **schema/data dictionary or owner-generated aggregate export**, not raw student/card logs.

## Current P0 unknowns

1. Who sets normal-term production quantity, campus allocation and service mode?
2. What is each action's exact freeze time?
3. Is reservation available/used in normal term, and what residual no-show/walk-in uncertainty remains?
4. What exactly do the current BUCard dining real-time and daily-passage report fields count?
5. Which report dimensions, retention and aggregate export capabilities exist?
6. Who currently reads the real-time dining report and does any operator act on it during service?
7. Can a second batch, reserve release, channel/campus reallocation or another same-day action change after live counts arrive?
8. Which record does the Control Organisation accept as operational truth?
9. Which quantity drives current TEMAŞ hakediş/payment?
10. Which source systems produce the current governance-required `produced / consumed / discarded` monthly report?
11. What share of addressable waste is pre-consumer surplus versus preparation/plate waste?
12. Who captures financial/operational benefit from a better decision?

## P0 evidence acquisition sequence

Use `bogazici_evidence_acquisition_queue.json` rather than repeating broad web research:

```text
EA-01  quantity owner + freeze time
EA-02  accepted-service + hakediş semantics
EA-03  existing BUCard dining-report schema/export + reservation → realized-service reconciliation
EA-04  physical surplus/waste boundary
EA-05  produced/consumed/discarded monthly report schema
EA-06  current authoritative contract/specification locator
```

Important routing refinement:

- Food Services / TEMAŞ answer the production workflow;
- Control Organisation helps identify accepted operational truth;
- **Tahakkuk** is a formal public owner for university hakediş payments and is therefore a high-value route for payment-basis artifacts;
- Procurement is the authoritative current-contract/specification route;
- **BİD should first be asked for the existing BUCard dining report schema/data dictionary or owner-generated aggregate report**, not person-level histories;
- interval-level aggregate counts should be requested only if a same-day decision is actually reachable;
- formal Bilgi Edinme is a narrow public-document fallback, not an access-control bypass.

## Candidate same-day control loop — HYPOTHESIS ONLY

```text
pre-service plan
→ service begins
→ existing aggregate live passage pace
→ expected-vs-realized deviation
→ second batch / reserve release / package-hall / campus-channel reallocation IF reachable
→ verified shortage + surplus outcome
```

Kill this loop if cooking/dispatch is already irreversible, report latency is too high, counts cannot be reconciled, or no authorized operator can act on them.

## Hard gates

Do not build complex ML unless:

- event/report semantics reconcile;
- a meaningful residual uncertainty exists after reservation/current heuristic;
- a real action is adjustable before the relevant signal arrives or before the decision freezes;
- a simple baseline is beaten out-of-sample on decision utility;
- shortage/food-access guardrails remain acceptable;
- the data path can be implemented with aggregate/minimized data;
- an operator can approve/override and outcomes can be verified.

Do not build a new telemetry or identity pipeline unless:

- the existing BUCard aggregate reporting surface cannot answer the named decision;
- the missing information is demonstrably necessary;
- the institutional owner approves the narrower additional data path.

Do not make monetary/contract claims unless:

- current accepted/hakediş quantity semantics are resolved from authoritative current evidence;
- relevant unit-price / variable-cost meaning is separately verified;
- user contribution, subsidy/accounting and contractor settlement are not conflated.

Failure at a gate means acquire the missing authoritative evidence, change the control point or stop — not add model complexity, raw personal data or weaker derivative sources.
