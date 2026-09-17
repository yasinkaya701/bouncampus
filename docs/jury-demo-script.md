# BOUNCAMPUS — 90-Second KREATE Jury Demo

## One-line product

**BOUNCAMPUS is an AI-assisted climate operations layer for reducing avoidable campus building energy use.**

It combines schedule-derived occupancy, weather and building context to surface a reviewable intervention, stress-test it, keep a human approval gate and learn from measured pilot outcomes.

## 0–15s — Climate problem

> University buildings can keep consuming HVAC and lighting energy after academic demand has dropped. The operator problem is not another dashboard; it is knowing which building, which time window and which intervention is worth testing safely.

Show the homepage headline and 3D campus.

Say:

> BOUNCAMPUS turns that low-use window into a climate operations decision.

## 15–35s — Evidence

Open **KREATE Demo**.

Show only:

1. BUIS/ÖBİKAS schedule snapshot
2. Bebek weather

Say:

> The schedule is a demand signal, not a live occupancy sensor. Weather is external context, not a connected BMS. Every input keeps its provenance and freshness state.

## 35–55s — Energy decision

Point to the energy intervention candidate.

Say:

> The system identifies a building and operating window where lower academic demand may justify reducing conditioned or lit space. It shows confidence and modeled impact, but it does not call that impact measured savings.

Point to:

- building / location
- operating window
- confidence
- modeled impact
- human guardrail

## 55–72s — 38°C stress test

Run **38°C heatwave**.

Say:

> Now we deliberately try to break the recommendation. Cooling demand changes, so the energy and carbon result changes too. The intervention is recomputed rather than shown as a canned before/after slide.

## 72–82s — Human approval

Open **Decisions**.

Say:

> The model cannot dispatch a BMS command. A facilities operator validates the field condition and decides whether the recommendation is suitable for a pilot.

## 82–90s — Measured pilot

Point to the Outcome Loop.

Say:

> The pilot closes the loop with smart-meter and anonymous aggregate occupancy data: expected kWh, measured kWh, model error and calibration for the next decision.

Close with:

> **One climate problem, one measurable loop: Sense → Decide → Stress-test → Approve → Pilot → Learn.**

# Judge questions

## “Is the occupancy live?”

No. It is schedule-derived and explicitly a model estimate. A real pilot would calibrate it with anonymous aggregate occupancy counts.

## “Are you connected to BMS or smart meters?”

No. The current product is decision support. Read-only smart-meter integration is part of the pilot; automatic control is not required to prove value.

## “So what is real today?”

The architecture, source-provenance layer, course-schedule snapshot, public/external weather context, building context, decision workflow, counterfactual simulation, human approval boundary and outcome-calibration workflow are implemented. Energy and CO₂ impact remain modeled until a field pilot measures them.

## “Why not show water, solar, transit and everything else?”

Because KREATE rewards a real climate problem, not feature count. We intentionally removed mock-heavy first-class surfaces and focus the jury story on avoidable building energy use. Food waste remains a secondary expansion use case; water and mobility stay roadmap items until trustworthy operational feeds exist.

## “What data do you need for the first real pilot?”

Minimum useful feeds:

1. building / floor smart-meter totals
2. anonymous aggregate occupancy counts

These are enough to compare expected and measured kWh without requiring raw student identity.

## “Why is this defensible?”

The defensibility is the decision system around the model:

- source provenance + degradation contract
- schedule-to-space demand model
- building-level decision ranking
- counterfactual stress testing
- human approval ledger
- measured-outcome calibration loop
- privacy-safe read-only pilot pattern

## “Where does this scale?”

University campuses are the beachhead. The same architecture can later serve hospitals, office campuses, public facilities and industrial sites where occupancy, weather and operational context affect building energy demand.
