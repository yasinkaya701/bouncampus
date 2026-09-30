# Agent Next Actions — Deep Research Handoff

**Research date:** 2026-10-01  
**Purpose:** Convert secondary research into executable work without promoting secondary evidence into PMR, pilot results or customer validation.

## Shared strategic conclusion

Current research supports testing BOUNCAMPUS as a **campus resource decision-and-verification layer**, with dining as the first candidate beachhead only if a real residual control problem survives PMR.

The dining wedge is no longer defined as `build an ML demand forecast`.

Boğaziçi public sources now establish:

- a measured food-waste stream;
- centralized food production and multi-campus service;
- BUCard / BUCampus digital meal-access surfaces;
- special-period reservation and cancellation capability;
- an uncancelled no-show commitment rule in a 2026 holiday regime;
- a historical 2024 rule where low reservation count changed service modality to packaged service;
- a formal Dining Hall / Cooking / Distribution Control Organisation;
- current food governance that explicitly includes **production planning** and monthly recording/reporting of **produced, consumed and discarded** food quantities/types.

The unresolved question is narrower and more valuable:

> **Which dining decision remains uncertain and economically/operationally important after existing reservation, access, operator and contract signals are used, and can that decision be changed before its freeze point?**

Candidate loop:

```text
Observe
→ Reconcile event semantics
→ Infer demand / intent / residual uncertainty
→ Diagnose reachable control point
→ Recommend quantity / allocation / service regime / batch
→ Human approve or override
→ Execute
→ Verify accepted service + physical outcome
→ Promote only defensible evidence
```

---

# IE — Customer Discovery & Market Lead

## P0: reconstruct one real service from intent to settlement

Interview order:

1. Food Services Branch;
2. TEMAŞ local project / kitchen operator;
3. Dining/Cooking/Distribution Control Organisation;
4. BUCard/BİD data owner;
5. Safe & Sustainable Food / monthly reporting owner;
6. waste-measurement owner;
7. SKS senior owner only for permission/escalation.

Read first:

- `BOGAZICI_DEMAND_CONTROL_SURFACES.md`
- `BOGAZICI_FOOD_GOVERNANCE_DECISION_RIGHTS.md`
- `BOGAZICI_PMR_TARGET_MAP.md`
- `BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`

For a recent concrete meal service reconstruct:

```text
intent / historical signal
→ quantity or service-mode calculation
→ decision owner
→ approval owner
→ freeze time
→ contractor execution
→ campus/channel allocation
→ control / acceptance record
→ validated served count
→ surplus / shortage / waste
→ user charge if relevant
→ contractor settlement quantity
→ monthly food-flow reporting
```

Do not ask `Would AI help?`

Ask `What happened yesterday / in the last error case?`

## P0 falsifiers

Modify or kill the current wedge if repeated evidence shows:

- reservation/current process already removes meaningful uncertainty;
- all useful decisions freeze before any signal can improve them;
- quantity, allocation, service mode, mix and batch are all non-discretionary;
- pre-consumer surplus is not a material part of the addressable waste/problem;
- operational ground truth cannot be reconciled;
- no actor has authority and incentive to change the decision;
- an incumbent tool already solves the workflow with little pain;
- user friction/equity costs make reservation-first intervention unacceptable and passive forecasting adds little value.

---

# EE — Physical Systems & Measurement Lead

## P0: define one service's physical truth

Do **not** design hardware first.

Determine whether these can be measured/exported consistently:

```text
planned_portions
produced_portions
delivered_portions
validated_served_count
edible_surplus
preparation_waste_kg
plate_waste_kg
shortage / early_sellout / substitution
service_mode
measurement_method
accepted_service_record
```

If reservation history is available, add:

```text
active_reservations_at_cutoff
reservations_cancelled
uncancelled_no_show
unreserved_or_late_demand
```

Required field audit:

```text
field
current source
physical/event meaning
owner
granularity
timestamp semantics
retention
quality
access
effort
blocker
```

The most important measurement question is whether `surplus/waste` can be attributed to the same campus × meal × service episode as the planning decision.

---

# CS1 — Decision Intelligence Lead

## P0: run the reservation-reconciliation ladder before complex ML

Read:

- `PILOT_RESERVATION_RECONCILIATION_PROTOCOL.md`
- `bogazici_dining_decision_graph.json`
- `BOGAZICI_SOURCE_RECONCILIATION.md`

### Step 0 — Event reconciliation

If historical reservation periods are available, first compare:

```text
active reservations at cutoff
vs
validated served demand
```

Quantify:

- cancellation rate;
- show rate;
- unreserved share;
- bias/error by campus/meal/service regime;
- unreconciled anomalies.

### Step 1 — Simple transparent correction

Test something equivalent to:

```text
Q_simple =
  reservations_at_cutoff * historical_show_rate
  + expected_unreserved_demand
```

### Step 2 — Passive historical baseline

Where reservation is unavailable, test:

1. same weekday + meal mean/median;
2. recent comparable-service mean;
3. service-regime/calendar-aware baseline.

### Step 3 — Contextual residual model

Only if simple strategies leave material predictable residual error, test menu/campus/calendar/event features.

Do not promote a model unless it improves **out-of-sample decision utility**, not just R²/MAE.

