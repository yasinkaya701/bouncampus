# BOUNCAMPUS — KREATE Winning Product Contract

## 1. One problem

**Avoidable institutional food waste caused by demand uncertainty and overproduction.**

For the KREATE demo, BOUNCAMPUS does not pitch itself as a generic smart-campus platform. The wedge is campus dining operations.

Boğaziçi University's official 2025 baseline is the opening evidence:

- 48,251 kg total food waste;
- 33,430 kg sent to İSTAÇ for recovery;
- 50,993 kg total food waste in 2024;
- six dining campuses and 1,734 published dining-hall capacity.

Source: https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

## 2. One promise

> BOUNCAMPUS recommends a safe production band for the next service and proves success with waste kg per service.

This is stronger than “AI predicts demand” because the product ends in an operational measurement loop.

## 3. Product loop

```text
official waste baseline
        ↓
next-service demand context
        ↓
production band recommendation
        ↓
human operator approval
        ↓
service executes
        ↓
produced / served / edible surplus / waste kg
        ↓
model recalibration
```

## 4. Truth boundary

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
- prevention/recovery scenarios.

### Not available today

- POS transactions;
- actual produced portions;
- actual served portions;
- plate-level waste;
- kitchen inventory telemetry.

The UI must never blur these three classes.

## 5. 90-second jury choreography

### 0–20 s — prove the problem

Open `/demo`.

Say:

> “Boğaziçi already measures the problem: 48,251 kg of food waste in 2025. We are not inventing the climate problem; we are operationalizing it.”

Open the official source if challenged.

### 20–45 s — show the decision

Show the next-service model band.

Say:

> “We combine schedule, academic-calendar, weather and menu context to estimate demand. We do not tell the kitchen a magic number; we propose a conservative band and require an operator decision.”

Point at the `MODEL_ESTIMATE` label.

### 45–65 s — stress-test

Move the prevention slider.

Say:

> “This is not claimed savings. It is the pilot target applied to the official historical baseline, so the operator can understand the scale of a decision before trying it.”

### 65–90 s — prove the path to impact

Show the 14-day pilot.

Say:

> “We only need four measurements per service: produced, served, edible surplus and waste kg. The KPI is waste kg per service. If it does not fall against control, our hypothesis fails.”

Close with:

> “The 48-ton problem is already known. BOUNCAMPUS moves from reporting it to preventing the next kilogram and measuring the result.”

## 6. What not to show first

Do not lead with:

- 3D buildings;
- shuttle routing;
- generic AI assistant;
- energy scenarios;
- long feature lists;
- unsupported CO₂ or water-equivalent claims;
- fake kitchen dispatch buttons.

These can be shown only after the core food-waste story lands.

## 7. Why the platform can scale

The same operating loop transfers to:

- hospitals;
- factory cafeterias;
- schools;
- municipal kitchens;
- large catering operators.

The transferable asset is not the campus UI. It is the decision loop:

```text
forecast → recommend → approve → measure → learn
```

## 8. Pilot acceptance criteria

A 14-day pilot is successful only if all are true:

1. control and intervention services are comparable;
2. produced and served portions are recorded for every pilot service;
3. edible surplus and waste kg are measured consistently;
4. operator overrides are logged;
5. intervention waste kg/service is compared with control;
6. forecast error and overproduction rate are reported;
7. no impact claim is promoted from model estimate to measured impact before pilot evidence exists.

## 9. Hackathon product hierarchy

### Primary

- `/`
- `/food-waste`
- `/demo`
- `/api/v1/food`
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

## 10. Final pitch sentence

**BOUNCAMPUS is the decision layer that turns measured institutional food waste into a human-approved production recommendation and a measurable next-service outcome.**
