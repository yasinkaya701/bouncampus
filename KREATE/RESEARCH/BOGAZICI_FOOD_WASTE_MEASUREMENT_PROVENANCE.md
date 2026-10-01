# Boğaziçi Food-Waste Measurement Provenance Audit — 2023→2025

**Research date:** 2026-10-01  
**Purpose:** Determine whether Boğaziçi's published food-waste numbers can be compared across years or used to test the production-mismatch hypothesis.  
**Status:** Secondary/public-source research. **NOT PMR. NOT proof of current kitchen waste composition. NOT permission to claim a longitudinal reduction/increase.**

---

# 0. Executive conclusion

The published Boğaziçi food-waste series is useful for proving that the university measures a material food-waste stream, but it is **not currently safe as a longitudinal causal/trend series**.

The key reason is measurement-provenance mismatch:

```text
2023
published daily table = WASTE PORTIONS + KG
published rows exhibit an exact 0.30 kg per waste-portion arithmetic relationship

2024
monthly KG totals
reported as food waste collected across the university / dining halls and canteens
plus recovery-channel accounting

2025
monthly KG totals
plus amount delivered to İSTAÇ and waste-oil streams
with internal monthly reconciliation anomalies
```

Therefore:

> **Do not say food waste doubled from 2023 to 2024, fell 5% in 2025 because operations improved, or infer a production-forecast effect from the annual totals.**

Those statements require evidence that the measurement boundary, conversion method, collection scope, timing convention and waste-stage taxonomy are comparable.

The most important pilot implication is separate:

> Current public reporting classifies waste mainly by **collection/recovery pathway**, not by the **operational stage where the waste was created**.

That means the published totals cannot answer the P0 causal question:

> How much current waste is preparation waste vs unserved cooked surplus vs service-line leftover vs plate waste?

A prospective pilot needs a new operational-stage taxonomy even if the University's sustainability reporting remains unchanged.

---

# 1. Source map

## FW-PROV-01 — Current 2025 campus food-waste page

Official Boğaziçi institutional-data page:

https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

Published 2025 totals:

- `TOTAL_FOOD_WASTE_KG = 48,251`
- `DELIVERED_TO_ISTAC_KG = 33,430`
- `WASTE_OIL_KG = 6,305`
- all waste oil reported as delivered for recycling.

The page states that amounts delivered to İSTAÇ are included within total food waste.

It also documents current/ongoing waste-reduction practices such as:

- portion control;
- removal of unpopular dishes;
- composting;
- surplus-food redistribution;
- waste-oil recovery.

### What this source is good for

- current problem-scale context;
- current monthly food-waste table;
- recovery-channel context;
- confirmation that downstream mitigation already exists.

### What it does NOT provide

- preparation waste;
- unserved cooked surplus;
- service-line leftovers;
- plate waste;
- campus × meal decomposition;
- produced portions;
- served portions;
- causal reason for each kg;
- a documented quantity-planning baseline.

---

## FW-PROV-02 — 2024 food-waste reporting

Official Boğaziçi SDG / campus food-waste material reports:

- `TOTAL_FOOD_WASTE_KG = 50,993`
- `RECYCLED_OR_RECOVERED_FOOD_KG = 29,776`
- `FOOD_RECOVERY_RATE = 58.4%`
- `WASTE_OIL_KG = 5,710`

Official campus page / SDG surface:

https://impact.bogazici.edu.tr/221-campus-food-waste-tracking

2025 sustainability-report indexed material also labels the 2024 `50,993 kg` as the amount collected from **dining halls and canteens** and the `29,776 kg` as sent to compost/shelters.

### Important semantics

This is primarily a **collection/recovery-path** representation:

```text
food waste collected
→ recovered/recycled
→ other
```

It is not a kitchen-process causal decomposition.

---

## FW-PROV-03 — 2023 daily food-waste table

The 2024 Sustainability / SDG-2 material republishes the 2023 food-waste monitoring table and reports:

