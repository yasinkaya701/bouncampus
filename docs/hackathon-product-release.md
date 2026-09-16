# BOUNCAMPUS Hackathon Product Release

## Product surface

The jury-facing product is intentionally narrower and more coherent than the full experiment repository.

### Core workspaces

1. **Overview** — live operating brief, public feeds, model KPIs, campus map, source provenance.
2. **Campus** — building inventory and schedule-derived building intelligence.
3. **Courses** — BUIS/ÖBİKAS schedule explorer with department/day/campus filters.
4. **Decisions** — human-approved operational recommendation queue.
5. **Scenarios** — counterfactual workspace using the current dashboard state as baseline.
6. **Data Trust** — runtime source health and provenance contract.
7. **Prototype Lab** — experimental workflows that are explicitly separated from production-facing claims.

## Data truth contract

BOUNCAMPUS uses four user-visible classes:

- `OFFICIAL_LIVE` — currently fetched Boğaziçi public page/data.
- `OFFICIAL_SNAPSHOT` — dated local snapshot originating from an official Boğaziçi source.
- `EXTERNAL_LIVE` — current third-party data such as weather.
- `MODEL_ESTIMATE` — computed decision-support output.

`FALLBACK` means a source could not be used. A fallback must never fabricate a previous live value.

The product does not currently claim access to university BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, shuttle GPS or live IoT telemetry.

## Runtime model architecture

The standalone Next.js product is the default hackathon deployment. Its `/api/v1` routes provide the source-traceable product API.

- `/api/v1/dashboard` is the primary operating-state endpoint.
- `/api/v1/buildings` derives current building utilization from the dashboard model.
- `/api/v1/occupancy` derives utilization from the course schedule snapshot.
- `/api/v1/energy` combines building profiles, schedule-derived utilization and current external weather.
- `/api/v1/food` exposes a cafeteria demand estimate without inventing POS-measured waste savings.
- `/api/v1/actions` derives recommendations from the current dashboard model instead of fixed demo text.
- `/api/v1/scenarios/simulate` applies explicit counterfactual deltas to the current dashboard baseline.
- `/api/v1/health` reports upstream source and schedule-snapshot readiness.

The FastAPI service remains available as a separate deployment option but is not required for the standalone hackathon web app.

## Demo path

Recommended 4–6 minute jury flow:

1. Open **Overview** and explain the Data Trust distinction.
2. Show official SKS / Mekik / calendar feeds and external weather.
3. Open **Campus**, pick a building and explain schedule-derived occupancy vs live sensors.
4. Open **Decisions** and show that recommendations stop before automatic actuation.
5. Open **Scenarios** and run a heatwave or exam-week counterfactual.
6. Open **Data Trust** to prove where every signal came from.
7. Only enter **Lab** if the jury asks about future BMS/IoT/energy-control extensions.

## Deployment contract

### Vercel

- Project root: `frontend`
- Framework: Next.js
- `NEXT_PUBLIC_API_URL` should remain empty for the standalone build.
- After deployment verify:
  - `/`
  - `/buildings`
  - `/courses`
  - `/decisions`
  - `/scenarios`
  - `/data`
  - `/api/v1/health`

### Optional FastAPI deployment

Copy `backend/.env.example` to `.env` and set production `CORS_ORIGINS` to the exact frontend origins. Do not use wildcard CORS with credentials.

## Data freshness gate

The current BUIS/ÖBİKAS snapshot predates the 28–30 September 2026 add/drop period. It must be refreshed after add/drop before the final hackathon release. The runtime health layer is designed to expose stale snapshot state rather than hide it.

## Validation pending

Feature implementation and product convergence are separate from release validation. Before merge/release, run:

- `npm ci`
- `npm run typecheck`
- `npm run lint`
- `npm run build`
- backend Python compile/import checks
- source parser checks in the deployed Vercel runtime
- responsive smoke tests on desktop and mobile

GitHub Actions hosted runner allocation is currently tracked separately and should be repaired before release validation is considered complete.
