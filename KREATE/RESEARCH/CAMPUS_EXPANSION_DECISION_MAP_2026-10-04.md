# Campus Expansion Decision Map — 2026-10-04

**Purpose:** Keep the long-term campus-optimization vision credible without turning the KREATE beachhead into feature sprawl.  
**Status:** Public-source decision mapping. **Every non-food domain remains an unvalidated market hypothesis.**

---

# Executive conclusion

Boğaziçi already has substantial governance and measurement across energy, water, transportation and sustainability.

Therefore BOUNCAMPUS should **not** expand by saying:

> "we will add sensors and dashboards for everything."

The reusable product principle should be:

```text
existing governance/data
        ↓
identify a named unresolved decision
        ↓
measure only the missing state
        ↓
recommend under constraints
        ↓
human act
        ↓
verify result
```

Food remains the KREATE beachhead because it currently offers the clearest repeated decision + short physical feedback loop. The following domains are **adjacent hypotheses only**.

---

# 1. Energy — mature measurement/governance already exists

## Public evidence

Boğaziçi's Climate Action Plan and energy-management pages state that the university:

- operates under an **ISO 50001 Energy Management System**;
- continuously monitors energy use;
- has defined Energy Managers / Building Energy Efficiency responsibilities;
- uses energy-management processes and action plans;
- targets building-efficiency interventions;
- names **optimising the use of space** as an energy/emissions action;
- already has building-management and technical teams in the energy-governance structure.

Sources:

- https://kurumsalveri.bogazici.edu.tr/tr/pages/1332-climate-action-plan-shared/1428
- https://kurumsalveri.bogazici.edu.tr/tr/pages/724-plan-to-reduce-energy-consumption/1367
- https://kurumsalveri.bogazici.edu.tr/tr/pages/722-upgrade-buildings-to-higher-energy-effici/1365

## What this kills

Weak proposition:

> "BOUNCAMPUS shows electricity/gas consumption on a dashboard."

The university already has formal energy measurement/governance.

## Candidate residual decisions to test

- Which building anomaly deserves investigation first?
- Which heating/cooling intervention should be prioritized under a constrained budget?
- Can energy be normalized by weather + occupancy + actual use before judging a building?
- Can underused spaces be consolidated to avoid conditioning lightly occupied buildings?
- Which retrofit generated measured post-intervention savings?

## Hardware implication

**EnergyGateway** should primarily integrate existing commercial meters/BMS/Modbus outputs where needed.

Do **not** custom-build a mains meter to recreate existing metrology.

Add physical sensing only where an identified decision lacks a trustworthy input.

---

# 2. Space/classroom utilization — official optimization goal, operational pain still unvalidated

## Public evidence

The Net Zero action plan explicitly names:

> **optimising the use of space**

and explains that more intensive building use can reduce energy per person.

Source:
https://kurumsalveri.bogazici.edu.tr/tr/pages/1332-climate-action-plan-shared/1428

The university also publicly notes classroom-location reorganization for accessibility where necessary.

Source:
https://kurumsalveri.bogazici.edu.tr/tr/pages/1067-accessible-facilities/1394

## What remains unknown

Public evidence does not establish:

- real classroom occupancy vs scheduled enrollment;
- frequency of empty/underfilled rooms;
- who owns room-allocation changes;
- timetable constraints;
- whether existing scheduling software already optimizes capacity sufficiently;
- whether dynamic room changes are operationally acceptable.

## Candidate decision to test

> **Which classes/activities should be assigned to which rooms/buildings so that space is used intensively without harming schedule, accessibility or student experience?**

Possible sub-decisions:

- room assignment at semester planning;
- consolidating evening/low-load activity into fewer buildings;
- identifying chronic schedule-vs-occupancy mismatch;
- accessibility-aware reassignment;
- choosing which zones can reduce HVAC/lighting hours.

## Hardware implication

**RoomNode / DoorFlow** is justified only if actual occupancy/flow is a missing decision-critical signal.

Existing schedule/enrollment data should be used first.

Preferred physical sensing:

- privacy-preserving radar/ToF/door flow;
- CO2/temp/RH as environmental context, not as a magical exact people counter.

---

# 3. Shuttle mobility — optimization already happens

## Public evidence

Boğaziçi publicly states that:

- free inter-campus shuttle services operate;
- routes and timings are **regularly optimized**;
- route optimization and capacity increases have raised staff-shuttle occupancy;
- shuttle route optimization is part of the Scope-3/commuting action plan.

Sources:

- https://kurumsalveri.bogazici.edu.tr/tr/pages/1141-sustainable-practices-targets/1406
- https://kurumsalveri.bogazici.edu.tr/tr/pages/1332-climate-action-plan-shared/1428

## What this kills

Weak proposition:

> "Universities do not optimize shuttle routes, so our AI will optimize them."

At least Boğaziçi already claims route/timing optimization.

## Candidate residual decisions to test

- Is passenger-load data measured per trip or estimated manually?
- Which departures are chronically overcrowded/underused?
- How often can frequency be changed?
- Are route changes constrained by driver/fleet/contract schedules?
- Can academic-calendar/events predict temporary demand shifts?
- What is the cost/service tradeoff of adding/removing a departure?

## Hardware implication

**Shuttle Passenger Counter** is a P3 validation/measurement device, not the primary product.

