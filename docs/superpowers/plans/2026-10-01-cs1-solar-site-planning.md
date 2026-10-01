# CS1 Solar Exposure & Site Planning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add explainable room/class solar exposure analysis, advisory new-building orientation ranking, and optional solar-aware class assignment to the existing CS1 campus-operations decision layer.

**Architecture:** A shared Python solar/site-planning decision module owns solar geometry and orientation ranking. Existing class scheduling consumes an optional precomputed room/slot exposure map so hard feasibility remains independent from solar heuristics. FastAPI endpoints expose analysis and planning with the same fail-closed, operator-gated semantics as other CS1 modules.

**Tech Stack:** Python 3.11, stdlib math/datetime, FastAPI, repository script-style regression tests.

**Spec:** `docs/superpowers/specs/2026-10-01-cs1-solar-site-planning-design.md`

## Global Constraints
- No new runtime dependency for solar geometry.
- All timestamps must be timezone-aware ISO-8601.
- No live BMS, calibrated daylight, thermal-load, 3D ray-tracing, or achieved-savings claim.
- Automatic actuation/design selection remains disabled.
- Existing class capacity/feature/conflict behavior must remain backward compatible when solar weight is zero.

## Review Focus
- Naive timestamps must fail closed rather than assume timezone.
- Bad latitude/longitude/facade geometry must fail closed.
- Room solar maps outside [0,1] must fail closed when active.
- Session room/timestamp references must match analyzed samples.
- Solar weighting must never bypass hard class feasibility constraints.

---

### Task 1: Solar/site decision core

**Files:**
- Create: `backend/app/decision/solar_site_planning.py`
- Test: `scripts/test_cs1_solar_site_planning.py`

**Interfaces:**
- Produces: `solar_position(...)`, `analyze_room_solar_exposure(...)`, `rank_new_building_orientations(...)`.

- [ ] Write focused tests for solar position, facade exposure, obstruction, class linkage, orientation ranking, and invalid geometry.
- [ ] Run test and confirm RED because the module is missing.
- [ ] Implement deterministic NOAA-approximation solar position and advisory exposure/orientation scoring.
- [ ] Run focused test and confirm GREEN.

### Task 2: Solar-aware class assignment

**Files:**
- Modify: `backend/app/decision/class_assignment.py`
- Modify: `backend/app/decision/class_conflicts.py`
- Test: `scripts/test_cs1_solar_class_integration.py`

**Interfaces:**
- Consumes: room `solar_load_by_slot: {slot: 0..1}`.
- Produces: optional `solar_exposure_weight` parameter propagated through conflict-aware scheduling.

- [ ] Write regressions proving lower-exposure room preference when active, zero-weight legacy behavior, and fail-closed malformed maps.
- [ ] Confirm RED against current scheduler signature/behavior.
- [ ] Add validated solar loss term without changing hard constraints.
- [ ] Confirm focused and existing class tests GREEN.

### Task 3: Campus-ops API wiring

**Files:**
- Modify: `backend/app/routers/campus_ops.py`
- Test: `scripts/test_cs1_solar_ops_api.py`

**Interfaces:**
- Produces: `POST /api/v1/ops/solar`, `POST /api/v1/ops/site-orientation`, solar-aware `/classes`, and capability entries.

- [ ] Write API wiring regression first.
- [ ] Confirm RED because routes/capabilities are absent.
- [ ] Wire the shared decision module and class weight into the router.
- [ ] Run focused API regression and existing campus-ops API tests.

### Task 4: Repository verification

**Files:**
- No production files.

- [ ] Compile `backend/app` and `scripts`.
- [ ] Run new solar regressions.
- [ ] Run existing class/campus-ops/energy regressions.
- [ ] Open PR to `role/cs1-decision-intelligence` and require exact-head CI before merge.
