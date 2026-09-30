# Food-Waste Pilot Protocol Red Team — Causal & Measurement Addendum

**Research date:** 2026-10-01  
**Purpose:** Red-team the existing [`docs/food-waste-pilot-protocol.md`](../../docs/food-waste-pilot-protocol.md) before any real field test, using the accumulated Boğaziçi research and institutional-food-waste literature.  
**Status:** Research/methodology addendum. **Does not change the current protocol by itself.** Human/domain owner must update the execution protocol before a real pilot.

---

# 0. Executive conclusion

The existing protocol is directionally strong because it already has:

- control vs intervention;
- human approval;
- measured waste rather than model-estimated impact;
- normalized waste KPI;
- early-sellout guardrail;
- override tracking;
- claim firewall.

But it should **not yet be interpreted as a statistically validated experimental design**.

Highest-risk issues:

1. `5 services per arm` and `10% reduction` are policy targets, not power calculations.
2. Running control first and intervention later can confound intervention with time/menu/calendar changes.
3. `served_portions` becomes a **censored demand proxy** when a service sells out.
4. One `early_sellout` boolean is too weak to quantify service harm.
5. Waste needs a production-relevant boundary: unserved surplus vs preparation vs plate waste.
6. Operator overrides create treatment-adherence questions; they should not be silently excluded.
7. Menu composition changes kg/meal even with identical operational quality.
8. Missing/exclusion rules should be predeclared.
9. Measurement reliability itself needs a gate.

The pilot can still remain lightweight. The fix is not “do a giant RCT”; it is to avoid causal claims the design cannot support.

---

# 1. What the existing protocol gets right

## RT-01 — Service is the unit of analysis

The protocol explicitly uses one dining service rather than one student as the unit. That aligns well with the operational intervention, which changes production quantity at service level.

Keep this.

## RT-02 — Human review is preserved

The intervention is operator-reviewed decision support, not autonomous kitchen control.

Keep this as a safety and workflow requirement.

## RT-03 — Waste is measured physically

The protocol does not promote forecast output into impact. It requires actual waste/surplus measurement.

Keep this claim boundary.

## RT-04 — Control and intervention use the same field set

This is necessary for comparable measurement.

Keep, but strengthen measurement-quality checks below.

---

# 2. Fixed sample size is not statistical power

## RT-05 — `5 measured services per arm` is a minimum evidence heuristic

The current protocol says five measured services per arm are required and uses a 10% lower mean waste threshold.

That may be a useful hackathon/pilot **policy heuristic**, but it is not enough to infer a statistically reliable effect without baseline variance, pairing structure and expected effect size.

### Required relabeling before real pilot

```text
MIN_SERVICES_PER_ARM = PILOT_FEASIBILITY_FLOOR
TARGET_REDUCTION = POLICY_TARGET
```

not:

```text
statistically sufficient sample
proven 10% causal reduction
```

### Better sequence

1. instrument baseline services;
2. estimate within-stratum variability;
3. decide whether the field pilot is exploratory or powered;
4. if a statistical effect claim is required, compute sample size from observed variance and desired detectable effect.

For hackathon evidence, an explicitly exploratory pilot is acceptable if claims stay narrow.

---

# 3. Sequential control-then-intervention is confounded by time

## RT-06 — Days 3–6 control then days 7–12 intervention can mistake temporal change for treatment effect

Possible confounders include:

- menu appeal;
- exam/academic-calendar state;
- weather;
- price/support regime;
- campus closures/service changes;
- special events;
- operator learning;
- supplier/ingredient disruptions.

### Preferred design when operationally feasible

Use **interleaved blocked assignment** or matched-pair crossover rather than placing all control days first.

Example concept:

```text
stratum = campus × meal_period × comparable_menu_class × service_regime

pair A:
  service 1 -> CONTROL
  service 2 -> INTERVENTION

pair B:
  service 1 -> INTERVENTION
  service 2 -> CONTROL
```

Assignment should be determined before outcomes are known.

### If interleaving is impossible

Keep sequential design, but label it **quasi-experimental** and avoid strong causal wording. Record major time-varying context and use matched comparisons cautiously.

---

# 4. Served portions are censored demand under sellout

## RT-07 — `served_portions` cannot always be used as true demand

Suppose:

```text
true demand = 700
produced = 600
served = 600
sellout = true
```

If the model forecast was 600, forecast APE against `served_portions` becomes zero even though actual demand exceeded supply.

This is **demand censoring**.

### Required rule

```text
if sellout == true:
    served_portions is a LOWER BOUND on demand
    do not compute ordinary forecast APE as if demand were fully observed
```

### Add fields

```text
sellout_timestamp
service_end_timestamp
estimated_unserved_demand_if_available
substitution_or_extra_batch_qty
queue_or_turnaway_signal
```

Do not invent unserved demand. Mark it unknown/censored if it cannot be measured.

---

