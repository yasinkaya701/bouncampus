# CS2 Pilot & Evidence Gate — Current-Master Recut

**Date:** 2026-10-06  
**Owner:** CS2 with CS1/IE/EE handoff  
**Status:** proposed operating protocol. It is not evidence that a pilot has occurred.

## Goal

Move from repository sophistication to a falsifiable operational test without overstating data access, semantic certainty, model performance, or impact.

The pilot ladder is deliberately conservative:

```text
admitted source truth
→ transparent baseline
→ shadow recommendation
→ advisory recommendation with human approval
→ bounded intervention
→ prospective measurement
→ evidence review
```

Skipping a stage requires stronger evidence, not enthusiasm.

## Stage 0 — Evidence admission

Before model comparison:

- identify the decision owner;
- identify the freeze/cutoff time;
- define the target quantity and unit;
- identify the source owner;
- obtain an aggregate export or measurement artifact;
- record provenance and version/time scope;
- verify or explicitly leave unverified the mapping to operational truth;
- document missingness, reversals, exclusions, and correction policy;
- separate generated/sandbox data from measured service data.

**Fail closed** if the target semantics are uncertain.

## Stage 1 — Cheapest transparent baseline

Evaluate the simplest policy that matches available information at decision time.

Examples may include:

- recent historical average;
- same-weekday historical average;
- reservation count as an intent-only baseline;
- historical show-rate correction;
- operator's existing plan when it can be captured prospectively.

Rules:

- no future leakage;
- common support for candidate comparisons;
- explicit exclusions;
- target and cutoff fixed before evaluation;
- no business-impact language attached to arbitrary loss weights.

A complex model earns promotion only if it beats the transparent baseline on a decision-relevant metric with reproducible evidence.

## Stage 2 — Shadow mode

The system produces recommendations but operators do not see them before the normal decision is locked.

Record:

```text
operator_baseline
system_recommendation
uncertainty_or_range
actual_measured_outcome
surplus_or_shortage
data_quality_flags
```

Purpose:

- test timing and coverage;
- detect leakage;
- evaluate abstention;
- test calibration/uncertainty behavior;
- identify failure regimes;
- avoid changing operations before the measurement chain is trusted.

Shadow success is not waste-reduction evidence.

## Stage 3 — Advisory mode

The recommendation becomes visible, but execution still requires an accountable human decision.

Record separately:

```text
operator_initial_plan
system_recommendation
operator_final_action
override_reason
execution_confirmation
```

Never overwrite the operator baseline with the final approved action.

The product must support:

- approve;
- edit;
- hold/abstain.

Automatic kitchen dispatch remains out of scope unless a later explicitly approved product decision changes that boundary.

## Stage 4 — Bounded intervention

A real intervention may begin only after:

- Stage 0 source semantics are adequate;
- baseline comparison is reproducible;
- recommendation arrives before freeze;
- operator workflow accepts the advisory step;
- measurement can capture both surplus and shortage/service risk;
- assignment/comparison design is predeclared;
- exclusion rules are predeclared;
- override handling is predeclared;
- safety/service guardrails are explicit.

## Measurement contract

At minimum, each evaluated service should capture:

```text
date
campus_or_service_location
meal_or_service_class
decision_cutoff
operator_initial_plan
system_recommendation
final_approved_quantity
produced_or_dispatched_quantity
accepted_or_served_outcome   # only with verified semantics
unserved_surplus
waste_measurement
shortage_or_sellout_event
override_reason
source_quality_flags
measurement_quality_flags
assignment_or_phase
```

If a field is not available, record it as unavailable rather than inferring it from a nearby proxy.

## Primary evaluation questions

The pilot must answer, in this order:

1. Is there a reachable decision before freeze?
2. Is measured outcome truth trustworthy enough?
3. Does the transparent baseline improve on current practice?
4. Does the model improve on the transparent baseline?
5. Does the recommendation fit the operator workflow?
6. Does bounded intervention improve the target operational outcome without unacceptable shortage/service harm?
7. Is the effect repeatable enough to justify broader product claims?

## Guardrails

Do not optimize only surplus/waste.

Track service risk such as:

- shortage;
- early sellout;
- unmet demand;
- emergency replenishment;
- operator override;
- abnormal service regime;
- missing/low-quality measurement.

A recommendation that lowers surplus by creating unacceptable shortages is not a successful product outcome.

## Causal and reporting discipline

Before presenting an intervention result:

- distinguish control/shadow/intervention periods;
- record assignment logic;
- check menu/calendar/service-regime imbalance;
- keep overrides in the analysis;
- disclose exclusions;
- disclose missingness;
- separate pre-consumer surplus from preparation/plate waste when possible;
- avoid treating a small feasibility sample as a powered causal study.

A pre-registered target such as a desired waste-reduction threshold is a target, not a result.

## Evidence promotion

A result may move into application/product claims only after:

1. source artifacts are admitted;
2. semantics are verified or limitations are explicit;
3. evaluation code/configuration is reproducible;
4. measured rows are distinct from sandbox/generated rows;
5. result scope is narrow and traceable;
6. CS2 claim wording matches the actual evidence class;
7. required human evidence attestation is completed when the repository policy requires it.

## Stop / modify conditions

Stop or modify the pilot if:

- source truth cannot be reconciled;
- recommendation systematically arrives after freeze;
- operator cannot act on the recommendation;
- measurement quality is inadequate;
- the dominant waste mechanism is outside the decision;
- model complexity does not beat the transparent baseline;
- service-risk guardrails fail;
- data acquisition requires unjustified person-level tracking;
- the workflow has no credible user/beneficiary incentive.

## Cross-role acceptance

**IE:** confirms real workflow, user, pain, authority, workaround, and incentive evidence.  
**EE/EHB:** confirms physical measurement truth when relevant.  
**CS1:** confirms data admission, target semantics, baseline/model evaluation, abstention and recommendation behavior.  
**CS2:** confirms claim scope, product gate, pilot narrative, evidence provenance and KEEP/MODIFY/KILL decision.

No single role may promote a measured impact claim by itself.
