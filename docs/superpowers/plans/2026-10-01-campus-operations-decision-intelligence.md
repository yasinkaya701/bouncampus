# Campus Operations Decision Intelligence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a shared CS1 campus-operations decision layer that unifies aggregate campus state, shuttle pressure, classroom/space review, and cross-domain orchestration without weakening BOUNCAMPUS truth boundaries or human-control gates.

**Architecture:** Separate vertical decision policies consume one shared aggregate campus-state/source-health contract and emit a common recommendation envelope. A deterministic orchestrator preserves readiness, provenance, limitations, and conflict records; no component performs autonomous execution. Existing food-policy work remains authoritative and is integrated by adapter/fan-in rather than duplicated.

**Tech Stack:** Python 3.11+ decision modules and regression scripts; Next.js/TypeScript API adapters; existing repository source snapshots and CI gates.

**Spec:** `docs/superpowers/specs/2026-10-01-campus-operations-decision-intelligence-design.md`

## Global Constraints

- Contract version is `campus-ops-v1.0`.
- Every operational recommendation must set `operator_approval_required = true` and `automatic_execution_allowed = false`.
- Future information (`published_at` / equivalent availability time later than the decision cutoff) is ineligible and must fail closed.
- Missing critical evidence degrades readiness or returns `WITHHOLD`; missing live telemetry must never be replaced by fabricated telemetry.
- Person-level identifiers are rejected from the campus-operations core; aggregate section, room, route, zone, service, building and event identifiers are permitted.
- Building capacity must never substitute for room capacity; course existence must never substitute for enrollment.
- Shuttle GPS, ridership, occupancy and vehicle capacity may not be claimed unless verified sources are integrated.
- Model/scenario values remain labeled estimates; no measured food, energy, CO2, cost, water or mobility improvement may be claimed without measured evidence.
- Existing active CS1 files for reservation reconciliation, matched pilots, method selection, stability, context ablation and food-policy integration are not to be rewritten by this workstream.
- New implementation should prefer additive paths and merge through `role/cs1-decision-intelligence`; exact-head CI remains authoritative.

## Review Focus

1. Legacy provenance aliases such as `PUBLIC_SOURCE` must normalize to canonical `OFFICIAL_PUBLIC` without weakening unknown-value rejection.
2. Duplicate zone, source, route, course or room-time identifiers must fail validation or be surfaced deterministically rather than silently double-counted.
3. Non-finite numeric inputs (`NaN`, `inf`) and negative capacities/loads must fail validation before policy scoring.
4. Mixed timezone / malformed timestamps must not accidentally admit future information; timestamp parsing must be explicit and offset-aware.
5. An orchestrator must never strengthen a domain recommendation (`WITHHOLD` → `REVIEW_REQUIRED` or `PILOT_READY`) merely because another domain is healthy.

---

## File Structure

### Backend decision core

- Create `backend/app/decision/source_health.py` — canonical source/provenance normalization and decision-time eligibility.
- Create `backend/app/decision/campus_state.py` — aggregate zone validation and campus-state contract.
- Create `backend/app/decision/mobility_policy.py` — schedule-derived route/time-window pressure and evidence-gated shuttle review actions.
- Create `backend/app/decision/space_policy.py` — room-time collision, cross-campus transition, building-load and capacity-gated review candidates.
- Create `backend/app/decision/campus_orchestrator.py` — common recommendation validation, conflict detection and deterministic priority ordering.

### Focused regression scripts

- Existing `scripts/test_cs1_campus_state.py` — retained and expanded.
- Create `scripts/test_cs1_source_health.py`.
- Create `scripts/test_cs1_mobility_policy.py`.
- Create `scripts/test_cs1_space_policy.py`.
- Create `scripts/test_cs1_campus_orchestrator.py`.

### Product runtime, only after backend contracts stabilize

- Create `frontend/src/lib/campus-ops.ts` — TypeScript contract types and deterministic adapter helpers.
- Create `frontend/src/app/api/v1/campus-ops/state/route.ts`.
- Create `frontend/src/app/api/v1/campus-ops/recommendations/route.ts`.
- Create `frontend/src/app/api/v1/campus-ops/mobility/evaluate/route.ts`.
- Create `frontend/src/app/api/v1/campus-ops/space/evaluate/route.ts`.
- Add contract fixtures under `frontend/src/data/campus_ops_contract_fixtures.json` only if parity tests require serialized examples.

