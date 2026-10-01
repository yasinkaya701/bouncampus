# CS1 Campus Operations Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn existing shuttle and course-schedule assets into tested, explainable CS1 decisions while preserving the food decision core and truth boundary.

**Architecture:** Add a small shared campus-decision contract, then isolated shuttle and space policies. Expose both through Next API routes. Use pure-policy Node 24 TypeScript tests plus the repository’s existing typecheck/lint/build and KREATE gates.

**Tech Stack:** Next.js 14, TypeScript 5, Node 24, existing JSON source snapshots, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-01-cs1-campus-operations-suite-design.md`

## Global Constraints

- Do not invent live shuttle GPS, shuttle occupancy, room occupancy, room capacity, access-control or BMS telemetry.
- `automaticDispatchAllowed` is always `false`; operator approval is always required for actionable recommendations.
- Official schedule/network snapshots and user-supplied values remain distinguishable by provenance.
- Preserve existing food decision behavior and routes.
- Avoid new runtime/test dependencies unless the existing stack cannot express the required behavior.

## Review Focus

- Transfer routing must not reverse a one-way ordered route segment.
- A batch allocation must never place two requests in the same room/hour.
- Missing verified capacity must not become a capacity claim.
- Stale course metadata must degrade readiness without erasing schedule-conflict protection.
- Invalid stop/day/hour/duration inputs must fail safely and deterministically.

---

### Task 1: Executable decision-policy test gate

**Files:**
- Create: `frontend/src/lib/decision-intelligence/campus-operations.test.ts`
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: future `recommendShuttleItinerary`, `buildRoomScheduleIndex`, `allocateRooms` exports.
- Produces: CI behavior tests that must fail until Tasks 2-3 exist.

- [ ] Write Node assert tests for direct/transfer shuttle routing, invalid stops, room conflicts, deterministic allocation, capacity and stale-snapshot behavior.
- [ ] Add a frontend CI step running `node --experimental-strip-types src/lib/decision-intelligence/campus-operations.test.ts` before typecheck.
- [ ] Open/update the feature PR and verify the new test gate fails for missing implementation, proving RED.
- [ ] Commit test gate.

### Task 2: Shared contract and shuttle policy

**Files:**
- Create: `frontend/src/lib/decision-intelligence/campus-contracts.ts`
- Create: `frontend/src/lib/decision-intelligence/shuttle-policy.ts`
- Create: `frontend/src/app/api/v1/shuttles/recommend/route.ts`

**Interfaces:**
- Consumes: `shuttleStops`, `shuttleRoutes`, `OFFICIAL_SHUTTLE_SOURCE` from `@/lib/shuttle-network`.
- Produces: `CampusDecision<T>` and `recommendShuttleItinerary(originStopId, destinationStopId, options?)`.

- [ ] Implement common readiness/provenance decision envelope.
- [ ] Implement ordered direct and one-transfer candidate enumeration.
- [ ] Rank by estimated distance plus fixed transfer penalty, deterministic tie-break.
- [ ] Return `REVIEW_REQUIRED` for feasible topology because official timetable verification is still required; `WITHHOLD` for invalid/no-trip/no-path conditions.
- [ ] Expose GET recommendation API with validated query params and no ETA/capacity claims.
- [ ] Run campus operations test; shuttle tests must pass while space tests remain RED.
- [ ] Commit.

### Task 3: Course-snapshot space allocation policy

**Files:**
- Create: `frontend/src/lib/decision-intelligence/space-allocation.ts`
- Create: `frontend/src/app/api/v1/spaces/allocate/route.ts`

**Interfaces:**
- Consumes: official course snapshot records, course snapshot metadata, optional explicit room-capacity map.
- Produces: `buildRoomScheduleIndex(snapshot)`, `allocateRooms(requests, context)` and POST API.

- [ ] Build occupancy and same-day room-load indexes from aligned `days/hours/rooms` triples only.
- [ ] Validate requests and enforce all requested slots free.
- [ ] Sort batch by constrainedness; reserve slots after each allocation to prevent double booking.
- [ ] Apply capacity only when supplied; otherwise degrade to `REVIEW_REQUIRED` when capacity is required.
- [ ] Add stale-snapshot reason from metadata while preserving conflict checks.
- [ ] Expose POST API with snapshot provenance and explicit truth boundary.
- [ ] Run campus operations test; all behavior tests must pass.
- [ ] Commit.

### Task 4: Verification and integration readiness

**Files:**
- Modify only if required by discovered verification failure; no speculative refactor.

**Interfaces:**
- Consumes: all prior tasks.
- Produces: green feature PR ready for CS1 role integration.

- [ ] Run/observe exact-head CI for the feature PR.
- [ ] Confirm frontend TypeScript policy tests, typecheck, lint and build pass.
- [ ] Confirm repository Python compile, agent fabric, KREATE, and feature-preservation checks pass.
- [ ] Review diff for accidental live-telemetry/impact claims and unrelated shared-file edits.
- [ ] Record remaining blockers; do not weaken tests to hide failures.
