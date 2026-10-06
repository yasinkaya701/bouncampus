# IE Dining Decision Economics v1 — Pre-Registered Operating Model

**Owner:** IE — Customer Discovery & Market  
**Date:** 2026-10-06  
**Evidence class:** repository framework / pre-registration only  
**Current result:** NOT RUN on measured Boğaziçi service economics.

## Question

Can a human-reviewed meal-production decision be framed so that it explicitly trades off surplus and shortage consequences, respects real operational constraints, and produces a recommendation that is more useful than a point forecast alone?

This experiment does **not** assume:
- that Boğaziçi overproduces;
- that demand mismatch is the dominant waste cause;
- that unit costs are known;
- that the university rather than the contractor bears the economic consequence;
- that the classical newsvendor model exactly matches operations.

Those are PMR / contract / measurement questions.

## Decision variable

For one service:

- `D`: realized service demand under an admitted semantic definition;
- `q`: production / allocation quantity that the identified decision owner can actually choose before the verified freeze point.

If multiple decisions exist, model them separately:

```text
q_total
→ q_campus
→ q_meal_period
→ q_batch / replenishment
```

Do not collapse all stages into one variable until PMR proves they share the same owner and freeze point.

## Core asymmetric loss

For an admissible single-period decision:

```text
L(q, D) =
    C_over  * max(q - D, 0)
  + C_under * max(D - q, 0)
  + C_override
  + C_guardrail
```

Where:

- `C_over` is the marginal evidence-backed consequence of one excess portion;
- `C_under` is the marginal evidence-backed consequence of one unmet portion;
- `C_override` is optional and only used if operator override burden is actually measured;
- `C_guardrail` represents hard or soft penalties for violating service, capacity, quality or safety constraints.

### Evidence requirements

A numeric `C_over` or `C_under` may be admitted only when its provenance is explicit.

Allowed examples:
- authoritative unit-price / contract term with correct settlement semantics;
- measured ingredient / disposal / emergency-prep marginal cost from the responsible owner;
- explicit contractual penalty;
- documented operational consequence converted to a cost only with owner-approved logic.

Disallowed examples:
- contract value divided by listed meals;
- assumed “average meal cost”;
- literature cost copied into Boğaziçi;
- arbitrary shortage penalty chosen to make a model look good;
- sustainability value monetized without a declared method.

## Classical newsvendor benchmark

If all of the following approximately hold:
1. one quantity must be chosen before demand is realized;
2. overage and underage consequences are approximately linear at the margin;
3. demand distribution is estimated without future leakage;
4. no later action materially changes the decision;

then the classical critical fractile provides a transparent benchmark:

```text
alpha* = C_under / (C_under + C_over)
q*     = F_D^{-1}(alpha*)
```

This is useful because it exposes the policy trade-off directly.

It is not automatically the production policy.

## When the benchmark is invalid or incomplete

Use a richer constrained model if PMR shows:
- multiple batches can be produced;
- campus allocation can change after total production freezes;
- substitute menus provide recourse;
- demand is censored by sellout;
- minimum contractual quantities exist;
- capacity is menu-dependent;
- second meals / package meals have separate settlement;
- shortage cost is nonlinear;
- food-safety discard creates hard time constraints;
- service demand is not observable from the available record.

## Constraint contract

The admissible set `Q` should be documented from real operations.

Candidate constraints, all UNKNOWN until verified:

```text
q_min ≤ q ≤ q_max
q ∈ batch_size multiples
sum_campus q_campus ≤ central_kitchen_capacity
q_campus ≤ local_holding_capacity
q must be finalized by freeze_time
reallocation after dispatch may be limited
food-safety / holding-time rules remain hard constraints
```

No constraint is considered verified merely because it appears operationally plausible.

## Scenario mode before economics are known

Until real `C_over` and `C_under` are available, compute **sensitivity scenarios**, not “optimal savings.”

Recommended scenario grid:

| Scenario | Underage:Overage ratio | Interpretation |
| --- | ---: | --- |
| S1 | 1:1 | symmetric reference only |
| S2 | 2:1 | moderate shortage aversion |
| S3 | 4:1 | strong shortage aversion |
| S4 | 8:1 | extreme shortage aversion stress test |

These ratios are not local estimates. They reveal how sensitive a quantity recommendation is to risk preference.

If the recommended quantity changes dramatically across plausible ratios, the economics are decision-critical and PMR must resolve them before deployment.

## Operator baseline

Every evaluation must compare against the quantity decision actually used today, captured **before** the service when possible.

Minimum comparison set:

1. operator/status-quo quantity;
2. simple historical baseline;
3. model point estimate;
4. asymmetric-loss recommendation under declared scenario(s).

The model is not useful if a simpler or operator baseline has equal or lower admitted decision loss.

