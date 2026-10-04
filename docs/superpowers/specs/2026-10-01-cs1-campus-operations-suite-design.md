# CS1 Campus Operations Suite — Design Specification

**Date:** 2026-10-01

**Owner:** CS1 — Decision Intelligence Lead

**Status:** execution-authorized extension of the approved CS1 decision-intelligence direction

## Purpose

Extend the existing evidence-aware food decision core into a reusable campus operations decision layer. The first durable domains are food, shuttle routing, and classroom/space allocation. Each domain must produce an explainable recommendation without pretending that unavailable live telemetry exists.

## Product rule

Every CS1 decision must expose the same truth boundary:

- `decisionId` and domain,
- readiness: `READY | REVIEW_REQUIRED | WITHHOLD`,
- `abstained`,
- provenance for material inputs,
- reason codes and limitations,
- human approval requirement,
- `automaticDispatchAllowed: false`,
- recommendation payload only when the hard constraints allow it.

## Existing assets to preserve

- food decision policy, readiness, provenance, pilot and claim-firewall behavior;
- official shuttle topology and official schedule source at `mekik.bogazici.edu.tr`;
- official 2026/2027-1 course schedule snapshot and its metadata;
- existing mobility, courses, occupancy and decision UI surfaces.

No live shuttle GPS, shuttle occupancy, room occupancy, access-control, BMS or verified room-capacity feed may be invented.

## Architecture

```text
Official / measured / user-supplied inputs
                ↓
      domain snapshot adapters
                ↓
   deterministic decision policies
        ↙        ↓         ↘
      food    shuttle      space
        ↘        ↓         ↙
      common decision envelope
                ↓
       Next API + product UI
```

The runtime policy is deterministic and auditable. ML may rank or forecast only when evidence exists; hard safety/feasibility constraints are never delegated to an opaque model.

## Shuttle decision policy

`recommendShuttleItinerary(originStopId, destinationStopId, options)` works over the current route topology.

1. Reject unknown stop IDs.
2. If origin equals destination, withhold with `NO_TRIP_REQUIRED`.
3. Enumerate direct paths where a route contains both stops in traversable order.
4. If no direct path exists, enumerate one-transfer paths through a shared stop.
5. Score feasible candidates deterministically by estimated route distance plus a transfer penalty.
6. Return the lowest-score candidate and alternatives.
7. Because the repository has no live departure/ETA/capacity feed, an otherwise feasible itinerary is `REVIEW_REQUIRED` with `OFFICIAL_TIMETABLE_CHECK_REQUIRED`.
8. Climate output, when requested, remains a labeled scenario estimate and never becomes achieved impact.

The algorithm optimizes network topology, not live departure timing.

## Space/class allocation policy

The course snapshot is transformed into an occupancy index keyed by `(day, hour, room)`. A request contains a day, start hour, duration, optional candidate-room list, and optional required capacity.

Hard constraints:

- valid day and positive duration;
- every requested hourly slot must be free in the schedule snapshot;
- one allocation batch cannot double-book a room;
- candidate-room constraints are respected;
- if capacity is declared as a hard requirement, it is checked only against an explicitly supplied/verified capacity map.

Soft scoring:

- prefer rooms with lower same-day scheduled load;
- prefer fewer schedule-adjacent occupied slots to reduce fragmentation;
- deterministic lexical room ID tie-break for reproducibility.

If the request can be placed but capacity is unknown, return the candidate as `REVIEW_REQUIRED` with `ROOM_CAPACITY_UNVERIFIED`. If the schedule snapshot is stale according to its metadata, also add `COURSE_SNAPSHOT_REFRESH_REQUIRED`. If no feasible room exists, `WITHHOLD` with `NO_FEASIBLE_ROOM`.

Batch allocation sorts requests by constrainedness before greedy assignment so the most restricted requests are placed first. Unassigned requests remain explicit; the engine never silently violates constraints.

## Shared contracts

Create `frontend/src/lib/decision-intelligence/campus-contracts.ts` with generic `CampusDecision<T>` and common provenance/readiness types. Shuttle and space modules depend only on this contract and domain data, keeping them independently testable.

## API surfaces

- `GET /api/v1/shuttles/recommend?origin=...&destination=...&passengerTrips=...`
- `POST /api/v1/spaces/allocate`
- existing `/api/v1/shuttles` remains a source/network snapshot endpoint.

The space API uses the bundled official course snapshot as its schedule source and accepts optional room capacities as explicit request input; it never labels user-supplied capacities as university telemetry.

## Failure handling

- invalid input → 400 at API boundary;
- unknown stop/room constraint → structured `WITHHOLD` decision where appropriate;
- stale course snapshot → recommendation may remain visible only as `REVIEW_REQUIRED`;
- missing capacity data → no capacity claim;
- missing live shuttle timing → no ETA claim;
- no feasible allocation/path → `WITHHOLD`, not a fabricated fallback.

## Tests

Behavior tests must cover:

- direct and one-transfer shuttle paths;
- unknown stops and no-trip requests;
- deterministic shuttle ranking;
- room conflict rejection;
- deterministic free-room selection;
- batch no-double-booking;
- required capacity with and without verified capacity data;
- stale snapshot readiness degradation;
- truth-boundary markers preventing live GPS/occupancy/capacity claims.

Node 24’s TypeScript type stripping is used for pure policy tests so decision behavior is exercised without adding a new test framework. CI also keeps typecheck, lint and production build gates.

## Acceptance criteria

1. Existing food behavior is preserved.
2. Shuttle API can return a deterministic direct or transfer itinerary with explicit timetable-review requirement.
3. Space API can allocate one or more requests without schedule conflicts or within-batch double bookings.
4. A stale schedule or unknown capacity cannot be represented as live/verified state.
5. All new decision responses require human approval and forbid automatic dispatch.
6. Policy behavior has executable tests, not only TypeScript compilation checks.
7. Frontend typecheck, lint, build, repository Python compile, KREATE checks and feature-preservation gates remain green.
