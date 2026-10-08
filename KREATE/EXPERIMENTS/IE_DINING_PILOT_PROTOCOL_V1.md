# IE Dining Pilot Protocol v1 — Waste, Service, and Decision Utility

**Owner:** IE — Customer Discovery & Market  
**Date:** 2026-10-06  
**Status:** pre-registration / operating protocol; no measured pilot result is claimed.

## Purpose

Define the minimum IE-valid pilot needed to test whether a human-reviewed production/allocation recommendation improves an upstream food-waste outcome **without worsening service**.

This protocol complements the CS1 decision-intelligence pre-registration. It focuses on:
- causal/operational comparability;
- KPI definitions;
- asymmetric service guardrails;
- buyer/value evidence;
- stop/modify rules.

It does not authorize automatic kitchen dispatch.

## Pilot entry gates

Do not begin an intervention pilot until all are true:

1. **Control point verified** — a real actor can change/approve a relevant quantity before a known freeze point.
2. **Outcome semantics verified** — produced, served/passages, surplus/waste and sellout fields are defined by source owners.
3. **Baseline captured prospectively** — operator/status-quo quantity is recorded before the service.
4. **Measurement boundary fixed** — waste stage(s), weighing method and exclusions are defined before outcomes are seen.
5. **Guardrails agreed** — early sellout, emergency substitution, food safety, quality and capacity constraints are explicit.
6. **Human approval retained** — every recommendation can be accepted, modified or rejected by the authorized operator.
7. **No hidden future information** — intervention inputs must exist by the real decision cutoff.

If any gate fails, remain in observation / shadow mode.

## Pilot phases

### Phase 0 — observational reconstruction

Goal: validate data semantics before comparing methods.

For at least several chronological services, collect:
- operator planned quantity;
- produced quantity;
- reported served/passages;
- edible surplus;
- other waste stages if measured;
- sellout/substitution events;
- relevant decision-time inputs;
- timestamps and source IDs.

No recommendation changes operations.

### Phase 1 — shadow recommendation

Generate a recommendation before freeze, but do not alter operations.

Compare:
- operator quantity;
- simple baseline;
- model/policy recommendation;
- realized outcome.

Goal: detect semantic errors, impossible constraints, instability and poor risk calibration before intervention.

### Phase 2 — bounded human-reviewed intervention

Only after Phases 0–1 are acceptable.

The authorized operator sees:
- baseline;
- recommendation/range;
- reason codes;
- known missing data;
- declared risk scenario;
- binding constraints.

The operator may:
- accept;
- modify;
- reject.

The final action and reason are recorded.

## Unit of analysis

Default unit:

```text
campus × meal_period × service_date
```

If production is centrally decided and later allocated, preserve both levels:

```text
central production decision
→ campus/service allocation
→ service outcome
```

Do not duplicate one central decision into multiple independent observations without accounting for shared treatment.

## Required fields

### Identification / timing
- `service_id`
- `service_date`
- `campus_id`
- `meal_period`
- `decision_cutoff_at`
- `recommendation_generated_at`
- `operator_action_at`

### Decision quantities
- `operator_baseline_quantity`
- `recommended_quantity` or range
- `operator_final_quantity`
- `produced_portions`

### Outcome
- source-defined served/passage count
- `actual_surplus_portions` when accepted
- stage-specific `waste_kg`
- `shortage_or_early_sellout`
- substitution / emergency-prep flag
- service delay where measurable
- accepted/reconciled outcome flag

### Decision audit
- model/policy version
- risk scenario / admitted cost inputs
- input snapshot IDs
- operator override
- override reason
- missing-data/readiness reason
- source record IDs

### Measurement provenance
- measurement method
- scale/device/manual source
- tare / calibration status where relevant
- measurement timestamp
- responsible role
- exclusions

## Primary KPI

Use a **stage-specific upstream waste** outcome whenever the measurement supports it.

Preferred form:

```text
edible_surplus_kg_per_100_served_meals
= 100 × edible_surplus_kg / served_meals
```

If only portions are valid:

```text
surplus_portions_per_100_served
= 100 × surplus_portions / served_meals
```

Do not mix:
- preparation loss;
- edible unserved surplus;
- plate waste;
- disposal after food-safety expiry

into one causal metric unless the measurement protocol explicitly requires a combined total and the intervention plausibly affects all included stages.

## Service guardrails

A waste reduction result is not acceptable if it is purchased by materially worse service.

Track at minimum:

1. early-sellout incidence;
2. unmet demand / rejected diners where measurable;
3. emergency substitution incidence;
4. emergency additional production / replenishment;
5. service delay;
6. operator-reported unacceptable service risk;
7. food-safety / quality nonconformance.

### Hard rule

Any food-safety or legally binding contract requirement remains a hard constraint. The experiment does not trade it for lower waste.

## Secondary decision KPIs

- absolute quantity error;
- signed quantity error;
- excess portions per 100 served;
- shortage portions per 100 served;
- asymmetric decision loss using evidence-backed or clearly labeled scenario costs;
- operator override rate;
- `WITHHOLD` rate;
- recommendation lead time before freeze.

## Buyer / adoption KPIs

These are process measurements, not PMF proof:

