# CS1 Campus Operations Decision Intelligence — Architecture Design

Date: 2026-10-01
Owner: CS1 — Decision Intelligence Lead
Status: design approved in chat; written spec awaiting user review
Target role branch: `role/cs1-decision-intelligence`
Related active implementation branch: `agent/api-product/cs1-campus-ops-core`

## 1. Purpose

BOUNCAMPUS currently has a strong food-waste decision loop plus secondary shuttle, occupancy, building, energy, course, and scenario surfaces. The next CS1 step is to turn those isolated capabilities into one auditable campus-operations decision system without weakening the repository's evidence boundary.

The system must answer a consistent operational question across domains:

> Given the information that was actually available at decision time, what bounded action should an operator consider, how uncertain is that recommendation, what evidence supports it, and when should the system abstain?

The initial operational domains are:

1. cafeteria production and service planning,
2. shuttle pressure and schedule-review support,
3. classroom / space allocation and timetable-quality analysis,
4. aggregate campus-state estimation,
5. building / energy-aware scheduling scenarios,
6. event and service-disruption impact analysis.

The goal is not autonomous campus control. The goal is a common decision-intelligence layer that produces explainable, provenance-aware, human-reviewed recommendations that can later be evaluated against real operational outcomes.

## 2. Success criteria

This architecture is successful when all of the following are true:

- food, shuttle, and space decisions can be represented through one common decision contract;
- all important inputs retain provenance, availability time, freshness, and source-health state;
- no domain can silently substitute fake telemetry for missing live data;
- missing critical inputs cause an explicit downgrade or abstention;
- no recommendation can automatically dispatch a kitchen, shuttle, room reassignment, building-control command, or external action;
- course-schedule information is reused across food, mobility, occupancy, and space decisions instead of being reimplemented separately;
- the system can identify room-time collisions, cross-campus transition pressure, building load concentration, and shuttle pressure using aggregate operational data;
- capacity-sensitive room reassignment is withheld unless room capacity and enrollment inputs are actually verified;
- shuttle occupancy / ETA / capacity claims are withheld unless those data sources are actually integrated;
- every recommendation is reproducible from a versioned input snapshot and decision cutoff;
- each domain can be tested independently, while the orchestrator can rank compatible recommendations across domains;
- the design preserves the current food pilot evidence chain and existing truth boundaries.

## 3. Non-goals

The following are explicitly outside this version:

- autonomous kitchen production dispatch;
- automatic shuttle dispatch or timetable publication;
- automatic classroom reassignment in university systems;
- live GPS ETA unless an authorized shuttle telemetry source is later integrated;
- live shuttle occupancy or vehicle-capacity claims without verified data;
- student-level tracking, Wi-Fi identity, device identity, payment identity, or person-level mobility traces;
- claiming actual campus occupancy from schedule-derived or modeled estimates;
- claiming measured energy, CO2, cost, water, food-waste, or mobility savings before real outcome evidence exists;
- treating building capacity as room capacity;
- treating course existence as enrollment;
- presenting scenario coefficients or heuristic weights as learned optimal parameters unless a documented evaluation supports that statement.

## 4. Architectural principles

### 4.1 Decision first, model second

Each domain starts from an operational decision, not from a preferred algorithm. A simple transparent rule is acceptable when it is more defensible than a complex model.

### 4.2 Evidence-time boundary

A decision may use only information whose `available_at` / `published_at` timestamp is at or before the decision cutoff. Future information leakage is a hard failure.

### 4.3 Aggregate by default

Campus state, shuttle pressure, and space analysis must work on aggregate course, room, zone, building, route, and event records. Person-level identifiers are rejected from the core campus-state contract.

### 4.4 Human control

All operational recommendations require human review.

```text
operator_approval_required = true
automatic_execution_allowed = false
```

This rule is domain independent.

### 4.5 Abstention is a valid output

The system may return `WITHHOLD` when critical sources are absent, stale beyond policy, unavailable at decision time, structurally inconsistent, or insufficient for the requested decision.

### 4.6 Provenance survives orchestration

