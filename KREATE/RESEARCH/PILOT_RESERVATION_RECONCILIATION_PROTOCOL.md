# Pilot Protocol — Reservation → Service → Waste Reconciliation

**Research date:** 2026-10-01  
**Purpose:** Define the smallest falsifiable technical experiment for the dining wedge before building complex ML.  
**Status:** Proposed pilot protocol. **No pilot has run. No Boğaziçi data access is assumed.**

## Why this pilot comes first

Boğaziçi public sources establish special-period reservation capability, cancellation, digital meal access and at least one historical case where reservation count changed service modality. Academic research also shows that when booking exists, no-show behavior and residual uncertainty can matter.

Therefore the first technical test should not be `train XGBoost on public data`.

It should answer:

> **How much uncertainty remains between the best pre-freeze intent signal and actual service, and is that residual large/predictable enough to justify a decision model?**

If the answer is `very little`, a simple reservation/control rule may dominate ML.

---

# 1. Pilot hypotheses

## H-P0 — Event reconciliation is feasible

For at least one historical/special-period dataset, the team can reconcile:

```text
active reservations at cutoff
→ cancellations/no-shows
→ actual validated service count
```

**Falsifier:** records are unavailable or definitions/timestamps cannot be reconciled at service level.

## H-P1 — Raw reservation is imperfect

`active_reservations_at_cutoff` differs materially enough from actual served/validated demand that operators still need a buffer/correction.

**Falsifier:** reservation count is already operationally sufficient within accepted shortage/surplus tolerance.

## H-P2 — A simple correction beats raw reservation

A transparent correction based on historical show/no-show and unreserved demand improves decision loss over `Q = active reservations`.

**Falsifier:** simple correction does not improve out-of-sample decision utility.

## H-P3 — Contextual features add incremental value

Only after H-P2, campus/meal/calendar/menu context explains residual error.

**Falsifier:** contextual model does not beat the simple correction on held-out services.

## H-P4 — Better estimate changes a reachable decision

An operator can use the estimate to change at least one real action before its freeze point:

- production quantity;
- reserve/safety batch;
- campus allocation;
- package vs dining-hall mode;
- menu mix.

**Falsifier:** prediction arrives too late or no meaningful decision is adjustable.

---

# 2. Minimum dataset

One row per **service episode**:

```text
service_id
service_date
campus
meal_period
service_regime
reservation_required
reservation_cutoff_at
reservations_created
reservations_cancelled_before_cutoff
active_reservations_at_cutoff
uncancelled_no_show_count
unreserved_or_late_served_count
validated_served_count
planned_portions
produced_portions
edible_surplus_portions_or_kg
shortage_event
early_sellout_or_substitution
service_mode
accepted_service_record_source
```

Optional only after core reconciliation:

```text
menu_id
menu_class
academic_state
special_event
weather
historical_comparable_service_count
```

Do not request user IDs for Pilot 0.

---

# 3. Semantic checks before analysis

The dataset is **not usable** until all of these are resolved or explicitly marked unknown:

1. Does `reservation` mean created request or active request at cutoff?
2. Are cancellations timestamped before/after cutoff?
3. Does `validated_served_count` come from turnstile/QR, kitchen count or control record?
4. Can one person create multiple service events?
5. Are no-shows distinguishable from late collection?
6. Are unreserved diners allowed?
7. Does package delivery create a turnstile-free service event?
8. Are staff/student/guest channels combined?
9. Does `produced` include reserve/emergency batches?
10. Is surplus measured before reuse/donation/disposal?
11. Is `service_date` the production/service date rather than accounting date?

If a field cannot be reconciled, preserve `UNKNOWN` and do not fabricate it.

---

# 4. Pilot 0 — Retrospective event reconciliation

For each service episode calculate:

```text
show_count = active_reservations_at_cutoff - uncancelled_no_show_count

reservation_show_rate =
    show_count / active_reservations_at_cutoff

unreserved_share =
    unreserved_or_late_served_count / validated_served_count

reservation_error =
    active_reservations_at_cutoff - validated_served_count
```

Where denominators are zero, keep metric null rather than forcing zero.

### Outputs

- distribution of show rate;
- distribution of unreserved share;
- absolute/percentage reservation error;
- error by campus;
- error by meal period;
- error by service regime;
- anomaly log for services that cannot reconcile.

### Gate

Proceed only if enough service episodes have reliable event semantics to compare strategies.

---

# 5. Pilot 1 — Transparent reservation correction

Start with a correction that an operator can understand.

Example candidate:

```text
Q_simple =
    active_reservations_at_cutoff * historical_show_rate
    + historical_expected_unreserved_demand
```

Estimate parameters on training/history only.

Alternative robust form:

```text
Q_simple = median(
    realized_demand / active_reservations_at_cutoff
    for comparable historical services
) * active_reservations_at_cutoff
```

Never tune on the test period.

---

# 6. Decision metric — not only prediction error

