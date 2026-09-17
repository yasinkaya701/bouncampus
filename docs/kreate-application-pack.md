# KREATE for Climate — BOUNCAMPUS Application Pack

## One-line product

**BOUNCAMPUS turns measured institutional food waste into an uncertainty-aware, human-approved production decision, then uses a controlled pilot to prove whether the intervention actually reduced waste.**

## Problem

Boğaziçi University publicly reports **48,251 kg of food waste for 2025**. A meaningful part of the campus sustainability challenge therefore sits before composting or recovery: how much food should be prepared for the next service when demand is uncertain?

Today the operational decision can be made with incomplete context. A quiet service can make raw waste kilograms look artificially good, while overproduction can increase waste and aggressive underproduction can increase early sell-out risk. The missing layer is a decision system that combines campus context, exposes uncertainty, keeps the operator in control, and measures whether the intervention worked.

## Solution

BOUNCAMPUS is a food-waste prevention decision layer for campus dining operations.

The release follows this loop:

1. **Official baseline** — start from the university's public food-waste history.
2. **Context health** — verify course schedule, weather, menu and academic-calendar availability.
3. **Demand band** — produce a planning band rather than a false single-number certainty.
4. **Decision readiness** — classify the recommendation as `PILOT_READY`, `REVIEW_REQUIRED`, or `WITHHOLD`.
5. **Human gate** — an operator reviews the recommendation; automatic kitchen dispatch is disabled.
6. **Controlled pilot** — compare matched CONTROL and INTERVENTION services over 14 days.
7. **Measured scorecard** — use normalized waste, early-sellout and operational guardrails.
8. **Learn** — only measured evidence is allowed to support impact claims.

## Why it is climate tech

Food waste embeds agricultural inputs, water, energy, logistics and disposal impacts. BOUNCAMPUS targets **prevention at the production-decision stage**, before waste is created. It does not count recovery or composting as equivalent to prevention.

The product deliberately does **not** claim CO2 or water savings before a measured pilot exists. Climate accounting is a second step after the operational effect is measured.

## Innovation

The novelty is not another dashboard or a more complex forecasting model. It is the **closed-loop decision and evidence contract**:

- source health is visible,
- uncertainty changes the operating band,
- missing critical context can force `WITHHOLD`,
- human approval is mandatory,
- success criteria are pre-registered,
- normalized waste is measured against a control arm,
- an intervention can fail,
- the AI cannot declare its own success.

## Current evidence

What is real now:

- 2024 and 2025 public food-waste totals,
- 2025 monthly food-waste/recovery history,
- public dining-service context,
- a working decision-readiness engine,
- a human approval gate,
- a measured-pilot score engine,
- a strict CSV field-measurement workflow,
- a fail-safe jury/demo mode that withholds operational advice if live context is unavailable.

What is **not** claimed yet:

- actual food waste saved by BOUNCAMPUS,
- actual CO2 saved,
- actual water saved,
- actual cafeteria production optimized,
- validated POS-level demand accuracy.

## Pilot design

**Duration:** 14 days  
**Design:** matched CONTROL vs INTERVENTION services  
**Primary KPI:** `waste kg / 100 served meals`  
**Minimum evidence:** at least 5 measured services per arm  
**Pre-registered target:** at least 10% lower normalized waste in INTERVENTION vs CONTROL  
**Service guardrail:** early-sellout incidence must not increase  
**Safety guardrail:** no food-safety process may be bypassed  
**Privacy:** no personal/student-level data is required

The 10% figure is a **pilot target, not an achieved result**.

## Why normalize by served meals?

Raw kilograms per service are confounded by service volume. A low-attendance day may show fewer kilograms of waste without any operational improvement. The primary KPI therefore normalizes waste by the number of served meals.

## Technical approach

The hackathon release uses a transparent signal-weight contract:

- course schedule: 50%
- weather: 20%
- menu context: 20%
- academic calendar: 10%

The course schedule is the backbone signal. Context coverage controls readiness and band width. When the backbone or sufficient context is missing, the system can refuse to recommend a production number.

This is intentionally more defensible than describing an unvalidated black-box model as production-ready.

## Target users

Initial operator:

- university dining-service operations,
- sustainability offices,
- campus facility/operations teams.

The first user is **not** an individual student. BOUNCAMPUS is an institutional decision layer.

## Scalability

The core contract is portable to other institutional kitchens:

`historical waste + service context + operator gate + matched pilot + normalized measurement`

The model adapters can change by institution while the safety and evidence contract remains stable.

Expansion modules already exist for energy, mobility and campus spatial context, but they are intentionally secondary to the food-waste wedge during KREATE.

## Why BOUNCAMPUS can win KREATE

BOUNCAMPUS combines four properties that are often separated:

1. **A real, quantified climate problem** backed by the institution's own data.
2. **A working technology product** rather than a slide-only idea.
3. **Operational safety** through uncertainty and human approval.
4. **Falsifiability** through a pilot capable of returning `FAILED`.

## What we want from the accelerator

The next milestones are not “more dashboard features.” They are:

1. secure a dining-operation pilot partner,
2. connect actual production/served-meal telemetry where available,
3. execute the 14-day matched pilot,
4. audit measurement quality and food-safety workflow,
5. calibrate demand bands against measured service data,
6. calculate climate impact only after waste reduction is measured,
7. replicate the operating contract at a second campus.

## 15-second answer

> BOUNCAMPUS starts from a real 48-ton food-waste baseline, turns campus context into an uncertainty-aware production band, keeps a human in control, and has a pre-registered 14-day pilot that can prove the product wrong. We are building the decision layer before the waste happens, not another dashboard after it does.

## 45-second answer

> Boğaziçi University publicly reported 48,251 kilograms of food waste in 2025. We focus on a decision made before that waste exists: how much should be prepared for the next meal service? BOUNCAMPUS combines course schedules, weather, menu and academic-calendar context into a demand band, but it also scores whether the context is good enough to act. If it is not, the system says WITHHOLD. A human operator always remains in control. Then we run a matched 14-day CONTROL versus INTERVENTION pilot using waste kilograms per 100 served meals, with a pre-registered 10% target and an early-sellout guardrail. The model cannot declare victory; measured evidence does.

## Common judge questions

### “Is this just forecasting?”
No. Forecasting is one component. The product value is the operating contract around the forecast: source health, uncertainty, readiness, human approval, pilot measurement and a claim firewall.

### “Why not just use last week's meal count?”
That is a valid baseline and should be compared in pilot calibration. BOUNCAMPUS earns its place only if context-aware decisions outperform a simpler baseline without increasing service risk.

### “Where is the AI?”
The product converts heterogeneous campus signals into an operational demand estimate and decision band. We intentionally keep the current method transparent until measured cafeteria data justifies a more complex model.

### “Why do you need a human?”
Because an unvalidated model should not autonomously change food production. Human approval is a product feature, not a temporary weakness.

### “What happens when APIs fail during the demo or in production?”
The official historical baseline remains available, but operational advice falls back to `WITHHOLD`. The system does not fabricate live context or silently reuse stale values as if they were current.

### “Have you already reduced waste by 10%?”
No. Ten percent is the pre-registered pilot target. The product explicitly labels it `TARGET_NOT_RESULT`.

### “How do you stop the model gaming waste by underproducing?”
The pilot has an early-sellout guardrail. Waste reduction cannot be called promising if service availability deteriorates.

### “What would prove you wrong?”
If the intervention does not reduce normalized waste by the pre-registered threshold, increases early sell-outs, violates food-safety review, or fails to outperform a simpler baseline, we should not scale it.