The campus orchestrator may aggregate and rank recommendations, but it may not erase source provenance, decision cutoff, limitations, readiness, or domain-specific constraints.

## 5. Existing assets to preserve and reuse

The design must reuse, not replace, current repository assets where appropriate:

- CS1 food policy and baseline-first decision logic;
- food pilot template / scorecard / matched-pair work;
- reservation reconciliation and prospective decision-audit work as it lands;
- method-selection, stability, and context-ablation work as it lands;
- `frontend/src/lib/shuttle-network.ts` official shuttle network adapter and truth boundary;
- `frontend/src/app/api/v1/shuttles/route.ts` official-route surface;
- `frontend/src/data/real_boun_courses.json` and backend course snapshot;
- aggregate building metadata in `campus_config.json`;
- existing occupancy / energy research models as explicitly labeled model outputs;
- Next.js `/api/v1/*` as the standalone product runtime;
- Python backend modules as the CS1 research, validation, and offline analysis surface.

No active CS1 feature branch should be overwritten or duplicated. New modules must use additive file boundaries unless integration explicitly requires an adapter.

## 6. System overview

```text
PUBLIC / VERIFIED SOURCES
  course schedule
  academic calendar
  official shuttle routes/schedules
  public menu/context
  public events
  verified operator measurements when available
          |
          v
SOURCE NORMALIZATION + HEALTH
  provenance
  available_at
  fetched_at
  freshness
  coverage
  decision-time eligibility
          |
          v
AGGREGATE CAMPUS STATE
  campus / zone loads
  schedule transitions
  event loads
  occupancy model estimates
  source limitations
          |
          +----------------------+----------------------+-------------------+
          |                      |                      |                   |
          v                      v                      v                   v
      FOOD POLICY          MOBILITY POLICY          SPACE POLICY      ENERGY/BUILDING
          |                      |                      |                   |
          +----------------------+----------------------+-------------------+
                                 |
                                 v
                      COMMON DECISION CONTRACT
                                 |
                                 v
                       CAMPUS ORCHESTRATOR
                                 |
                                 v
                   HUMAN-REVIEW DECISION QUEUE
                                 |
                                 v
                         MEASURED OUTCOMES
                                 |
                                 v
                      CALIBRATION / EVALUATION
```

## 7. Core contracts

### 7.1 SourceHealth

Every material source used by CS1 decision logic should normalize into:

```python
{
    "source_id": str,
    "domain": str,
    "provenance": "OFFICIAL_PUBLIC" | "OFFICIAL_LIVE" | "OFFICIAL_SNAPSHOT" | "EXTERNAL_LIVE" | "MODEL_ESTIMATE" | "OPERATOR_MEASUREMENT",
    "available": bool,
    "published_at": str | None,
    "fetched_at": str | None,
    "decision_cutoff": str,
    "freshness_seconds": int | None,
    "coverage": float | None,
    "status": "VERIFIED" | "STALE" | "PARTIAL" | "UNAVAILABLE" | "NOT_AVAILABLE_AT_DECISION_TIME",
    "reason_codes": list[str],
}
```

`published_at` or an equivalent availability timestamp controls decision-time eligibility. If a source becomes available after the cutoff, it cannot influence that decision.

Input adapters may accept legacy source labels only as explicit aliases. In particular, the existing campus-state TDD fixture uses `PUBLIC_SOURCE`; the source-health layer must normalize that alias to the canonical emitted provenance `OFFICIAL_PUBLIC`. Canonical decision outputs must not emit the legacy alias.

### 7.2 CampusState

Contract version: `campus-ops-v1.0`.

The existing TDD contract on `agent/api-product/cs1-campus-ops-core` establishes these required semantics:

- aggregate zone inputs;
- no person-level identifiers;
- campus totals;
- source-aware readiness;
- `REVIEW_REQUIRED` for usable but unvalidated aggregate state;
- `WITHHOLD` when required schedule or occupancy-model inputs are missing;
- future information rejected at decision time;
- `automatic_execution_allowed = false`;
- `operator_approval_required = true`;
- explicit `NO_LIVE_TELEMETRY_CLAIM` limitation.

A normalized result should include at least:

```python
{
    "contract_version": "campus-ops-v1.0",
    "decision_time": str,
    "decision_readiness": "PILOT_READY" | "REVIEW_REQUIRED" | "WITHHOLD",
    "abstained": bool,
    "campus_totals": {...},
    "zone_states": [...],
    "source_health": [...],
    "reason_codes": [...],
    "limitations": [...],
    "operator_approval_required": True,
    "automatic_execution_allowed": False,
}
```

`PILOT_READY` is reserved for a domain decision whose required inputs and evaluation contract are sufficiently defined for a bounded human-reviewed pilot. Aggregate campus state itself should normally remain `REVIEW_REQUIRED` until downstream policy confirms its own requirements.

### 7.3 DecisionRecommendation

All vertical policies expose a common envelope:

```python
{
    "decision_id": str,
    "contract_version": "campus-ops-v1.0",
    "domain": "food" | "mobility" | "space" | "energy" | "event",
    "target_id": str,
    "decision_time": str,
    "baseline": {...},
    "recommendation": {...} | None,
    "readiness": "PILOT_READY" | "REVIEW_REQUIRED" | "WITHHOLD",
    "abstained": bool,
    "reason_codes": list[str],
    "constraints": list[str],
    "source_health": list[dict],
    "provenance": list[str],
    "limitations": list[str],
    "operator_approval_required": True,
    "automatic_execution_allowed": False,
}
```

Optional numeric uncertainty fields may be present only when their semantics are defined. Arbitrary heuristic bands must not be described as calibrated confidence intervals.

## 8. Domain engine: food operations

### 8.1 Scope

Food remains the best-developed and primary KREATE evidence chain. This architecture does not replace it.

Food decisions may include:

- production starting quantity,
- batch size,
- preparation timing,
- replenishment timing,
- controlled surplus intervention,
- pilot eligibility.

### 8.2 Inputs

Candidate inputs include:

- reservation intent when available and reconciled;
- historical service baselines;
- course-schedule-derived campus flow;
- menu context;
- academic calendar;
- weather available at the decision horizon;
- operator constraints;
- measured service outcomes after service completion.

### 8.3 Rules

- reservation is intent, not served demand;
- model estimates remain distinct from measurements;
- no automatic kitchen dispatch;
- current open CS1 work on reservation reconciliation, method selection, stability, context ablation, matched pilot pairs, and decision records remains authoritative for those slices;
- campus-state integration should provide context through an adapter rather than duplicating food policy logic.

## 9. Domain engine: mobility / shuttle decision support

### 9.1 Decision target

The first mobility decision is not live dispatch. It is:

> Which route / time windows have enough evidence of aggregate transfer pressure to justify operator review of schedule or capacity allocation?

### 9.2 Inputs

- official shuttle route topology;
- official published departure schedule when parsable / integrated;
- course end/start transitions by campus or stop-compatible zone;
- aggregate event transitions;
- academic-calendar phase;
- verified vehicle capacity if later integrated;
- measured ridership if later integrated.

### 9.3 Derived signals

The policy may compute:

- `scheduled_transfer_pressure`;
- origin/destination transition counts or weighted course-flow proxies;
- pressure by route and time window;
- number of compatible published departures;
- source coverage;
- whether capacity-sensitive analysis is possible.

### 9.4 Output semantics

Candidate actions:

- `KEEP_CURRENT_SCHEDULE`;
- `REVIEW_DEPARTURE_TIMING`;
- `REVIEW_CAPACITY`;
- `REVIEW_EXTRA_TRIP`;
- `WITHHOLD`.

Rules:

- without verified vehicle capacity, `REVIEW_CAPACITY` cannot contain an asserted load percentage;
- without ridership / occupancy measurements, route pressure is a schedule-derived or model-derived proxy, not observed passenger demand;
- without GPS, no live ETA is generated;
- additional-trip recommendations remain human-reviewed planning recommendations;
- climate impact remains scenario analysis unless measured operational evidence supports a stronger claim.

## 10. Domain engine: classroom / space allocation

### 10.1 Decision target

The initial space policy answers:

> Are there timetable collisions, avoidable cross-campus transitions, or building-load concentrations that justify a human review of room / timetable allocation?

It does not automatically reassign rooms.

### 10.2 Inputs available now

The course snapshot already exposes, where present:

- course code;
- day;
- hour;
- assigned room;
- instructor;
- course metadata.

Building metadata exposes aggregate building capacities and building identity.

### 10.3 Inputs not assumed

The following must be treated as unavailable until a verified adapter exists:

- actual room capacity;
- actual section enrollment;
- accessibility requirements for a specific section;
- laboratory / equipment constraints unless explicitly modeled;
- authoritative room availability outside the observed timetable snapshot.

Building-level capacity must never be substituted for room capacity.

### 10.4 Checks available before room-capacity integration

The first policy can safely detect:

- same-room / same-time collisions in the snapshot;
- inconsistent room references;
- repeated room changes across consecutive meetings;
- campus transitions between adjacent class periods;
- building-level scheduled load concentration;
- time windows with unusually concentrated or sparse scheduled activity;
- candidate timetable-locality improvements that do not claim capacity fit.

### 10.5 Candidate reassignment semantics

A room-change candidate may be produced only as a review candidate.

Example:

```json
{
  "course_id": "...",
  "current_room": "NH 401",
  "candidate_zone": "south-academic",
  "capacity_fit": "NOT_VERIFIED",
  "readiness": "REVIEW_REQUIRED",
  "reason_codes": ["REDUCES_CROSS_CAMPUS_TRANSITION"],
  "constraints": ["ROOM_CAPACITY_SOURCE_REQUIRED", "ENROLLMENT_SOURCE_REQUIRED"]
}
```

No candidate becomes `PILOT_READY` for capacity-sensitive reassignment until room capacity and enrollment contracts are verified.

## 11. Domain engine: building / energy-aware scheduling

This engine remains scenario-first.

It may use aggregate schedule / campus state plus existing energy-model estimates to compare scheduling patterns such as:

- concentrating low-load sessions into fewer buildings during low-demand windows;
- avoiding unnecessary building activation;
- comparing alternative timetable concentration patterns.

Rules:

- model energy estimates remain `MODEL_ESTIMATE`;
- modeled cost / CO2 differences are scenario outputs, not achieved savings;
- no BMS / smart-meter claim is permitted without verified integration;
- no building-control action is automatically executed.

## 12. Event and disruption analysis

A lightweight event policy may model the operational effect of:

- large public events;
- exam-period load shifts;
- building closure;
- heavy-rain mobility changes;
- unusual academic-calendar periods.

The output should identify which domain policies need re-evaluation, not invent measured effects.

Example:

```text
EVENT
  -> campus-state recomputation
  -> food demand context invalidated / widened
  -> shuttle pressure review
  -> room / building load review
```

## 13. Campus orchestrator

### 13.1 Responsibility

The orchestrator does not create domain evidence. It:

1. collects domain recommendations;
2. rejects recommendations whose required source-health contract is invalid;
3. preserves provenance and limitations;
4. identifies conflicts between recommendations;
5. ranks review priority;
6. emits one human-review queue.

### 13.2 Priority ranking

Ranking should use explicit, deterministic factors such as:

- readiness state;
- severity / reason-code class;
- time to decision deadline;
- number of affected aggregate services / zones;
- whether an existing operator commitment is at risk;
- source-health quality.

No hidden learned ranking should be introduced in v1.

### 13.3 Cross-domain conflicts

The orchestrator must surface conflicts rather than silently optimizing one domain at the expense of another.

Examples:

- moving a class may reduce shuttle pressure but worsen building activation;
- reducing food production may reduce expected surplus but raise stockout risk;
- concentrating classes may improve energy scenarios but create mobility congestion.

The v1 orchestrator should return a conflict record with competing reason codes and require human review.

## 14. Runtime and API design

### 14.1 Python research / decision modules

New additive modules should live under:

```text
backend/app/decision/
  campus_state.py
  source_health.py
  mobility_policy.py
  space_policy.py
  campus_orchestrator.py
```

Existing active modules owned by open CS1 PRs must not be rewritten merely to fit this architecture.

