# CS1 Decision Intelligence — System Map

Branch: `agent/cs1/campus-operations`
Base: `role/cs1-decision-intelligence`

This file is the integration map for the additive CS1 campus-operations lane. It is intentionally separate from the reservation/reconciliation and method-selection work active in PRs #69 and #70.

## Decision surfaces

| Surface | API | Decision | Automatic actuation |
| --- | --- | --- | --- |
| Food operations | `POST /api/v1/decision/food/plan` | Production quantity / planning range | Disabled |
| Meal recommendation | `POST /api/v1/decision/meals/recommend` | Student-facing menu ranking baseline | N/A |
| Recommendation provenance | `POST /api/v1/decision/meals/impression` | Record what ranking was shown at decision time | N/A |
| Shuttle operations | `POST /api/v1/decision/shuttle/plan` | Vehicles/capacity per departure | Disabled |
| Classroom operations | `POST /api/v1/decision/classrooms/allocate` | Room assignment under capacity/time constraints | Disabled |
| Flexible spaces | `POST /api/v1/decision/spaces/plan` | Capacity-safe space consolidation | Disabled |
| Cross-domain state | `POST /api/v1/decision/snapshot` | Worst-domain readiness across food/shuttle/classroom | N/A |
| Capability discovery | `GET /api/v1/decision/capabilities` | Machine-readable current decision surfaces | N/A |

## Shared truth boundary

The lane separates four concepts that must not be conflated:

1. **measurement** — observed input from a source,
2. **estimate** — forecast or supplied planning estimate,
3. **recommendation** — a policy output subject to operator review,
4. **outcome** — evidence collected after the decision.

No endpoint in this lane claims realized climate, cost, food-waste, energy, ridership, utilization, or service-quality improvement.

`PILOT_READY` means the supplied planning inputs pass the current policy gate for an operator-reviewed pilot action. It does not mean the method is scientifically validated or that impact has been achieved.

## Food operations

`campus_operations.py` keeps food production planning separate from student recommendation.

Production planning uses:

- explicit baseline or robust historical served-demand median,
- schedule/menu/calendar/weather availability flags,
- bounded contextual multipliers,
- reservation intent only as a conservative floor,
- empirical planning spread when enough history exists,
- asymmetric shortage/surplus sensitivity,
- abstention when schedule/context support is insufficient.

The output never dispatches a kitchen instruction automatically.

## Meal recommendation

`meal_recommendation.py` is a transparent benchmark, not a claim that the existing ALS prototype is validated.

Ranking behavior:

- hard dietary-tag exclusions,
- deterministic population prior from available popularity/rating evidence,
- explicit 1–5 item feedback with shrinkage,
- explicit category feedback with stronger shrinkage,
- malformed feedback counted and ignored,
- deterministic tie-breaking,
- impression logging with request/policy/ranking provenance.

The existing `models/collaborative.py` ALS path is deliberately not called because its generated training-data provenance has not yet been validated. A collaborative/contextual model must beat this baseline on held-out prospective or properly time-split evidence before promotion.

## Shuttle operations

`plan_shuttle_service` combines forecast demand and observed waiting queue, applies reserve capacity, and computes the minimum vehicle count per departure while never reducing below the scheduled count.

Outputs expose planned load, added vehicles, seats, overflow and reason codes. A malformed departure cannot silently disappear into a `PILOT_READY` plan: partial invalid data degrades readiness to `REVIEW_REQUIRED`.

## Classroom operations

`allocate_classrooms` enforces hard constraints before applying any soft objective:

- room available in slot,
- room capacity >= expected attendance,
- no double-booking of the same room/slot.

Among feasible rooms it minimizes a transparent score combining unused seats, supplied relative energy cost, and a building-activation penalty. Largest sessions are allocated first. This is an auditable baseline for later CP-SAT comparison, not a claim of global optimality.

The repository already contains `backend/app/data/real_boun_courses.json`; it can provide schedule structure, but room-capacity and measured energy coefficients still need defensible source contracts before automatic reallocation is presented as production-ready.

## Flexible-space operations

`space_operations.py` keeps mandatory available spaces open, then activates optional spaces by relative energy-cost-per-seat until demand plus reserve capacity is covered.

If available capacity cannot cover the target, the policy returns `WITHHOLD`. Relative energy values are explicitly labelled planning scores rather than kWh or monetary savings.

## Verification files

Pure decision logic:

- `scripts/test_cs1_campus_operations.py`
- `scripts/test_cs1_space_operations.py`
- `scripts/test_cs1_meal_recommendation.py`

API contracts:

- `scripts/test_cs1_campus_operations_api.py`
- `scripts/test_cs1_meal_recommendation_api.py`

The repository workflow already compiles `backend/app` and `scripts`. Exact-head behavioral CI for this feature branch cannot start until a CS1 feature-PR slot is available; the role currently has its configured maximum of three active feature PRs (#68, #69, #70).

## Fan-in contract with active CS1 agents

After #69 integrates:

- consume its canonical reservation reconciliation and prospective decision-record artifacts;
- do not create a second reservation truth source.

After #70 integrates:

- consume its method-selection, stability and context-ablation outputs for promotion decisions;
- do not duplicate its evaluation gates.

This lane remains the operational policy/API layer that turns those upstream artifacts into auditable operator decisions.

## Next evidence gates

No algorithmic sophistication substitutes for these inputs:

- reconciled meal outcomes,
- actual recommendation impressions + choices/ratings,
- actual shuttle schedule/capacity/queue or ridership observations,
- defensible room capacities,
- measured or source-backed energy coefficients,
- operator override/outcome capture.

Until those exist, the correct output is a transparent baseline, explicit uncertainty/readiness, and a measurable pilot protocol — not invented savings.
