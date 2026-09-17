# BOUNCAMPUS — KREATE Winning Product Contract

## 1. One climate problem

**Avoidable institutional food waste caused by demand uncertainty and overproduction.**

For KREATE, BOUNCAMPUS does not pitch itself as a generic smart-campus platform. The primary wedge is campus dining operations because it has:

- a real institutional baseline;
- a repeated operational decision;
- a short pilot cycle;
- a direct physical KPI;
- a clear path to other institutional kitchens.

Boğaziçi University's official opening evidence:

- **48,251 kg** total food waste in 2025;
- **33,430 kg** sent to İSTAÇ for recovery in 2025;
- **50,993 kg** total food waste in 2024;
- six dining campuses and published dining capacity.

Source: https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

## 2. One product promise

> **BOUNCAMPUS converts source-backed campus context into an uncertainty-aware production band, keeps a human operator in control, and proves or rejects the intervention in a matched pilot.**

This is stronger than “AI predicts demand” because the product ends in an operational evidence loop and can deliberately refuse to recommend when context is weak.

## 3. Product loop

```text
official waste baseline
        ↓
source health + demand context
        ↓
production band + signal coverage
        ↓
PILOT_READY / REVIEW_REQUIRED / WITHHOLD
        ↓
human operator approval / edit / hold
        ↓
matched control/intervention service
        ↓
normalized waste + service guardrails
        ↓
model recalibration
```

## 4. Decision-readiness contract

Every production band exposes:

- `predictedMeals`;
- `lowerBound`;
- `recommendedTarget`;
- `upperBound`;
- `signalCoveragePct`;
- `decisionReadiness`;
- source-level availability;
- missing-context reason codes;
- `provenance=MODEL_ESTIMATE`;
- `operatorApprovalRequired=true`;
- `autoDispatchAllowed=false`.

Readiness states:

### `PILOT_READY`

Enough current context exists to show an operator-reviewed recommendation in a controlled pilot.

It **does not** mean the model is validated against cafeteria POS or historical production telemetry.

### `REVIEW_REQUIRED`

Core context exists, but missing signals increase uncertainty. Operator review is mandatory and the band should be treated cautiously.

### `WITHHOLD`

Critical decision context is missing. The product must not recommend operational use.

The ability to say “do not act” is a required product feature, not an error state.

## 5. Truth boundary

### Official/public evidence

- annual and monthly food-waste baseline;
- official dining-service scale/capacity;
- public menu;
- public academic calendar;
- dated public course schedule snapshot;
- external weather.

### Model estimates

- next-service meal demand;
- production planning band;
- decision readiness derived from source availability;
- prevention/recovery scenarios.

### Not available today

- cafeteria POS transactions;
- actual produced portions;
- actual served portions;
- plate-level waste;
- kitchen inventory telemetry.

The UI and API must never blur these classes.

## 6. Claim firewall

### Allowed before pilot

- official baseline;
- current source health;
- model-estimated demand band;
- readiness state;
- scenario values explicitly labeled as scenarios;
- pre-registered pilot target and formulas.

### Forbidden before measured evidence

- achieved food-waste savings;
- achieved CO2 savings;
- achieved water savings;
- actual cafeteria optimization;
- actual student demand observation.

Any future CO2/water conversion requires measured food-waste reduction and a documented lifecycle factor.

## 7. 14-day pilot

Design: matched `CONTROL` vs `INTERVENTION` services.

Required fields:

1. date;
2. service ID;
3. arm;
4. model forecast meals;
5. produced portions;
6. served portions;
7. edible surplus kg;
8. waste kg;
9. early sell-out;
10. operator override;
11. notes.

No personal data is required.

Downloadable template:

```text
GET /api/v1/food/pilot-template
```

## 8. Primary KPI

**Waste kg per 100 served meals**:

```text
(waste_kg / served_portions) * 100
```

This replaces `waste kg / service` as the primary KPI because raw waste per service is confounded by service volume.

Secondary metrics:

- waste kg / service;
- overproduction rate;
- edible surplus kg / 100 served;
- forecast absolute percentage error;
- operator override rate;
- early-sellout incidence.

## 9. Pre-registered pilot gate

A promising pilot requires:

1. at least **5 measured services per arm**;
2. at least **10% lower normalized waste** versus matched control;
3. no increase in early-sellout incidence;
4. no food-safety process bypass;
5. comparable measurement quality across arms;
6. operator overrides reported instead of silently excluded.

The **10% threshold is a target, not a current result**.

If the target is missed, service degrades, or evidence quality is weak, the result must be reported as `FAILED` or `INCONCLUSIVE` rather than reframed as success.

## 10. 90-second jury choreography

### 0–18 s — PROBLEM

Open `/demo`.

> “Boğaziçi already measures the problem: 48,251 kg of food waste in 2025. The first number you see is not generated by our model.”

### 18–40 s — DECISION

Show production band, source coverage and readiness.

> “We do not output a magic number. The recommendation carries its own evidence quality. Missing context widens uncertainty; insufficient context becomes WITHHOLD.”

### 40–55 s — HUMAN GATE

Press approve/hold.

> “AI never dispatches to the kitchen. A human accepts, edits or holds. Even this demo does not fake an external kitchen integration.”

### 55–70 s — SCENARIO

Move the prevention/recovery sliders.

> “This is scenario math on the official baseline—not achieved savings.”

### 70–90 s — EVIDENCE

Show the normalized KPI and CSV template.

> “We pre-register failure. Less than 10% normalized reduction, more early sell-out, or weakened food-safety process means we do not call the pilot successful.”

Close:

> **“The model does not declare victory. The measured pilot does.”**

## 11. What not to show first

Do not lead with:

- 3D buildings;
- shuttle routing;
- generic AI assistant;
- energy scenarios;
- long feature lists;
- unsupported CO2 or water-equivalent claims;
- fake kitchen dispatch buttons.

These are expansion capabilities only after the core food-waste story lands.

## 12. Why the platform can scale

The transferable asset is the operating contract:

```text
sense → quantify uncertainty → recommend → approve → measure → learn
```

Potential environments:

- hospitals;
- factory cafeterias;
- schools;
- municipal kitchens;
- large catering operators.

The signal mix changes by site, but provenance, readiness, human control and evidence rules remain reusable.

## 13. Hackathon product hierarchy

### Primary

- `/`
- `/food-waste`
- `/demo`
- `/api/v1/food`
- `/api/v1/food/pilot-template`
- `/data`

### Supporting

- `/decisions`
- `/courses`
- campus map / 3D context

### Expansion, not the pitch

- building energy;
- scenario workspace;
- shuttle mobility;
- prototype lab.

## 14. What the accelerator should fund next

1. first cafeteria pilot partner;
2. stable service-level measurement process;
3. calibration with real produced/served data;
4. matched 14-day pilot;
5. second-site replication;
6. only after measured reduction: documented climate-equivalent accounting.

## 15. Final pitch sentence

**BOUNCAMPUS is the human-controlled decision layer that acts before institutional food becomes waste and uses measured evidence—not demo claims—to prove climate impact.**
