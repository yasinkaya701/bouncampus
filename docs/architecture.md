# BOUNCAMPUS — Architecture

## Product architecture for KREATE

BOUNCAMPUS is currently a **decision-support and evidence system**, not an autonomous campus-control system.

The KREATE release centers on food-waste prevention while preserving existing energy, mobility and 3D modules as secondary surfaces.

```text
OFFICIAL / PUBLIC BASELINE
├─ Boğaziçi food-waste history
├─ dining-service context
└─ published institutional sources
            │
            ▼
CURRENT CONTEXT ADAPTERS
├─ course schedule snapshot
├─ weather
├─ menu
└─ academic calendar
            │
            ▼
SOURCE HEALTH + PROVENANCE
            │
            ▼
TRANSPARENT DEMAND HEURISTIC
            │
            ▼
UNCERTAINTY-AWARE PRODUCTION BAND
├─ lower bound
├─ recommended operator starting point
├─ upper bound
├─ signal coverage
└─ reason codes
            │
            ▼
DECISION READINESS
├─ PILOT_READY
├─ REVIEW_REQUIRED
└─ WITHHOLD
            │
            ▼
HUMAN OPERATOR GATE
├─ approve controlled pilot
├─ edit recommendation
└─ hold
            │
            ▼
MATCHED CONTROL / INTERVENTION PILOT
            │
            ▼
MEASURED SCORECARD
├─ waste kg / 100 served meals
├─ overproduction rate
├─ edible surplus intensity
├─ forecast error
├─ early sell-out
└─ operator override
            │
            ▼
CALIBRATION / NEXT SERVICE
```

## Runtime boundary

The standalone hackathon product runs primarily through the **Next.js application and its `/api/v1/*` route handlers**.

The repository also contains a FastAPI/Python research backend and legacy/experimental modules. Those are not required for the core KREATE flow unless explicitly connected by the release.

## Core KREATE API contract

### `GET /api/v1/food`

Returns:

- official food-waste baseline;
- monthly historical values;
- source-backed demand context;
- production band;
- signal coverage;
- decision readiness;
- human-approval policy;
- scenario output;
- pilot contract;
- claim policy;
- truth boundary.

### `GET /api/v1/food/pilot-template`

Returns a downloadable CSV template for the 14-day service-level pilot.

### `POST /api/v1/food/pilot-score`

Accepts **measured** control/intervention service outcomes and computes the pre-defined scorecard. It does not generate fake measurements.

### `GET /api/v1/dashboard`

Provides shared campus context used by the product, including schedule-derived occupancy context, weather/menu/calendar adapters and secondary platform model outputs.

## Current food-demand method

The current implementation is intentionally transparent and pilot-oriented.

The dashboard estimates lunch demand from schedule-derived midday class flow and available contextual signals. The food endpoint then converts that estimate into a production decision band.

This release does **not** claim that an XGBoost, neural network, collaborative-filtering model or cafeteria POS-trained model is running when such a model is not present in the runtime path.

### Signal-coverage policy

Current transparent pilot weights:

| Signal | Weight |
|---|---:|
| Course schedule | 50% |
| Weather | 20% |
| Menu context | 20% |
| Academic calendar | 10% |

These weights control readiness/uncertainty behavior; they are not presented as learned optimal coefficients.

### Readiness logic

- Schedule available + coverage ≥70% → `PILOT_READY`
- Schedule available + coverage ≥50% → `REVIEW_REQUIRED`
- Otherwise → `WITHHOLD`

Uncertainty widens when context is missing.

`PILOT_READY` means **suitable for a human-reviewed test**, not “validated production-grade forecast.”

## Human-control architecture

The product contract is:

```text
operatorApprovalRequired = true
autoDispatchAllowed = false
```

No KREATE release path sends a command to a real cafeteria production system.

The UI may demonstrate approval state, but that is explicitly labeled as an internal/demo workflow unless an authorized external integration is later added.

## Pilot evidence architecture

### Required service-level fields

```text
date
service_id
arm
model_forecast_meals
produced_portions
served_portions
edible_surplus_kg
waste_kg
early_sellout
operator_override
notes
```

### Primary metric

```text
waste_kg_per_100_served = (waste_kg / served_portions) * 100
```

### Scorecard engine

The scorecard compares measured control and intervention services and reports:

- number of measured services;
- mean normalized food waste;
- mean raw waste per service;
- mean overproduction rate;
- mean edible-surplus intensity;
- mean forecast absolute percentage error;
- early-sellout rate;
- operator-override rate;
- normalized waste reduction versus control;
- evidence and service guardrails.

A `PROMISING` pilot classification requires the numeric gates to pass, but food-safety compliance still requires manual operational review.

## Pre-registered pilot gate

Current KREATE pilot contract:

- ≥5 measured services in control;
- ≥5 measured services in intervention;
- ≥10% lower `waste kg / 100 served meals` in intervention versus control;
- no increase in early-sellout incidence;
- no food-safety process bypass.

The 10% value is a target, not an achieved impact claim.

## Claim firewall

### Direct evidence allowed

- published food-waste history;
- source provenance and availability;
- measured pilot service outcomes once actually collected.

### Model/scenario outputs allowed only with labels

- next-service meal estimate;
- production band;
- readiness state;
- scenario prevention/recovery values.

### Not claimable before measurement

- kilograms saved by BOUNCAMPUS;
- carbon avoided by BOUNCAMPUS;
- water saved by BOUNCAMPUS;
- actual cafeteria production optimized;
- actual student demand observed.

## Secondary platform architecture

The repository retains existing modules for:

- schedule-derived campus occupancy context;
- building energy scenarios;
- building directory and map layers;
- Cesium/3D/photogrammetry;
- shuttle mobility;
- decision and scenario workspaces.

These surfaces are preserved for platform expansion, but they do not replace the primary KREATE food-waste evidence chain.

## Energy model status

The current dashboard contains a simplified building-energy estimate based on building profile, schedule-derived occupancy context and outside temperature. It is a `MODEL_ESTIMATE`, not BMS or smart-meter telemetry.

The KREATE food-waste release must not present modeled energy savings as measured climate impact.

## Data provenance rule

Every important input/output should remain classifiable as one of:

- `OFFICIAL_PUBLIC`
- `OFFICIAL_LIVE`
- `OFFICIAL_SNAPSHOT`
- `EXTERNAL_LIVE`
- `MODEL_ESTIMATE`

If the source is missing or stale, the product must degrade visibly rather than silently replacing it with fabricated telemetry.

## Privacy architecture

The first food-waste pilot requires no student-level identity.

Service measurements are aggregate operational records. The product does not require:

- named student records;
- payment identity;
- device identity;
- Wi-Fi tracking;
- individual meal consumption history.

## Design principle

The technical differentiator is not a claim of model complexity.

It is the closed operating contract:

```text
PROVENANCE
→ UNCERTAINTY
→ HUMAN DECISION
→ MEASURED OUTCOME
→ CALIBRATION
```

The model can become more sophisticated after real operational data exists without changing this evidence architecture.
