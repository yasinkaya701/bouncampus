# Campus Operations Decision OS — Architecture Design

**Date:** 2026-10-01  
**Status:** Approved design, implementation pending written-spec review  
**Primary role:** CS1 — Decision Intelligence Lead  
**Cross-role impact:** CS2 product surface, EE measurement inputs, IE workflow/decision-right validation  
**Existing implementation owner:** `TASK-CS1-CAMPUS-OPS-CORE` / `agent/api-product/cs1-campus-ops-core`

## 1. Goal

Extend BOUNCAMPUS from a food-focused decision-support system into a reusable **Campus Operations Decision OS** that can support dining, shuttle planning, classroom allocation, occupancy/energy coordination, and later compatible campus operations domains without presenting estimates as live university telemetry.

The product is not a dashboard of disconnected cards. Each domain must participate in a common loop:

```text
OBSERVE
→ SNAPSHOT / RECONCILE
→ ESTIMATE
→ GENERATE CANDIDATES
→ CHECK CONSTRAINTS
→ SCORE / RANK
→ READINESS GATE
→ HUMAN REVIEW
→ EXECUTE OUTSIDE THIS PACKAGE
→ RECONCILE OUTCOME
→ AUDIT
```

## 2. Existing truth boundaries

The design inherits and strengthens current repository truth rules:

- no claim of live shuttle GPS, real-time vehicle occupancy, verified fleet capacity, Wi-Fi/turnstile occupancy, cafeteria POS, BMS, registrar write access, or smart-meter control unless explicitly integrated and verified;
- course schedules are **official snapshots**, not live room occupancy;
- repository-generated occupancy predictions are model estimates and cannot be promoted to measured occupancy;
- food reservation counts are intent signals, not served demand;
- no optimizer may convert public/synthetic/model-estimated inputs into achieved climate/cost/waste claims;
- human approval remains mandatory for bounded operational recommendations;
- automatic university operational dispatch is outside this package.

## 3. Architecture

The system is split into a shared decision kernel plus domain-specific policies.

```text
                         Campus Decision Kernel
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
       Dining                  Shuttle                Classroom
          │                       │                       │
 reservation/reconcile      demand/capacity          course/room
 forecast/baseline          headway/seat plan        hard constraints
 production target          trip recommendation      assignment plan
          │                       │                       │
          └───────────────┬───────┴────────┬──────────────┘
                          │                │
                     Portfolio        Audit / Outcome
                          │                │
                    Human Review      Reconciliation
```

### 3.1 Shared decision kernel

The common kernel must be domain-neutral and expose only decision-support semantics. It owns:

- stable decision identity;
- input snapshot references;
- decision-time cutoff / freeze semantics;
- provenance classes;
- hard-constraint status;
- recommendation + alternatives;
- readiness state;
- reason codes;
- human review requirement;
- audit metadata;
- later outcome linkage.

It does **not** own domain-specific optimization math.

### 3.2 Domain policies

Domain policies translate aggregate operational inputs into bounded candidates:

- dining: quantity / allocation / service-mode / batch recommendation;
- shuttle: keep schedule / add capacity / shift departure / review capacity;
- classroom: room assignment / reassignment / conflict resolution / consolidation candidate;
- energy/occupancy adapters: advisory cross-domain implications only until stronger evidence exists.

## 4. Canonical decision contract

`backend/app/decision/campus_contract.py` should define the canonical internal contract.

Required fields:

```text
decision_id
service_or_window_id
domain
created_at
decision_cutoff_at
freeze_at
input_snapshot_ids[]
input_provenance[]
recommendation
alternatives[]
hard_constraints[]
soft_objectives[]
readiness
reason_codes[]
operator_approval_required
auto_dispatch_allowed=false
claim_scope
```

Allowed readiness states:

- `READY_FOR_REVIEW` — inputs and hard constraints are sufficient for an operator-reviewed decision;
- `REVIEW_REQUIRED` — a candidate exists but uncertainty, freshness, disagreement, or operational ambiguity requires review;
- `WITHHOLD` — required evidence or hard-constraint validity is missing/contradictory.

The kernel must never infer `READY_FOR_REVIEW` from prediction confidence alone.

## 5. Provenance and evidence classes

At minimum, every input and derived output must retain one of these classes:

- `PUBLIC_SOURCE`
- `OFFICIAL_SNAPSHOT`
- `MEASURED_PILOT_DATA`
- `MODEL_ESTIMATE`
- `POLICY_HEURISTIC`
- `SYNTHETIC_OR_GENERATED`
- `UNKNOWN`

A derived recommendation must expose the weakest material provenance affecting the decision. Missing provenance for a required input is fail-closed.

## 6. Campus state snapshot

`backend/app/decision/campus_state.py` should construct aggregate state snapshots only.

The contract may include:

```text
campus / building / route / room identifiers
time window
scheduled course demand
verified capacities where known
public timetable facts
reservation aggregates
weather/calendar/menu context when decision-time-valid
model estimates with explicit provenance
freshness / captured_at / valid_through
```

It must reject or ignore individual-level movement histories, student identifiers, BUCard identifiers, scholarship data, private grades, or inferred personal trajectories.

## 7. Shuttle policy

`backend/app/decision/shuttle_policy.py` owns mobility recommendations.

### Inputs

- route identifier;
- published timetable/headway snapshot;
- aggregate demand signal for a decision window;
- verified or operator-supplied vehicle capacity when available;
- fleet/vehicle availability constraints when available;
- service freeze time;
- provenance/freshness metadata.

### Hard gates

A capacity-changing recommendation must `WITHHOLD` when verified usable capacity or required fleet constraints are absent.

If demand is estimated but capacity is unknown, the policy may emit **advisory risk only**, e.g. `REVIEW_CAPACITY`, not a fabricated number of buses.

### Candidate actions

- `KEEP_SCHEDULE`
- `ADD_CAPACITY`
- `SHIFT_DEPARTURE`
- `REVIEW_CAPACITY`
- `WITHHOLD`

### Objective

After hard constraints pass, score candidates using caller-registered weights such as:

- unmet seat demand / overload risk;
- excessive idle capacity;
- schedule deviation;
- transfer/campus movement burden;
- operational complexity.

Weights are policy parameters unless measured economics exist.

### Explicit non-claim

Course-end schedules may be used as aggregate demand context but are never live passenger counts.

## 8. Classroom allocation policy

`backend/app/decision/classroom_policy.py` owns room assignment.

### Inputs

- course meeting instances;
- candidate rooms;
- room capacities;
- room campus/building;
- accessibility requirements;
- equipment requirements;
- fixed/unmovable assignments;
- time-slot conflicts;
- snapshot freshness.

### Hard constraints

The allocator must enforce before optimization:

1. one room cannot host overlapping meetings;
2. room capacity must satisfy required enrollment/capacity input when that input is verified;
3. accessibility requirements cannot be violated;
4. required equipment cannot be violated;
5. fixed/manual constraints must be preserved;
6. unsupported/missing critical room metadata produces `REVIEW_REQUIRED` or `WITHHOLD`, not a confident assignment;
7. stale schedule snapshots cannot produce an auto-promotable assignment plan.

### Soft objectives

After hard feasibility:

- minimize unused seat capacity;
- minimize unnecessary cross-campus movement;
- minimize room churn;
- prefer building/floor consolidation when it does not violate academic constraints;
- expose possible energy-consolidation benefits only as `POLICY_HEURISTIC` or later verified evidence.

The first algorithm should be deterministic and explainable. A greedy/min-cost baseline is preferred before introducing a heavier solver. OR-Tools/ILP is justified only when the baseline cannot meet acceptance criteria.

## 9. Dining integration

The common kernel must adapt, not rewrite, the existing food work.

Existing CS1 feature ownership remains authoritative:

- PR #68: matched-pilot evidence structure;
- PR #69: reservation-first reconciliation / decision-loss production;
- PR #70: method selection / stability / context-ablation.

The Campus Operations work must not duplicate these implementations. It should consume their stabilized outputs after role-branch convergence.

Food decisions mapped into the common contract should preserve:

- reservation-is-intent semantics;
- decision cutoff/freeze;
- baseline/model method identity;
- `WITHHOLD` / review semantics;
- operator approval;
- no automatic kitchen dispatch;
- outcome reconciliation separate from prospective recommendation.

## 10. Cross-domain portfolio

`backend/app/decision/campus_portfolio.py` should aggregate independent domain decisions without pretending they are jointly optimized unless a registered joint objective exists.

Examples of allowed cross-domain signals:

- classroom consolidation candidate → energy review candidate;
- scheduled course release window → shuttle demand context;
- academic calendar/menu/service windows → dining context;
- known campus transfer pattern from public timetable → mobility planning context.

Examples of forbidden inference:

- class schedule → live building occupancy;
- room assignment → actual student attendance;
- shuttle timetable → actual passenger count;
- food reservation → actual served count.

Portfolio ranking may prioritize urgent/conflicting decisions but must preserve each domain’s provenance and readiness independently.

## 11. API surface

`backend/app/routers/campus_ops.py` should expose a read/compute decision-support API without claiming write access to university operational systems.

Initial endpoints:

```text
GET  /api/v1/campus-ops/health
POST /api/v1/campus-ops/state/evaluate
POST /api/v1/campus-ops/shuttle/recommend
POST /api/v1/campus-ops/classrooms/allocate
POST /api/v1/campus-ops/portfolio/evaluate
```

Responses must include:

