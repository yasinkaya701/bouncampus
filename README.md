# BOUNCAMPUS

**The decision layer between campus data and real operations.**

BOUNCAMPUS is a source-traceable campus **Mission Control** for Boğaziçi University. It fuses public university signals, a dated official course-schedule snapshot, external weather and transparent decision models into one operational mission: what should a human operator review, why now, what evidence supports it, how robust is it under a shock, and what happened after a pilot?

> **Boğaziçi'nin verisi var. Eksik olan karar katmanı.**

## Why this is not another dashboard

The product loop is:

```text
SENSE → DECIDE → STRESS-TEST → HUMAN APPROVAL → PILOT → LEARN
```

1. **Sense** — ingest source-traceable campus context.
2. **Decide** — rank a human-reviewable operational mission with evidence and confidence.
3. **Stress-test** — recompute the current baseline under rain, heatwave, exam, event or closure scenarios.
4. **Human approval** — create an auditable pilot-review state without dispatching a campus command.
5. **Pilot** — execute only after field verification and operator approval.
6. **Learn** — compare an observed outcome with modeled potential and capture calibration error.

## 90-second Jury Mode

Open:

```text
/demo
```

The jury flow is deliberately four screens:

- **01 / SENSE** — official/public signals + provenance + source health
- **02 / REASON** — today's campus mission + confidence + modeled impact
- **03 / SIMULATE** — live-baseline counterfactual stress test
- **04 / ACT** — explicit human approval boundary + decision receipt

Full demo narration: [`docs/jury-demo-script.md`](docs/jury-demo-script.md)

## Product surfaces

| Surface | Purpose |
|---|---|
| `/` | Mission Control: today's mission, source context, map, KPIs and decision queue |
| `/demo` | 90-second Jury Mode |
| `/buildings` | Campus building intelligence and schedule-derived utilization |
| `/courses` | BUIS/ÖBİKAS schedule explorer |
| `/decisions` | Human approval ledger + outcome calibration loop |
| `/scenarios` | Counterfactual decision stress testing |
| `/data` | Data Trust + production pilot readiness |
| `/lab` | Clearly separated future/prototype workflows |
| `/api/v1/brief` | Machine-readable current Mission Brief |
| `/api/v1/health` | Public-source health and freshness state |

## What is actually live?

| Feed | Source | Product class |
|---|---|---|
| Cafeteria menu | Boğaziçi SKS | `OFFICIAL_LIVE` when verified |
| Shuttle timetable | Boğaziçi Mekik | `OFFICIAL_LIVE` when verified |
| Academic calendar | Boğaziçi Academic Calendar | `OFFICIAL_LIVE` when verified |
| Course timetable | BUIS/ÖBİKAS public schedule | `OFFICIAL_SNAPSHOT` |
| Bebek weather | Open-Meteo at campus coordinates | `EXTERNAL_LIVE` |
| Occupancy | timetable + room-capacity model | `MODEL_ESTIMATE` |
| Energy | building profile + occupancy + weather model | `MODEL_ESTIMATE` |
| Food demand | lunch class-flow + weather model | `MODEL_ESTIMATE` |
| Savings / CO₂ | optimization model outputs | `MODEL_ESTIMATE` |

If an official public page temporarily fails, BOUNCAMPUS may show a **last-known-good official public snapshot for continuity**, but that source is explicitly marked degraded and is **not** presented as live.

BOUNCAMPUS does **not** currently claim access to university BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, shuttle GPS or live IoT telemetry.

See [`docs/live-data-contract.md`](docs/live-data-contract.md) for the complete provenance contract.

## Mission Brief

`GET /api/v1/brief` turns the dashboard state into a deterministic, inspectable decision object:

```text
Mission Brief
├─ status
├─ title + recommendation
├─ why_now
├─ confidence
├─ location + operating window
├─ evidence[]
│  ├─ value
│  ├─ interpretation
│  └─ provenance
├─ impact[]
├─ source_health
└─ human guardrail
```

This is the central product abstraction. A UI card, Copilot explanation or external integration can all consume the same Mission Brief.

## Decision accountability

The decision workspace is more than a recommendation list.

Each candidate can be locally marked:

- `REVIEW`
- `APPROVED_FOR_PILOT`
- `DECLINED`