# 5. Early-sellout boolean needs severity

## RT-08 — A boolean cannot distinguish a 2-minute sellout from a 45-minute service failure

Keep `early_sellout`, but add severity metrics:

```text
sellout_minutes_before_service_end
shortage_portions_if_observable
forced_substitution_event
emergency_batch_event
service_delay_minutes
```

Primary guardrail can remain simple, but richer fields are necessary for diagnosis and asymmetric loss design.

---

# 6. Waste boundary must isolate the mechanism being tested

## RT-09 — Total waste can fall for reasons unrelated to production quantity

Production recommendation most directly targets **unserved excess**, not all plate waste.

Minimum categories should distinguish:

```text
PREPARATION_WASTE_KG
UNSERVED_EDIBLE_SURPLUS_KG
SERVICE_LINE_LEFTOVER_KG      # if distinct operationally
PLATE_WASTE_KG
OTHER_WASTE_KG
```

If measurement burden forces simplification, at minimum separate:

```text
pre_consumer_or_unserved
vs
post_consumer_plate
```

### Primary mechanism KPI

If quantity optimization is the intervention, `unserved_edible_surplus` or a clearly defined pre-consumer excess measure may be more mechanistically direct than undifferentiated `waste_kg`.

Do not change the primary KPI until the waste owner confirms measurement feasibility.

---

# 7. Kg per served meal is useful but menu composition can still confound it

## RT-10 — Normalization solves volume, not mass-composition differences

`waste kg / 100 served meals` is better than raw kg for different service sizes, but two menus can have different portion masses and waste propensity.

Example:

- soup-heavy meal;
- rice/stew meal;
- packaged meal;
- fruit-heavy meal.

They can produce different kilograms of waste per served meal even with equally good quantity planning.

### Mitigation

Match/block on broad menu class or include menu context in analysis.

Where practical, add:

```text
planned_portion_mass_or_menu_class
```

Do not overcomplicate the first pilot with full nutrient/LCA modeling.

---

# 8. Measurement reliability is itself an acceptance gate

## RT-11 — Weighing process must be stable across arms

Institutional food-waste studies emphasize explicit weighing and separation methods. A reference methodology by Boschini et al. uses separate measurement of initial servings, plate waste and non-served food; large-scale work by Boschini et al. also separately measures prepared, plate-leftover and non-served food when studying drivers.

Academic references:

- Boschini M, Falasconi L, Giordano C, Alboni F. (2018). *Food waste in school canteens: A reference methodology for large-scale studies.* Journal of Cleaner Production, 182, 1024–1032.  
  https://consensus.app/papers/food-waste-in-school-canteens-a-reference-methodology-for-boschini-falasconi/75e74e10a5f855e288b6d3cfb8597d5e/?utm_source=chatgpt
- Boschini M, Falasconi L, Cicatiello C, Franco S. (2020). *Why the waste? A large-scale study on the causes of food waste at school canteens.* Journal of Cleaner Production, 246, 118994–119005.  
  https://consensus.app/papers/why-the-waste-a-largescale-study-on-the-causes-of-food-waste-boschini-falasconi/62a0bfdeedb85a509104d2d0295538fd/?utm_source=chatgpt

### Pilot measurement checklist

Before first scored service:

- same scale/device where possible;
- tare procedure documented;
- category containers labeled;
- same category definitions across arms;
- staff rehearse one unscored service;
- measurement timestamp recorded;
- missing/spillage/contamination noted;
- units locked.

---

# 9. Current operator quantity must be recorded separately from model forecast

## RT-12 — Need three numbers, not two

The existing fields include model forecast, produced and served.

Add:

```text
operator_baseline_planned_qty
model_recommended_qty_or_band
final_approved_qty
```

Why:

- model may forecast better but operator override improves it;
- operator may already have stronger information;
- production can differ from both plan and recommendation because of kitchen constraints.

This allows decomposition:

```text
forecast value
policy value
human override value
execution deviation
```

---

# 10. Shadow recommendations improve control learning

## RT-13 — Generate model output in control services but hide it operationally

If safe and feasible, compute a **shadow recommendation** for control services without showing it to the operator before the decision.

Store only after the normal production decision is locked.

Benefits:

- evaluates model against the same services;
- reduces dependence on different calendar periods;
- separates forecast performance from intervention/adoption effect.

Strict rule:

```text
CONTROL shadow recommendation must not influence production decision
```

Use audit timestamp to prove recommendation was generated/locked appropriately.

---

# 11. Override handling needs an analysis rule

## RT-14 — Overrides are part of treatment, not inconvenient noise

Primary operational analysis should keep intervention-assigned services even if the operator edits/holds the recommendation.

This is closer to an **intent-to-treat-like** product evaluation: what happens when the decision-support workflow is offered?

Secondary diagnostic analysis can distinguish:

```text
approved_as_is
edited
held_or_rejected
```

