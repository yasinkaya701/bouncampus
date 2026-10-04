# Climate-Impact Conversion Hierarchy — 2026-10-04

**Purpose:** define when BOUNCAMPUS may translate measured physical food prevention into climate/resource estimates without false precision.  
**Status:** methodology research. **No BOUNCAMPUS climate savings have been measured.**

## Executive conclusion

The strongest first climate KPI is not CO2e.

It is the directly observed physical effect:

```text
avoidable edible food prevented
without worsening service availability
```

Climate conversion should be layered according to the quality of information about the prevented food.

A single universal conversion such as:

```text
1 kg food = X kg CO2e
```

is too crude for a defensible product claim because environmental intensity varies materially by food category, production method, sourcing, system boundary and LCA method.

---

# 1. Why a single factor is risky

Poore & Nemecek's large cross-food analysis consolidated evidence from:

- 38,700 farms;
- 1,600 processors, packaging types and retailers;
- five environmental indicators.

They report very large producer-level variation, including up to roughly 50-fold variation in impacts within the same product category.

Reference:
Joseph Poore, Thomas Nemecek (2018), **Reducing food's environmental impacts through producers and consumers**, *Science* 360, 987–992.
https://consensus.app/papers/reducing-food%E2%80%99s-environmental-impacts-through-producers-poore-nemecek/d09a442ade855716bf30aceb3d7f15d5/

A 2025 systematic review/meta-analysis of 118 food-production LCA studies similarly finds substantial variation related to:

- food category;
- LCA method;
- lifecycle phase/scope;
- region/country;
- whether waste is included.

Reference:
Mandouri et al. (2025), **Carbon footprint of food production: a systematic review and meta-analysis**, *Scientific Reports* 15.
https://consensus.app/papers/carbon-footprint-of-food-production-a-systematic-review-mandouri-onat/4d84f75c4d145fd5b3fd78033b23af1f/

### BOUNCAMPUS implication

The more generic the factor, the weaker the claim must be.

---

# 2. Impact evidence hierarchy

## Level C0 — no operational reduction measured

Available:
- public annual waste;
- model scenario;
- proposed intervention.

Allowed:
> potential climate relevance / scenario only.

Forbidden:
> BOUNCAMPUS avoided X kg CO2e.

---

## Level C1 — physical food reduction measured, composition unknown

Available:
- consistent direct mass/portion measurement;
- control/intervention or other defensible comparison;
- stage identified as addressable edible surplus.

Primary claim:
> X kg of edible surplus was prevented under the pilot conditions.

Climate treatment:
- do not force a precise CO2e figure;
- optional broad scenario range only if clearly labelled and factor provenance is shown.

---

## Level C2 — food category known

Available:
- prevented mass by broad category, e.g. beef-based main, poultry, legumes/grains, vegetables.

Possible conversion:

```text
prevented_mass_by_category
× category-specific LCA factor/range
```

Required:
- source for each factor;
- lifecycle boundary;
- geography/sourcing caveat;
- uncertainty/range rather than fake precision.

Allowed claim:
> estimated upstream climate impact avoided under the stated category factors.

---

## Level C3 — recipe/ingredient composition known

Available:
- standardized recipe;
- ingredient quantities;
- measured prevented portions/mass;
- documented sourcing assumptions.

Possible conversion:

```text
sum(
  prevented_ingredient_mass_i
  × factor_i
)
+ documented cooking/processing components if included
```

This is substantially stronger than a generic food-average multiplier.

Still label as **derived estimate**, not direct CO2 measurement.

---

## Level C4 — institution-specific audited lifecycle model

Available:
- supplier/sourcing information;
- energy/process data;
- waste treatment boundary;
- validated recipe/procurement records;
- documented LCA methodology.

This can support a stronger institution-specific estimate, but remains model-derived unless direct lifecycle emissions are measured.

This level is unnecessary for the KREATE application gate.

---

# 3. Avoided waste stage matters

If BOUNCAMPUS prevents **unserved edible surplus**, the relevant counterfactual is food that would otherwise have been produced and then not consumed.

If the measured change is only lower **plate waste**, causal attribution may involve:

- smaller portions;
- menu preference;
- taste/quality;
- behavioral changes;
- production quantity.

Therefore climate attribution should preserve:

```text
measurement_stage
intervention_pathway
counterfactual
```

Do not convert a mixed waste-bin reduction into `production emissions avoided` without documenting why the food would not have been produced absent the intervention.

---

# 4. Waste treatment and upstream avoidance are different scopes

A prevention intervention can affect:

- upstream agricultural production;
- ingredient processing;
- transport;
- cooking/energy;
- downstream waste handling.

A waste-management intervention can affect mostly the downstream pathway.

Do not combine both into one number unless scopes are explicit.

Recommended fields:

```text
impact_scope:
  upstream_food_production
  processing
  transport
  cooking
  waste_treatment

factor_source
factor_geography
factor_year
factor_boundary
factor_uncertainty
```

---

# 5. Water impact needs equal caution

Water intensity varies strongly by:

- crop/animal product;
- geography;
- blue/green/grey water definition;
- production system;
- water scarcity context.

Therefore:

```text
kg food prevented
× one generic liters/kg factor
```

should not be presented as institution-specific water savings.

If water is shown in a future pitch, prefer:

- recipe/category-specific factor;
- explicit source/boundary;
- range;
- `DERIVED ESTIMATE` label.

---

# 6. Money is not a climate conversion

Financial value must be computed from actual marginal economics, not from climate-factor logic.

Do not calculate:

```text
contract_value / contracted_meals
× avoided_portions
```

and call it savings.

The contract unit price may bundle:

- labor;
- service;
- distribution;
- cleaning;
- overhead;
- contractor margin;
- fixed costs.

Only PMR/contract evidence can establish the avoidable marginal cost and who captures it.

---

# 7. Recommended hackathon climate scorecard

## Directly measured

```text
edible_surplus_kg_prevented
served_meals
sellout / shortage guardrail
```

## Derived only when factor quality permits

```text
estimated_CO2e_range
estimated_water_range
```

## Always display

```text
factor_source
factor_scope
factor_quality
uncertainty / range
```

This is more credible than a large single climate number.

---

# 8. UI / evidence contract

Climate output should be typed as:

```text
PHYSICAL_MEASUREMENT
DERIVED_ESTIMATE
MODEL_SCENARIO
```

Example:

```text
12.4 kg edible surplus prevented     PHYSICAL_MEASUREMENT
X–Y kgCO2e estimated avoidance       DERIVED_ESTIMATE
25 kg future monthly scenario        MODEL_SCENARIO
```

Never render all three with the same visual confidence.

---

# 9. Application-safe wording before pilot

Safe:
> Food-waste prevention can avoid upstream resources embedded in food that otherwise would be produced and discarded. We will quantify climate impact only after measuring the physical food reduction and applying documented food-specific factors.

Unsafe:
> Boğaziçi's 48,251 kg food waste equals X tonnes of CO2 and BOUNCAMPUS will save Y tonnes.

---

## Current conclusion

For KREATE selection, the strongest climate credibility comes from **refusing fake precision**.

The evidence chain should be:

```text
validated operational intervention
-> measured edible food prevented
-> food composition/category
-> documented LCA factor/range
-> derived climate estimate
```

not:

```text
annual public waste
× generic internet factor
= claimed BOUNCAMPUS climate impact
```
