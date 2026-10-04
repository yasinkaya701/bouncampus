# Pilot Measurement & Evidence Standard — 2026-10-04

**Purpose:** Define what a real food-production pilot would need to measure before BOUNCAMPUS can claim operational impact.  
**Status:** Research/evaluation design. **Not evidence that a pilot occurred.**

---

# Executive conclusion

The existing 14-day `CONTROL vs INTERVENTION` protocol is useful as a **hackathon promotion gate**, but the current `5 services/arm + 10% lower normalized waste` threshold must not be described as statistical or causal validation by itself.

A strong pilot needs four separate layers of evidence:

```text
measurement validity
    +
workflow/adoption validity
    +
decision-performance validity
    +
impact comparison
```

If any layer is weak, the result should be `INCONCLUSIVE`, not reframed as success.

---

# 1. Measurement comes before intervention claims

UNEP Food Waste Index 2024 emphasizes that food-waste measurement methods differ in strengths, limitations, scope and comparability, and provides food-service-specific measurement guidance.

Sources:

- https://www.unep.org/resources/publication/food-waste-index-report-2024
- https://wedocs.unep.org/handle/20.500.11822/45230

EPA similarly recommends a waste audit / baseline assessment and tracking the **amount, type and reason** for wasted food before selecting source-reduction interventions.

Sources:

- https://www.epa.gov/sustainable-management-food/resources-assessing-wasted-food
- https://www.epa.gov/sustainable-management-food/tools-preventing-and-diverting-wasted-food

### BOUNCAMPUS implication

Do not define `waste_kg` without a measurement boundary.

At minimum retain:

```text
measurement_stage
measurement_method
scale/device/process
edible_vs_inedible if available
liquid_handling rule
service scope
observed_at
collector/operator
quality flag
```

---

# 2. Separate the waste stages

For the production-planning hypothesis, the most causally relevant outcome is not necessarily total mixed food waste.

Target hierarchy:

## Primary addressable stage

```text
unserved edible surplus
```

This is closest to a production-quantity intervention.

## Secondary

```text
plate/post-consumer waste
```

This can be influenced by portion size, food quality, menu preference and student behavior and should not automatically be attributed to forecasting.

## Separate process metric

```text
preparation waste
```

This can be driven by trimming, cooking/process failures and recipe operations.

### Rule

Do not combine all three and state that a lower total was caused by a demand forecast unless the intervention pathway is documented.

---

# 3. Normalize by service volume

Raw waste per service is confounded by how many meals were served.

A reasonable primary normalized metric remains:

```text
waste_kg_per_100_served
    = waste_kg / served_portions * 100
```

For the production-specific thesis, prefer an additional stage-specific metric:

```text
edible_surplus_kg_per_100_served
```

and a portion-based decision metric:

```text
overproduction_portions
    = max(produced_portions - served_portions, 0)
```

### Important caveat

`produced - served` is not automatically waste:

- safe surplus might be reused/donated;
- some produced portions may remain serviceable;
- counting semantics may differ.

Keep physical disposition separate where possible.

---

# 4. Service quality is a co-primary guardrail

A waste-only objective can encourage underproduction.

Record at least:

```text
early_sellout
stockout_time
emergency_substitution
unmet_demand if measurable
service_delay
operator_override
```

The intervention should not be called better merely because less food remains if student service worsens.

Academic uncertainty-based university-dining research explicitly treats waste and shortage as opposing costs rather than optimizing waste alone.

Reference:
https://consensus.app/papers/preventing-food-waste-in-subsidybased-university-dining-faezirad-pooya/23aef70d39095db990688f4d358c5af9/

---

# 5. Match or adjust for service context

A simple before/after comparison can be badly confounded by:

- campus;
- weekday;
- meal period;
- academic phase;
- service availability;
- menu composition/popularity;
- special events;
- weather;
- exam/holiday periods;
- channel mix (dine-in/package);
- measurement-method changes.

### Preferred small-pilot structure

For a bounded operational test:

```text
CONTROL service
↔ matched INTERVENTION service
```

Match on the strongest known confounders first:

1. campus;
2. meal period/channel;
3. weekday/comparable term state;
4. service regime;
5. broad menu type;
6. major event/weather anomaly flag.

Do not overfit matching with too many dimensions when sample size is tiny; instead record residual differences and classify evidence quality.

---

# 6. Current 5-per-arm gate is a promotion gate, not statistical proof

The current repository protocol asks for at least five measured services per arm.

That is useful to prevent a one-day anecdote, but it is too small to imply a general causal effect without very large/stable effects and strong assumptions.

A 2025 scoping review of university food-waste interventions found only 27 studies directly measuring intervention changes and highlighted:

- inconsistent waste-measurement methods;
- different treatment of liquid/unavoidable food;
- short intervention durations;
- resulting difficulty comparing effects and judging persistence.