Do not delete override services to make the model look better.

---

# 12. Predeclare exclusion and missing-data rules

## RT-15 — Post-hoc exclusions can bias a tiny pilot

Before scoring starts, define how to handle:

- missing waste measurement;
- scale failure;
- campus closure;
- menu substitution;
- event day;
- emergency kitchen disruption;
- service interruption;
- incomplete portion counts.

Recommended output state:

```text
INCLUDED
EXCLUDED_PREDEFINED_REASON
MEASURED_BUT_FLAGGED
```

Never silently drop inconvenient services.

---

# 13. Intervention contamination and operator learning

## RT-16 — Same operator can learn from recommendations and change later control behavior

If control and intervention alternate, carryover is possible.

Mitigations:

- use shadow predictions but do not reveal on control days;
- document whether operator has seen similar recommendation patterns;
- avoid claiming perfect randomization independence;
- if pilot is short, treat learning as part of product deployment effect but report it.

The goal is decision evidence, not pretending operational humans are laboratory-isolated.

---

# 14. Suggested revised minimal service record

```text
# identity/context
date
service_id
campus
meal_period
service_regime
menu_class
arm

# decision
operator_baseline_planned_qty
model_forecast_meals
model_recommended_low
model_recommended_high
final_approved_qty
operator_action              # APPROVE / EDIT / HOLD
production_lock_timestamp

# execution
produced_portions
served_portions

# censoring / service guardrail
early_sellout
sellout_timestamp
service_end_timestamp
forced_substitution_event
emergency_batch_event
service_delay_minutes
estimated_unserved_demand_if_available

# waste boundary
preparation_waste_kg
unserved_edible_surplus_kg
plate_waste_kg
other_waste_kg

# measurement quality
measurement_complete
measurement_issue_code
notes
```

A smaller schema is acceptable if each removed field has a reason.

---

# 15. Analysis hierarchy

## Primary operational question

Does offering operator-reviewed decision support reduce the **production-relevant waste metric** without worsening service guardrails?

## Secondary questions

- Does the model beat current operator baseline?
- How often and why does operator override?
- Are errors mostly excess or shortage?
- Which contexts fail?
- Is menu mix/campus allocation more important than total demand?

## Do not lead with

- R²;
- model leaderboard;
- CO2 estimate;
- water estimate;
- extrapolated annual savings.

---

# 16. Statistical language gate

With a very small exploratory pilot, safe outputs include:

- raw paired differences;
- median/mean descriptive change;
- service-by-service plots;
- exact number of shortage events;
- override counts;
- confidence/uncertainty clearly labeled if calculated appropriately.

Do not claim:

- statistically proven reduction;
- generalizable effect;
- calibrated confidence interval;
- causal effect beyond the design's support.

A 10% internal target is not a p-value or confidence threshold.

---

# 17. Recommended pilot design options

Choose only after P0 evidence-gap questions are answered.

## Option A — Interleaved matched service pairs

Best when comparable services repeat and intervention can alternate.

Pros:

- reduces time confounding;
- simple to explain.

Cons:

- imperfect matching;
- operator carryover possible.

## Option B — Blocked crossover by repeated meal context

Best when the same campus/meal/menu class recurs enough.

Pros:

- stronger within-context comparison.

Cons:

- may require longer pilot.

## Option C — Sequential quasi-experiment

Use only when operations cannot interleave treatment.

Pros:

- easiest operationally.

Cons:

- weakest causal attribution;
- requires cautious wording and context controls.

---

# 18. Literature role

The external literature is used only to strengthen measurement design, not to predict Boğaziçi effect size.

A school-canteen intervention study by Vidal-Mones, Díaz-Ruíz & Gil (2022) used staged real-world measurement and intervention evaluation, illustrating the value of direct waste measurement and context-specific implementation rather than relying on modeled impact alone.

Reference:  
https://consensus.app/papers/from-evaluation-to-action-testing-nudging-strategies-to-vidal-mones-díaz-ruíz/7a8861096e3854b98bb84176bc09869f/?utm_source=chatgpt

No external reduction percentage should become the Boğaziçi expected effect.

---

# 19. Protocol upgrade gate

Before a real field pilot, the execution owner should explicitly decide:

1. exploratory vs powered study;
2. intervention assignment scheme;
3. primary production-relevant waste boundary;
4. sellout censoring rule;
5. service severity guardrails;
6. current operator baseline field;
7. shadow-control recommendation policy;
8. override analysis rule;
9. missing/exclusion rules;
10. measurement QA procedure.

Until those are decided, the existing protocol is a strong **falsifiability scaffold**, not a finished causal study protocol.

---

# 20. Bottom line

The pilot should answer:

> Does this decision-support workflow improve the real production decision under the same operational constraints, while preserving access/service quality?

not:

> Did average waste happen to be lower during a later week when our model was turned on?

That distinction is the difference between a demo metric and defensible evidence.
