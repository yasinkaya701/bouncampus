# BOUNCAMPUS — Product Walkthrough

## Product definition

BOUNCAMPUS is a source-traceable **campus Mission Control** for Boğaziçi University.

The hackathon build is designed around one operational loop:

```text
SENSE → DECIDE → STRESS-TEST → HUMAN APPROVAL → PILOT → LEARN
```

It is intentionally **not** presented as a live SCADA/BMS platform. The current product does not have authorized university BMS, smart-meter, turnstile, Wi-Fi occupancy, cafeteria POS, shuttle GPS or IoT telemetry.

---

## 1. Mission Control — `/`

The landing workspace is the operational briefing, not a generic dashboard.

It shows:

- today's Mission Brief;
- source confidence;
- top modeled impact;
- public-source context;
- schedule-derived campus utilization;
- a campus map;
- ranked human-reviewable decision candidates;
- provenance for every input.

Primary CTA: **Run 90-second Jury Mode**.

---

## 2. Jury Mode — `/demo`

Four-stage guided demo:

### SENSE

Evidence cards expose the current source state:

- BUIS/ÖBİKAS schedule snapshot;
- SKS menu;
- Mekik timetable;
- Bebek weather.

Each card shows provenance and health.

### REASON

The deterministic Mission Brief contains:

- recommendation;
- why now;
- confidence;
- location;
- operating window;
- modeled impacts;
- human guardrail.

### SIMULATE

The current dashboard baseline can be recomputed under a counterfactual such as heavy rain or heatwave.

These outputs are scenario model estimates, not forecasts or telemetry.

### ACT

The demo can create a browser-only **pilot review receipt**.

This does not dispatch a real command.

---

## 3. Mission Brief API — `/api/v1/brief`

The Mission Brief is the central product object.

```text
{
  status,
  title,
  one_liner,
  why_now,
  confidence,
  confidence_label,
  decision_id,
  decision_type,
  location,
  operating_window,
  recommendation,
  guardrail,
  evidence[],
  impact[],
  source_health,
  dashboard
}
```

Confidence is calculated from **upstream input sources**, not from the health of the product's own model outputs.

A model cannot increase its own confidence score simply by being available.

---

## 4. Data Trust — `/data`

Provenance classes:

- `OFFICIAL_LIVE`
- `OFFICIAL_SNAPSHOT`
- `EXTERNAL_LIVE`
- `MODEL_ESTIMATE`
- `FALLBACK`

The product never silently converts one class into another.

### Demo resilience

Selected official public sources also have a dated last-known-good public snapshot.

If the current upstream cannot be verified:

- snapshot content can remain visible for continuity;
- the source remains `ok=false`;
- provenance is snapshot/degraded;
- Mission confidence decreases;
- the UI explicitly says the value is not live.

This prevents a temporary public-page timeout from destroying the demo while preserving the truth boundary.

---

## 5. Campus — `/buildings`

Building inventory and detail pages expose campus configuration and schedule-derived utilization.

Current occupancy is **not** a live sensor measurement.

The model derives demand from:

- official-source course schedule snapshot;
- room/building mapping;
- capacity assumptions;
- evaluation hour.

A real pilot would calibrate this against authorized anonymous occupancy aggregates.

---

## 6. Schedule Explorer — `/courses`

The schedule workspace makes the official-source course snapshot explorable by:

- department/course;
- day;
- room/building;
- campus context.

The snapshot has an explicit freshness boundary and must be refreshed after schedule-changing registration periods.

---

## 7. Decision Ledger — `/decisions`

Each surfaced decision remains human-controlled.

Local demo states:

- `REVIEW`
- `APPROVED_FOR_PILOT`
- `DECLINED`

The ledger is intentionally browser-local in the hackathon build. It demonstrates the workflow without pretending a production identity/audit backend already exists.

---

## 8. Outcome Calibration Loop

The Decisions workspace also contains the learning loop.

A user can select a decision candidate, enter an observed pilot result, and compare it with the pre-pilot model potential.

The UI calculates model error and records browser-local calibration evidence.

```text
model potential → human pilot → observed outcome → model error
```

A production implementation would persist this evidence server-side with operator identity, authorization and immutable audit history.

---

## 9. Counterfactual Simulator — `/scenarios`

Supported scenarios include:

- heatwave;
- exam week;
- campus event;
- rain;
- building closure;
- summer school.

The scenario API starts from the current dashboard state. It does not swap to a separate canned result table.

Endpoint:

```text
POST /api/v1/scenarios/simulate
```

---

## 10. Decision Explainer

The floating assistant is a deterministic, mission-aware explainer.

It can answer:

- Why this mission?
- Which evidence is weakest?
- Which values are live?
- What must a human verify before acting?
- What would improve confidence?

It cannot dispatch a campus command.

---

## 11. Current public data inputs

### Official/public Boğaziçi sources

- SKS cafeteria menu;
- Mekik published timetable;
- Academic Calendar;
- dated BUIS/ÖBİKAS course schedule snapshot.

### External live context

- Open-Meteo weather for Bebek campus coordinates.

### Model outputs

- schedule-derived utilization;
- physics-lite building energy;
- cafeteria demand;
- savings potential;
- CO₂ potential;
- counterfactual scenario deltas.

Model outputs are never labeled as campus sensor readings.

---

## 12. Prototype Lab — `/lab`

Legacy / future-looking modules remain available under a clearly marked Prototype Lab.

They are not part of the core production-facing claim until the required university data or hardware integration exists.

This keeps technical exploration without contaminating the primary product truth boundary.

---

## 13. Pilot readiness

Highest-value read-only integrations:

1. anonymous occupancy aggregates;
2. building/floor smart-meter or BMS totals;
3. anonymized cafeteria POS totals by time bucket;
4. shuttle AVL/GPS.

No raw student identity is required for the core optimization loop.

### Proposed 30-day pilot

- **Week 1:** read-only integration
- **Week 2:** calibration
- **Week 3:** human-approved operator pilot
- **Week 4:** outcome proof

### Proposed validation gates — not current performance claims

- occupancy model ≤20% MAPE;
- food-demand model ≤15% MAPE;
- measured positive energy savings for qualifying interventions;
- ≥70% operator acceptance/usefulness for surfaced missions.

---

## 14. Privacy model

Default principles:

- aggregate before individual data;
- no raw student identifiers in the decision layer;
- read-only integrations before control;
- source-level provenance and freshness metadata;
- human approval before any real-world operational action.

---

## 15. Product endpoints

```text
GET  /api/v1/health
GET  /api/v1/dashboard
GET  /api/v1/brief
GET  /api/v1/actions
GET  /api/v1/buildings
GET  /api/v1/occupancy
GET  /api/v1/energy
GET  /api/v1/food
POST /api/v1/scenarios/simulate
```

---

## 16. Demo order

Recommended judging path:

```text
/demo
  ↓
Signal fusion
  ↓
Mission + confidence
  ↓
Counterfactual stress test
  ↓
Human approval receipt
  ↓
/decisions
  ↓
Outcome calibration loop
  ↓
/data
  ↓
30-day pilot + privacy-safe integration plan
```

The complete 90-second narration lives in [`jury-demo-script.md`](jury-demo-script.md).

---

## Current release truth

The product implementation is substantially complete, but final release validation is a separate gate.

Before a hackathon release, run:

- dependency install;
- TypeScript typecheck;
- lint;
- Next.js production build;
- route/API smoke testing;
- mobile/desktop visual smoke testing;
- deployed `/api/v1/health` and `/api/v1/brief` verification.

Do not infer that a feature is validated merely because it exists in the repository.
