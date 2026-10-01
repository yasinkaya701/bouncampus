# Agent Next Actions — Deep Research Handoff

**Research date:** 2026-10-01  
**Purpose:** Convert secondary research into executable work without promoting secondary evidence into PMR.

## Shared strategic conclusion

Current research supports one execution hierarchy:

> **Test BOUNCAMPUS as a campus resource decision-and-verification layer, with dining production as the first beachhead; treat classroom allocation and shuttle scheduling as P1 adjacency hypotheses, not parallel pivots.**

Why:

- Boğaziçi already publishes sustainability metrics and has established water/energy governance; “first dashboard” is not a strong novelty claim.
- Public food-waste scale is measurable and non-zero.
- Dining has a short action/outcome feedback cycle.
- Classroom scheduling now has a publicly identified owner and a 161-room general-use capacity inventory.
- Shuttle operations expose public route/timetable structure, but departure-level pain remains unverified.
- Türkiye's policy/ranking landscape increasingly rewards measurement, digitalization, governance and operational efficiency.

Read first:

1. `CAMPUS_DECISION_SURFACE_ATLAS.md`
2. `BOGAZICI_DATA_SYSTEM_OWNERSHIP_MAP.md`
3. the domain pack for your task

The common loop is:

```text
Observe -> Reconcile -> Decision Context -> Predict/Optimize -> Recommend -> Human Act -> Verify
```

---

# IE — Customer Discovery & Market Lead

## P0: reconstruct the real dining production decision

Target stakeholders:

1. Food Services Branch manager + one Food Engineer;
2. dining control organization owner/member for unresolved acceptance/hakediş semantics;
3. TEMAŞ local project/production operator;
4. BİD data owner after the business fields are known;
5. waste/measurement owner.

Ask for a **recent concrete service**, not opinions.

Reconstruct:

```text
when demand was estimated
who estimated it
what data they looked at
who approved quantity
when quantity became difficult to change
what happened if too much was produced
what happened if too little was produced
what was measured afterward
who bore operational/economic consequences
```

### Dining kill/modify conditions

Modify or kill the wedge if repeated evidence shows:

- production quantity is fixed outside the reachable workflow;
- excess production is not a material component of measured waste;
- decisions cannot be changed at a useful time;
- the decision owner has no actionable discretion;
- required data cannot be captured at acceptable effort;
- shortage/service-level risk makes the proposed control point unacceptable.

## P1a probe: classroom allocation — ONE owner interview first

Read `BOGAZICI_CLASSROOM_ALLOCATION_AND_OCCUPANCY.md`.

Public route: **Kayıt İşleri Şube Müdürlüğü** is responsible for general-use classroom scheduling.

The goal is not to pitch optimization. Determine whether a material problem exists.

Ask:

```text
Walk me through the latest semester room-assignment cycle.
What was the hardest exception?
Which part is still manual?
What caused the most rework after the first schedule?
What constraints cannot be violated?
Which trade-off do you make most often?
When does the assignment become expensive to change?
```

Continue deeper only if manual burden, mismatch, late changes or movement cost are recurring and consequential.

## P1b probe: shuttle scheduling — ONE operator interview first

Read `BOGAZICI_SHUTTLE_OPERATIONS_AND_DEMAND.md`.

Ask for the last overloaded/empty/unreliable departure and how the timetable was changed afterward.

Discover:

```text
operator
approver
ridership measurement
timetable change cadence
vehicle/driver constraint
left-behind/queue failure
reliability failure
contract constraint
```

Do not ask generic students “would you like a smarter shuttle app?” before the operator workflow is known.

---

# EE — Physical Systems & Measurement Lead

## P0: validate measurement feasibility for one dining service

Do not design hardware until current measurement is known.

For one service, determine whether these can be measured/exported:

