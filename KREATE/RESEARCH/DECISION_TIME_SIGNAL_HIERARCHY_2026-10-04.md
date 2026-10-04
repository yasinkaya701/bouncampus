# Decision-Time Signal Hierarchy — 2026-10-04

**Purpose:** determine which signals should be treated as required, optional or unavailable at the real production-decision cutoff.  
**Status:** research synthesis. **No signal weight or mandatory-backbone rule is validated on Boğaziçi measured demand data.**

## Executive conclusion

The current repository policy treats course schedule as a required backbone and uses fixed signal weights such as schedule/weather/menu/calendar.

Research does **not** support making `course schedule` a universal hard dependency across the beachhead.

Different institutional dining workflows have different strongest pre-service signals:

```text
no-reservation site
    -> recent demand + calendar/service regime + menu/context

reservation-first site
    -> reservation count + no-show/walk-in behavior

card/turnstile mature site
    -> historical realized demand + academic/service regime

joint contractor/university site
    -> current operator plan + client/context signals + contract cutoff
```

Therefore readiness should eventually be **segment/source-contract specific**, not based on one globally required schedule feature.

---

# 1. Academic calendar is strongly public and temporally well-defined

Boğaziçi's official Academic Calendar provides dated term events and historical/current academic-year views.

Official source:
https://akademiktakvim.bogazici.edu.tr/

Useful states include:

- teaching term;
- add/drop;
- exams;
- holidays;
- summer periods;
- registration/administrative transitions.

### Modeling implication

Academic state is a robust candidate context feature because it is:

- known before the service;
- institutionally authoritative;
- historically dateable.

Its incremental value still needs measured target data.

---

# 2. Course schedule is plausible, but a universal mandatory backbone is not established

Academic literature supports calendar/schedule-related temporal patterns in institutional demand, and current Boğaziçi registration systems expose course scheduling operationally.

However, current research has **not** established that:

- course-by-course schedule density is the dominant driver of meal demand;
- a stable historical schedule export is available through a supported institutional interface;
- schedule improves forecast utility after recent demand and service regime are known;
- schedule should override stronger local signals such as reservations;
- absence of schedule should always force `WITHHOLD`.

### Product consequence

`course_schedule_available = false` should not automatically mean `no useful recommendation` for every future segment.

---

# 3. Reservation-first sites have a stronger direct intent signal

Amasya University explicitly uses meal reservations to determine total meal count and reduce waste.

Evidence:
- `E-PUB-022`;
- `E-PUB-024`.

At such a site, a reasonable signal order to test is:

```text
1. reservations available at decision cutoff
2. historical show/no-show conversion
3. expected walk-ins
4. recent demand
5. service/academic regime
6. menu/context
7. weather/mobility if incremental
```

Making course schedule mandatory would be difficult to justify without measured incremental benefit.

---

# 4. Historical realized demand is a high-priority baseline signal

Academic studies of institutional/university dining repeatedly find strong value in:

- recent historical demand;
- weekly cycles;
- academic calendar;
- turnstile/served counts.

Current literature reviewed in:
`ACADEMIC_DEMAND_MODELING_EVIDENCE_2026-10-04.md`.

### Product consequence

The first question should be:

> What is the strongest direct observed demand signal available **before** this decision?

not:

> Do we have every contextual feature configured in the demo?

---

# 5. Current operator plan is itself a critical input/baseline

A recommendation should not ignore the operator's existing planned quantity.

Minimum decision record:

```text
operator_current_plan
operator_current_method
system_recommendation
system_delta_vs_plan
operator_action
operator_reason
actual_outcome
```

### Why

The real product value is often:

```text
improvement over current plan
```

rather than absolute demand prediction.

If the system cannot beat or materially improve the operator's plan, it adds little value even with a good MAE.

---

# 6. Menu features are plausible but should not be assigned fixed universal weight

University-refectory literature supports meal ingredients/menu composition as candidate predictive features.

Boğaziçi also has a reproducible public menu archive.

But:

- exact menu impact can vary by population;
- menu popularity is not the same as an LLM-generated semantic score;
- vote/tasting history is not publicly available as a time series;
- menu may affect both attendance and plate waste through different mechanisms.

### Rule

Use menu as a feature family to test, not a guaranteed `20% signal`.

---

# 7. Weather should be decision-time forecast, not realized weather

Weather can plausibly affect campus mobility/attendance, and academic studies report temperature/context associations.

But the correct feature is:

```text
weather_forecast_snapshot_available_at_decision_time
```

not:

```text
actual weather observed later
```

otherwise evaluation leaks future information.

Weather should remain optional until it improves out-of-time decision utility.

---

# 8. Campus mobility/occupancy can be valuable but creates burden

Academic campus studies support mobility/density as candidate context.

Possible institutional signals:

- aggregate access counts;
- shuttle arrivals;
- room/teaching activity;
- event attendance;
- Wi-Fi/occupancy aggregates.

### Boundary

The value must exceed:

- privacy/security burden;
- integration cost;
- semantics risk;
- maintenance burden.

Do not build a sensor network to gain a marginal feature before testing simpler sources.

---

# 9. Proposed segment-specific readiness contract

Instead of:

```text
schedule is required
+ fixed weights
```

future measured policy should move toward:

```text
segment_profile
required_source_set
optional_source_set
minimum direct-demand evidence
source freshness
source semantics quality
operator-plan availability
```

Example:

## Profile N — non-reservation dining

Required candidate set to validate:

```text
recent comparable demand
service regime
academic state
```

Optional:

```text
menu
weather
schedule density
mobility
```

## Profile R — reservation dining

Required candidate set:

```text
reservation snapshot before cutoff
historical show/no-show behavior
service regime
```

Optional:

```text
calendar
menu
weather
mobility
```

## Profile O — operator-plan augmentation

Required:

```text
operator current plan
recent realized demand
service regime
```

Optional:

```text
all incremental context
```

---

# 10. Recommended readiness logic after measured data exist

A signal should become `required` only if one of these is true:

1. operational policy requires it;
2. without it the decision is unsafe;
3. measured ablation shows recommendations become materially worse/unreliable without it;
4. it is necessary to interpret another source correctly.

Not because:

- the demo was originally designed around it;
- the team assigned it a high heuristic weight;
- it makes the architecture look more intelligent.

---

# 11. Application copy consequence

Do not submit as validated technology:

> Course schedules are 50% of demand and weather/menu/calendar have learned weights of 20/20/10.

Safe:

> The current prototype uses transparent policy heuristics to demonstrate how campus context can affect readiness and planning bands. The final source hierarchy and weights will be calibrated only after real service-level data and decision timing are validated.

Stronger after PMR:

> At this site, the production decision occurs at X and the operator currently uses A/B. Our pilot will test whether C adds incremental value before that cutoff.

---

# 12. Current CS1 research implication

Keep:

- abstention / WITHHOLD capability;
- source health;
- decision-time timestamps;
- provenance;
- baseline comparisons;
- operator approval.

Modify later if product policy is promoted:

- universal schedule hard dependency;
- fixed source weights;
- one source contract across all university workflows.

---

## Current conclusion

The best signal is not the most sophisticated one.

It is the signal that is:

```text
available before the decision
+ semantically valid
+ low-friction to obtain
+ measurably improves the decision
```

The source hierarchy must follow the customer workflow, not precede it.
