# BOUNCAMPUS

**Campus food-waste decision intelligence for KREATE for Climate.**

BOUNCAMPUS turns a measured institutional climate problem into a safe operating decision loop. For the hackathon, the product is deliberately focused on **food-waste prevention in university dining operations**.

Boğaziçi University publicly reports:

- **50,993 kg** food waste in 2024;
- **48,251 kg** food waste in 2025;
- **33,430 kg** of 2025 food waste sent to İSTAÇ for recovery;
- dining services spanning six campuses, with published dining-hall capacity and service schedules.

Official baseline: https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

> **The 48-ton problem is already known. BOUNCAMPUS acts before the next kilogram becomes waste—and lets measured pilot evidence, not the model, decide whether the intervention worked.**

## Hackathon thesis

The focused product loop is:

```text
OFFICIAL WASTE BASELINE
        ↓
SOURCE HEALTH + CAMPUS CONTEXT
(schedule + academic calendar + weather + menu)
        ↓
UNCERTAINTY-AWARE DEMAND / PRODUCTION BAND
        ↓
DECISION READINESS
PILOT_READY / REVIEW_REQUIRED / WITHHOLD
        ↓
HUMAN OPERATOR GATE
approve / edit / hold
        ↓
MATCHED 14-DAY PILOT
        ↓
WASTE KG / 100 SERVED MEALS + GUARDRAILS
        ↓
MODEL CALIBRATION
        ↺
```

BOUNCAMPUS does **not** autonomously dispatch a kitchen command. A human operator accepts, edits or rejects every production recommendation.

## Why this is stronger than another sustainability dashboard

The product does four things the typical reporting dashboard does not:

1. acts **before** avoidable food waste is created;
2. exposes model uncertainty and missing-source context;
3. can explicitly **withhold** an operational recommendation;
4. defines the field measurement that can prove the product wrong.

The goal is not “predict demand accurately” in isolation. The goal is to reduce normalized food waste **without degrading service reliability**.

## Decision readiness

Every production band carries:

- predicted meals;
- lower and upper operating bounds;
- operator starting point;
- signal coverage;
- `PILOT_READY`, `REVIEW_REQUIRED`, or `WITHHOLD`;
- missing-signal reason codes;
- `MODEL_ESTIMATE` provenance;
- `operatorApprovalRequired=true`;
- `autoDispatchAllowed=false`.

Current signal weights are deliberately transparent:

| Signal | Weight |
|---|---:|
| Course schedule | 50% |
| Weather | 20% |
| Menu context | 20% |
| Academic calendar | 10% |

This is a pilot policy, not a claim that these weights are universally optimal. Real service data is required for calibration.

## Truth boundary / claim firewall

The hackathon story separates evidence from estimates.

### Official/public

- 2024 and 2025 annual food-waste totals;
- 2025 monthly food-waste values;
- 2025 recovery totals;
- Boğaziçi dining-service scale and published capacities;
- official menu, academic-calendar and shuttle pages when available.

### Model estimates

- next-service meal demand;
- uncertainty-aware production planning band;
- decision readiness based on source availability;
- prevention/recovery scenarios;
- occupancy and building-energy estimates elsewhere in the platform.

### Not currently available

BOUNCAMPUS does **not** claim access to:

- cafeteria POS transactions;
- actual produced or served portions per service;
- plate-level waste measurements;
- university BMS or smart meters;
- turnstiles or Wi-Fi occupancy telemetry;
- shuttle GPS;
- live IoT sensor networks.

### Forbidden claims before a measured pilot

The UI/API explicitly rejects statements such as:

- “BOUNCAMPUS saved X kg of food”;
- “BOUNCAMPUS avoided Y kg CO2”;
- “BOUNCAMPUS saved Z liters of water”;
- “we observe actual student demand”;
- “we optimized actual cafeteria production.”

Scenario values remain scenarios. Climate-equivalent conversions require measured waste reduction plus a documented lifecycle factor.

## 90-second Jury Mode

Open:

```text
/demo
```

The jury flow is five beats:

1. **PROBLEM** — prove the official 48,251 kg 2025 baseline.
2. **DECISION** — show the next-service band, signal coverage and readiness state.
3. **HUMAN GATE** — show approve/hold and `AUTO_DISPATCH=false`.
4. **SCENARIO** — stress-test prevention/recovery without presenting modeled outcomes as achieved savings.
5. **EVIDENCE** — show the pre-registered pilot target, primary KPI and downloadable measurement template.

The one-line pitch:

> **“BOUNCAMPUS turns measured institutional food waste into an uncertainty-aware, human-approved production decision and a controlled pilot that can prove the product wrong.”**

## Product surfaces

| Surface | Purpose |
|---|---|
| `/` | Focused KREATE command center and official problem baseline |
| `/food-waste` | Core decision workspace: baseline, source health, readiness, operator gate, scenario lab and pilot contract |
| `/demo` | 90-second jury choreography |
| `/decisions` | Existing human-review decision ledger and outcome loop |
| `/data` | Source provenance and truth boundary |
| `/buildings` | Existing campus building intelligence |
| `/scenarios` | Existing counterfactual model workspace |
| `/mobility` | Existing source-backed campus/inter-campus shuttle workspace |
| `/courses` | BUIS/ÖBİKAS schedule explorer |
| `/lab` | Experimental/future modules kept outside the primary jury story |