Reference:
https://consensus.app/papers/strategies-to-curb-food-waste-on-university-campuses-a-dyrbye-wright-stull/4c51cb380c0b5694a7ced9d030870590/

### Claim rule

With a small bounded pilot, safe language is:

> `promising preliminary operational evidence`

or:

> `the pre-registered pilot gate was met`

not:

> `BOUNCAMPUS is statistically proven to reduce university food waste by X%`.

---

# 7. Pre-register measurement before seeing outcomes

Before the first intervention service, freeze:

- primary KPI;
- stage definition of `waste_kg`;
- sellout/service guardrail;
- matching logic;
- inclusion/exclusion rules;
- handling of missing measurements;
- intervention policy version;
- model version;
- operator override recording;
- minimum evidence gate.

This prevents choosing metrics after seeing which one looks favorable.

---

# 8. Do not discard operator overrides

An override is product evidence.

Store:

```text
recommendation
operator_action
amount_changed
reason_code
free_text_note
actual_outcome
```

Potential reason codes:

- known event missing from model;
- expected group/visitor arrival;
- menu quality concern;
- contractor constraint;
- inventory constraint;
- food-safety rule;
- staff judgement;
- data stale/missing;
- service change;
- other.

### Why

Repeated override reasons reveal:

- missing features;
- policy constraints;
- trust problems;
- wrong intervention point.

A high override rate can invalidate workflow fit even if offline forecast error is good.

---

# 9. Direct weighing remains the strongest simple ground truth where feasible

EPA/UNEP measurement frameworks recognize direct measurement/weighing as a core method for food-only waste streams.

For one-service pilot instrumentation:

```text
container tare
+ calibrated scale
+ stage-separated bin/container
+ timestamp/service label
+ consistent liquid policy
```

is preferable to uncalibrated visual estimates if operationally feasible.

### TrayGate role

TrayGate can provide continuous, granular plate-level estimates, but a bounded validation set should still use physical weighing/ground truth to quantify error before its output replaces direct measurement.

---

# 10. Example evidence-quality levels

## Level 0 — demo only

- model recommendation shown;
- no real operation/outcome.

Allowed claim:

> prototype / scenario only.

## Level 1 — measurement feasibility

- real service measured consistently;
- no intervention.

Allowed claim:

> we established a service-level measurement process.

## Level 2 — preliminary matched pilot

- bounded control/intervention services;
- consistent measurement;
- operator action recorded;
- guardrails recorded.

Allowed claim:

> preliminary/pilot evidence under defined conditions.

## Level 3 — replicated operational pilot

- more services/time;
- repeated across menus/regimes;
- stable measurement;
- prespecified analysis;
- outcome persists.

Allowed claim:

> replicated operational evidence at this site.

## Level 4 — cross-site evidence

- repeated at multiple institutions/contracts;
- comparable definition and analysis.

Allowed claim:

> evidence of repeatability across target segment.

No level automatically supports a broad national effect percentage.

---

# 11. Carbon/water/money should be downstream conversions

First establish:

```text
measured physical food reduction
```

Then, if useful, calculate:

```text
physical reduction
× documented context-appropriate factor
= derived impact estimate
```

Store factor provenance and uncertainty.

### Monetary claims

Do not derive financial savings from average contract value / meal count unless the real marginal payment/cost semantics are established.

A unit-price procurement total is not the same as marginal cost of one avoided surplus portion.

---

# 12. Recommended pilot result table

For every matched service pair report:

| Field | Control | Intervention |
| --- | ---: | ---: |
| campus / meal / channel |  |  |
| service regime |  |  |
| produced portions |  |  |
| served portions |  |  |
| edible surplus kg |  |  |
| prep waste kg |  |  |
| plate waste kg |  |  |
| primary waste kg / 100 served |  |  |
| early sellout |  |  |
| substitution/delay |  |  |
| operator override |  |  |
| measurement quality |  |  |
| major confounder note |  |  |

Aggregate results should be accompanied by the individual service rows rather than only an average.

---

# 13. Interpretation categories

## PROMISING

- measurement comparable;
- prespecified primary outcome improves meaningfully;
- service guardrails do not worsen materially;
- operator can use the recommendation;
- no major confounder plausibly explains the whole effect.

## FAILED

- prespecified target missed;
- service quality worsened materially;
- recommendation routinely unusable;
- causal mechanism contradicted.

## INCONCLUSIVE

- too few services;
- mixed measurement method;
- poor matching;
- major regime/event confounding;
- missing served/surplus/sellout data;
- effect inconsistent and uncertainty too high.

`INCONCLUSIVE` must remain a valid outcome.

---

# 14. Application implication

Before a pilot, the strongest credible statement is:

> **We have pre-defined what data, guardrails and failure conditions would be required to prove or reject the intervention.**

That is stronger than presenting scenario savings as if they have already been achieved.
