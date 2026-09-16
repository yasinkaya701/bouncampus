# BOUNCAMPUS — Hackathon Pitch

## One sentence

> **BOUNCAMPUS is the decision layer between campus public data and real operations.**

It turns disconnected Boğaziçi signals into a source-traceable operational mission, stress-tests that mission, keeps a human approval gate, and learns from pilot outcomes.

---

## Opening — 20 seconds

> Boğaziçi already publishes useful operational context: the course schedule, cafeteria menu, shuttle timetable and academic calendar. Weather is available too.
>
> The problem is not that there is zero data. The problem is that these signals live in separate systems and none of them answers one operational question:
>
> **What should the campus do differently today?**

---

## Product — 25 seconds

> BOUNCAMPUS is Mission Control for campus operations.
>
> It fuses source-traceable public signals with transparent demand and energy models, then creates one human-reviewable mission with:
>
> - why now;
> - where and when;
> - evidence;
> - confidence;
> - modeled impact;
> - and a clear human-control boundary.

The product never upgrades a model estimate into “live sensor data.”

---

## The product loop

```text
SENSE → DECIDE → STRESS-TEST → HUMAN APPROVAL → PILOT → LEARN
```

### 1. Sense

Current product inputs:

- Boğaziçi SKS public menu;
- Boğaziçi Mekik public timetable;
- Boğaziçi Academic Calendar;
- dated official-source BUIS/ÖBİKAS course schedule snapshot;
- Open-Meteo weather at Bebek campus coordinates.

### 2. Decide

The Mission Brief converts the current campus state into one inspectable recommendation with confidence and evidence.

Machine-readable endpoint:

```text
GET /api/v1/brief
```

### 3. Stress-test

Before a human acts, the same live product baseline can be recomputed under counterfactuals such as:

- heavy rain;
- heatwave;
- exam week;
- event load;
- building closure.

### 4. Human approval

The model cannot dispatch a BMS, kitchen, transport or IoT command.

The decision ledger records only a review state:

- REVIEW
- APPROVED_FOR_PILOT
- DECLINED

### 5. Pilot

A real-world action happens only after field verification and an accountable operator decision.

### 6. Learn

The Outcome Loop accepts an observed pilot result and compares it with modeled potential, creating calibration evidence for the next decision.

---

## 90-second demo

Open `/demo`.

### Screen 1 — Signal fusion

Show the four evidence cards and source readiness.

Say:

> Every signal has provenance and freshness. If a public page fails, BOUNCAMPUS can show a dated last-known-good official snapshot for continuity, but the product becomes degraded rather than pretending that snapshot is live.

### Screen 2 — Decision

Show the current Mission Brief.

Point to:

- confidence;
- why now;
- location and operating window;
- modeled impact;
- human guardrail.

### Screen 3 — Stress test

Run Heavy Rain or Heatwave 38°C.

Say:

> This starts from the current BOUNCAMPUS baseline; it is not a canned before/after slide.

### Screen 4 — Human approval

Click **Approve for pilot review**.

Say:

> Approval creates a decision receipt. It does not send a field command.

Then open `/decisions` and show the Outcome Loop:

> After a real pilot we enter the measured result, calculate model error and improve the next mission.

---

## Why this can become a real university product

BOUNCAMPUS does not require replacing existing university software.

It can begin as a read-only layer above current systems.

Highest-value production calibration feeds:

1. anonymous occupancy aggregates;
2. building/floor smart-meter totals;
3. anonymized cafeteria POS totals by time bucket;
4. shuttle AVL/GPS.

No raw student identity is necessary for the core optimization loop.

---

## 30-day pilot

| Week | Goal |
|---|---|
| 1 | Read-only aggregate integrations |
| 2 | Model calibration against measured data |
| 3 | Small human-approved operator pilot |
| 4 | Outcome proof and operator feedback |

Proposed validation gates — **targets, not current claims**:

- occupancy model: ≤20% MAPE;
- food-demand model: ≤15% MAPE;
- energy pilot: measured positive savings under a qualifying intervention;
- operator usefulness: ≥70% of surfaced missions accepted or rated useful.

---

## Why this is defensible

The moat is not “we trained one model.”

It is the system around decisions:

- Boğaziçi-specific source adapters;
- provenance and freshness contract;
- graceful degradation without fake live data;
- schedule-to-space demand model;
- mission ranking and confidence;
- counterfactual stress testing;
- human approval ledger;
- outcome calibration loop;
- privacy-safe pilot integration pattern.

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

Occupancy, energy, food demand, savings and CO₂ values are model estimates until calibrated against authorized operational data.

---

## Closing — 15 seconds

> Universities do not need another dashboard telling them what already happened.
>
> They need a decision layer that turns fragmented signals into an action a human can understand, challenge, test and measure.
>
> **BOUNCAMPUS: Sense. Decide. Pilot. Learn.**