If existing ticketing/manual occupancy data are sufficient, integrate them instead.

If not, EE can validate a privacy-preserving in/out counter and uncertainty budget.

---

# 4. Water — formal commission + periodic measurement already exists

## Public evidence

Boğaziçi's Water Management Directive requires:

- water use to be determined and recorded;
- water loss/leak reduction;
- measurement of recovered grey/rain water;
- unit-level responsibilities;
- water consumption/recovery data to be submitted every **three months** to the Water Management Commission;
- commission decision/governance processes.

Official/public sources:

- https://impact.bogazici.edu.tr/1541-water-discharge-guidelines-and-standards
- https://kurumsalveri.bogazici.edu.tr/tr/pages/641-water-reuse-policy/1354

The university already operates grey-water and rainwater recovery systems at specific buildings.

## What this kills

Weak proposition:

> "BOUNCAMPUS creates the university's first water monitoring system."

## Candidate residual decisions to test

- Is quarterly data too slow for leak/anomaly response?
- Which building should be inspected first after abnormal consumption?
- How should irrigation timing respond to season/weather/soil conditions?
- Which grey/rainwater investment should be prioritized?
- Can interventions be verified against normalized baselines?

## Hardware implication

**WaterGateway** should read existing pulse/M-Bus/Modbus/utility-meter outputs where available.

Do not redesign plumbing metrology unless PMR/technical audit finds an actual measurement gap.

---

# 5. Solar / building orientation — validation layer, not standalone market

## Public evidence

Boğaziçi's climate/building plans include:

- energy-efficient building design;
- retrofit/heat-pump/renewable integration;
- rooftop PV investment priority;
- new-building sustainable standards.

Sources:

- https://kurumsalveri.bogazici.edu.tr/tr/pages/1332-climate-action-plan-shared/1428
- https://kurumsalveri.bogazici.edu.tr/tr/pages/1148-planning-development-new-build-standar/1413

## Candidate product role

Solar geometry can support:

- facade/classroom heat/light exposure analysis;
- comparing design orientations;
- validating modeled exposure against physical measurements;
- potential scheduling context where glare/thermal load is genuinely operationally important.

## Hardware implication

**Solar Validation Node** belongs to EE as requested:

- irradiance/illuminance/temp where justified;
- orientation/tilt/placement metadata;
- calibration/error budget.

It validates a model; it does not itself prove HVAC or energy savings.

---

# 6. Food cold chain — adjacent to dining but different causal mechanism

## Candidate decision

> Which refrigeration/storage excursion needs intervention before food becomes unsafe or unusable?

This could reduce spoilage-related food waste, but it is distinct from the production-demand mismatch beachhead.

## Hardware

**Cold-Chain Node**:

- fridge/cold-room temperature;
- door-open duration;
- excursion events;
- timestamp / device health.

## PMR required

- Are excursions/spoilage a material problem?
- Are commercial temperature logs already present?
- Who acts on alarms?
- Is the outcome measurable?

If current refrigeration monitoring already solves the job, do not duplicate it.

---

# 7. Queue / DoorFlow — measurement reusable across decisions

A privacy-preserving directional counter can potentially serve:

- cafeteria arrival flow;
- library/room utilization;
- shuttle boarding areas;
- service queue detection.

But **one sensor should not create four product modules by assumption**.

For each deployment ask:

> What action changes because this count exists?

Examples:

- open another service line;
- release a batch;
- modify next-semester room assignment;
- adjust shuttle departure frequency.

If the action is merely "show a graph," value is weak.

---

# 8. Hardware architecture implication

The reusable infrastructure should be the part that truly generalizes:

```text
Generic Campus Gateway
    ├─ device identity
    ├─ timestamps
    ├─ offline buffering
    ├─ retry/idempotency
    ├─ schema/provenance
    └─ health/connectivity
```

Then domain measurement modules plug in only where evidence requires them:

```text
TrayGate / counters
RoomNode / DoorFlow
ColdChain
EnergyGateway
WaterGateway
Shuttle Counter
Solar Validation
```

This is more defensible than building separate bespoke IoT stacks for each module.

---

# 9. Expansion promotion gate

A new campus domain should not become a product module until all are answered:

1. **Named user** — who makes the decision?
2. **Repeated decision** — how often?
3. **Current process** — what is used today?
4. **Pain/consequence** — what goes wrong?
5. **Action space** — what can realistically change?
6. **Timing** — when must the recommendation arrive?
7. **Measurement** — how do we know the action worked?
8. **Incumbent** — existing BMS/software/operator workflow?
9. **Data gap** — which missing observation actually matters?
10. **Sponsor** — who captures enough value to adopt/pay?

If one of the first seven is missing, do not build hardware/software for that domain yet.

---

# 10. KREATE storytelling consequence

## Primary story

Institutional dining production decision.

## Expansion proof

The architecture is reusable because each future domain follows:

```text
measure only what matters
→ decision under uncertainty
→ human action
→ outcome verification
```

## Do not lead with

- five sensor boxes;
- generic 3D campus map;
- "AI optimizes everything";
- shuttle/energy/water feature lists;
- claims that current university governance is absent.

The public evidence shows the opposite: significant governance already exists. The opportunity, if validated, is **better operational decisions on top of it**.