The hackathon build keeps this ledger in browser storage and explicitly does **not** send BMS, kitchen, transport or IoT commands.

After a pilot, the **Outcome Loop** accepts the observed result and compares it with the model prediction, producing model error as calibration evidence.

```text
model potential → human pilot → observed outcome → model error → better calibration
```

## Decision Explainer

The floating product assistant is mission-aware rather than a generic chatbot. It explains:

- why today's mission exists;
- which evidence supports it;
- which evidence is weakest;
- why confidence is high/medium/low;
- what must be verified before a real pilot;
- which values are live, snapshots or model estimates.

It cannot dispatch a field command.

## Architecture

```text
OFFICIAL / PUBLIC SIGNALS

SKS Menu ───────┐
Mekik ──────────┤
Academic Calendar│
BUIS snapshot ──┤
Open-Meteo ─────┘
        │
        ▼
PROVENANCE + SOURCE HEALTH
        │
        ▼
CAMPUS STATE MODELS
├─ schedule-derived utilization
├─ physics-lite energy
└─ cafeteria demand
        │
        ▼
MISSION BRIEF
├─ recommendation
├─ why now
├─ evidence
├─ confidence
└─ modeled impact
        │
        ├──────────────► COUNTERFACTUAL ENGINE
        │                    │
        ▼                    ▼
HUMAN DECISION LEDGER ◄─ stress-tested mission
        │
        ▼
PILOT OUTCOME
        │
        ▼
CALIBRATION EVIDENCE
```

## Production pilot path

BOUNCAMPUS does not require the university to replace an existing system. It sits above existing sources as a read-only decision layer first.

Highest-value calibration feeds:

1. **P0 — anonymous occupancy aggregates**: Wi-Fi AP, turnstile or room-count totals; no raw identities required.
2. **P0 — building/floor smart-meter totals**: measure energy baseline vs pilot outcome.
3. **P1 — cafeteria POS totals by time bucket**: calibrate demand and overproduction estimates without student/payment identity.
4. **P1 — shuttle AVL/GPS**: upgrade timetable context to actual arrival reliability.

### 30-day pilot

| Week | Goal |
|---|---|
| 1 | Read-only aggregate integrations |
| 2 | Model calibration against measured data |
| 3 | Small human-approved operator pilot |
| 4 | Outcome proof, model error and operator feedback |

Privacy defaults:

- aggregate counts before individual records;
- no raw student identifiers in the decision layer;
- read-only integrations before control;
- every adapter retains provenance and freshness metadata.

## Demo resilience

A hackathon product cannot collapse because one public page times out during judging.

For selected official public feeds, the repository contains a dated **last-known-good public snapshot**. If the current upstream cannot be verified:

- the product may display that snapshot for continuity;
- the source is marked degraded / snapshot;
- confidence falls;
- the UI never calls that value live.

This keeps the demo reliable without crossing the truth boundary.

## Tech stack

| Layer | Technology |
|---|---|
| Mission Control / gateway | Next.js 14 / TypeScript |
| Research backend | FastAPI / Python 3.11+ |
| Models | transparent schedule / energy / demand logic; research ML stack available |
| Optimization | decision rules + counterfactual scenario engine |
| Frontend | React, Tailwind, Recharts |
| Maps | Leaflet / optional 3D campus visualization |
| Deployment target | Vercel frontend + optional FastAPI service |

## Run locally

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`.

Important product endpoints:

```text
GET /api/v1/health
GET /api/v1/dashboard
GET /api/v1/brief
POST /api/v1/scenarios/simulate
```

The Next.js product gateway is sufficient for the hackathon demo; the FastAPI service is optional research infrastructure.

## Validation sequence

Implementation is intentionally separated from final validation. Before release:

```bash
cd frontend
npm ci
npm run typecheck
npm run lint
npm run build
```

Then verify:

- `/`
- `/demo`
- `/decisions`
- `/scenarios`
- `/data`
- `/api/v1/health`
- `/api/v1/brief`

The repository currently follows the temporary single-branch policy documented in [`AGENTS.md`](AGENTS.md): routine engineering work targets `master` until the owner changes that rule.

---

Built for the Sustainability Hackathon — **15 October 2026**.