Report MAE/RMSE for diagnostics, but the primary evaluation should reflect the actual action.

For candidate production quantity `Q` and realized demand `D`:

```text
surplus = max(Q - D, 0)
shortage = max(D - Q, 0)

DecisionLoss =
    C_excess * surplus
  + C_shortage * shortage
```

Before contract/economic validation:

- report results across a **sensitivity grid** of `C_shortage / C_excess` rather than inventing one ratio;
- separately report shortage frequency and maximum shortage;
- do not translate to TRY savings.

Recommended diagnostics:

```text
MAE
bias
mean surplus portions
mean shortage portions
P(shortage > 0)
P(shortage > guardrail)
90th/95th percentile absolute error
DecisionLoss across cost ratios
```

---

# 7. Pilot 2 — Contextual residual model

Only run if Pilot 1 leaves meaningful residual error.

Target residual rather than relearning reservation from scratch:

```text
residual = validated_served_count - Q_simple
```

Candidate features:

- campus;
- meal period;
- weekday;
- academic state;
- service regime;
- menu class / menu ID if available;
- special-event flag;
- recent show-rate drift.

Weather/mobility should enter only if they improve held-out decision utility.

### Baselines to beat

1. raw reservation;
2. global show-rate correction;
3. campus/meal-specific historical correction;
4. recent rolling correction.

No complex model is promoted unless it beats all relevant simple baselines out-of-sample.

---

# 8. Calibration and uncertainty

The operator may need a range rather than a point.

Possible output:

```text
recommended_quantity: 510
planning_band: 495–530
shortage_risk_at_510: 4%
known_missing_signal: menu_change
```

But call it a `planning_band` or `empirical prediction interval` only if the method supports that semantics.

Do not label an arbitrary ± percentage as confidence.

Calibration test:

- if a nominal 90% interval is produced, approximately 90% of held-out realized demand should fall inside it;
- report empirical coverage and interval width.

---

# 9. Service-mode decision extension

Historical Boğaziçi evidence shows reservation count can influence package-vs-hall service mode in a special regime.

If PMR confirms current service-mode discretion, define a separate decision test:

```text
state:
expected demand distribution
campus
meal period
staffing / service constraints

candidate actions:
open hall
package service
reduced service
normal service

outcomes:
food waste
labor/service cost
wait/service quality
shortage
```

Do not reuse the historical `<15` threshold as a current policy parameter.

The experiment should compare a current operator rule against an alternative decision rule only after current constraints are documented.

---

# 10. Prospective pilot — only after retrospective gates

A prospective pilot requires human approval and should not autonomously control production.

Recommended sequence:

```text
1. shadow mode
   system produces recommendation
   operator ignores it for operations
   compare afterward

2. advisory mode
   operator sees recommendation + reasons + uncertainty
   operator records accept/override + reason

3. bounded intervention
   only within agreed guardrails
   prospective measurement of surplus + shortage + service outcome
```

Never jump directly from retrospective model accuracy to autonomous production control.

---

# 11. Required decision record

For every advisory/intervention service:

```text
decision_id
service_id
created_at
information_cutoff_at
input_snapshot_ids
strategy_version
raw_reservation_count
simple_baseline
model_estimate_if_any
planning_band
recommended_action
operator_action
operator_override
operator_override_reason
actual_served
actual_surplus
shortage_event
accepted_service_record
verification_state
```

This is the core audit artifact for later KREATE claims.

---

# 12. Success gates

## Data gate

PASS only if:

- reservation and realized service can be reconciled at service level;
- timestamp/cutoff semantics are known;
- no PII is required for the core experiment.

## Decision-value gate

PASS only if:

- residual uncertainty is material;
- a strategy materially improves decision loss or an agreed operational metric over current/simple baseline;
- shortage guardrails do not degrade unacceptably.

## Workflow gate

PASS only if:

- an identified operator can receive the result before freeze time;
- at least one action is genuinely adjustable;
- override and outcome can be recorded.

## Product gate

PASS only if:

- current tools/reservation/manual process leave a meaningful gap;
- stakeholder pain/incentive is confirmed by PMR;
- the workflow is repeatable beyond a single exceptional service.

Failure at any gate means **change the control point or stop**, not add a larger model.

---

# 13. Agent ownership

### IE

Own decision owner, freeze time, service-mode authority, current heuristic, incentives and pilot permission.

### EE

Own physical measurement boundary: produced, served, surplus, shortage and waste-stage measurement feasibility.

### CS1

Own retrospective reconciliation, baselines, residual modeling, calibration and decision-loss evaluation.

### CS2

Own claim firewall, evidence promotion, application narrative and whether the result changes the beachhead thesis.

### Backend/data

Own event schema, stable service/decision IDs, provenance and separation of reservation/served/user-charge/contract-settled events.

### Frontend

Only after workflow validation: render one decision card with signal state, recommendation, risk, missing data, approve/override and verified outcome. Do not build a KPI wall as the pilot proof.
