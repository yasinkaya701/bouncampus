# BOUNCAMPUS

**Campus food-waste decision intelligence for KREATE for Climate.**

## Team — start here

New teammate? You do **not** need to read the whole repository before contributing.

### 5-minute start

Requirements: Git + Node.js **24.x**.

```bash
git clone https://github.com/yasinkaya701/bouncampus.git
cd bouncampus/frontend
npm ci
npm run dev
```

Open `http://localhost:3000`, then visit `/demo` and `/food-waste` first.

For a complete first-session path, use **[`docs/ONBOARDING.md`](docs/ONBOARDING.md)**. For branch, validation, commit, evidence, and PR rules, use **[`CONTRIBUTING.md`](CONTRIBUTING.md)**.

### Human team roles

| Role | Primary ownership | Good starting area |
|---|---|---|
| **IE — Customer Discovery & Market Lead** | PMR, beachhead, buyer/persona, interview evidence | `KREATE/`, PMR/evidence issues |
| **EE — Physical Systems & Measurement Lead** | measurement design, instrumentation, pilot feasibility | measurement/pilot tasks under `KREATE/` |
| **CS1 — Decision Intelligence Lead** | modeling, uncertainty, evaluation, decision logic | `backend/`, `frontend/src`, analytical scripts |
| **CS2 — Product Strategy, Evidence Synthesis & Application Lead** | product synthesis, application narrative, evidence integration | `KREATE/`, product/application docs |

### Normal teammate workflow

```text
pick a bounded issue
        ↓
update master
        ↓
create human/<role>/<task>
        ↓
implement a small change
        ↓
validate locally
        ↓
self-review the diff + evidence
        ↓
use the single integration PR slot
        ↓
CI / review / merge
```

Do not commit routine work directly to `master`. Do not open a second parking-lot PR while another integration PR is active. You may continue non-conflicting work on your own branch until the integration slot is free.

### Fast validation

Frontend:

```bash
cd frontend
npm run typecheck
npm run lint
```

Merge candidate:

```bash
cd frontend
npm run verify
```

Repository/KREATE checks when relevant:

```bash
python scripts/kreate_check.py
python scripts/agent_fabric_check.py
python -m compileall -q backend/app scripts
```

### Where should I edit?

```text
frontend/      active Next.js product + co-located /api/v1 routes
backend/       FastAPI research/backend service
KREATE/        roles, PMR, evidence, application and hackathon execution
docs/          maintained product/technical documentation
scripts/       repository validation and coordination tooling
.agents/       autonomous multi-agent coordination
legacy/        old experiments/mocks — not the default place for new work
```

The full autonomous execution and merge contract lives in [`AGENTS.md`](AGENTS.md). Humans can start with the onboarding/contribution guides above and use `AGENTS.md` when working with agents or integration mechanics.

---

## Product overview

BOUNCAMPUS turns a measured institutional climate problem into a safe operating decision loop. For the hackathon, the product is deliberately focused on **food-waste prevention in university dining operations**.

Boğaziçi University publicly reports:

- **50,993 kg** food waste in 2024;
- **48,251 kg** food waste in 2025;
- **33,430 kg** of 2025 food waste sent to İSTAÇ for recovery;
- dining services spanning six campuses, with published dining-hall capacity and service schedules.

Official baseline: https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

> **The 48-ton problem is already known. BOUNCAMPUS acts before the next kilogram becomes waste—and lets measured pilot evidence, not the model, decide whether the intervention worked.**

## Hackathon thesis

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
MEASURED PILOT SCORECARD
        ↓
MODEL CALIBRATION
        ↺
```

BOUNCAMPUS does **not** autonomously dispatch a kitchen command. A human operator accepts, edits or holds every production recommendation.

## Why this is stronger than another sustainability dashboard

The product:

1. acts **before** avoidable food waste is created;
2. exposes model uncertainty and missing-source context;
3. can explicitly **withhold** an operational recommendation;
4. keeps a human operator in control;
5. defines the field measurement that can prove the product wrong;
6. already contains the evidence-scoring path for real pilot measurements.

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

Current transparent pilot weights:

| Signal | Weight |
|---|---:|
| Course schedule | 50% |
| Weather | 20% |
| Menu context | 20% |
| Academic calendar | 10% |

These weights are pilot policy, not learned universal coefficients. Real service data is required for calibration.

## Truth boundary / claim firewall

### Official/public

- 2024 and 2025 annual food-waste totals;
- 2025 monthly food-waste values;
- 2025 recovery totals;
- Boğaziçi dining-service scale and published capacities;
- official/public contextual sources when available.

### Model estimates

- next-service meal demand;
- uncertainty-aware production planning band;
- decision readiness based on source availability;
- prevention/recovery scenarios;
- occupancy and building-energy estimates elsewhere in the platform.

### Not currently available

BOUNCAMPUS does **not** claim access to:

- cafeteria POS transactions;
- actual produced or served portions per service before the pilot;
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
5. **EVIDENCE** — show the pre-registered pilot target, primary KPI and measurement workflow.

One-line pitch:

> **“BOUNCAMPUS turns measured institutional food waste into an uncertainty-aware, human-approved production decision and a controlled pilot that can prove the product wrong.”**

## Product surfaces

| Surface | Purpose |
|---|---|
| `/` | Focused KREATE command center and official problem baseline |
| `/food-waste` | Core decision workspace: baseline, source health, readiness, operator gate, scenario lab and pilot contract |
| `/food-waste/pilot` | Pilot Evidence Lab for entering real control/intervention service measurements and scoring the pre-registered gates |
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
GET  /api/v1/food
GET  /api/v1/food/pilot-template
GET  /api/v1/food/pilot-score
POST /api/v1/food/pilot-score
GET  /api/v1/dashboard
GET  /api/v1/health
GET  /api/v1/brief
POST /api/v1/scenarios/simulate
```