- planned portions;
- produced portions;
- served portions;
- preparation waste kg;
- edible production surplus kg;
- plate/post-consumer waste kg;
- early sell-out/substitution;
- service start/end;
- scale/measurement method.

Required table:

```text
field | current source | owner | granularity | retention | quality | access | effort | blocker
```

If waste streams cannot be separated safely, document the smallest feasible distinction rather than inventing precision.

## Classroom measurement rule

Before proposing occupancy sensors, test whether enrollment/assignment/change data already solve the decision. If occupancy sensing is actually required:

- ground-truth a sample physically/manual first;
- do not equate raw Wi-Fi client count with occupancy;
- record estimation uncertainty;
- aggregate for privacy;
- label inferred values `ESTIMATED_OCCUPANCY`.

## Shuttle measurement rule

Before new counters, audit existing:

- manual ridership counts;
- vehicle logs;
- driver/operations records;
- any card/access telemetry;
- actual departure/arrival history.

Hardware is justified only by a verified measurement gap.

## Water/energy later-stage discovery

Water already has formal quarterly measurement/reporting responsibility. Energy already has ISO 50001 measurement/governance. Therefore future interviews should ask **what action remains hard despite measurement**, not whether measurement exists.

---

# EHB — Embedded Hardware, Communications & Integration Lead

Read `BOGAZICI_DATA_SYSTEM_OWNERSHIP_MAP.md` before proposing any sensing stack.

## Rule: close an evidence gap, do not create a hardware project

A new device is justified only when all are true:

```text
real decision validated
+ required physical variable identified
+ existing system cannot provide acceptable signal
+ measurement accuracy/latency requirement known
+ installation/privacy/safety boundary acceptable
```

Candidate future gaps only after validation:

- dining weight/count measurement where current records fail;
- shuttle aggregate passenger counting where no usable logs exist;
- room occupancy ground truth for calibration;
- water/energy submeter gap if an actionable decision requires it.

Do not build display/kiosk hardware as a substitute for PMR.

---

# CS1 — Decision Intelligence Lead

## P0: dining baseline-first

Before complex ML, implement/evaluate simple comparators when real historical data arrive:

1. same weekday + meal historical mean;
2. trailing comparable-service mean/median;
3. calendar-aware linear/tree baseline;
4. only then richer models using menu/weather/mobility/event context.

Evaluate decision utility, not only RMSE/MAE.

Candidate loss:

```text
loss = overproduction_cost * surplus_portions
     + shortage_cost * unmet_demand_or_early_sellout
     + override/friction penalty
```

Coefficients are workflow/policy parameters until evidence supports them.

Required behavior:

- `WITHHOLD` when source quality is insufficient;
- operator approval;
- overrides + reasons;
- honest uncertainty semantics;
- source-reported vs derived/model-estimated separation.

## P1 classroom model family

Only after the one-owner PMR probe validates pain:

```text
current assignment replay
-> feasibility validator
-> greedy best-fit
-> transparent ILP
-> multiobjective recommendation
```

Candidate objectives: capacity slack, room-type mismatch, room changes, transition distance/time. Preserve accessibility/equipment as constraints, not afterthoughts.

## P1 shuttle model family

Only after operator pain + departure-level measurement exist:

```text
current timetable
-> historical departure-load baseline
-> class-transition demand prior
-> simple threshold recommendation
-> constrained schedule optimization
-> richer prediction only if incremental value exists
```

Never use course schedule as a substitute for actual ridership.

---

# CS2 — Product Strategy, Evidence Synthesis & Application

## P0: keep narrative around observed facts + explicit unknowns

Safe context:

- Boğaziçi publicly reports 48,251 kg food waste for 2025.
- Boğaziçi already has sustainability monitoring/governance across multiple domains.
- Türkiye's sustainable-campus ecosystem is increasingly formal and digitally governed.

Still hypothesis:

- demand mismatch is a material cause;
- production planning is the best intervention point;
- operator persona will use recommendations;
- universities will pay for a cross-domain platform;
- reporting/provenance pain is commercially meaningful.