## Censored-demand warning

If food sells out, the observed served count may be lower than latent demand.

Therefore:

```text
served_count != unconstrained_demand
```

when early sellout or rejection occurs.

A benchmark must preserve:
- sellout flag;
- time of sellout when available;
- substitute/emergency service;
- rejected/unserved demand if measurable.

Do not train a model to treat sellout-censored demand as exact latent demand.

## Reconciliation boundary

BUCard / turnstile / QR / transaction counts are not `D` until the source owner establishes:
- accepted passage-to-meal semantics;
- duplicate/retry behavior;
- refunds/reversals/corrections;
- second-meal handling;
- package-meal semantics;
- finalization timing.

Issue #292 is the active truth-acquisition dependency.

## Recommendation output schema

Every IE-compatible decision artifact should include:

```json
{
  "service_id": "...",
  "decision_cutoff_at": "...",
  "decision_owner_role": "...",
  "baseline_quantity": null,
  "model_point_estimate": null,
  "risk_scenario": {
    "c_under": null,
    "c_over": null,
    "source": "UNKNOWN_OR_SCENARIO"
  },
  "recommended_quantity": null,
  "recommended_range": null,
  "binding_constraints": [],
  "readiness": "WITHHOLD",
  "reason_codes": [],
  "human_approval_required": true,
  "operator_action": null,
  "override_reason": null,
  "input_snapshot_ids": []
}
```

A null field is preferable to fabricated precision.

## Readiness states

### WITHHOLD
Use when any required decision semantics are missing, for example:
- no verified quantity owner;
- no verified freeze point;
- source data are unreconciled;
- demand estimate is invalid;
- the recommendation violates a hard operational constraint.

### REVIEW_REQUIRED
Use when a scenario recommendation can be inspected safely but economics / uncertainty / constraints remain partially unresolved.

### PILOT_READY
Use only when:
- owner and freeze point are verified;
- required data are admitted;
- constraints are documented;
- the recommendation is human-reviewed;
- a pilot protocol and guardrails are approved.

`PILOT_READY` is not a claim of product-market fit or measured impact.

## Economic-buyer sensitivity

The same decision can create value for different actors depending on settlement.

For every admitted cost element, attach:

```text
cost bearer
beneficiary if avoided
authority to change q
authority to buy
source / artifact
validity period
```

If the beneficiary and buyer differ, record the mechanism required to transfer value (contract requirement, shared KPI, procurement clause, service-level incentive, etc.).

## Offline evaluation metrics

### Forecast metrics
- MAE
- RMSE
- WAPE
- signed bias

### Decision metrics
- average asymmetric decision loss
- excess portions / 100 served
- shortage portions / 100 served
- early-sellout incidence
- emergency-substitution incidence
- decision regret versus best admitted benchmark, when calculable

### Process metrics
- operator override rate
- override reason distribution
- recommendation lead time before freeze
- missing-data / WITHHOLD rate

Forecast improvement without decision-loss improvement is not sufficient.

## Pre-registered comparisons

For chronological measured data, evaluate:

```text
operator baseline
vs simple historical baseline
vs model point estimate translated through the same policy
vs asymmetric-loss recommendation
```

All alternatives must use information available by the same decision cutoff.

Do not give richer models later information.

## Success condition

This IE model is useful enough to keep if:

1. a real controllable quantity and freeze point are verified;
2. admitted over/under consequences can be represented transparently;
3. the policy can abstain under missing semantics;
4. it can reproduce operator constraints;
5. measured evaluation shows lower decision loss or a materially better waste/service trade-off than credible simpler baselines;
6. operators can understand and override it safely.

## Modify condition

Modify the formulation if:
- there are sequential/replenishment decisions;
- campus allocation matters more than total production;
- waste-stage causality points away from pre-service quantity;
- settlement makes the economic objective misaligned with the actor who controls quantity;
- service quality or food-safety constraints dominate the numeric cost model.

## Kill condition

Kill the current quantity-decision wedge if credible primary evidence shows:
- no reachable quantity control point;
- production mismatch is immaterial to addressable waste;
- current process already dominates proposed decision support with no meaningful gap;
- required truth data cannot be obtained or prospectively measured;
- safe intervention cannot be tested without unacceptable service risk.

## Dependencies

- #292 — service-count and operational truth semantics.
- #358 — contract / unit-price / hakediş / change-right semantics.
- IE PMR interviews — quantity owner, freeze point, incidents, buyer/incentive chain.
- CS1 — leakage-safe forecasting and reproducible baseline infrastructure.
- EE — stage-specific waste measurement only when existing records are insufficient.

## Result

**NOT RUN.**

No local cost ratio, optimal quantity, savings estimate, measured decision-loss improvement, or buyer value is registered by this document.