`GET /api/v1/food` exposes the official baseline, source-backed demand context, decision band/readiness, human-approval policy, scenario output, pilot contract, claim policy and truth boundary.

`GET /api/v1/food/pilot-template` returns the blank measurement CSV.

`POST /api/v1/food/pilot-score` accepts **measured aggregate service outcomes only** and computes the predefined control/intervention scorecard. It does not fabricate pilot measurements.

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

### Measured evidence engine

The Pilot Evidence Lab starts empty. It does not seed synthetic “winning” results.

Once real service measurements are entered, the score engine reports:

- control/intervention sample counts;
- mean waste kg / 100 served meals;
- raw waste kg / service;
- overproduction rate;
- edible surplus intensity;
- forecast absolute percentage error;
- early-sellout rate;
- operator-override rate;
- normalized waste reduction versus control;
- minimum-evidence, reduction-target and early-sellout gates.

Possible numeric classifications:

- `INSUFFICIENT_EVIDENCE`
- `PROMISING`
- `FAILED`

`PROMISING` is intentionally not named `PROVEN`: food-safety review, service matching, measurement quality and replication remain necessary.

Detailed protocol: [`docs/food-waste-pilot-protocol.md`](docs/food-waste-pilot-protocol.md)

## Why the rest of the platform still matters

Food waste is the hackathon wedge, not the entire long-term platform.

Existing capabilities remain preserved as expansion modules:

- campus building/energy decisions;
- counterfactual scenarios;
- source-backed shuttle mobility;
- campus map and 3D/photogrammetry context;
- source provenance and human approval.

They demonstrate that the same `SENSE → QUALIFY → APPROVE → PILOT → LEARN` architecture can later expand to energy, mobility and other campus climate operations **after** one primary climate outcome is validated end to end.

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
├─ menu
├─ academic calendar
├─ course schedule snapshot
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
        │
        ▼
NORMALIZED SCORECARD + GUARDRAILS
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
- `/food-waste/pilot`
- `/demo`
- `/decisions`
- `/data`
- `/api/v1/food`
- `/api/v1/food/pilot-template`
- `/api/v1/food/pilot-score`
- `/api/v1/health`

Repository engineering and merge discipline are defined in [`AGENTS.md`](AGENTS.md). Human work uses short-lived `human/<role>/<task>` branches; autonomous work uses the agent branch/lease system. Integration is serialized through the single PR slot, merged to `master`, and verified after merge.

## KREATE for Climate

- **Hackathon:** 15 October 2026, İstanbul
- **Core climate problem:** avoidable institutional food waste
- **Primary pilot metric:** waste kg / 100 served meals
- **Pilot target:** ≥10% normalized reduction vs matched control, without service degradation
- **Scale path:** universities → hospitals → factories → schools → municipal kitchens → catering operators

## Jury preparation

- Team onboarding: [`docs/ONBOARDING.md`](docs/ONBOARDING.md)
- Contribution workflow: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Product contract: [`docs/kreate-winning-product.md`](docs/kreate-winning-product.md)
- 90-second script: [`docs/jury-demo-script.md`](docs/jury-demo-script.md)
- Full pitch: [`docs/pitch.md`](docs/pitch.md)
- Pilot protocol: [`docs/food-waste-pilot-protocol.md`](docs/food-waste-pilot-protocol.md)
- Judge red-team Q&A: [`docs/jury-q-and-a.md`](docs/jury-q-and-a.md)
- Runtime architecture: [`docs/architecture.md`](docs/architecture.md)
- Assumptions/methodology: [`docs/assumptions.md`](docs/assumptions.md)