- `2023 TOTAL FOOD WASTE = 24.3 tonnes`
- `2023 TOTAL WASTE OIL = 5.5 tonnes`

Indexed report source:

https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/16-bogazici-university-sustainability-yayin-20250512-140721.pdf

The source table has columns:

```text
Günler
Atık (Porsiyon)
Atık (Kg)
```

Across the published daily values visible in the indexed report, `Atık (Kg)` repeatedly equals exactly:

```text
Atık (Porsiyon) × 0.30 kg
```

Examples:

| Date | Waste portions | Published kg | Arithmetic |
| --- | ---: | ---: | --- |
| 01.01.2023 | 152 | 45.6 | 152 × 0.30 = 45.6 |
| 02.01.2023 | 433 | 129.9 | 433 × 0.30 = 129.9 |
| 10.01.2023 | 565 | 169.5 | 565 × 0.30 = 169.5 |
| 01.04.2023 | 172 | 51.6 | 172 × 0.30 = 51.6 |
| 02.07.2023 | 62 | 18.6 | 62 × 0.30 = 18.6 |
| 18.10.2023 | 726 | 217.8 | 726 × 0.30 = 217.8 |

Published monthly total example:

```text
January portions = 6,477
January kg       = 1,943.1
6,477 × 0.30     = 1,943.1
```

### Claim boundary

This arithmetic identity is a **derived observation from the published values**.

It does **not** by itself prove:

- that no physical weighing occurred;
- that `0.30 kg` was formally the University's conversion rule;
- what a `waste portion` operationally meant;
- whether the portion represented unserved food, plate waste or another category.

The indexed public text does not expose a data dictionary explaining the relationship.

Therefore represent the 2023 method as:

```text
PUBLISHED PORTION-BASED SERIES WITH EXACT 0.30 KG/PORTION NUMERIC RELATIONSHIP
MEASUREMENT METHOD = UNRESOLVED
```

not as `direct measured kg` unless a source owner confirms that interpretation.

---

# 2. Why the 2023→2025 trend is not yet defensible

Published annual totals imply mechanically:

```text
2023: 24.3 t
2024: 50.993 t
2025: 48.251 t
```

Raw arithmetic would produce:

- 2023→2024: approximately **+109.9%**;
- 2024→2025: approximately **−5.4%**.

But those percentages are **not an operational trend claim**.

Possible non-causal explanations that must be ruled out include:

- measurement method changed;
- source system changed;
- additional canteens/campuses entered the scope;
- waste categories changed;
- 2023 used portion-based estimation while later years use collected kg;
- recovery/disposal records became more complete;
- reporting timing changed;
- contractor or reporting-owner changed;
- service calendar / operating days changed.

### Agent rule

Until measurement comparability is verified:

```text
ALLOWED:
"Boğaziçi reports 24.3 t for 2023, 50.993 t for 2024 and 48.251 t for 2025 under published reporting artifacts whose measurement comparability is not yet established."

FORBIDDEN:
"Food waste doubled in 2024."
"Boğaziçi reduced waste 5.4% in 2025 because its sustainability measures worked."
"The historical trend proves demand mismatch worsened/improved."
```

---

# 3. 2025 monthly table has a reconciliation anomaly

The current 2025 page says the amount delivered to İSTAÇ is included within total food waste.

But at least these rows violate that literal monthly inclusion relationship:

```text
August 2025
TOTAL_FOOD_WASTE = 1,502 kg
DELIVERED_TO_ISTAC = 3,550 kg

October 2025
TOTAL_FOOD_WASTE = 1,334 kg
DELIVERED_TO_ISTAC = 4,850 kg
```

If `delivered_to_ISTAC` is a strict same-month subset of `total_food_waste`, those rows are impossible.

### Possible explanations — all remain hypotheses

- collection month and delivery month differ;
- stored/backlogged waste is delivered later;
- the two fields use different event-time semantics;
- transcription/data-entry error;
- `total` and `delivered` cover different boundaries despite the page note.

### Data-engineering rule