Candidate decision loss:

```text
surplus = max(Q - D, 0)
shortage = max(D - Q, 0)

DecisionLoss =
  C_excess * surplus
  + C_shortage * shortage
```

Before contract economics are known, use a sensitivity grid for `C_shortage / C_excess`; do not invent TRY savings.

### Required safety behavior

- allow `WITHHOLD` when data quality is inadequate;
- preserve operator approval;
- record overrides + reasons;
- expose planning-band/calibration semantics honestly;
- keep source-reported, derived and model-estimated values separate;
- never infer live occupancy from schedules;
- never equate reservation with served demand;
- never leak post-service variables into a pre-service forecast.

## Key falsifier

A more accurate estimate that cannot change quantity, allocation, batch or service regime before freeze has little product value.

---

# CS2 — Product Strategy, Evidence & Application

## P0: rewrite the product thesis around a reachable decision, not AI

Safe public-source context now includes:

- Boğaziçi reports a measurable food-waste stream;
- the university's food governance explicitly includes production planning and monthly produced/consumed/discarded reporting;
- special-period reservation capability exists;
- reservation count has historically changed service modality in one special regime;
- digital meal-access and explicit menu-preference signals exist;
- food-service execution, control, data and sustainability governance are split across multiple roles.

Still hypothesis:

- normal-term reservation coverage/use;
- material no-show/walk-in uncertainty;
- production mismatch as a major waste cause;
- daily quantity owner;
- current freeze point;
- contractor hakediş semantics;
- buyer/user willingness to pay;
- cross-campus repeatability.

Preferred category language:

- operational sustainability decision support;
- campus resource intelligence;
- intent + operations + verification;
- traceable decision evidence.

Avoid:

- autonomous campus optimization;
- generic AI sustainability OS;
- guaranteed waste reduction;
- guaranteed GreenMetric impact;
- claiming a reservation/no-show problem without data;
- treating historical `<15 → package` as current policy.

---

# Backend / Data agents

Read `bogazici_dining_decision_graph.json` and `METRIC_PROVENANCE_AND_VERIFICATION.md` before defining APIs.

First-class event types must remain separate:

```text
reservation_created
reservation_cancelled
active_reservation_at_cutoff
uncancelled_no_show
unreserved_or_late_demand
planned_portions
produced_portions
delivered_portions
validated_entry_or_served
accepted_service_quantity
user_charge
contract_settled_quantity
edible_surplus
preparation_waste
plate_waste
collected_waste
```

Minimum rules:

- event time != reporting period;
- service regime/effective policy version is first-class;
- reservation != turnstile != served != user charge != contractor settlement;
- source owner/provenance is mandatory;
- transformations/policies are versioned;
- unresolved conflicts are representable as `RECONCILIATION_REQUIRED`;
- service and decision IDs are stable;
- decision owner, execution owner, approval/control role and outcome are separately stored.

---

# Frontend / UX agents

Do not make the pilot proof a KPI wall or 3D map.

Primary interaction should be one **decision card**:

```text
service
signal state
reservations / historical context
recommended action or range
why
uncertainty / shortage risk
missing data
approve / override
override reason
later: actual served / surplus / shortage / verified outcome
```

The recommendation may be:

- quantity;
- reserve batch;
- campus allocation;
- package vs hall mode;
- menu mix.

Do not hard-code a control surface before PMR verifies it.

---

# Research backlog ranked by decision value

## P0 — primary research

1. Who sets current daily quantity, allocation and service mode?
2. What is each decision's exact freeze time?
3. Is reservation used/activatable in normal term and what residual uncertainty remains?
4. Can historical 2024/2026 reservation events be exported in aggregate?
5. Which record does the Control Organisation accept as operational truth?
6. What becomes contractor hakediş/payment: requested, produced, delivered, accepted, served or another quantity?
7. What source systems generate the directive-required monthly produced/consumed/discarded report?
8. What fraction of waste is pre-consumer surplus vs preparation vs plate waste?
9. What does underproduction cause operationally and financially?
10. Which role captures the benefit of a better decision?

## P1 — technical evidence

11. Run retrospective reservation reconciliation if data exist.
12. Compare raw reservation vs simple correction vs passive history.
13. Only then test contextual residual modeling.
14. Define one prospective shadow-mode decision record.
15. Validate measurement boundary and shortage guardrails.

## P2 — repeatability

16. Repeat the decision-rights interview at 2–3 Turkish universities using different procurement/reservation structures.
17. Segment market by decision structure and current substitute, not institution count alone.

---

# One-page mental model

```text
PUBLIC SOURCE:
Boğaziçi has food-governance obligations, digital dining events,
special-period reservation/control precedent and a measured waste stream.

UNKNOWN:
What residual uncertainty remains in normal operations, and which action is reachable?

PMR:
Resolve owner + signal + freeze + action + accepted truth + incentives.

TECH TEST:
Reconcile intent to service before training complex ML.

BASELINES:
reservation-only / simple correction / passive history.

MODEL:
Only if meaningful predictable residual remains.

PILOT:
Shadow → advisory → bounded intervention with shortage and waste guardrails.

ONLY THEN:
Claim measured impact or promote the beachhead.
```
