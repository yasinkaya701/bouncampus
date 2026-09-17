# BOUNCAMPUS — 90-Second KREATE Jury Demo

## One-line product

**BOUNCAMPUS uses a campus’s measured food-waste history to recommend how much to produce for the next service, then measures success in waste kg per service.**

## 0–20s — Prove the climate problem

Open `/demo`.

Say:

> Boğaziçi already measures the problem: 48,251 kg of food waste in 2025. This is the university’s own published baseline, not a number we generated for the demo.

If challenged, open the official source from the page.

Point to:

- 48,251 kg 2025 food waste;
- 33,430 kg sent to İSTAÇ recovery;
- 50,993 kg 2024 baseline.

## 20–45s — Turn history into the next-service decision

Show the demand / production band.

Say:

> The missing step is not another waste report. Before the next service, BOUNCAMPUS combines schedule, academic calendar, weather and menu context to estimate demand. It proposes a conservative production band rather than a magic number.

Point to the `MODEL_ESTIMATE` label.

Say:

> This is decision support. We do not claim POS, kitchen-production or served-meal telemetry that we do not have.

## 45–65s — Stress-test the target

Move the prevention and recovery sliders.

Say:

> This applies a pilot target to the official historical baseline. It lets the operator understand the scale of a decision before trying it, but we do not call the result measured savings.

## 65–85s — Show how impact will be proven

Point to the 14-day pilot.

Say:

> We need only four measurements per service: portions produced, portions served, edible surplus and waste kilograms. One comparable service is control, one is intervention.

Point to the primary KPI:

> Success is waste kg per service. If it does not fall against control, the product hypothesis fails.

## 85–90s — Close

> **The 48-ton problem is already known. BOUNCAMPUS moves from reporting it to preventing the next kilogram and measuring the result.**

# Judge questions

## “Is the 48,251 kg number real?”

Yes. It is Boğaziçi University’s published 2025 food-waste total. The product links to the official source.

## “Are the recommended meal numbers real production data?”

No. The current next-service demand and production band is explicitly a model estimate. The pilot will calibrate it using actual produced, served, surplus and waste measurements.

## “Are you connected to cafeteria POS?”

No. The hackathon product does not claim POS access. POS time-bucket totals could improve calibration later, but the first pilot can run with four aggregate service-level measurements and no student/payment identity.

## “Why AI or a model at all?”

Because dining demand changes with academic schedules, calendar effects, weather and menu context. A fixed production rule cannot respond to those shifts. The product also keeps a human operator in the loop, so the model recommends rather than autonomously dispatches.

## “What exactly is the pilot?”

A 14-day controlled operational test:

1. choose comparable control and intervention services;
2. record produced portions;
3. record served portions;
4. measure edible surplus and waste kg;
5. log operator overrides;
6. compare waste kg/service and overproduction rate;
7. recalibrate the model from measured outcomes.

## “Why is this climate tech?”

Food waste is a resource and emissions problem embedded in a repeated operating decision: how much food should be produced before uncertain demand is known? BOUNCAMPUS acts before waste occurs rather than only managing waste after it is created.

## “What happened to energy, mobility and 3D?”

They remain implemented expansion modules. The KREATE jury story deliberately leads with one measurable problem so the product is understandable and testable. The underlying source-provenance, human-approval and measure-learn architecture can later serve energy and mobility decisions too.

## “Where does it scale?”

The same `forecast → recommend → approve → measure → learn` loop applies to university cafeterias, hospitals, factories, schools, municipal kitchens and large catering operators.
