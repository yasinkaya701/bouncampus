# BOUNCAMPUS

**Predict campus demand. Optimize campus resources. Show exactly where every number comes from.**

BOUNCAMPUS is a Boğaziçi University campus sustainability and decision-support prototype for the October 15, 2026 hackathon. It combines public university feeds, an official course-schedule snapshot, external weather, and transparent decision models to recommend operational actions before energy, space or food is wasted.

## What is actually live?

| Feed | Source | Product class |
|---|---|---|
| Cafeteria menu | Boğaziçi SKS `yemekhane.bogazici.edu.tr` | `OFFICIAL_LIVE` |
| Shuttle timetable | Boğaziçi Mekik `mekik.bogazici.edu.tr` | `OFFICIAL_LIVE` |
| Academic calendar | `akademiktakvim.bogazici.edu.tr` | `OFFICIAL_LIVE` |
| Course timetable | BUIS/ÖBİKAS public schedule | `OFFICIAL_SNAPSHOT` |
| Bebek weather | Open-Meteo at campus coordinates | `EXTERNAL_LIVE` |
| Occupancy | timetable + room-capacity model | `MODEL_ESTIMATE` |
| Energy | building profile + occupancy + weather model | `MODEL_ESTIMATE` |
| Food demand | lunch class-flow + weather model | `MODEL_ESTIMATE` |
| Savings / CO2 | optimization model outputs | `MODEL_ESTIMATE` |

BOUNCAMPUS does **not** currently claim access to university BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS or shuttle GPS. Those integrations are pilot-stage targets and require university authorization.

See [`docs/live-data-contract.md`](docs/live-data-contract.md) for the complete provenance and release contract.

## Core modules

- **Data Trust Layer** — source health, timestamps and provenance for every live/model feed.
- **Occupancy Intelligence** — scheduled classroom load derived from the public course timetable snapshot.
- **Building Energy Optimizer** — physics-lite hourly energy and low-use consolidation model.
- **Cafeteria Demand Optimizer** — lunch-period demand estimate with official menu context.
- **Campus Action Engine** — prioritised actions with model-estimated impact.
- **Scenario Simulator** — what-if exploration for weather, exams, events and closures.
- **Campus Digital Twin UI** — building map, operational dashboards and source inspection.

## Architecture

```text
OFFICIAL BOUN PUBLIC FEEDS
  SKS Menu ──┐
  Mekik ─────┤
  Calendar ──┤
  BUIS snapshot
              ├─> DATA TRUST / PROVENANCE LAYER
Open-Meteo ───┘             │
                             v
                    Campus decision state
                    ├─ occupancy estimate
                    ├─ energy estimate
                    ├─ food-demand estimate
                    └─ source health
                             │
                             v
                    ACTION / OPTIMIZATION ENGINE
                             │
                             v
                    Dashboard + scenario tools
```

## Tech stack

| Layer | Technology |
|---|---|
| Web / live gateway | Next.js 14 / TypeScript |
| Backend research API | FastAPI / Python 3.11+ |
| ML | XGBoost, scikit-learn |
| Optimization | Google OR-Tools |
| Frontend | React, Tailwind, Recharts |
| Maps | Leaflet / 3D campus components |
| Deployment target | Vercel frontend + optional Railway FastAPI |

## Run locally

### Frontend / product gateway

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`.

Verification:

```bash
npm run typecheck
npm run lint
npm run build
```

Runtime source health:

```text
GET /api/v1/health
```

Dashboard API:

```text
GET /api/v1/dashboard
```

### FastAPI research backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The hackathon dashboard can run through its Next.js API gateway even if the optional FastAPI deployment is not connected.

## Hackathon jury story

The product is designed around one defensible sentence:

> **Boğaziçi already publishes enough operational context to predict tomorrow's campus demand; BOUNCAMPUS turns those signals into transparent, testable actions, and is ready to calibrate against BMS/POS/occupancy telemetry when the university authorizes those feeds.**

Every dashboard number can be inspected as official live data, official snapshot data, external live data, or a model estimate. If an upstream source fails, the dashboard enters a visible degraded state rather than fabricating a live value.

## Production/pilot path

Highest-value authorised integrations:

1. anonymised Wi-Fi/AP or turnstile occupancy aggregates;
2. building/floor BMS and smart-meter telemetry;
3. SKS POS totals in privacy-preserving time buckets;
4. shuttle GPS/AVL feed if available;
5. authoritative room capacity and current course-enrolment counts.

These feeds plug into the same provenance layer and are used to calibrate the current models.

## CI

Pull requests run:

- TypeScript typecheck
- Next.js lint
- production build
- backend Python syntax compilation
- critical JSON validation

No hackathon demo change should merge with a red CI gate.

---

Built for the Sustainability Hackathon — **15 October 2026**.
