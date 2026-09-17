# BOUNCAMPUS — KREATE for Climate Pitch

## One sentence

> **BOUNCAMPUS is an AI-assisted climate operations layer that helps campuses identify, stress-test and validate building energy-saving actions before waste becomes emissions.**

The beachhead problem is **avoidable campus building energy use**. The current product combines schedule-derived occupancy, weather and building context, produces a human-reviewable intervention candidate, stress-tests it, and learns from measured pilot outcomes.

---

## Opening — 20 seconds

> University buildings can remain fully conditioned and lit even when academic demand has fallen sharply. Operators rarely have one decision layer that says which building, which time window and which intervention is worth testing safely.
>
> **The climate problem is avoidable building energy use and the emissions attached to it.**

BOUNCAMPUS turns campus signals into a concrete, reviewable energy decision.

---

## Product — 25 seconds

> BOUNCAMPUS combines the course schedule, weather and building context to estimate low-use windows and surface energy interventions.
>
> Every recommendation includes:
>
> - where and when;
> - why now;
> - source provenance;
> - confidence;
> - modeled impact;
> - counterfactual stress testing;
> - and a human approval boundary.

The product never upgrades a model estimate into “live sensor data.”

---

## The product loop

```text
SENSE → DECIDE → STRESS-TEST → HUMAN APPROVAL → PILOT → LEARN
```

### 1. Sense

Core KREATE inputs:

- dated official-source BUIS/ÖBİKAS course schedule snapshot;
- Open-Meteo weather at Bebek campus coordinates;
- building metadata and source-backed / explicitly-fallback geolocation.

Other public campus feeds may remain contextual, but they are not part of the primary climate claim.

### 2. Decide

The product estimates where academic demand is low enough to justify reviewing an HVAC / lighting / space-consolidation intervention.

Machine-readable mission endpoint:

```text
GET /api/v1/brief
```

### 3. Stress-test

The jury scenario is intentionally narrow:

- baseline campus conditions;
- then a **38°C heatwave** counterfactual.

The goal is to show that an intervention is not static. Outdoor conditions can change cooling demand and therefore change whether the same action remains valuable or safe.

### 4. Human approval

BOUNCAMPUS does not dispatch a BMS command.

A decision can only move through review states such as:

- REVIEW
- APPROVED_FOR_PILOT
- DECLINED

### 5. Pilot

A real pilot requires field verification and an accountable facilities decision.

Minimum calibration feeds:

1. building / floor smart-meter totals;
2. anonymous aggregate occupancy counts.

### 6. Learn

The Outcome Loop compares expected and measured kWh, computes model error, and records calibration evidence for the next decision.

---

## 90-second jury demo

Open `/demo`.

### Screen 1 — Problem + evidence

Show only the climate-relevant evidence:

1. course schedule snapshot;
2. Bebek weather.

Say:

> The schedule is a demand signal, not a live occupancy sensor. Weather is external live context, not a connected BMS. Every source keeps its provenance.

### Screen 2 — Energy decision

Show the top energy intervention candidate.

Point to:

- location;
- operating window;
- confidence;
- modeled impact;
- human guardrail.

Say:

> This is modeled potential, not measured savings.

### Screen 3 — Heatwave stress test

Run **38°C heatwave**.

Say:

> The same decision is recomputed under higher cooling demand. We want the operator to challenge the recommendation before acting.

### Screen 4 — Pilot + learning

Open `/decisions` and the Outcome Loop.

Say:

> A real pilot closes the loop with smart-meter and aggregate occupancy data: expected kWh versus measured kWh, model error and recalibration.

---

## 30-day pilot

| Week | Goal |
|---|---|
| 1 | Read-only smart-meter + aggregate occupancy integration |
| 2 | Calibrate schedule-derived occupancy and building energy model |
| 3 | Small human-approved intervention pilot |
| 4 | Compare expected vs measured kWh and document operator feedback |

Validation gates — **targets, not current claims**:

- schedule-derived occupancy model: ≤20% MAPE after calibration;
- energy pilot: positive measured kWh savings for a qualifying intervention;
- model calibration: expected vs measured outcome recorded for every pilot;
- operator usefulness: ≥70% of surfaced energy missions accepted or rated useful.

---

## What stays secondary

### Food waste

A valid second use case because schedule + weather + menu can support demand forecasting. It requires POS totals for real calibration. It is not co-equal with the KREATE building-energy story.

### Water and mobility

Roadmap only until trustworthy field feeds exist. No cistern level, greywater flow, leak, sensor-count, savings, shuttle-GPS or similar operational claim is presented without a real source.

---

## Why this can scale

The product starts with universities because schedules provide a strong demand signal and campuses have multiple buildings under one operator.

The same decision architecture can later extend to:

- hospitals;
- office campuses;
- public facilities;
- industrial sites.

The reusable moat is not one model. It is the decision system around the model:

- source provenance and graceful degradation;
- schedule-to-space demand modeling;
- building-level decision ranking;
- counterfactual stress testing;
- human approval ledger;
- measured-outcome calibration loop;
- privacy-safe read-only pilot integration.

---

## Truth boundary

Today BOUNCAMPUS **does not claim** direct access to:

- BMS;
- smart meters;
- turnstiles;
- Wi-Fi occupancy;
- cafeteria POS;
- shuttle GPS;
- live IoT telemetry.

Occupancy, energy, savings and CO₂ values are model estimates until calibrated against authorized operational data.

---

## Closing — 15 seconds

> Campuses do not need another sustainability dashboard.
>
> They need a decision layer that identifies a specific energy intervention, lets an operator challenge it, and proves the result with measured data.
>
> **BOUNCAMPUS: Sense. Decide. Stress-test. Pilot. Learn.**
