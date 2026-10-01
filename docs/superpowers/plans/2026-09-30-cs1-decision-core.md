# CS1 Decision Intelligence v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the broadest defensible CS1 decision-intelligence layer for the KREATE food-waste wedge: versioned decision policy, abstention, source health, model provenance, leakage-safe baselines, pilot evidence gates, cross-surface claim firewall, and falsifiable evaluation.

**Architecture:** Separate four evidence layers that must never be conflated: model point estimation, policy heuristics, offline technical evaluation, and measured pilot outcomes. A single versioned food-decision contract is shared conceptually across Python and Next.js surfaces. Active product routes may expose a model estimate and operator-reviewed planning range, but they must abstain when required context is missing and must not emit achieved food-waste/cost/climate savings before measured evidence exists.

**Tech Stack:** Python 3.11, FastAPI/Pydantic, XGBoost model adapter, Next.js 14/TypeScript, standard-library regression tests, KREATE mechanical validation.

**Spec:** `KREATE/ROLES/03_CS1_DECISION_INTELLIGENCE_LEAD.md`, `docs/food-waste-pilot-protocol.md`, and `KREATE/EXPERIMENTS/CS1_DECISION_INTELLIGENCE_V1.md`.

## Global Constraints

- Do not invent PMR, calibration, pilot outcomes, model superiority, or achieved waste/cost/carbon/water savings.
- Human approval remains mandatory; automatic kitchen dispatch remains disabled.
- `WITHHOLD` must be a real operational state with no production target.
- Signal weights, readiness thresholds, and planning-band factors are `POLICY_HEURISTIC`, not learned probabilities.
- Planning ranges are `PLANNING_RANGE_NOT_CALIBRATED_INTERVAL` until measured calibration exists.
- Baseline/model evaluation must be chronological and past-only; no future outcome leakage.
- Offline forecast metrics are `TECH_TEST` / `OFFLINE_BENCHMARK_ONLY`, not impact evidence.
- Pilot evidence may be promoted only after data-quality, sample-size, waste-target, sellout, and manual food-safety review gates.
- Repository capability evidence does not promote H-006 beyond `TESTING` without operator/PMR or measured pilot evidence.
- Preserve the repository single-integration-PR rule and do not touch `.github/workflows/ci.yml` while TASK-FABRIC-CLI owns it.

## Review Focus

- Missing required schedule context or non-positive/non-finite demand must cause abstention.
- Dashboard/action routes must not bypass `/food` truth boundaries by emitting fabricated food-waste kg/TL impact.
- Model outputs, heuristic ranges, technical benchmark results, and measured pilot results must carry distinct provenance/claim semantics.
- Baseline generators must never use the target or future observation when forecasting that target.
- Pilot scorecards must reject malformed/duplicate/incomplete evidence and must never generalize a pilot result into climate-impact proof.

---

### Task 1: Versioned food decision policy and model separation

**Files:**
- Create: `backend/app/decision/__init__.py`
- Create: `backend/app/decision/food_policy.py`
- Modify: `backend/app/optimizers/food_optimizer.py`
- Modify: `backend/app/models/food_demand.py`
- Test: `scripts/test_food_decision_policy.py`

**Interfaces:**
- Consumes: a model point estimate plus source-availability booleans.
- Produces: policy version, model/policy provenance, planning range, readiness, abstention, reason codes, limitations, and human-review flags.

- [x] Write focused policy tests before implementation.
- [x] Remove the optimizer’s unsupported historical-buffer/waste-reduction calculation.
- [x] Separate point forecast from decision range and expose model/training provenance.
- [x] Make lunch/dinner selection explicit in food-model prediction.
- [x] Implement `PILOT_READY`, `REVIEW_REQUIRED`, and `WITHHOLD` with safe handling of invalid demand.

### Task 2: Leakage-safe baseline and evaluation framework

**Files:**
- Create: `backend/app/decision/baselines.py`
- Create: `scripts/cs1_baseline_benchmark.py`
- Test: `scripts/test_cs1_decision_intelligence.py`

**Interfaces:**
- Consumes: chronologically ordered measured/labeled service outcomes and optional model/operator forecasts.
- Produces: previous-service, expanding-mean, rolling-mean, seasonal-lag baselines plus MAE, RMSE, WAPE, signed bias, and deterministic ranking.

- [x] Implement past-only naive baselines.
- [x] Implement aligned forecast metrics with missing-pair handling.
- [x] Add CLI requiring explicit dataset provenance label; never synthesize observations.
- [x] Scope all output to `TECH_TEST` / `OFFLINE_BENCHMARK_ONLY`.

### Task 3: Python API and active-action contract parity

**Files:**
- Modify: `backend/app/schemas.py`
- Modify: `backend/app/routers/food.py`
- Modify: `backend/app/routers/dashboard.py`
- Modify: `backend/app/routers/actions.py`

