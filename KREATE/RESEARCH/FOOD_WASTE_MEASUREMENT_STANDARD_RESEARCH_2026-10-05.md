# Food-Waste Measurement Standard Research

**Research date:** 2026-10-05
**Status:** Secondary methodology research using UNEP/EPA guidance. Not a Boğaziçi measurement result.

## 1. Prevention hierarchy

US EPA's current Wasted Food Scale places **prevent wasted food / source reduction** at the top of the preferred pathways.

Sources:
- https://www.epa.gov/sustainable-management-food/wasted-food-scale
- https://www.epa.gov/sustainable-management-food/prevent-wasted-food-through-source-reduction

This supports BOUNCAMPUS's climate logic:

> If a production decision can safely prevent unnecessary food from being prepared, prevention occurs upstream of donation/recovery/composting/disposal.

It does **not** establish that the proposed production decision is the dominant preventable waste source at Boğaziçi.

## 2. UNEP Food Waste Index 2024 — food-service measurement methods

UNEP 2024 guidance identifies multiple methods that may be appropriate for food-service measurement, including:
- direct measurement / weighing of food-only streams;
- filled-volume assessment;
- direct measurement of individual items, including digital/smart-bin approaches;
- waste-composition analysis;
- scanning/counting discrete packaged items.

Source:
https://www.unep.org/resources/publication/food-waste-index-report-2024
Full methodology:
https://wedocs.unep.org/bitstream/handle/20.500.11822/45230/food_waste_index_report_2024.pdf

### Critical implication

There is no universal requirement that every pilot use one specific hardware measurement method.

Select the lowest-burden method that provides enough reliability for the decision question.

## 3. Measurement hierarchy for BOUNCAMPUS pilot

### Existing reliable operational record
Use it first if:
- scope is known;
- measurement stage is known;
- timestamps align with service decision/outcome;
- method is stable across control/intervention.

### Direct weighing
Preferred simple prospective ground truth for segregated streams when operationally feasible.

Advantages:
- direct mass;
- low conceptual ambiguity;
- useful calibration reference.

Limits:
- staff burden;
- requires stream separation;
- total bin mass alone may not identify food category/cause.

### Computer vision / TrayGate
Use when item/compartment-level post-consumer information is decision-relevant and normal tray-return workflow can provide repeatable capture.

Potential advantages:
- high-frequency observation;
- automatic category/compartment estimates;
- minimal manual weighing per tray once validated.

Limits:
- needs site-specific validation;
- visual percentage is not automatically grams;
- mixed/viscous foods are harder;
- changing tray geometry/lighting/menu can shift performance;
- camera/privacy/cleanability integration requirements.

### Volume / counting
Valid only when semantics are clear and the physical item supports it.

Example:
- packaged unopened items;
- countable portions;
- standardized containers.

## 4. Mandatory pilot measurement metadata

For every waste observation, record:

```text
measurement_id
service_id
waste_stage
measurement_method
mass_or_value
unit
edible_fraction_semantics
food_category_scope
measured_at
operator_or_device
calibration_version
quality_state
notes
```

### Waste stage must not collapse

At minimum attempt to distinguish:
- preparation waste;
- unserved edible production surplus;
- plate/post-consumer waste.

If separation is impossible, report the actual mixed boundary rather than inventing precision.

## 5. Why one total monthly figure is insufficient

A monthly university food-waste total cannot directly evaluate a service-level production intervention because:
- decision happens at service/batch scale;
- waste can have multiple causes/stages;
- collection date may differ from generation date;
- service volume changes;
- operational regime changes.

Pilot outcome should be measured prospectively at the same operational boundary as the decision.

## 6. Normalization

Primary decision outcome should include both absolute and normalized measures.

Example:

```text
waste_kg_per_100_served = waste_kg / served_portions * 100
```

But choose the waste numerator explicitly:
- total measured waste;
- edible surplus;
- plate waste;
- or another predeclared stage.

Do not switch numerator definition after seeing results.

## 7. Causes matter

EPA guidance explicitly recommends collecting the amount, type and **reason** for wasted food so operators can make meaningful changes.

Source:
https://www.epa.gov/sustainable-management-food/tools-preventing-and-diverting-wasted-food

Therefore outcome measurement should include structured reason/anomaly fields where possible:
- overproduction;
- poor demand estimate;
- recipe/taste issue;
- portion size;
- food-safety discard;
- service closure;
- event/campus disruption;
- preparation error;
- unknown.

These reason codes may initially be operator-reported rather than model-inferred.

## 8. Measurement consistency is more important than gadget sophistication

For a CONTROL vs INTERVENTION pilot:
- use the same measurement boundary in both arms;
- same equipment/method;
- same handling of liquids/inedible material;
- same service scope;
- same normalization denominator;
- record missingness and anomalies.

A fancy computer-vision sensor with unstable semantics can produce weaker evidence than a disciplined manual scale protocol.

## 9. TrayGate calibration position

TrayGate should be validated against direct physical ground truth before using its output as pilot evidence.

Suggested staged validation:

### Stage A — percentage/bin classification
- 0–25%
- 25–50%
- 50–75%
- 75–100%

### Stage B — continuous visual leftover fraction
Compare against annotated/controlled reference.

### Stage C — volume
RGB-D/depth where useful.

### Stage D — mass
Only after food-specific volume/density or direct paired weighing calibration supports it.

Do not jump from `segmented pixels` to `grams` without measured calibration.

## 10. Claim boundary

Safe:
> `UNEP recognizes several food-service measurement methods; we will choose and validate the minimum method needed for the pilot.`

Unsafe:
> `TrayGate provides certified food-waste measurement.`

No such validation currently exists.

## 11. Operational consequence

The measurement architecture should follow:

```text
use existing trustworthy records
→ direct scale/recording where simplest
→ add automated sensing only for a specific unresolved measurement gap
→ validate the sensor against physical ground truth
→ preserve method/provenance in every downstream metric
```

This is more defensible than hardware-first deployment.