### 14.2 Next.js product runtime

The standalone product should expose co-located routes that call deterministic TypeScript counterparts or serialized artifacts where practical.

Proposed routes:

```text
GET  /api/v1/campus-ops/state
GET  /api/v1/campus-ops/recommendations
POST /api/v1/campus-ops/mobility/evaluate
POST /api/v1/campus-ops/space/evaluate
```

These routes must be additive and must not replace existing `/api/v1/food`, `/api/v1/shuttles`, `/api/v1/occupancy`, or scenario routes.

### 14.3 Cross-language parity

Where the same decision semantics exist in Python and TypeScript, contract fixtures should verify parity for:

- readiness;
- abstention;
- reason codes;
- provenance classes;
- operator-approval policy;
- automatic-execution policy.

Complex research-only evaluation may remain Python-only if the product route consumes a versioned artifact rather than reimplementing the model.

## 15. Source-health policy

### 15.1 Required source classes

For aggregate campus state v1:

- course schedule: required;
- occupancy model / aggregate occupancy estimate: required for utilization claims;
- events: optional but tracked;
- academic calendar: optional context;
- shuttle schedule: required only for schedule-review mobility outputs;
- room capacity: required only for capacity-sensitive room outputs;
- enrollment: required only for capacity-sensitive room outputs.

### 15.2 Fail-closed behavior

Examples:

```text
missing schedule
    -> campus state WITHHOLD

occupancy estimate published after decision cutoff
    -> campus state WITHHOLD

missing shuttle capacity
    -> route pressure may be estimated
    -> occupancy percentage must be withheld

missing room capacity or enrollment
    -> collision detection may run
    -> capacity-fit recommendation must be NOT_VERIFIED
```

## 16. Privacy and data minimization

The campus-operations core must reject common person-level identifier fields including, at minimum:

- `student_id`;
- `person_id`;
- `email`;
- `device_id`;
- `wifi_client_id`;
- payment identity fields.

Aggregate section, room, route, zone, service, and event identifiers are acceptable.

A future connector requiring person-level data would require a separate privacy design and is outside this architecture.

## 17. Error handling

All policy modules should distinguish:

1. invalid input contract -> raise / return validation failure;
2. valid but insufficient evidence -> `WITHHOLD`;
3. valid but uncertain / incomplete operational evidence -> `REVIEW_REQUIRED`;
4. bounded pilot-ready decision -> `PILOT_READY` only where the domain defines a measurement plan.

Malformed numeric values, negative capacities, non-finite values, impossible timestamps, duplicate identifiers where uniqueness is required, and person-level fields should fail validation rather than being silently coerced.

## 18. Testing strategy

### 18.1 Campus-state regression tests

The existing `scripts/test_cs1_campus_state.py` contract is retained and expanded, not replaced.

Required tests:

- aggregate state builds without person-level data;
- missing schedule fails closed;
- missing required occupancy source fails closed for utilization decisions;
- future information cannot affect the decision;
- person-level identifiers are rejected;
- negative / non-finite capacity values are rejected;
- no live telemetry claim is emitted;
- automatic execution remains disabled.

### 18.2 Mobility tests

- course-transition pressure is deterministic;
- no GPS -> no ETA output;
- no ridership -> no observed-demand wording;
- no vehicle capacity -> no occupancy percentage;
- missing official schedule -> schedule-review action WITHHOLD;
- future schedule snapshot -> fail closed;
- recommendation requires operator review.

### 18.3 Space tests

- duplicate room-time assignment is detected;
- same course record does not self-collide;
- cross-campus consecutive transition is detected;
- missing room capacity prevents capacity-fit claim;
- missing enrollment prevents capacity-sensitive reassignment;
- building capacity is never substituted for room capacity;
- no automatic reassignment output exists.

### 18.4 Orchestrator tests

- preserves domain provenance;
- preserves domain limitations;
- never promotes `WITHHOLD` to a stronger state;
- detects cross-domain conflicts;
- deterministic priority ordering;
- rejects recommendation contract version mismatch;
- human approval required for every emitted action.

### 18.5 Repository validation

