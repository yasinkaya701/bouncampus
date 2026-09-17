# BOUNCAMPUS — Assumptions, Evidence & Methodology

BOUNCAMPUS separates **published facts**, **runtime observations**, **model assumptions**, **scenario targets**, and **measured pilot outcomes**. This distinction is part of the product contract, not just documentation.

## 1. Official food-waste baseline

The KREATE product uses Boğaziçi University's published food-waste tracking page as the historical baseline.

Current values encoded in the product:

- 2024 total food waste: **50,993 kg**;
- 2025 total food waste: **48,251 kg**;
- 2025 amount reported as sent to İSTAÇ recovery: **33,430 kg**;
- 2025 monthly food-waste values from the same published source.

These values are `OFFICIAL_PUBLIC`. They are historical/public institutional data, not live sensors.

## 2. Food-demand model status

The current KREATE runtime does **not** claim a POS-trained production model.

The current dashboard derives a transparent lunch-demand estimate from schedule-based midday class flow and contextual signals. The food decision layer then converts this into an uncertainty-aware operating band.

### Current decision-context weights

| Signal | Pilot weight | Meaning |
|---|---:|---|
| Course schedule | 50% | backbone demand context |
| Weather | 20% | current external context |
| Menu | 20% | service/menu context when adapter is healthy |
| Academic calendar | 10% | term/holiday context when available |

These are **transparent pilot policy weights**. They are not learned coefficients and must not be described as statistically optimized.

## 3. Readiness assumptions

The current pilot readiness policy is intentionally conservative:

```text
schedule available + coverage >= 70% → PILOT_READY
schedule available + coverage >= 50% → REVIEW_REQUIRED
otherwise                         → WITHHOLD
```

Interpretation:

- `PILOT_READY` = enough context for a **human-reviewed pilot recommendation**;
- `REVIEW_REQUIRED` = usable for inspection, but context is incomplete;
- `WITHHOLD` = insufficient evidence for operational recommendation.

None of these states means the model has already been validated against cafeteria POS or historical production records.

## 4. Production-band assumption

The product exposes a band rather than one authoritative number.

The band expands when source coverage drops. This is a product uncertainty policy, not a calibrated statistical confidence interval.

Therefore the UI should say:

- **decision band**;
- **planning band**;
- **model estimate**.

It should not say:

- “95% confidence interval” unless such calibration is later implemented;
- “actual expected production”;
- “observed demand.”

## 5. Human-in-the-loop assumption

The KREATE release assumes an accountable kitchen/operator role exists in any real pilot.

Product contract:

```text
operatorApprovalRequired = true
autoDispatchAllowed = false
```

An approval in the demo UI is not an external kitchen command.

## 6. Pilot methodology

Pilot design:

- 14 days;
- matched control and intervention services;
- aggregate service-level measurement;
- no personal data required.

Required measurements:

- forecast meals;
- produced portions;
- served portions;
- edible surplus kg;
- waste kg;
- early sell-out;
- operator override;
- anomaly notes.

## 7. Primary KPI

The primary KPI is:

```text
waste_kg_per_100_served = (waste_kg / served_portions) * 100
```

The product deliberately does **not** use raw `waste kg / service` as the only primary measure because service volume varies.

Secondary metrics include:

- raw waste kg / service;
- overproduction rate;
- edible surplus kg / 100 served;
- forecast absolute percentage error;
- operator override rate;
- early-sellout incidence.

## 8. Pre-registered target

The first pilot target is:

- minimum 5 measured services in each arm;
- ≥10% lower normalized waste in intervention versus matched control;
- no increase in early-sellout incidence;
- no food-safety process bypass.

**The 10% number is a target, not an achieved saving.**

It exists to make the pilot falsifiable and should be revised only prospectively, not after seeing the result.

## 9. Pilot scorecard interpretation

`POST /api/v1/food/pilot-score` can classify measured numeric evidence as:

- `INSUFFICIENT_EVIDENCE`;
- `PROMISING`;
- `FAILED`.

`PROMISING` is deliberately not named `PROVEN` or `SUCCESS` because:

- a small pilot does not establish universal effectiveness;
- food-safety compliance requires manual operational review;
- service matching and measurement quality still matter;
- replication at another site is needed for stronger generalization.

## 10. Food-safety guardrail

Food safety is not inferred from model scores.

The product must never recommend bypassing:

- safe holding-temperature procedures;
- storage rules;
- contamination controls;
- institutional kitchen safety policy.

The numeric scorecard marks food-safety review as a manual gate.

## 11. Climate-impact accounting

The direct first-order measurement is **food-waste mass**.

BOUNCAMPUS should not claim CO2, water or monetary savings from the pilot until:

1. food-waste reduction is actually measured;
2. an appropriate conversion methodology is documented;
3. the scope and uncertainty of the conversion are shown separately from the physical measurement.

This prevents a model estimate from being multiplied by another assumption and presented as measured climate impact.

## 12. Campus occupancy context

The current campus occupancy context is schedule-derived. It is not turnstile, Wi-Fi or camera telemetry.

The dashboard estimates student presence from public/dated course schedule information and room/building assumptions. This may be useful as contextual demand signal, but should not be described as a live headcount.

## 13. Energy model status

Existing building-energy surfaces use a simplified physics-lite model based on:

- building profile constants;
- schedule-derived occupancy context;
- outside temperature.

These outputs are `MODEL_ESTIMATE` and are preserved as a secondary platform module. They are not BMS or smart-meter readings and are not the primary KREATE impact claim.

## 14. What the current release does not assume

The KREATE food-waste product does **not** require or claim:

- student-level food preference profiles;
- anonymized student hash IDs;
- collaborative-filtering preference models;
- cafeteria POS access;
- kitchen inventory telemetry;
- actual historical production quantities;
- live student location;
- connected BMS;
- smart-meter access;
- shuttle GPS.

If any of these sources are later authorized, they must enter the same provenance and source-health contract.

## 15. Privacy statement

The first pilot works with aggregate service-level operational data.

No person-level tracking is necessary to evaluate the primary hypothesis.

The preferred product principle is:

> **Use the least invasive data that can answer the operational climate question.**

## 16. Methodological limitations

The current prototype has meaningful limitations that should remain visible:

1. the food-demand method is not yet calibrated on real produced/served history;
2. source coverage can change and public adapters can degrade;
3. readiness thresholds and signal weights are pilot policies, not learned universal parameters;
4. matched services may still differ in unobserved ways;
5. a 14-day pilot is sufficient for an early operational signal, not long-term causal proof;
6. food composition varies, so kilograms alone do not determine full lifecycle climate impact;
7. operator behavior is part of the system and must be measured rather than treated as noise.

These limitations are why BOUNCAMPUS includes `WITHHOLD`, human approval, explicit provenance and a measured outcome loop.