## Expansion narrative

Classroom and shuttle work may demonstrate that the reusable platform unit is not “food AI” but:

```text
owned decision
+ trusted inputs
+ constraints
+ recommendation
+ human override
+ outcome verification
```

Do not present these adjacency modules as validated customer demand until owner interviews confirm recurring pain.

Preferred category language:

- campus resource intelligence;
- operational sustainability decision support;
- measurement + recommendation + verification;
- traceable decision evidence.

Avoid until validated:

- autonomous campus optimization;
- real-time digital twin;
- AI operating system for all campus functions;
- guaranteed ranking improvement;
- guaranteed waste/energy reduction.

---

# Frontend / UX agents

Research should drive a common **decision card** primitive.

Show:

- action required;
- target/ranked option;
- why;
- missing data/readiness;
- hard constraints and risks;
- confidence/uncertainty;
- approve/override/reject;
- later actual outcome.

Domain examples:

- Dining: recommended production/allocation band.
- Classroom: ranked feasible room alternatives + constraint trade-offs.
- Shuttle: departure/frequency change + crowding/reliability trade-off.

De-prioritize generic KPI walls, decorative AI chat, unsupported live sensor animations and 3D-first navigation.

---

# Backend / data agents

Read `METRIC_PROVENANCE_AND_VERIFICATION.md` and `BOGAZICI_DATA_SYSTEM_OWNERSHIP_MAP.md` before durable schemas.

Minimum rules:

- event timestamp != reporting period;
- scheduled != observed;
- capacity != demand;
- estimated != measured;
- recommendation != approved action != executed action;
- business owner != technical owner != access authority;
- unresolved source conflict must be representable as `RECONCILIATION_REQUIRED`;
- operator decision and outcome need stable IDs.

Recommended ownership/provenance fields:

```text
source_system
business_owner
technical_owner
semantic_validator
access_authority
observed_at
available_at
privacy_class
transformation_version
```

---

# Research backlog ranked by expected decision value

## P0 — primary research, not more generic web browsing

1. Who owns daily dining production quantity and when is it frozen?
2. What share of food waste is pre-consumer surplus vs plate/preparation waste?
3. Which operational data are retained per service?
4. What happens when the kitchen under-produces?
5. What does the contractor get paid for: produced, delivered, accepted or served quantities?
6. Can the team access historical menu/served/waste data for a pilot?

## P1 — bounded adjacency probes

7. Registrar: is classroom allocation a repeated costly/manual decision, and what is the constraint hierarchy?
8. Shuttle operator: are there repeatable departure-level load/reliability imbalances, and can schedules be changed?
9. If either passes, request only the minimum field-level dataset defined in its research pack.

## P2 — water/energy action-gap discovery

10. Which water decisions are currently made from quarterly data, and which are delayed/manual?
11. Which energy anomalies/actions are already automated or manually reviewed under ISO 50001?
12. Who prepares sustainability evidence and where is reconciliation painful?
13. Does verification of savings affect capital budgets or procurement decisions?

## P3 — external market research

14. Repeat validated workflow interviews at 2–3 Turkish public universities.
15. Benchmark commercial systems only after the specific decision gap is validated; generic competitor research is lower value.

---

# One-page mental model for all agents

```text
PUBLIC SOURCE:
Boğaziçi has measurable sustainability operations, 48,251 kg reported 2025 food waste,
a named classroom-scheduling owner and a public multi-campus shuttle system.

UNKNOWN:
Which operational decisions are materially painful, actionable and data-accessible?

PMR:
Find owner, timing, constraints, data, consequences and workaround.

TECH TEST:
Can a transparent baseline improve the decision without violating service constraints?

PILOT:
Human-reviewed recommendation + measured outcome + guardrails.

ONLY THEN:
Claim measured impact and deepen/expand the module.
```