Before integration, run the existing repository gates in addition to focused tests:

```text
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
python -m compileall -q backend/app scripts
frontend typecheck
frontend lint
frontend build
feature-preservation verification for master integration
```

Exact-head CI remains authoritative.

## 19. Implementation isolation and active-branch coordination

Current CS1 work already occupies active feature slices. New campus-operations work must avoid overlapping their files.

Known active areas include:

- matched pilot enforcement;
- reservation reconciliation / decision records;
- method selection / stability / contextual-signal ablation;
- role-to-master decision-core integration.

Therefore v1 campus-operations implementation should prefer additive files:

```text
backend/app/decision/campus_state.py
backend/app/decision/source_health.py
backend/app/decision/mobility_policy.py
backend/app/decision/space_policy.py
backend/app/decision/campus_orchestrator.py
scripts/test_cs1_campus_state.py
scripts/test_cs1_mobility_policy.py
scripts/test_cs1_space_policy.py
scripts/test_cs1_campus_orchestrator.py
```

The existing `agent/api-product/cs1-campus-ops-core` branch has already added the first campus-state contract test. That branch should remain the canonical implementation branch for the first backend slice unless task ownership changes explicitly.

Frontend routes and UI integration should be a later non-overlapping slice after the core contracts are stable.

## 20. Delivery sequence

The architecture should be implemented in this order:

1. campus-state core satisfying the existing TDD contract;
2. shared source-health validation;
3. mobility policy on schedule-derived aggregate transfer pressure;
4. space policy for collisions, transition burden, and capacity-gated candidates;
5. campus orchestrator;
6. deterministic contract fixtures and focused tests;
7. Next.js API adapters;
8. operator review surface integration;
9. parity and repository-wide validation;
10. feature PR -> CS1 role branch;
11. role branch sync with current master;
12. exact-head role integration CI;
13. normal merge commit to master;
14. post-merge verification.

Food-policy changes owned by other active CS1 PRs should fan in through the role branch rather than being duplicated in this workstream.

## 21. Acceptance criteria

The backend campus-operations package is acceptable when:

- `campus_state.py` satisfies the existing contract tests;
- source-health logic rejects future information and missing required sources;
- mobility policy produces only evidence-compatible planning recommendations;
- mobility policy cannot emit live ETA, observed ridership, or occupancy percentage without verified source support;
- space policy detects room-time collisions and cross-campus transitions;
- space policy cannot claim capacity fit without verified room capacity and enrollment;
- orchestrator preserves readiness, provenance, limitations, and human approval requirements;
- no module performs automatic external execution;
- all new policy outputs are deterministic for fixed inputs;
- all focused tests pass;
- repository validation and exact-head CI pass before merge.

The product integration package is acceptable when:

- new campus-operations routes are additive;
- existing food, shuttle, occupancy, scenarios, and data routes remain available;
- UI wording preserves `MODEL_ESTIMATE`, public-source, and unavailable-source distinctions;
- no measured-impact claim is introduced without measured evidence;
- degraded data visibly degrades readiness rather than being replaced by fabricated telemetry.

## 22. Future extensions after v1

These are compatible with the architecture but not required for the first implementation package:

- verified room-capacity adapter;
- verified section-enrollment adapter;
- official shuttle timetable parser with versioned snapshots;
- authorized ridership / vehicle-capacity feed;
- measured campus-space occupancy pilot;
- energy-meter integration;
- multi-objective scenario optimization after real tradeoff weights are elicited;
- causal / quasi-experimental evaluation of schedule interventions;
- operator override learning once enough real decision records exist.

Each future extension must enter through the same source-health and decision-time boundary rather than bypassing it.

## 23. Final design decision

BOUNCAMPUS will use **separate vertical decision policies over a shared aggregate campus-state and source-health contract, coordinated by a deterministic human-review orchestrator**.

It will not use one opaque campus-wide optimizer in v1.

This keeps food, mobility, space, energy, and event reasoning independently testable, lets missing data fail closed per domain, preserves the repository's evidence firewall, reduces merge conflicts, and allows the team to add verified data sources later without changing the fundamental decision architecture.
