# BOUNCAMPUS Hackathon Product Release

## KREATE product surface

The jury-facing product is intentionally narrower than the full campus platform. The release must tell one climate story end to end: **measured food-waste problem → uncertainty-aware production decision → human gate → controlled pilot → measured evidence**.

### Primary workspaces

1. **Command Center (`/`)** — official 48,251 kg problem baseline, product thesis, pilot target and operating loop.
2. **Food Waste (`/food-waste`)** — official baseline, source health, readiness-aware production band, operator gate, scenario lab, pilot contract and claim firewall.
3. **Jury Mode (`/demo`)** — five-beat 90-second proof path.
4. **Evidence (`/data`)** — source provenance and truth boundary.
5. **Decisions (`/decisions`)** — existing human approval / outcome-loop infrastructure.

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
- demand-model availability;
- uncertainty-aware production band;
- signal coverage and per-signal availability;
- `PILOT_READY`, `REVIEW_REQUIRED` or `WITHHOLD` decision readiness;
- `operatorApprovalRequired=true`;
- `automaticKitchenDispatch=false`;
- prevention/recovery scenario output;
- pre-registered 14-day pilot contract;
- claim policy;
- explicit official / modeled / unavailable truth boundary.

The historical baseline remains available even if demand context is unavailable. Missing context must widen uncertainty or move the decision to `WITHHOLD`; it must never be replaced by invented certainty.

## Pilot measurement template

`GET /api/v1/food/pilot-template` returns a ready-to-use 14-day CSV with the required service-level fields:

- date;
- service ID;
- control/intervention arm;
- model forecast;
- produced portions;
- served portions;
- edible surplus kg;
- waste kg;
- early sell-out;
- operator override;
- notes.

This makes the day-after-hackathon field workflow executable rather than conceptual.

## Jury demo path

Recommended 90-second flow:

1. **PROBLEM** — show 48,251 kg official 2025 food waste and open the source if challenged.
2. **DECISION** — show next-service band, signal coverage, missing sources and readiness state.
3. **HUMAN GATE** — show approve/hold and `AUTO_DISPATCH=false`.
4. **SCENARIO** — adjust prevention/recovery target; keep `SCENARIO_NOT_RESULT` visible.
5. **EVIDENCE** — show the 14-day matched pilot, primary KPI, minimum evidence and downloadable CSV.

Do not lead with 3D, energy, mobility or feature count. Those are expansion evidence after the core problem is understood.

## Pilot contract

Design: matched `CONTROL` vs `INTERVENTION` services over 14 days.

Primary outcome:

```text
waste_kg_per_100_served = (waste_kg / served_portions) * 100
```

This normalized metric is primary because raw `waste kg / service` is confounded by service volume.

Pre-registered gate:

- minimum **5 measured services per arm**;
- target **≥10% lower normalized waste** versus matched control;
- no increase in early-sellout incidence;
- no food-safety process bypass;
- comparable measurement quality;
- operator overrides reported rather than removed.

The **10% value is a target, not an achieved result**.

Secondary outcomes:

- waste kg / service;
- overproduction rate;
- edible-surplus intensity;
- demand forecast error;
- operator override frequency;
- early-sellout incidence.

Detailed evidence rules live in `docs/food-waste-pilot-protocol.md`.

## Claim firewall

Before measured pilot evidence, the release may show:

- official historical baseline;
- source health and provenance;
- `MODEL_ESTIMATE` demand/production band;
- readiness state;
- explicitly labeled scenario outputs;
- pre-registered pilot target and formulas.

Before measured pilot evidence, the release must not show as achieved:

- kilograms saved by BOUNCAMPUS;
- CO2 avoided by BOUNCAMPUS;
- water saved by BOUNCAMPUS;
- actual cafeteria production optimization;
- actual student demand observation.

Any future carbon/water conversion requires measured direct waste reduction and a documented lifecycle factor.

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
  - `/api/v1/food/pilot-template`
  - `/api/v1/health`

### Optional FastAPI deployment

The FastAPI service remains research infrastructure and is not required for the standalone hackathon product. If deployed, use exact production `CORS_ORIGINS`; do not use wildcard CORS with credentials.

## Data freshness gate

The BUIS/ÖBİKAS schedule snapshot must be refreshed after the 28–30 September 2026 add/drop period before the final hackathon release. A stale snapshot must remain visibly classified as a snapshot rather than being presented as live.

Before the hackathon, also verify that public menu/calendar adapters still resolve and that degraded-source behavior correctly moves the production decision into a wider-band or withheld state.

## Presenter release gate

Before stage use:

1. open `/demo` in a clean browser session;
2. verify official-source link;
3. verify demand band renders or safe degraded state renders;
4. verify readiness badge and source pills;
5. verify pilot approval cannot occur outside `PILOT_READY`;
6. verify `AUTO_DISPATCH=false` text;
7. verify scenario cards say they are not results;
8. verify pilot CSV downloads;
9. rehearse both normal and degraded-source paths;
10. keep official source open in a second tab.

## Engineering validation gate

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

## Release definition of done

The hackathon release is ready only when:

- one primary food-waste story is visible across `/`, `/food-waste`, `/demo`, README and pitch docs;
- secondary energy/mobility/3D modules remain available but do not interrupt the jury path;
- no unsupported impact claim appears on the primary surfaces;
- pilot measurement can begin from the downloadable template without new product design;
- exact-head CI and post-merge master CI are green;
- no stale workstream or integration PR remains open.