**Interfaces:**
- Consumes: model estimates and the versioned decision policy.
- Produces: typed food forecasts/actions with provenance and no unsupported pre-pilot impact claims.

- [x] Replace food savings fields with decision-integrity fields.
- [x] Tag menu popularity and action values with explicit provenance.
- [x] Make dashboard food actions respect abstention/human review.
- [x] Remove fabricated food-waste saved kg/TL calculations from dashboard/action surfaces.
- [x] Mark `/metrics/impact` food-waste impact `UNMEASURED` while preserving energy-model compatibility.

### Task 4: Next.js decision contract and truth boundary

**Files:**
- Modify: `frontend/src/lib/food-waste.ts`
- Modify: `frontend/src/lib/types.ts`
- Modify: `frontend/src/app/api/v1/food/route.ts`

**Interfaces:**
- Consumes: dashboard source health and demand estimate.
- Produces: versioned production decision assessment, nullable actionable band, policy metadata, baseline-evaluation readiness, scenario labeling, and claim boundaries.

- [x] Mirror the versioned policy semantics in TypeScript.
- [x] Return `productionBand=null` when the decision abstains while retaining a full `decisionAssessment` for diagnostics.
- [x] Expose calibration status, signal coverage, reason codes, limitations, human gate, and forbidden-until-measured claims.
- [x] Distinguish official, modeled, policy-heuristic, measured-pilot, and unavailable truth classes.

### Task 5: Pilot evidence-quality and promotion gates

**Files:**
- Modify: `frontend/src/lib/food-waste.ts`
- Modify: `frontend/src/app/api/v1/food/pilot-score/route.ts`
- Modify: `frontend/src/app/api/v1/food/pilot-template/route.ts`

**Interfaces:**
- Consumes: real CONTROL/INTERVENTION service measurements only.
- Produces: validated pilot scorecard plus explicit evidence-promotion status.

- [x] Validate dates, service IDs, produced/served consistency, forecast retention, and numeric fields.
- [x] Detect duplicate service rows and require 100% intervention forecast retention.
- [x] Require minimum services per arm, normalized waste target, and early-sellout guardrail before `PROMISING`.
- [x] Keep food-safety review manual and block generalized climate-impact promotion.
- [x] Derive pilot CSV template fields/duration from the protocol contract.

### Task 6: Mechanical claim firewall and regression suite

**Files:**
- Modify: `scripts/kreate_check.py`
- Modify: `scripts/test_food_decision_policy.py`
- Create/modify: `scripts/test_cs1_decision_intelligence.py`

**Interfaces:**
- Consumes: all active food decision surfaces.
- Produces: deterministic failure when unsafe impact fields, missing policy markers, missing human gates, weakened pilot gates, or legacy fabricated dashboard/action claims reappear.

- [x] Guard `/food`, `/dashboard`, `/actions`, optimizer, schema, Next food API, pilot API, and baseline benchmark.
- [x] Add focused logic tests for readiness/abstention/baselines/metrics.
- [x] Add static regression checks for claim-firewall and provenance markers.
- [ ] Run the full validation command set on the exact branch head before integration.

### Task 7: Evidence and falsifiable evaluation record

**Files:**
- Create: `KREATE/EXPERIMENTS/CS1_DECISION_INTELLIGENCE_V1.md`
- Modify: `KREATE/EVIDENCE.md`
- Modify: `KREATE/ASSUMPTIONS.md`

**Interfaces:**
- Consumes: implemented repository capability and future real PMR/benchmark/pilot artifacts.
- Produces: narrow repo-state evidence today and pre-registered criteria for future KEEP/MODIFY/KILL decisions.

- [x] Register E-REP-004 as repository capability only.
- [x] Keep H-006 in `TESTING` and state what evidence is still missing.
- [x] Pre-register baseline, workflow, pilot success/failure, evidence promotion, and claim-boundary rules.
- [x] Explicitly record that no measured cafeteria-result/model-superiority/impact result has been run or promoted.

### Task 8: Integration verification

**Files:**
- No new product scope unless verification exposes a defect.

- [ ] Compare branch against latest `master` and inspect every changed path.
- [ ] Run `python scripts/test_food_decision_policy.py`.
- [ ] Run `python scripts/test_cs1_decision_intelligence.py`.
- [ ] Run `python scripts/kreate_check.py`.
- [ ] Run `python -m compileall -q backend/app scripts`.
- [ ] Run `cd frontend && npm run typecheck && npm run lint && npm run build`.
- [ ] Confirm the single integration PR slot is free before opening a CS1 PR.
- [ ] Merge only after exact-head validation, then mark the task `MERGED_VERIFIED` after post-merge checks.