## Task 1: Shared Source Health and Campus State Core

**Files:**
- Create: `backend/app/decision/source_health.py`
- Create: `backend/app/decision/campus_state.py`
- Modify: `scripts/test_cs1_campus_state.py`
- Create: `scripts/test_cs1_source_health.py`

**Interfaces:**
- Produces: `normalize_source(source_id: str, source: dict, decision_time: str, *, domain: str = "campus") -> dict`
- Produces: `normalize_sources(sources: dict[str, dict], decision_time: str, *, domain: str = "campus") -> list[dict]`
- Produces: `build_campus_state(zones: list[dict], sources: dict[str, dict], decision_time: str) -> dict`
- Canonical provenance: `OFFICIAL_PUBLIC | OFFICIAL_LIVE | OFFICIAL_SNAPSHOT | EXTERNAL_LIVE | MODEL_ESTIMATE | OPERATOR_MEASUREMENT`.
- Alias: input `PUBLIC_SOURCE` normalizes to `OFFICIAL_PUBLIC`; unknown provenance raises `ValueError`.

- [ ] **Step 1: Extend the existing campus-state test with review-focus validation cases**

Add assertions for duplicate `zone_id`, `NaN`/`inf`, negative loads, malformed timestamps and unknown provenance. Expected behavior: invalid input raises `ValueError`; decision-time future source returns `WITHHOLD`; canonicalized source health contains `OFFICIAL_PUBLIC` for legacy `PUBLIC_SOURCE` input.

- [ ] **Step 2: Write source-health failing tests**

Create focused tests named `test_normalizes_public_source_alias`, `test_unknown_provenance_is_rejected`, `test_future_source_is_ineligible`, `test_missing_required_source_is_unavailable`, and `test_timezone_aware_cutoff_is_respected`.

- [ ] **Step 3: Run focused tests and confirm RED**

Run:

```bash
python scripts/test_cs1_source_health.py
python scripts/test_cs1_campus_state.py
```

Expected: source-health module and/or campus-state implementation missing, plus new contract cases failing.

- [ ] **Step 4: Implement `source_health.py` minimally**

Parse ISO-8601 timestamps into timezone-aware datetimes; reject malformed/naive ambiguity rather than guessing. Normalize provenance aliases, availability, decision-time eligibility and status. Do not introduce freshness thresholds not defined by callers.

- [ ] **Step 5: Implement `campus_state.py` minimally**

Validate aggregate zones, reject person-level identifier keys, require schedule and occupancy-model source availability for utilization claims, aggregate by campus, compute `utilization_pct = occupancy_estimate / capacity * 100` when valid, and preserve `NO_LIVE_TELEMETRY_CLAIM`. Healthy aggregate state is `REVIEW_REQUIRED`, not `PILOT_READY`.

- [ ] **Step 6: Run focused tests and confirm GREEN**

```bash
python scripts/test_cs1_source_health.py
python scripts/test_cs1_campus_state.py
python -m py_compile backend/app/decision/source_health.py backend/app/decision/campus_state.py
```

Expected: all focused cases pass.

- [ ] **Step 7: Commit Task 1**

```bash
git add backend/app/decision/source_health.py backend/app/decision/campus_state.py scripts/test_cs1_source_health.py scripts/test_cs1_campus_state.py
git commit -m "feat(cs1): add campus state source health core"
```

## Task 2: Mobility / Shuttle Decision Policy

**Files:**
- Create: `backend/app/decision/mobility_policy.py`
- Create: `scripts/test_cs1_mobility_policy.py`

**Interfaces:**
- Consumes: normalized source-health semantics from Task 1.
- Produces: `evaluate_mobility_pressure(transitions: list[dict], routes: list[dict], sources: dict[str, dict], decision_time: str) -> dict`
- Output recommendation actions: `KEEP_CURRENT_SCHEDULE | REVIEW_DEPARTURE_TIMING | REVIEW_CAPACITY | REVIEW_EXTRA_TRIP | WITHHOLD`.

- [ ] **Step 1: Write failing mobility tests**

Cover deterministic aggregate transfer pressure, missing official shuttle schedule → `WITHHOLD`, future schedule snapshot → `WITHHOLD`, no GPS → no ETA field, no ridership → no observed-demand wording, no vehicle capacity → no occupancy percentage, duplicate transition IDs rejected, and operator approval always required.