Do not silently repair the rows.

Store:

```text
measurement_period
collection_date_semantics
transfer_date_semantics
reporting_period
source_owner
boundary_definition
```

and mark the conflict as unresolved.

---

# 4. Recovery rate is not the production-optimization KPI

For 2024 the University explicitly publishes a `58.4%` food recovery rate.

For 2025, a mechanical calculation:

```text
33,430 / 48,251 ≈ 69.3%
```

must **not** automatically be promoted to a comparable `2025 recovery rate` because:

1. the page does not publish that KPI as such;
2. monthly subset semantics are internally inconsistent;
3. delivery timing may differ from generation timing.

More importantly, even a perfectly measured recovery rate answers a different question from the KREATE dining wedge.

```text
recovery/diversion KPI:
Where did waste go after it existed?

production-decision KPI:
Why did avoidable food become surplus/waste in the first place?
```

A high recovery rate can coexist with high avoidable overproduction.

---

# 5. Public taxonomy is disposal-path oriented, not causal-stage oriented

Official Boğaziçi sustainability/waste policy describes streams such as:

- cooked food scraps;
- bread scraps;
- tea waste;
- compostable organic waste;
- waste oil;
- material sent to shelters;
- material sent to İSTAÇ;
- surplus food delivered to people in need.

Relevant official source:

https://kurumsalveri.bogazici.edu.tr/tr/pages/1225-policy-for-minimisation-of-plastic-use/1419

These categories are valuable for Zero Waste operations, but they do not tell the decision engine whether the avoidable mechanism was:

```text
PREPARATION_LOSS
OVERPRODUCTION_UNSERVED
SERVICE_LINE_LEFTOVER
PLATE_WASTE
MENU_REJECTION
SPOILAGE
OTHER
```

### P0 consequence

Current public data cannot validate:

> `demand mismatch materially contributes to avoidable food waste`

The team needs a bounded prospective or internal historical **waste-stage decomposition**.

---

# 6. Minimum causal-stage measurement contract

For a pilot, preserve the University's existing downstream reporting while adding a production-relevant layer.

## Required minimum

```text
SERVICE_ID
DATE
CAMPUS
MEAL_PERIOD
SERVICE_REGIME

PRODUCED_PORTIONS
SERVED_PORTIONS

PREPARATION_WASTE_KG
UNSERVED_EDIBLE_SURPLUS_KG
PLATE_WASTE_KG
OTHER_FOOD_WASTE_KG

RECOVERED_OR_DONATED_KG
ISTAC_TRANSFER_KG
WASTE_OIL_KG

MEASUREMENT_METHOD
MEASUREMENT_TIMESTAMP
SOURCE_OWNER
NOTES
```

### If measurement burden is too high

At minimum separate:

```text
PRE_CONSUMER_OR_UNSERVED_KG
POST_CONSUMER_PLATE_KG
```

because production-quantity intervention should not claim credit for plate-waste changes it did not cause.

---

# 7. Recommended metric hierarchy

## Tier 1 — directly tied to production decision

```text
unserved_edible_surplus_kg / served_meals
excess_portions / produced_portions
shortage_events
sellout_minutes_before_end
```

## Tier 2 — broader physical waste

```text
pre_consumer_waste_kg / served_meals
plate_waste_kg / served_meals
total_food_waste_kg / served_meals
```

## Tier 3 — downstream disposition

```text
recovery/diversion kg
compost kg
shelter kg
ISTAC transfer kg
donation kg
```

## Tier 4 — modeled impact

```text
TRY impact
CO2e impact
water impact
```

Only calculate Tier 4 after its separate economic/LCA semantics are verified.

---

# 8. Longitudinal provenance schema

Every year/series should carry explicit metadata:

```text
year
metric_name
value
unit
source_url
source_report_version
scope_campuses
scope_facilities
scope_service_channels
waste_stage_definition
collection_boundary
destination_boundary
measurement_method
conversion_factor_if_any
recorded_at_granularity
reporting_period_granularity
data_owner
known_anomalies
comparability_group
```