- input provenance;
- freshness;
- readiness;
- reason codes;
- human approval required;
- `auto_dispatch_allowed: false`;
- claim boundary.

Persistent approval/outcome endpoints may be added only when storage semantics are defined; this architecture does not fabricate persistence.

## 12. Action engine migration

The current hard-coded `ActionEngine` is not a valid operational intelligence layer. It should eventually become an adapter over validated campus decision outputs, not a generator of fabricated impact numbers.

Migration rule:

- do not delete it until feature preservation confirms downstream users;
- first add the new campus decision API;
- then adapt callers;
- only then remove or deprecate hard-coded actions in a separate, reviewable change.

## 13. Failure semantics

Required fail-closed behavior:

- non-finite numeric input → reject/withhold;
- negative capacity/demand → reject/withhold;
- conflicting fixed room assignments → withhold with explicit conflict IDs;
- missing required room attributes → review/withhold;
- stale schedule snapshot → review/withhold;
- missing shuttle capacity for capacity-changing action → withhold;
- post-freeze recommendation → withhold;
- contradictory provenance or malformed timestamps → withhold;
- model-estimated occupancy presented as measured → contract violation/test failure.

## 14. Testing strategy

Implementation is TDD and deterministic.

### Kernel/state tests

- valid aggregate snapshot;
- stale input;
- malformed timestamps;
- privacy-rejected fields;
- mixed provenance;
- decision after freeze.

### Shuttle tests

- nominal verified-capacity recommendation;
- overload candidate;
- unknown capacity → advisory only;
- malformed/negative demand;
- insufficient fleet evidence;
- decision after freeze.

### Classroom tests

- feasible assignment;
- oversubscribed demand;
- overlapping room conflict;
- accessibility requirement;
- equipment requirement;
- fixed assignment preservation;
- stale snapshot;
- impossible assignment → explicit withheld/unassigned set.

### Portfolio tests

- independent readiness preserved;
- one domain withheld does not silently invalidate or promote another;
- no cross-domain provenance promotion;
- no automatic dispatch;
- no fabricated impact.

## 15. Delivery decomposition

The architecture is intentionally split into independently reviewable implementation packages:

### Package A — Shared campus decision kernel

Files:

- `backend/app/decision/campus_contract.py`
- `backend/app/decision/campus_state.py`
- `scripts/test_cs1_campus_state.py`

### Package B — Shuttle policy

Files:

- `backend/app/decision/shuttle_policy.py`
- `scripts/test_cs1_shuttle_policy.py`

### Package C — Classroom allocation

Files:

- `backend/app/decision/classroom_policy.py`
- `scripts/test_cs1_classroom_policy.py`

### Package D — Portfolio + API

Files:

- `backend/app/decision/campus_portfolio.py`
- `backend/app/routers/campus_ops.py`
- `backend/app/main.py`
- `scripts/test_cs1_campus_portfolio.py`

### Package E — Frontend/operator integration

Only after API contracts stabilize. UI must show provenance, readiness, constraints, alternatives, and human review status without fake telemetry.

## 16. Ownership and merge discipline

The active owner of Packages A-D is already registered as:

- task: `TASK-CS1-CAMPUS-OPS-CORE`;
- branch: `agent/api-product/cs1-campus-ops-core`;
- owner agent: `cs1-campus-ops-core`.

Other agents must not edit its declared paths while its lease is active.

Current CS1 role integration capacity is blocked by the three open feature PRs #68, #69, #70. Implementation may proceed on the existing task branch, but a fourth role-targeted PR must not open until a slot clears.

No merge to `role/cs1-decision-intelligence` or `master` without exact-head required CI green.

## 17. Acceptance criteria

The architecture is considered implemented when all of the following are true:

1. common campus state + decision contracts exist and are fail-closed;
2. shuttle policy can produce bounded advisory recommendations from aggregate inputs without inventing live capacity/occupancy;
3. classroom allocator enforces hard constraints before soft optimization and returns explicit unassigned/conflict diagnostics;
4. portfolio aggregation preserves domain-level provenance/readiness;
5. FastAPI exposes campus-ops endpoints with `auto_dispatch_allowed=false`;
6. tests cover nominal and failure cases listed above;
7. food work remains owned by #68/#69/#70 and is not duplicated;
8. current hard-coded action paths are not silently promoted into real operational claims;
9. no individual student movement/profile data is required;
10. exact-head CI is green before merge.

## 18. Explicitly deferred

Not required for the first implementation package:

- live shuttle GPS;
- real-time occupancy sensors;
- registrar write-back;
- automatic room reassignment in production;
- automatic vehicle dispatch;
- BMS actuation;
- individual student routing;
- monetary/climate impact optimization without measured/calibrated evidence;
- joint multi-domain mathematical optimization.

These can only be added as later evidence-backed workstreams.
