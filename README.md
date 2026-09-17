# BOUNCAMPUS

**Campus food-waste decision intelligence for KREATE for Climate.**

BOUNCAMPUS turns a measured campus climate problem into an operator decision loop. For the hackathon, the product is deliberately focused on **food-waste prevention in university dining operations**.

Boğaziçi University publicly reports:

- **50,993 kg** food waste in 2024;
- **48,251 kg** food waste in 2025;
- **33,430 kg** of 2025 food waste sent to İSTAÇ for recovery;
- dining services spanning six campuses, with published dining-hall capacity and service schedules.

Official baseline: https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

> **The 48-ton problem is already known. BOUNCAMPUS moves from reporting it to preventing the next kilogram and measuring the result.**

## Hackathon thesis

The focused product loop is:

```text
OFFICIAL WASTE BASELINE
        ↓
NEXT-SERVICE DEMAND BAND
(schedule + academic calendar + weather + menu context)
        ↓
OPERATOR-REVIEWED PRODUCTION BAND
        ↓
MEASURED SERVICE OUTCOME
(produced / served / edible surplus / waste kg)
        ↓
MODEL CALIBRATION
        ↺
```

BOUNCAMPUS does **not** autonomously dispatch a kitchen command. A human operator accepts, edits or rejects every production recommendation.

## Why this is credible

The hackathon story separates evidence from estimates.

### Official/public

- 2024 and 2025 annual food-waste totals;
- 2025 monthly food-waste values;
- 2025 recovery totals;
- Boğaziçi dining-service scale and published capacities;
- official menu, academic-calendar and shuttle pages when available.

### Model estimates

- next-service meal demand;
- conservative production planning band;
- prevention/recovery scenario outcomes;
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

This truth boundary is visible in the UI because hackathon credibility matters more than fake precision.

## 90-second Jury Mode

Open:

```text
/demo
```

The jury flow is four steps:

1. **PROVE** — show the official 48,251 kg 2025 baseline and source.
2. **FORECAST** — show the next-service demand/production band as `MODEL_ESTIMATE`.
3. **STRESS-TEST** — change prevention and recovery targets on the official baseline.
4. **PILOT** — show the 14-day A/B measurement plan and success metric: **waste kg / service**.

The one-line pitch:

> **“BOUNCAMPUS uses a campus’s measured food-waste history to recommend how much to produce for the next service, then measures success in waste kg per service.”**

## Product surfaces

| Surface | Purpose |
|---|---|
| `/` | Focused KREATE command center and official problem baseline |
| `/food-waste` | Core food-waste workspace, source-backed monthly history, demand band and scenario lab |
| `/demo` | 90-second jury flow |
| `/decisions` | Human-review decision ledger and outcome loop |
| `/data` | Source provenance and truth boundary |
| `/buildings` | Existing campus building intelligence |
| `/scenarios` | Existing counterfactual model workspace |
| `/mobility` | Existing source-backed campus/inter-campus shuttle workspace |
| `/courses` | BUIS/ÖBİKAS schedule explorer |
| `/lab` | Experimental/future modules separated from the jury story |

Important endpoints:

```text
GET /api/v1/food
GET /api/v1/dashboard
GET /api/v1/health
GET /api/v1/brief
POST /api/v1/scenarios/simulate
```

`GET /api/v1/food` exposes the official food-waste baseline, demand-model context, scenario output and the explicit evidence boundary in one machine-readable contract.

## What happens in the 14-day pilot?

Use one comparable dining service as control and one as intervention. Record only four service-level values:

1. portions produced;
2. portions served;
3. edible surplus;
4. waste kg.

Primary outcome:

```text
waste kg / service
```

Secondary outcomes:

- overproduction rate;
- edible-surplus recovery;
- forecast error band;
- operator override frequency.

The pilot can therefore prove or reject the product hypothesis without requiring invasive personal data or a large integration project.

## Why the rest of the platform still matters

Food waste is the hackathon wedge, not the entire long-term platform.

Existing capabilities are preserved as expansion modules:

- campus building/energy decisions;
- counterfactual scenarios;
- source-backed shuttle mobility;
- campus map and 3D/photogrammetry context;
- source provenance and human approval.

They show that the same `SENSE → DECIDE → APPROVE → PILOT → LEARN` architecture can later expand to energy, mobility and other campus climate operations without diluting the jury narrative today.

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
PRODUCTION BAND
        │
        ▼
HUMAN OPERATOR GATE
        │
        ▼
14-DAY PILOT
├─ produced portions
├─ served portions
├─ edible surplus
└─ waste kg
        │
        ▼
CALIBRATION / NEXT SERVICE
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
- `/api/v1/health`

Repository engineering and merge discipline are defined in [`AGENTS.md`](AGENTS.md). Work is performed on short-lived agent branches, validated through the single integration PR, merged to `master`, and post-merge verified before completion.

## KREATE for Climate

- **Hackathon:** 15 October 2026, İstanbul
- **Core climate problem:** avoidable institutional food waste
- **Primary pilot metric:** waste kg / service
- **Scale path:** universities → hospitals → factories → schools → large catering operations

Detailed product rationale and pitch structure: [`docs/kreate-winning-product.md`](docs/kreate-winning-product.md).
