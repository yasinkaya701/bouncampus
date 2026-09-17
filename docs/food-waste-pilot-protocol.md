# BOUNCAMPUS Food-Waste Pilot Protocol v1.0

This protocol turns the hackathon demo into a falsifiable field test. It is deliberately designed so BOUNCAMPUS can fail: a model estimate is not promoted to climate impact until measured operational evidence passes the gate below.

## 1. Hypothesis

**An operator-reviewed next-service production band, informed by campus demand context, reduces normalized food waste without increasing early sell-out risk or bypassing food-safety processes.**

The intervention is decision support, not autonomous kitchen control.

## 2. Pilot design

- Duration: **14 days**.
- Design: matched **CONTROL vs INTERVENTION** services.
- Minimum evidence: **5 measured services per arm** before a success decision.
- Unit of analysis: one dining service, not one student.
- Personal data: **none required**.
- Intervention arm: operator sees BOUNCAMPUS demand band and may approve, edit or hold it.
- Control arm: normal planning process; BOUNCAMPUS recommendation is not used operationally.

Whenever possible, match services on weekday, meal period, campus and broad menu type. Do not compare a quiet weekend breakfast against a high-volume weekday lunch and call the difference model impact.

## 3. Required measurements

Each service records:

| Field | Unit | Why it exists |
|---|---:|---|
| `date` | date | temporal matching |
| `service_id` | text | traceable service identifier |
| `arm` | CONTROL / INTERVENTION | causal comparison |
| `model_forecast_meals` | portions | forecast error / calibration |
| `produced_portions` | portions | production decision |
| `served_portions` | portions | normalize waste by actual service volume |
| `edible_surplus_kg` | kg | distinguish recoverable surplus |
| `waste_kg` | kg | primary waste measurement |
| `early_sellout` | boolean | service-level guardrail |
| `operator_override` | boolean | human-in-the-loop behavior |
| `notes` | text | anomalies: event, outage, menu issue, measurement issue |

The downloadable template is exposed at:

```text
GET /api/v1/food/pilot-template
```

## 4. Primary KPI

The primary KPI is **waste kg per 100 served meals**:

```text
waste_kg_per_100_served = (waste_kg / served_portions) * 100
```

Why not only `waste kg / service`?

Because service volumes vary. A low-demand service can produce less total waste even when the operating decision is worse. Normalizing by served volume makes the control/intervention comparison more defensible.

## 5. Secondary metrics

### Overproduction rate

```text
overproduction_rate = max(0, produced_portions - served_portions) / produced_portions
```

### Edible surplus intensity

```text
edible_surplus_kg_per_100_served = (edible_surplus_kg / served_portions) * 100
```

### Forecast absolute percentage error

```text
forecast_ape = abs(model_forecast_meals - served_portions) / served_portions
```

### Operator override rate

```text
override_rate = overridden_intervention_services / measured_intervention_services
```

Override is not automatically a failure. It is evidence about model usefulness, workflow fit and confidence calibration.

## 6. Pre-registered success gate

The pilot is considered promising only when all of the following are true:

1. at least **5 measured services per arm** exist;
2. intervention mean `waste kg / 100 served meals` is at least **10% lower** than matched control;
3. early-sellout incidence does **not increase** versus control;
4. no food-safety process is bypassed by a model recommendation;
5. no missing-data pattern makes the control/intervention comparison misleading;
6. the team reports operator overrides instead of silently excluding them.

The **10% value is a pilot target, not a claimed achieved reduction**.

## 7. Failure states

The pilot fails or remains inconclusive when any of these occur:

- waste reduction target is not met;
- early sell-out increases materially;
- measurement quality is inconsistent between arms;
- service matching is obviously invalid;
- the operator must override most recommendations because the band is operationally unusable;
- food-safety or operational rules would need to be weakened to follow the recommendation;
- insufficient measured services exist.

A failed pilot is still useful: it identifies whether the problem is forecast quality, signal availability, workflow fit, or an invalid product assumption.

## 8. Decision-readiness policy

BOUNCAMPUS exposes a readiness state together with every production band:

- `PILOT_READY` — course-schedule backbone exists and contextual signal coverage is sufficient for an operator-reviewed pilot recommendation.
- `REVIEW_REQUIRED` — recommendation may be inspected, but missing context increases uncertainty.
- `WITHHOLD` — decision context is insufficient; the system must not recommend operational use.

`PILOT_READY` does **not** mean validated against POS or historical production telemetry. It means the current source set is sufficient to test safely with a human operator.

## 9. Claim firewall

Before measured pilot evidence, BOUNCAMPUS may say:

- the official historical waste baseline;
- what public/live/model sources are available;
- what demand band the model estimates;
- what scenario a selected target would imply;
- what the pre-registered pilot target is.

Before measured pilot evidence, BOUNCAMPUS must **not** say:

- “we saved X kg of food”;
- “we avoided Y kg CO2”;
- “we saved Z liters of water”;
- “we optimized actual cafeteria production”;
- “we observe actual student demand.”

Any future carbon or water conversion must use a documented, context-appropriate LCA factor and remain separate from the directly measured food-waste KPI.

## 10. Suggested 14-day operating sequence

### Days 1–2 — instrument and rehearse

- weigh waste consistently;
- confirm portion counting process;
- train operator on approve/edit/hold states;
- verify the CSV/data-entry workflow.

### Days 3–6 — establish matched control evidence

- collect normal-operation services;
- flag unusual events in `notes`;
- do not retroactively discard inconvenient control observations.

### Days 7–12 — intervention evidence

- show the production band;
- record operator decision and override;
- measure the same fields using the same process as control.

### Days 13–14 — repeat weak pairs and review quality

- repeat poorly matched services if operationally possible;
- calculate primary and secondary metrics;
- classify the result as `PROMISING`, `FAILED`, or `INCONCLUSIVE`.

## 11. Hackathon jury interpretation

The demo should never pretend these measurements already exist. The winning story is stronger when it says:

> We know exactly what would prove us wrong, we know exactly what to measure on day one, and the product already exposes the evidence boundary required to run that test safely.
