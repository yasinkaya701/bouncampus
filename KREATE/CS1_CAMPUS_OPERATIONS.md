# CS1 Campus Operations Decision Layer

## Purpose

This layer turns CS1 from a food-only forecasting lane into a reusable campus decision system while preserving the KREATE truth boundary. It currently supports three operator decisions with one shared readiness model:

1. **Food production planning** — baseline-first demand planning with bounded contextual adjustments, reservation intent handling, asymmetric shortage/surplus preferences, planning ranges, and abstention.
2. **Shuttle capacity planning** — demand + waiting-queue aware vehicle allocation per departure with reserve capacity and overflow diagnostics.
3. **Classroom allocation** — capacity, time-slot conflict, unused-seat, energy-cost, and building-activation aware assignment.

A fourth endpoint produces a fail-closed cross-domain snapshot so the product does not present the overall campus state as ready when one operational domain should be withheld.

## API

All endpoints live under `/api/v1/decision`.

| Endpoint | Purpose |
| --- | --- |
| `GET /capabilities` | Discover supported decision domains and hard safety boundaries |
| `POST /food/plan` | Produce an operator-reviewed food production plan |
| `POST /shuttle/plan` | Produce shuttle vehicle-capacity recommendations |
| `POST /classrooms/allocate` | Allocate sessions to rooms under hard constraints |
| `POST /snapshot` | Build a combined fail-closed campus decision snapshot |

## Shared readiness states

- `PILOT_READY`: supplied decision inputs pass the current policy gates. This does **not** mean impact has been proven.
- `REVIEW_REQUIRED`: the system has a usable plan but incomplete or partially invalid evidence requires operator review.
- `WITHHOLD`: the system must not emit an actionable recommendation because required evidence or feasible capacity is missing.

## Food planning contract

### Inputs

- `historical_served`: reconciled prior served-demand observations where available.
- `baseline_estimate`: optional explicit baseline; otherwise the robust historical median is used.
- `reservations`: optional intent signal; never treated as served demand.
- `signals`: availability flags for `schedule`, `menu`, `calendar`, `weather`, `reservation`.
- `context_multipliers`: caller-supplied candidate adjustments, bounded to `[0.85, 1.15]` before use.
- `shortage_weight` and `surplus_weight`: relative sensitivity parameters, not observed currency costs.

### Decision logic

- A schedule signal is currently required for an actionable plan.
- Context multipliers are bounded so one unvalidated signal cannot dominate the result.
- Reservations can raise an implausibly low baseline through a conservative intent floor, but do not replace reconciliation evidence.
- With at least five historical observations, the planning range uses an empirical interquartile spread. Otherwise it is explicitly labelled heuristic.
- Asymmetric shortage/surplus weights choose a point inside the planning range; they do not manufacture an economic-savings claim.
- Automatic kitchen dispatch is disabled.

## Shuttle planning contract

### Inputs

- `vehicle_capacity`
- optional `reserve_ratio` (default `0.10`, capped at `0.50`)
- `departures[]` with `departure_id`, `predicted_demand`, optional `waiting_queue`, optional `scheduled_vehicles`

### Decision logic

For each departure the system computes usable seats per vehicle after the reserve ratio, adds observed waiting queue to forecast demand, and recommends the minimum vehicle count required to serve that planning load. It never reduces below the supplied scheduled vehicle count.

Outputs include:

- recommended and added vehicles,
- planned seats,
- planned load ratio,
- projected overflow,
- per-departure reason codes.

Automatic vehicle dispatch is disabled.

## Classroom allocation contract

### Inputs

Rooms contain:

- `room_id`
- `capacity`
- `building_id`
- `energy_cost` — a relative planning input unless backed by measured energy data
- `available_slots[]`

Sessions contain:

- `session_id`
- `slot`
- `expected_attendance`

### Hard constraints

- room must be available in the requested slot,
- room capacity must meet expected attendance,
- one room cannot host two sessions in the same slot.

### Soft objective

Candidates are scored by:

`unused_seats * unused_seat_weight + energy_cost * energy_weight + new_building_activation_penalty`

Sessions are allocated largest-first to make the deterministic baseline easy to audit. This is a transparent baseline suitable for later comparison with an OR-Tools/CP-SAT optimizer; it is not claimed to be globally optimal.

Automatic timetable commit is disabled.

## Cross-domain snapshot

`POST /snapshot` runs all three policies and reports the **worst readiness state** as the overall state. One withheld domain therefore prevents the application from presenting the full campus plan as ready.

No realized cost, carbon, waste, service-quality, utilization, or ridership improvement is claimed by this endpoint.

## Verification

Regression coverage lives in:

- `scripts/test_cs1_campus_operations.py`

Current focused checks cover:

- food abstention when schedule evidence is absent,
- asymmetric shortage/surplus sensitivity,
- shuttle peak-capacity augmentation,
- bad shuttle-row handling,
- classroom capacity and conflict constraints,
- infeasible classroom demand,
- fail-closed cross-domain readiness.

An isolated local execution of these focused tests passed **7/7** before the files were committed. API smoke checks also returned HTTP 200 for capabilities and shuttle planning against the committed interface shape. Repository exact-head CI remains authoritative before integration.

## Integration / multi-agent boundary

The branch for this work is `agent/cs1/campus-operations`, based on `role/cs1-decision-intelligence`.

At creation time CS1 already had three open feature PRs, equal to `.agents/fabric.json`'s per-role limit. This branch therefore intentionally does not open a fourth feature PR until one active CS1 PR is integrated or closed. It can be rebased/fanned into the role branch when that slot is available.

The implementation is additive and deliberately avoids changing active CS2 product-strategy files or EE hardware ownership.

## Next technical gates

Before claiming optimization superiority or climate impact:

1. reconcile real historical meal counts against reservations and menu/schedule context,
2. benchmark the food policy against status quo and existing CS1 baselines,
3. obtain actual shuttle schedule/capacity/ridership or queue observations,
4. derive a stable room inventory and measured/defensible building-energy coefficients,
5. compare the deterministic classroom baseline with a CP-SAT optimizer on identical inputs,
6. preserve operator overrides and outcomes for prospective evaluation,
7. only promote a domain when measured pilot evidence supports the claim.