- [ ] **Step 2: Run test and confirm RED**

```bash
python scripts/test_cs1_mobility_policy.py
```

Expected: module missing.

- [ ] **Step 3: Implement `evaluate_mobility_pressure(...)`**

Use only aggregate origin/destination/time-window transitions and compatible route metadata. Compute a deterministic pressure proxy from supplied transition weights/counts; do not invent passenger demand, vehicle capacity, timetable frequency or thresholds not present in caller inputs. If schedule-review prerequisites are absent, return `WITHHOLD` with reason codes.

- [ ] **Step 4: Run mobility tests and compile**

```bash
python scripts/test_cs1_mobility_policy.py
python -m py_compile backend/app/decision/mobility_policy.py
```

Expected: PASS.

- [ ] **Step 5: Commit Task 2**

```bash
git add backend/app/decision/mobility_policy.py scripts/test_cs1_mobility_policy.py
git commit -m "feat(cs1): add evidence gated mobility policy"
```

## Task 3: Classroom / Space Review Policy

**Files:**
- Create: `backend/app/decision/space_policy.py`
- Create: `scripts/test_cs1_space_policy.py`

**Interfaces:**
- Produces: `evaluate_space_plan(course_meetings: list[dict], building_map: dict[str, dict], *, room_capacities: dict[str, int] | None = None, enrollments: dict[str, int] | None = None) -> dict`
- Produces collision records, cross-campus transition records, building-load summaries and optional review candidates.

- [ ] **Step 1: Write failing space tests**

Pin: duplicate room-time collision detected; same meeting does not self-collide; adjacent-period cross-campus transition detected; malformed/duplicate meeting IDs rejected; missing room capacity returns `capacity_fit = NOT_VERIFIED`; missing enrollment prevents capacity-sensitive recommendation; building capacity is never used as room capacity; no automatic reassignment flag/action exists.

- [ ] **Step 2: Run test and confirm RED**

```bash
python scripts/test_cs1_space_policy.py
```

Expected: module missing.

- [ ] **Step 3: Implement `evaluate_space_plan(...)`**

Normalize room/building references conservatively, detect collisions by `(day, hour, room)`, derive cross-campus transitions only where consecutive schedule slots and campus mapping are known, and emit candidate-zone review records rather than authoritative room assignments when capacity/enrollment evidence is absent.

- [ ] **Step 4: Run space tests and compile**

```bash
python scripts/test_cs1_space_policy.py
python -m py_compile backend/app/decision/space_policy.py
```

Expected: PASS.

- [ ] **Step 5: Commit Task 3**

```bash
git add backend/app/decision/space_policy.py scripts/test_cs1_space_policy.py
git commit -m "feat(cs1): add classroom space review policy"
```

## Task 4: Campus Orchestrator and Cross-Domain Conflicts

**Files:**
- Create: `backend/app/decision/campus_orchestrator.py`
- Create: `scripts/test_cs1_campus_orchestrator.py`

**Interfaces:**
- Consumes: domain recommendation dicts using `campus-ops-v1.0` envelope.
- Produces: `orchestrate_recommendations(recommendations: list[dict], *, decision_time: str) -> dict`
- Output includes `review_queue`, `conflicts`, `withheld`, `limitations`, `operator_approval_required=True`, `automatic_execution_allowed=False`.

- [ ] **Step 1: Write failing orchestrator tests**

Test provenance/limitations preserved, contract-version mismatch rejected, duplicate decision IDs rejected, `WITHHOLD` never promoted, deterministic ordering for equal inputs, food-vs-mobility and space-vs-energy conflict records surfaced, malformed/non-finite priority inputs rejected, human approval always required.

- [ ] **Step 2: Run test and confirm RED**

```bash
python scripts/test_cs1_campus_orchestrator.py
```

Expected: module missing.

- [ ] **Step 3: Implement `orchestrate_recommendations(...)`**

Use explicit deterministic ranking from readiness class, caller-supplied severity/deadline/affected-unit values where present and source-health quality; do not learn weights. Keep withheld items in a separate collection and never strengthen readiness. Represent conflicts explicitly with participating decision IDs and reason codes.

- [ ] **Step 4: Run all backend CS1 campus-ops focused tests**

```bash
python scripts/test_cs1_source_health.py
python scripts/test_cs1_campus_state.py
python scripts/test_cs1_mobility_policy.py
python scripts/test_cs1_space_policy.py
python scripts/test_cs1_campus_orchestrator.py
python -m compileall -q backend/app/decision scripts
```

