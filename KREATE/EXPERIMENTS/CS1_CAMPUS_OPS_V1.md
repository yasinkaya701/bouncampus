# CS1 Campus Operations Decision Core v1

Status: **implementation branch / pre-integration**  
Owner: **CS1 — Decision Intelligence Lead**  
Contract: `campus-ops-v1.0`

## Purpose

Build one aggregate, fail-closed campus decision-support core for cafeteria production, shuttle capacity, classroom allocation, building-energy operating modes, space/zone activation, and shared resource capacity without fabricating live university telemetry or measured impact.

The v1 flow is:

```text
aggregate sources + decision cutoff
  -> campus state snapshot
  -> shuttle capacity/headway plan
  -> classroom allocation
  -> cafeteria production target
  -> building-energy operating-mode review
  -> space/zone activation review
  -> shared-capacity allocation
  -> cross-domain portfolio
  -> human review
```

This package never auto-dispatches shuttles, changes classrooms, controls BMS/HVAC/lighting, opens/closes zones, alters cafeteria production, or allocates physical resources without operator approval.

## Modules

### 1. Aggregate campus state

`backend/app/decision/campus_state.py`

Inputs include aggregate zone capacity/occupancy/scheduled/event load plus source provenance, publication timestamps, and the decision cutoff. `schedule` and `occupancy_model` are required; future information is rejected; person-level identifiers are rejected. Missing required evidence fails closed to `WITHHOLD`; otherwise the pre-pilot state remains `REVIEW_REQUIRED`.

Source health is emitted with canonical provenance, decision-time acceptance, freshness when a timestamp is available, coverage metadata, and a status. Legacy input aliases are normalized before output.

### 2. Shuttle capacity planner

`backend/app/decision/shuttle_policy.py`

Uses aggregate demand, vehicle capacity/count, service-window/round-trip timing, min/max headway, and an explicit reserve ratio. It returns seat/trip requirements, feasibility, estimated shortfall, and a planning headway target. Capacity-sensitive output is withheld unless the vehicle-capacity snapshot has verified operational provenance. This is not live GPS dispatch.

### 3. Classroom allocator

`backend/app/decision/classroom_policy.py`

Hard constraints: campus, capacity, accessibility, equipment, and time collision. Among feasible rooms the transparent v1 heuristic prefers lower spare-seat and declared energy-cost penalties. Infeasible sessions are surfaced rather than force-assigned. Room inventory and attendance/enrollment must carry verified operational provenance before an assignment is emitted. Boolean accessibility fields are strict and are never inferred from string truthiness.

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

### 6. Space / zone activation policy

`backend/app/decision/space_activation_policy.py`

Enumerates feasible bundles of aggregate campus zones and minimizes a transparent registered loss over occupancy scenarios, idle capacity, shortage sensitivity, and activation weights. A bundle must satisfy the registered pointwise service floor. Physical zone capacity must have verified provenance; sandbox/unavailable/pure-policy occupancy evidence cannot drive an operator recommendation.

The result is an advisory open/close review only. It explicitly sets `energy_savings_claim_allowed=false`; selected zones are not converted into claimed kWh, TRY, carbon, or measured savings.

### 7. Shared-capacity allocator

`backend/app/decision/shared_capacity_policy.py`

Allocates discrete aggregate capacity across named requests using registered minimums, desired levels, and priority weights. Minimums are satisfied first; remaining units are assigned deterministically by registered priority. If minimums exceed available capacity, the allocator returns `WITHHOLD`. Person-level allocation and automatic actuation are outside scope.

### 8. Cross-domain portfolio

`backend/app/decision/campus_portfolio.py`

The portfolio does not invent a global sustainability score. It exposes one operator-reviewed view containing:
- campus demand context;
- cafeteria recommended production when available;
- building energy review modes;
- selected space/zone bundle and aggregate capacity when available;
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
- `POST /api/v1/campus-ops/space-activation/plan`
- `POST /api/v1/campus-ops/shared-capacity/allocate`
- `POST /api/v1/campus-ops/portfolio`
- `POST /api/v1/campus-ops/plan`

`/plan` executes one decision-cutoff-consistent advisory pass and returns state, shuttle, classroom, optional food, optional energy, optional space activation, optional shared-capacity, and the combined portfolio.

## Evidence and truth boundary

This implementation establishes **repository capability**, not deployment evidence. It does not establish live BMS, Wi-Fi/turnstile occupancy, shuttle GPS, cafeteria POS, registrar integration, achieved savings, or autonomous pilot readiness.

Canonical provenance emitted by the contract is restricted to:
- `OFFICIAL_PUBLIC`
- `OFFICIAL_LIVE`
- `OFFICIAL_SNAPSHOT`
- `EXTERNAL_LIVE`
- `MODEL_ESTIMATE`
- `OPERATOR_MEASUREMENT`
- `POLICY_HEURISTIC`
- `SCENARIO`
- `GENERATED_SANDBOX`
- `UNAVAILABLE`

Legacy input aliases such as `PUBLIC_SOURCE` and `MEASURED_PILOT` may be accepted only through the contract normalizer and are emitted canonically as `OFFICIAL_PUBLIC` and `OPERATOR_MEASUREMENT`. Capacity-sensitive shuttle/classroom/space decisions require the stricter verified-capacity provenance set defined in `campus_contract.py`.

Impact claims remain unmeasured until real pilot evidence exists.

## Privacy boundary

The aggregate campus-operations contract rejects person-level identifiers including student IDs, BUCard IDs, user/person IDs, emails, phones, scholarship status, national identifiers, device IDs, and Wi-Fi client identifiers. The supported decisions do not require individual movement profiling.

## Focused validation commands

Dependency-light policy suite:

```bash
python scripts/run_cs1_campus_ops_tests.py
```

Full suite in a backend environment with FastAPI/Pydantic installed:

```bash
python scripts/run_cs1_campus_ops_tests.py --with-api
```

Individual regression files remain under `scripts/test_cs1_*.py`. Repository-level checks remain:

```bash
python -m compileall -q backend/app scripts
python scripts/kreate_check.py
```

Important: the current repository GitHub Actions workflow compiles Python and runs repository/governance/front-end gates, but it does **not** directly execute `scripts/test_cs1_*.py`. Therefore a green repository CI run must not be represented as targeted CS1 runtime-test evidence. Both exact-head repository CI and a fresh focused CS1 runner result are required before this feature is represented as integration-ready.

## Integration state

The implementation remains isolated on `agent/api-product/cs1-campus-ops-core` from `role/cs1-decision-intelligence` and is tracked by draft PR **#89**.

The role branch currently has open CS1 feature work in #68, #69, and #89, which fills the configured three-feature concurrency limit. Do not open another role-targeting CS1 PR until a slot is freed. Merge #89 only after the current role base remains an ancestor, exact-head repository CI is green, and fresh targeted CS1 runtime evidence is recorded.