### Comparability rule

Two years may be plotted as a connected trend only when:

```text
same/equivalent scope
+ same/equivalent waste definition
+ same/equivalent measurement method
+ same/equivalent time semantics
```

Otherwise show them as separate sourced observations with a visible methodology break.

---

# 9. P0 owner questions generated by this audit

## Waste / Zero Waste owner

1. What exactly counted as one `Atık (Porsiyon)` in the 2023 report?
2. Was the published kg physically weighed or calculated from portions?
3. If calculated, what was the conversion factor and why?
4. Which campuses/facilities were included in 2023?
5. Did the measurement method or facility scope change in 2024?
6. In 2024/2025, is `Total Food Waste` generated waste, collected waste, transferred waste or another operational quantity?
7. Are dining halls and canteens combined into one total?
8. Can food waste be separated into kitchen/preparation, unserved cooked surplus and plate waste?
9. What does `delivered to İSTAÇ` timestamp represent — generation month, pickup month or transfer month?
10. Why do August and October 2025 delivered amounts exceed the same month's total?

## Food Services / contractor

1. Is any unserved surplus recorded before it enters the general food-waste stream?
2. Are produced and served portions retained by campus/meal?
3. Is excess edible food donated/transferred before waste weighing?
4. Can one week of surplus be weighed separately without disrupting operations?

---

# 10. Falsification / product-direction consequences

## If unserved surplus is material

Keep the production-quantity / allocation wedge and run a decision-support pilot.

## If preparation waste dominates

Shift toward recipe/preparation/process control rather than attendance forecasting.

## If plate waste dominates

Shift toward menu mix, portion choice, behavioral/service interventions or preference systems.

## If waste-stage data cannot be obtained but produced/served counts exist

Run a narrower operational excess-portions pilot and avoid broad `food waste reduction` claims.

## If neither stage data nor produced/served data can be obtained

The dining decision wedge cannot yet support a measured field-impact claim.

---

# 11. Safe application language

### Safe

> `PUBLIC SOURCE` Boğaziçi reports 48,251 kg of food waste for 2025 and already operates several downstream prevention/recovery practices. `RESEARCH GAP` The public reporting does not separate preparation waste, unserved cooked surplus and plate waste at the service level, so the team is testing whether production mismatch is actually a material share before claiming that forecasting can reduce the total.

### Unsafe

> "Boğaziçi's food waste doubled between 2023 and 2024."

> "Boğaziçi reduced food waste by 5.4% in 2025."

> "69.3% of 2025 food waste was recycled."

> "48 tonnes are caused by demand forecasting errors."

> "Our model will reduce the University's reported food waste total."

None of those statements is established by the current provenance chain.

---

# 12. Sources

1. Boğaziçi University — Campus Food Waste Tracking, current institutional data page:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310
2. Boğaziçi University — legacy/current SDG Campus Food Waste Tracking page with 2024 and 2023 references:  
   https://impact.bogazici.edu.tr/221-campus-food-waste-tracking
3. Boğaziçi University Sustainability / SDG material containing the published 2023 daily portion/kg tables:  
   https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/16-bogazici-university-sustainability-yayin-20250512-140721.pdf
4. Boğaziçi University waste-policy / organic-waste-stream context:  
   https://kurumsalveri.bogazici.edu.tr/tr/pages/1225-policy-for-minimisation-of-plastic-use/1419

---

# 13. Bottom line

The published sustainability numbers are strong **problem-scale and waste-governance evidence**.

They are not yet the outcome variable for the product.

The causal chain must be rebuilt prospectively:

```text
production decision
→ produced quantity
→ served quantity
→ unserved surplus
→ waste stage
→ downstream recovery/disposal
```

Only then can BOUNCAMPUS distinguish:

- avoiding waste;
- diverting waste after generation;
- improving service;
- merely changing reporting.

That provenance distinction should be treated as a hard requirement for any future jury, pilot, economic or climate claim.