Important endpoints:

```text
GET /api/v1/food
GET /api/v1/food/pilot-template
GET /api/v1/dashboard
GET /api/v1/health
GET /api/v1/brief
POST /api/v1/scenarios/simulate
```

`GET /api/v1/food` exposes, in one machine-readable contract:

- official baseline;
- source-backed demand context;
- production decision band;
- readiness and human-approval policy;
- scenario output;
- pilot evidence contract;
- claim policy;
- explicit truth boundary.

## 14-day falsifiable pilot

The pilot uses matched **CONTROL vs INTERVENTION** services.

Record aggregate operational fields only:

1. date / service ID / arm;
2. model forecast meals;
3. produced portions;
4. served portions;
5. edible surplus kg;
6. waste kg;
7. early sell-out;
8. operator override;
9. anomaly notes.

No student identity, payment identity, device tracking or individual consumption data is required.

### Primary KPI

```text
waste_kg_per_100_served = (waste_kg / served_portions) * 100
```

Why normalize by served meals?

Because `waste kg / service` alone is confounded by service volume. A quiet day can look artificially successful. The normalized metric makes control/intervention comparison more defensible.

### Pre-registered success gate

A promising pilot requires all of the following:

- at least **5 measured services per arm**;
- at least **10% lower waste kg / 100 served meals** versus matched control;
- no increase in early-sellout incidence;
- no food-safety process bypass;
- comparable measurement quality across arms;
- operator overrides reported rather than hidden.

The **10% value is a target, not an achieved result**.

Detailed protocol: [`docs/food-waste-pilot-protocol.md`](docs/food-waste-pilot-protocol.md)

## Why the rest of the platform still matters

Food waste is the hackathon wedge, not the entire long-term platform.

Existing capabilities remain preserved as expansion modules:

- campus building/energy decisions;
- counterfactual scenarios;
- source-backed shuttle mobility;
- campus map and 3D/photogrammetry context;
- source provenance and human approval.

They demonstrate that the same `SENSE → DECIDE → APPROVE → PILOT → LEARN` architecture can later expand to energy, mobility and other campus climate operations **after** one primary climate outcome is validated end to end.

## Scale path

The transferable asset is not a Boğaziçi-specific dashboard. It is the operating loop and evidence contract.

Potential next environments:

- university cafeterias;
- hospitals;
- factories;
- schools;
- municipal kitchens;
- large catering operators.

Each deployment can swap in local demand signals while keeping the same provenance, readiness, human-control and measurement framework.

## Architecture

```text
OFFICIAL / PUBLIC SIGNALS
├─ food-waste baseline
├─ SKS menu
├─ academic calendar
├─ BUIS/ÖBİKAS schedule snapshot
└─ weather
        │
        ▼
PROVENANCE + SOURCE HEALTH
        │
        ▼
FOOD DEMAND CONTEXT
        │
        ▼
UNCERTAINTY-AWARE PRODUCTION BAND
        │
        ▼
READINESS / WITHHOLD POLICY
        │
        ▼
HUMAN OPERATOR GATE
        │
        ▼
14-DAY MATCHED PILOT
├─ forecast meals
├─ produced portions
├─ served portions
├─ edible surplus kg
├─ waste kg
├─ early sell-out
└─ operator override
        │
        ▼
NORMALIZED SCORECARD + CALIBRATION
```

## Tech stack

| Layer | Technology |
|---|---|
| Product gateway | Next.js 14 / TypeScript |
| Research backend | FastAPI / Python 3.11+ |
| Frontend | React, Tailwind, Recharts |
| Maps | Leaflet + optional 3D/photogrammetry |
| Models | transparent schedule / demand / energy logic |
| Deployment target | Vercel frontend + optional FastAPI service |

## Run locally

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`.

## Validation sequence

```bash
cd frontend
npm ci
npm run typecheck
npm run lint
npm run build
```

Then verify at minimum:

- `/`
- `/food-waste`
- `/demo`
- `/decisions`
- `/data`
- `/api/v1/food`
- `/api/v1/food/pilot-template`
- `/api/v1/health`

Repository engineering and merge discipline are defined in [`AGENTS.md`](AGENTS.md). Work is performed on short-lived agent branches, validated through the single integration PR, merged to `master`, and post-merge verified before completion.

## KREATE for Climate

- **Hackathon:** 15 October 2026, İstanbul
- **Core climate problem:** avoidable institutional food waste
- **Primary pilot metric:** waste kg / 100 served meals
- **Pilot target:** ≥10% normalized reduction vs matched control, without service degradation
- **Scale path:** universities → hospitals → factories → schools → municipal kitchens → catering operators

## Jury preparation

- Product contract: [`docs/kreate-winning-product.md`](docs/kreate-winning-product.md)
- 90-second script: [`docs/jury-demo-script.md`](docs/jury-demo-script.md)
- Full pitch: [`docs/pitch.md`](docs/pitch.md)
- Pilot protocol: [`docs/food-waste-pilot-protocol.md`](docs/food-waste-pilot-protocol.md)
- Judge red-team Q&A: [`docs/jury-q-and-a.md`](docs/jury-q-and-a.md)