- minutes spent preparing/approving the quantity decision;
- number of systems/manual handoffs;
- override reason distribution;
- number of required approvals;
- data-preparation burden;
- pilot approval time;
- stakeholder willing to sponsor the next test;
- procurement path identified.

A positive pilot does not by itself establish willingness to pay.

## Design

### Preferred: matched / blocked comparison

Match or block services using factors known **before treatment**, such as:
- campus;
- meal period;
- weekday;
- academic-calendar phase;
- service type;
- menu family / coarse complexity class if pre-registered;
- expected demand regime from the same information set used operationally.

Do not construct pairs after seeing waste outcomes.

### Treatment assignment

If operationally feasible:
- randomize within pre-declared blocks; or
- alternate intervention/control using a pre-declared schedule that operators cannot selectively change after seeing expected demand.

If randomization is infeasible, document the quasi-experimental assignment and likely confounders.

### Control

The control arm should use the real status-quo decision process.

Do not replace it with an intentionally weak naive baseline and call the result operational impact.

## Existing repository minimum vs inference strength

The current CS1 pilot scorecard can mechanically classify a pilot only after at least **5 valid services per arm**.

IE interpretation rule:

> 5 per arm is a **minimum computational / feasibility gate**, not enough on its own for a strong causal or generalized impact claim.

For effect estimation:
- report sample size;
- report paired/unpaired design;
- report effect size and uncertainty;
- avoid significance language when the design is underpowered;
- perform power/sample-size planning once real baseline variance is observed;
- never tune the success threshold after seeing outcomes.

## Analysis

### Primary effect

For normalized upstream waste:

```text
relative_change =
(mean_intervention - mean_control) / mean_control
```

Also report the absolute difference in the native metric.

For matched pairs, prioritize paired differences:

```text
delta_i = intervention_i - matched_control_i
```

Report:
- mean/median paired difference;
- uncertainty interval where justified;
- full distribution / outliers;
- guardrail differences.

### Decision utility

If valid `C_over` and `C_under` exist:

```text
L_i =
C_over * max(q_i - D_i, 0)
+ C_under * max(D_i - q_i, 0)
```

Compare intervention policy to operator/control policy on the same admitted service semantics.

If costs are only scenarios, label all resulting values `SCENARIO_DECISION_LOSS`.

## Pre-registered interpretation

### PROMISING FEASIBILITY
Allowed only when:
- measurement validation passes;
- no duplicate service rows remain;
- intervention recommendations were generated before cutoff;
- operator baseline was captured prospectively;
- at least the repository mechanical minimum per arm is met;
- normalized upstream waste moves in the intended direction;
- early-sellout/service guardrails do not worsen materially;
- no food-safety issue is introduced.

This label means only that a larger/better pilot is warranted.

### MODIFY
Use when:
- waste decreases but shortages/substitutions increase;
- operator overrides are frequent for a coherent reason;
- the relevant decision occurs at another level/time;
- the measured waste stage is not the one affected by quantity;
- data quality is insufficient for attribution;
- product integration burden dominates operational value.

### KILL / PAUSE
Use when:
- no material addressable upstream waste is observed;
- no safe quantity adjustment window exists;
- control/status-quo is already as good or better on decision utility;
- service guardrails fail;
- causal measurement cannot be made credible enough for the intended claim.

## Claim firewall

### Safe after a valid small pilot

Examples:
- “In this bounded pilot, the intervention arm had lower measured edible surplus per 100 served meals, with no observed increase in early sellout under the registered guardrail.”
- “The result is preliminary and limited to the observed services.”

Only say this if the corresponding data actually exist and pass validation.

### Unsafe

- “We reduce campus food waste by X%” from a tiny or uncontrolled sample.
- “We save Y TL” without evidence-backed unit economics.
- “The model prevents overproduction” when waste stage/causality is not measured.
- “No service impact” when unmet demand was not observable.
- “Statistically significant” without an appropriate analysis/design.

## Evidence package

A promotable pilot package should include:

1. protocol version;
2. raw immutable service rows or provenance-preserving reference;
3. data dictionary;
4. treatment-assignment rule;
5. operator baseline capture;
6. recommendation logs;
7. override logs;
8. waste measurement provenance;
9. guardrail outcomes;
10. analysis script/version;
11. exclusions with reasons;
12. result summary;
13. limitations;
14. human reviewer / evidence attestation where required.

## Cross-role ownership

### IE
- control point and buyer/persona validation;
- status-quo workflow;
- incentive/cost semantics;
- pilot design and operational acceptance;
- interpretation / claims boundary.

### CS1
- leakage-safe forecast/baseline generation;
- decision-policy implementation;
- reproducible analysis;
- recommendation logging.

### EE
- stage-specific measurement validity;
- calibration/uncertainty;
- physical measurement protocol where required.

### EHB
- device/firmware only if a proven measurement gap requires it.

### CS2
- application wording must reflect the actual evidence class and limitations.

## Dependencies

- #292 — reconciled service truth.
- #358 — contract / hakediş / incentive semantics.
- Real PMR — decision owner, freeze point, current workflow, guardrails.
- Measurement owner — valid waste-stage definition.

## Result

**NOT RUN.**

No service-level intervention result, savings, waste reduction, model lift, buyer adoption, or climate impact is created by this protocol.
