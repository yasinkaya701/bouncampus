# CS1 Campus Operations Decision Core v1

Status: **implementation branch / pre-integration**  
Owner: **CS1 — Decision Intelligence Lead**  
Contract: `campus-ops-v1.0`

## Purpose

Build one aggregate, fail-closed campus decision-support core for cafeteria production, shuttle capacity, classroom allocation, building-energy operating modes, and shared resource capacity without fabricating live university telemetry or measured impact.

The v1 flow is:

```text
aggregate sources + decision cutoff
  -> campus state snapshot
  -> shuttle capacity/headway plan
  -> classroom allocation
  -> cafeteria production target
  -> building-energy operating-mode review
  -> shared-capacity allocation
  -> cross-domain portfolio
  -> human review
```

This package never auto-dispatches shuttles, changes classrooms, controls BMS/HVAC/lighting, alters cafeteria production, or allocates physical resources without operator approval.

## Modules

### 1. Aggregate campus state

`backend/app/decision/campus_state.py`

Inputs include aggregate zone capacity/occupancy/scheduled/event load plus source provenance, publication timestamps, and the decision cutoff. `schedule` and `occupancy_model` are required; future information is rejected; person-level identifiers are rejected. Missing required evidence fails closed to `WITHHOLD`; otherwise the pre-pilot state remains `REVIEW_REQUIRED`.

### 2. Shuttle capacity planner

`backend/app/decision/shuttle_policy.py`

Uses aggregate demand, vehicle capacity/count, service-window/round-trip timing, min/max headway, and an explicit reserve ratio. It returns seat/trip requirements, feasibility, estimated shortfall, and a planning headway target. This is not live GPS dispatch.

### 3. Classroom allocator

`backend/app/decision/classroom_policy.py`

Hard constraints: campus, capacity, accessibility, equipment, and time collision. Among feasible rooms the transparent v1 heuristic prefers lower spare-seat and declared energy-cost penalties. Infeasible sessions are surfaced rather than force-assigned.

### 4. Cafeteria production policy

`backend/app/decision/food_ops_policy.py`

Uses caller-supplied demand scenarios and registered asymmetric surplus/shortage sensitivity weights to choose an integer production target within max capacity. Only `PILOT_ELIGIBLE` / `PILOT_EVALUATED` method evidence can produce a reviewable target. Sandbox evidence and upstream `WITHHOLD` states fail closed.

Truth markers:
- reservation remains `INTENT_SIGNAL_NOT_SERVED_DEMAND`;
- objective units are `REGISTERED_RELATIVE_SENSITIVITY_UNITS`;
- weights are not observed TRY/economic costs;
- no automatic kitchen dispatch is allowed.

### 5. Building-energy policy

`backend/app/decision/building_energy_policy.py`

Consumes aggregate zone capacity/occupancy and caller-registered utilization thresholds. It emits operator-review modes only:
- `SETBACK_REVIEW`;
- `PARTIAL_LOAD_REVIEW`;
- `NORMAL_SERVICE_REVIEW`.

Occupancy above declared capacity fails closed. No live BMS access, calibrated kWh model, or achieved energy/cost/carbon saving is claimed.

### 6. Shared-capacity allocator

`backend/app/decision/shared_capacity_policy.py`

Allocates discrete aggregate capacity across named requests using registered minimums, desired levels, and priority weights. Minimums are satisfied first; remaining units are assigned deterministically by registered priority. If minimums exceed available capacity, the allocator returns `WITHHOLD`. Person-level allocation and automatic actuation are outside scope.

### 7. Cross-domain portfolio

`backend/app/decision/campus_portfolio.py`

The portfolio does not invent a global sustainability score. It exposes one operator-reviewed view containing:
- campus demand context;
- cafeteria recommended production when available;
- building energy review modes;
- shared-capacity allocations;
- shuttle capacity-shortfall routes;
- unassigned classroom sessions;
- building attendance targets;
- per-domain readiness status.

A withheld core campus state withholds the entire portfolio. Optional withheld domains produce no fabricated recommendation and remain explicitly marked in `domain_status` / reason codes.

## FastAPI surface

Router: `backend/app/routers/campus_ops.py`

Endpoints:
- `GET /api/v1/campus-ops/contract`
- `POST /api/v1/campus-ops/state`
- `POST /api/v1/campus-ops/shuttle/plan`
- `POST /api/v1/campus-ops/classrooms/allocate`
- `POST /api/v1/campus-ops/food/plan`
- `POST /api/v1/campus-ops/energy/plan`
- `POST /api/v1/campus-ops/shared-capacity/allocate`
- `POST /api/v1/campus-ops/portfolio`
- `POST /api/v1/campus-ops/plan`

`/plan` executes one decision-cutoff-consistent advisory pass and returns state, shuttle, classroom, optional food, optional energy, optional shared-capacity, and the combined portfolio.

## Evidence and truth boundary

This implementation establishes **repository capability**, not deployment evidence. It does not establish live BMS, Wi-Fi/turnstile occupancy, shuttle GPS, cafeteria POS, registrar integration, achieved savings, or autonomous pilot readiness.

Allowed provenance labels remain explicit: `PUBLIC_SOURCE`, `MODEL_ESTIMATE`, `POLICY_HEURISTIC`, `MEASURED_PILOT`. Impact claims remain unmeasured until real pilot evidence exists.

## Privacy boundary

The aggregate campus-operations contract rejects person-level identifiers including student IDs, BUCard IDs, user/person IDs, emails, phones, scholarship status, and national identifiers. The supported decisions do not require individual movement profiling.

## Focused validation commands

```bash
python scripts/test_cs1_campus_state.py
python scripts/test_cs1_shuttle_policy.py
python scripts/test_cs1_classroom_policy.py
python scripts/test_cs1_food_ops_policy.py
python scripts/test_cs1_building_energy_policy.py
python scripts/test_cs1_shared_capacity_policy.py
python scripts/test_cs1_campus_portfolio.py
python scripts/test_cs1_campus_ops_router.py
python scripts/test_cs1_source_health.py
python -m compileall -q backend/app scripts
python scripts/kreate_check.py
```

These commands are the intended focused validation suite; repository CI remains authoritative before integration.

## Integration state

The implementation remains isolated on `agent/api-product/cs1-campus-ops-core` from `role/cs1-decision-intelligence`.

The CS1 role currently has three open feature PR slots occupied by #68, #69, and #83. Do not open a fourth role-targeting PR until a slot is freed. When a slot opens, promote this existing branch rather than creating a duplicate campus-ops branch. Exact-head CI must be green before merge.
