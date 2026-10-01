# CS1 Campus Operations Decision Core v1

Status: **implementation branch / pre-integration**  
Owner: **CS1 — Decision Intelligence Lead**  
Contract: `campus-ops-v1.0`

## Purpose

Extend the existing food-focused CS1 decision-intelligence work into a reusable campus-operations core without fabricating live university telemetry or measured impact.

The v1 flow is:

```text
aggregate sources
  -> campus state snapshot
  -> shuttle capacity plan
  -> classroom allocation
  -> cross-domain portfolio
  -> human review
```

This package is decision support. It does not auto-dispatch shuttles, change classrooms, control buildings, alter cafeteria production, or execute any irreversible university operation.

## Modules

### 1. Aggregate campus state

`backend/app/decision/campus_state.py`

Inputs:
- aggregate zone capacity;
- aggregate occupancy estimate;
- aggregate scheduled load;
- aggregate event load;
- source availability/provenance;
- source publication time;
- decision cutoff time.

Hard boundaries:
- `schedule` and `occupancy_model` are required sources;
- source information published after the decision cutoff is not accepted;
- person-level identifiers are rejected;
- invalid/negative capacity or load values fail closed;
- occupancy estimates above physical capacity are bounded and surfaced as a review reason.

Current readiness semantics:
- insufficient required evidence -> `WITHHOLD`;
- otherwise -> `REVIEW_REQUIRED`;
- v1 does not promote model-only context to autonomous execution.

### 2. Shuttle capacity planner

`backend/app/decision/shuttle_policy.py`

Inputs per route:
- aggregate forecast demand;
- vehicle capacity;
- available vehicles;
- service window;
- round-trip duration;
- min/max planning headway;
- explicit reserve ratio.

Outputs:
- required seats;
- required trips;
- maximum supported trips;
- capacity feasibility;
- estimated unserved seat demand when oversubscribed;
- planning headway target.

Important: headway is a planning target, not live dispatch. No shuttle GPS integration is claimed.

### 3. Classroom allocator

`backend/app/decision/classroom_policy.py`

Hard constraints:
- room capacity;
- campus match;
- accessibility requirement;
- equipment requirement;
- room time conflicts.

Soft selection objective among feasible rooms:
- lower spare-seat penalty;
- lower declared room energy-cost score.

The allocator is intentionally transparent and greedy in v1. It does not claim global optimality. Sessions that cannot be assigned are surfaced for operator review rather than forcing an infeasible assignment.

Outputs also include aggregate building attendance targets so building/energy logic can consume the same classroom decision without student-level traces.

### 4. Cross-domain portfolio

`backend/app/decision/campus_portfolio.py`

The portfolio deliberately avoids inventing a single global sustainability score. It exposes shared decision context:
- campus demand context for dining;
- campus occupancy context for energy;
- shuttle routes with capacity shortfalls;
- unassigned classroom sessions;
- aggregate building attendance targets.

Existing food and energy decisions can be attached as domain status inputs, but v1 does not rewrite their independent policies.

## FastAPI surface

Router: `backend/app/routers/campus_ops.py`

Endpoints:
- `GET /api/v1/campus-ops/contract`
- `POST /api/v1/campus-ops/state`
- `POST /api/v1/campus-ops/shuttle/plan`
- `POST /api/v1/campus-ops/classrooms/allocate`
- `POST /api/v1/campus-ops/portfolio`
- `POST /api/v1/campus-ops/plan`

`/plan` executes one decision-cutoff-consistent advisory pass through state -> shuttle -> classroom -> portfolio.

## Evidence and truth boundary

This implementation establishes **repository capability**, not university deployment evidence.

It does **not** establish:
- access to live BMS data;
- access to Wi-Fi/turnstile occupancy;
- access to shuttle GPS;
- access to cafeteria POS;
- access to registrar scheduling systems;
- achieved energy, carbon, water, food-waste, time, or cost savings;
- pilot readiness for autonomous execution.

Allowed provenance labels remain explicit:
- `PUBLIC_SOURCE`
- `MODEL_ESTIMATE`
- `POLICY_HEURISTIC`
- `MEASURED_PILOT`

Impact claims remain unmeasured until real pilot evidence exists.

## Privacy boundary

The aggregate CS1 campus-operations contract rejects person-level fields such as student IDs, BUCard IDs, user/person IDs, emails, phone numbers, scholarship status, and national identifiers.

The supported decisions do not require individual movement profiling.

## Focused validation

```bash
python scripts/test_cs1_campus_state.py
python scripts/test_cs1_shuttle_policy.py
python scripts/test_cs1_classroom_policy.py
python scripts/test_cs1_campus_portfolio.py
python scripts/test_cs1_campus_ops_router.py
python -m compileall -q backend/app scripts
python scripts/kreate_check.py
```

CI remains authoritative before integration.

## Integration state

The implementation is isolated on `agent/api-product/cs1-campus-ops-core` from `role/cs1-decision-intelligence`.

At task claim time the CS1 role already had three open feature PRs (#68, #69, #70), which is the repository concurrency limit. Do not open a fourth feature PR until a CS1 slot is freed. The branch may continue to be implemented and audited in the meantime.
