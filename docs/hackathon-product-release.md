# BOUNCAMPUS Hackathon Product Release

## KREATE product surface

The jury-facing product is intentionally narrower than the full campus platform.

### Primary workspaces

1. **Command Center (`/`)** — official 48,251 kg problem baseline, product thesis and operating loop.
2. **Food Waste (`/food-waste`)** — monthly official baseline, next-service planning context, prevention/recovery scenario and pilot measurement contract.
3. **Jury Mode (`/demo`)** — four-step 90-second proof path.
4. **Evidence (`/data`)** — source provenance and truth boundary.
5. **Decisions (`/decisions`)** — human approval / outcome-loop infrastructure.

### Supporting platform surfaces

- `/courses` — schedule context.
- `/buildings` — campus building intelligence.
- `/scenarios` — existing counterfactual model workspace.
- `/mobility` — source-backed shuttle workspace.
- `/lab` — experimental workflows, never part of the primary pitch.

## Data truth contract

BOUNCAMPUS uses visible provenance classes:

- `OFFICIAL_LIVE` — currently fetched Boğaziçi public page/data;
- `OFFICIAL_SNAPSHOT` — dated local snapshot from an official Boğaziçi source;
- `EXTERNAL_LIVE` — current third-party context such as weather;
- `MODEL_ESTIMATE` — computed decision-support output;
- `OFFICIAL_PUBLIC` — source-backed historical/public institutional baseline used by the food-waste module.

The product does not claim access to university BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, kitchen production telemetry, shuttle GPS or live IoT telemetry unless such a source is explicitly integrated and verified.

## Food-waste runtime contract

`GET /api/v1/food` is the primary KREATE product endpoint. It returns:

- 2024/2025 official food-waste baseline;
- 2025 monthly food-waste values;
- official annual recovery value;
- demand-model availability and conservative production band;
- prevention/recovery scenario output;
- explicit official / modeled / unavailable truth boundary.

The historical baseline remains available even if the dashboard demand context is unavailable. If demand cannot be calculated, the product withholds a production recommendation instead of inventing one.

## Jury demo path

Recommended 90-second flow:

1. **PROVE** — show 48,251 kg official 2025 food waste and open the source if challenged.
2. **FORECAST** — show the next-service demand/production band and its `MODEL_ESTIMATE` label.
3. **STRESS-TEST** — adjust prevention/recovery target against the official historical baseline.
4. **PILOT** — show the 14-day controlled measurement plan and primary outcome `waste kg / service`.

Do not lead with 3D, energy, mobility or feature count. Those are expansion evidence after the core problem is understood.

## Pilot contract

For each pilot service record:

1. portions produced;
2. portions served;
3. edible surplus;
4. waste kg;
5. operator override / reason when applicable.

Primary outcome:

```text
waste kg / service
```

Secondary outcomes:

- overproduction rate;
- edible-surplus recovery;
- demand forecast error;
- operator override frequency.

No modeled scenario result may be presented as measured impact before this pilot evidence exists.

## Deployment contract

### Vercel

- Project root: `frontend`
- Framework: Next.js
- `NEXT_PUBLIC_API_URL` should remain empty for the standalone build.
- After deployment verify:
  - `/`
  - `/food-waste`
  - `/demo`
  - `/decisions`
  - `/data`
  - `/api/v1/food`
  - `/api/v1/health`

### Optional FastAPI deployment

The FastAPI service remains research infrastructure and is not required for the standalone hackathon product. If deployed, use exact production `CORS_ORIGINS`; do not use wildcard CORS with credentials.

## Data freshness gate

The BUIS/ÖBİKAS schedule snapshot must be refreshed after the 28–30 September 2026 add/drop period before the final hackathon release. A stale snapshot must remain visibly classified as a snapshot rather than being presented as live.

## Validation gate

Before merge/release:

```bash
cd frontend
npm ci
npm run typecheck
npm run lint
npm run build
```

Repository gate:

```bash
python scripts/verify_feature_preservation.py --base-ref <master-sha>
```

Also compile backend Python, validate critical JSON datasets, require exact-head PR CI, merge through the repository integration contract, then verify the resulting `master` commit before releasing the workstream.
