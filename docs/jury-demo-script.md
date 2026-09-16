# BOUNCAMPUS — 90-Second Jury Demo

## One-line product

**BOUNCAMPUS is the decision layer between campus public data and real operations.**

It turns disconnected public university signals into source-traceable operational missions, stress-tests them, keeps a human approval gate, and learns from measured pilot outcomes.

## 0–15s — Problem

> Boğaziçi already publishes useful operational context: course schedules, cafeteria menus, shuttle timetables and the academic calendar. The problem is that they live in separate systems and do not tell an operator what to do differently today.

Open **Jury Mode**.

Show the headline:

> Boğaziçi'nin verisi var. Eksik olan karar katmanı.

## 15–35s — Signal fusion

Show four evidence cards:

1. BUIS/ÖBİKAS schedule snapshot
2. current SKS menu
3. official Mekik timetable
4. external Bebek weather

Say:

> We never call an estimate a sensor reading. Every input has provenance, freshness and a health state. If a live public page fails, we can show the last-known-good snapshot but the product becomes degraded instead of pretending it is live.

## 35–55s — Decision

Advance to **Decision**.

Say:

> BOUNCAMPUS fuses these signals into one mission. It explains why now, where, when, expected model impact and confidence. The model does not dispatch anything.

Point to:

- confidence
- location + operating window
- modeled impact
- human guardrail

## 55–70s — Stress test

Advance to **Stress test**.

Run either:

- Heavy rain
- Heatwave 38°C

Say:

> Before acting, the operator can break the recommendation with a counterfactual. This scenario starts from the current product baseline, not a canned demo result.

## 70–82s — Human approval

Advance to **Human approval**.

Click **Approve for pilot review**.

Say:

> The human remains accountable. Approval creates a decision receipt; it does not send a BMS, kitchen or transport command.

## 82–90s — Learning loop / close

Open **Decisions** and point to the **Outcome calibration loop**.

Say:

> After a real pilot, we enter the measured outcome, compare it with the model and improve the next decision. So the product loop is Sense → Decide → Pilot → Learn.

Close with:

> We are not asking the university to replace its systems. BOUNCAMPUS sits above them as a privacy-safe decision layer. A 30-day pilot only needs aggregate occupancy, smart-meter and POS totals to turn today’s model estimates into measured operational impact.

# Judge questions

## “Is the occupancy live?”

No. It is schedule-derived and explicitly labeled as a model estimate. Real-time occupancy is a pilot integration using anonymized aggregate counts.

## “Are you connected to BMS?”

No. The current product is decision support only. Read-only BMS / smart-meter integration is a pilot step before any control integration is considered.

## “What is actually live?”

The product fetches public Boğaziçi sources (SKS, Mekik, Academic Calendar), uses a dated official-source course schedule snapshot, and external Open-Meteo weather. Each source carries provenance metadata.

## “Why is this defensible?”

The defensibility is not a single model. It is the decision system:

- campus-specific source adapters
- provenance + degradation contract
- schedule-to-space demand model
- decision ranking
- counterfactual testing
- human approval ledger
- outcome-calibration loop

## “What would you do with university access?”

Highest-value calibration feeds:

1. anonymous occupancy aggregates
2. building/floor smart-meter totals
3. cafeteria POS totals by time bucket
4. shuttle AVL/GPS

No raw student identity is required for the core optimization loop.
