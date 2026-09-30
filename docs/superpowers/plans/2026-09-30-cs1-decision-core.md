# CS1 Food Decision Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the smallest defensible food-decision core: no unsupported pre-pilot savings claims, explicit readiness/abstention, human review, reason codes, and provenance.

**Architecture:** Keep the current food-demand model untouched. Refactor `FoodOptimizer` into a transparent operator-reviewed planning policy, expose that contract through the Python food API, and mechanically guard the claim boundary in KREATE validation. The planning band is a `POLICY_HEURISTIC`, not a calibrated confidence interval.

**Tech Stack:** Python 3.11, FastAPI/Pydantic, standard-library regression tests.

**Spec:** `KREATE/ROLES/03_CS1_DECISION_INTELLIGENCE_LEAD.md` and `docs/food-waste-pilot-protocol.md`.

## Global Constraints

- Do not claim achieved waste, cost, carbon, or water savings before measured pilot evidence.
- Human approval remains mandatory; automatic kitchen dispatch remains disabled.
- `WITHHOLD` must be available when the schedule backbone is missing.
- Heuristic band widths must be labeled `POLICY_HEURISTIC`; do not call them confidence intervals.
- Do not add benchmarking, calibration, ablation, or broad UI changes in this package.

## Review Focus

- Missing schedule context must withhold an operational recommendation.
- Missing optional menu context must degrade to review-required rather than look fully ready.
- Full core context must still require a human operator.
- The policy must never emit `waste_reduction`, `potential_waste_saved_kg`, or `cost_saved_tl` as achieved impact.
- Zero/negative demand inputs must remain safe and non-negative.

---

### Task 1: Lock the decision policy contract with failing tests

**Files:**
- Create: `scripts/test_food_decision_policy.py`
- Modify later: `backend/app/optimizers/food_optimizer.py`

**Interfaces:**
- Consumes: `FoodOptimizer.optimize(date, cafeteria_id, predicted_demand, menu, signal_availability=None)`.
- Produces: regression expectations for readiness, abstention, provenance, reason codes, and absence of savings claims.

- [ ] Write tests for `WITHHOLD`, `REVIEW_REQUIRED`, `PILOT_READY`, provenance, human review, and claim-firewall fields.
- [ ] Run `python scripts/test_food_decision_policy.py` and confirm RED against current optimizer.
- [ ] Implement only the policy behavior required by those tests.
- [ ] Re-run the test and confirm GREEN.

### Task 2: Expose the minimal contract through the Python food API

**Files:**
- Modify: `backend/app/schemas.py`
- Modify: `backend/app/routers/food.py`

**Interfaces:**
- Consumes: the `FoodOptimizer.optimize(...)` result from Task 1.
- Produces: `FoodDemandForecast` with planning bounds, optional recommendation, readiness, model/policy provenance, human-review flags, reason codes, and limitations.

- [ ] Remove pre-pilot savings fields from the food response schema.
- [ ] Map optimizer output into the response without inventing calibrated confidence or measured impact.
- [ ] Compile Python sources.

### Task 3: Add a mechanical claim-firewall gate

**Files:**
- Modify: `scripts/kreate_check.py`

**Interfaces:**
- Consumes: active food decision source files.
- Produces: CI failure when forbidden pre-pilot savings fields return to the Python food decision contract.

- [ ] Add a KREATE source-contract check for forbidden food-impact output fields and required decision-integrity markers.
- [ ] Run `python scripts/kreate_check.py`.
- [ ] Run `python scripts/test_food_decision_policy.py` and `python -m compileall -q backend/app scripts`.