Expected: PASS.

- [ ] **Step 5: Commit Task 4**

```bash
git add backend/app/decision/campus_orchestrator.py scripts/test_cs1_campus_orchestrator.py
git commit -m "feat(cs1): add campus operations orchestrator"
```

## Task 5: Next.js API Adapters and Contract Parity

**Files:**
- Create: `frontend/src/lib/campus-ops.ts`
- Create: `frontend/src/app/api/v1/campus-ops/state/route.ts`
- Create: `frontend/src/app/api/v1/campus-ops/recommendations/route.ts`
- Create: `frontend/src/app/api/v1/campus-ops/mobility/evaluate/route.ts`
- Create: `frontend/src/app/api/v1/campus-ops/space/evaluate/route.ts`
- Optional create: `frontend/src/data/campus_ops_contract_fixtures.json`

**Interfaces:**
- TypeScript contract mirrors `campus-ops-v1.0` readiness/provenance/human-control semantics.
- Existing `/api/v1/food`, `/api/v1/shuttles`, `/api/v1/occupancy` and `/api/v1/scenarios/*` remain untouched and available.

- [ ] **Step 1: Add TypeScript contract types and validation helpers**

Define canonical readiness, provenance, SourceHealth and DecisionRecommendation types; include legacy `PUBLIC_SOURCE` input alias normalization only at adapter boundaries.

- [ ] **Step 2: Add API route contract tests through typecheck/static fixtures**

Fixtures must prove `WITHHOLD` preservation, future-source rejection semantics, operator approval required and automatic execution disabled. Do not add synthetic operational outcomes.

- [ ] **Step 3: Implement additive state/recommendation/mobility/space route handlers**

Handlers validate input, call deterministic adapter logic or consume versioned backend artifacts, and return explicit truth-boundary metadata. Do not expose live ETA, observed shuttle occupancy or verified room-capacity fit when sources are unavailable.

- [ ] **Step 4: Run frontend validation**

```bash
cd frontend
npm run typecheck
npm run lint
npm run build
```

Expected: PASS.

- [ ] **Step 5: Run repository regression gates**

```bash
cd ..
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
python -m compileall -q backend/app scripts
```

Expected: PASS.

- [ ] **Step 6: Commit Task 5**

```bash
git add frontend/src/lib/campus-ops.ts frontend/src/app/api/v1/campus-ops frontend/src/data/campus_ops_contract_fixtures.json
git commit -m "feat(cs1): expose campus operations api contracts"
```

## Task 6: Integration, Preservation, and PR Fan-In

**Files:**
- No product changes unless validation exposes a defect.
- PR metadata documents all touched paths and truth-boundary guarantees.

**Interfaces:**
- Consumes all prior tasks as one campus-ops feature package.
- Produces a feature PR targeting `role/cs1-decision-intelligence`.

- [ ] **Step 1: Rebase/sync the implementation branch on the latest CS1 role branch without discarding active CS1 work**

Resolve conflicts by preserving both valid implementations; never use whole-file blind `ours`/`theirs` for shared decision surfaces.

- [ ] **Step 2: Run focused + broad validation on exact head**

```bash
python scripts/test_cs1_source_health.py
python scripts/test_cs1_campus_state.py
python scripts/test_cs1_mobility_policy.py
python scripts/test_cs1_space_policy.py
python scripts/test_cs1_campus_orchestrator.py
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
python -m compileall -q backend/app scripts
cd frontend && npm ci --no-audit --no-fund && npm run typecheck && npm run lint && npm run build
```

Expected: PASS.

- [ ] **Step 3: Run feature-preservation comparison for the target role integration context**

Use the repository-prescribed `verify_feature_preservation.py` invocation with the current base ref/SHA before any role-to-master integration.

- [ ] **Step 4: Open/update the feature PR to `role/cs1-decision-intelligence`**

PR description must state: no autonomous execution; no live shuttle telemetry claim; no verified room-capacity/enrollment claim unless integrated; no measured impact claim; all outputs preserve provenance and decision cutoff.

- [ ] **Step 5: Require exact-head CI before merge**

Do not treat local/focused checks as merge authority.

- [ ] **Step 6: After role fan-in, verify the role-to-master integration contains the campus-ops commits and current master before merge**

Final completion is only after verified master contains the work per repository policy.
