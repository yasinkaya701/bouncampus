# Agent Next Actions — Deep Research Handoff

**Research date:** 2026-10-01  
**Purpose:** Convert secondary research into executable work without promoting secondary evidence into PMR.

## Shared strategic conclusion

Current research makes one direction substantially more defensible than the generic alternatives:

> **BOUNCAMPUS should be tested as a campus resource decision-and-verification layer, with dining production as the first beachhead.**

Why:

- Boğaziçi already publishes sustainability metrics and has established water/energy governance; "first dashboard" is not a strong novelty claim.
- Public food-waste scale is measurable and non-zero.
- Dining has a short action/outcome feedback cycle.
- Academic literature supports demand forecasting and structural food-waste interventions as legitimate problem classes.
- The central causal claim — demand mismatch materially drives avoidable Boğaziçi waste — is still unvalidated and must remain a hypothesis.
- Türkiye's policy/ranking landscape increasingly rewards measurement, digitalization, governance and operational efficiency.

The strongest product loop to test is:

```text
Observe -> Reconcile -> Predict -> Diagnose -> Recommend -> Human Act -> Verify
```

---

# IE — Customer Discovery & Market Lead

## P0 task: reconstruct the real dining production decision

Target stakeholders:

1. SKS / Food Services decision owner;
2. North Campus central kitchen production lead;
3. food engineer/dietitian involved in menu/portion planning;
4. contractor-side operations manager if contractor participates in quantity planning;
5. institutional procurement/contract owner for economic incentive questions.

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

## Kill/modify conditions

Modify or kill the current wedge if repeated evidence shows:

- production quantity is contractually/factually fixed outside the reachable workflow;
- excess production is not a material component of the measured waste stream;
- decisions cannot be changed at a useful time;
- the decision owner has no actionable discretion;
- required data cannot be captured at acceptable cost/effort;
- shortage/service-level risk makes the suggested control point unacceptable.

## National buyer questions

Use `TURKIYE_POLICY_RANKING_PULL.md` only as context. Test whether external pressure actually changes work:

- Which rankings/YÖK/ISO/internal targets create recurring evidence workload?
- Who consolidates sustainability data?
- Does reporting influence budgets or only create administrative work?
- Which intervention was hardest to prove after implementation?

---

# EE — Physical Systems & Measurement Lead

## P0 task: validate measurement feasibility for one dining service

Do not design new hardware until current measurement is known.

For one service, determine whether the following can be measured or exported:

- planned portions;
- produced portions;
- served portions;
- preparation waste kg;
- edible production surplus kg;
- plate/post-consumer waste kg;
- early sell-out/substitution;
- service start/end;
- scale or measurement method.

## Required output

Create a field-by-field table:

```text
field | current source | owner | granularity | retention | quality | access | effort | blocker
```

If waste streams cannot be separated safely, document the smallest feasible distinction rather than inventing precision.

## Water/energy later-stage discovery

Research already indicates:

- Water Management Commission + periodic unit reporting exists publicly;
- ISO 50001 Energy Management System + Energy Management Team exists publicly.

Therefore future interviews should ask **what decision remains hard**, not whether measurement exists.

---

# CS1 — Decision Intelligence Lead

## P0 task: make the food decision model baseline-first

Before complex ML, implement/evaluate simple comparators when actual historical data becomes available:

1. same weekday + meal historical mean;
2. trailing comparable-service mean/median;
3. calendar-aware linear/tree baseline;
4. only then richer models using menu/weather/mobility/event context.

Evaluate decision utility, not just RMSE/MAE.

Candidate loss:

```text
loss = overproduction_cost * surplus_portions
     + shortage_cost * unmet_demand_or_early_sellout
     + override/friction penalty where relevant
```

The coefficients are workflow/policy parameters until evidence supports them.

## Required safety behavior

- expose `WITHHOLD` when input quality is insufficient;
- retain operator approval;
- record overrides and reasons;
- label planning band semantics honestly;
- keep source-reported data separate from model estimates;
- never infer live occupancy from schedule data.

## Key research falsifier

A high-accuracy forecast has no product value if it arrives after the production decision or the operator cannot act on it.

---

# CS2 — Product Strategy, Evidence Synthesis & Application

## P0 task: rewrite narrative around observed facts + explicit unknowns

Safe problem context:

- Boğaziçi publicly reports 48,251 kg food waste for 2025.
- Boğaziçi already has sustainability monitoring/governance across multiple domains.
- Türkiye's sustainable-campus ecosystem is increasingly formal and digitally governed.

Still hypothesis:

- demand mismatch is a material cause;
- production planning is the best intervention point;
- operator persona will use recommendations;
- universities will pay for a cross-domain platform;
- reporting burden/provenance pain is commercially meaningful.

## Stronger category language

Preferred:

- campus resource intelligence;
- operational sustainability decision support;
- measurement + recommendation + verification;
- traceable decision evidence.

Avoid until validated:

- autonomous campus optimization;
- real-time digital twin;
- AI operating system for all campus functions;
- guaranteed GreenMetric improvement;
- guaranteed X% food-waste reduction.

## Ranking narrative

UI GreenMetric 2026 gives a useful **why-now** hook because Governance & Digitalization now explicitly includes ICT-based sustainability monitoring/evaluation and advanced digital technologies supporting decisions/operational efficiency.

Use it to contextualize the market, not as proof of buyer demand.

---

# Frontend / UX agents

Research should change the primary screen hierarchy.

Prefer:

## Today / Tomorrow decision card

- action required;
- target quantity/range;
- why the system recommends it;
- missing data / readiness;
- risk guardrails;
- human approve/override;
- later actual outcome.

De-prioritize:

- generic KPI wall;
- eco-score gamification;
- heavy 3D campus map as the main product;
- decorative AI chat;
- unsupported live sensor animations.

The proof-of-value interaction is **decision -> action -> measured result**.

---

# Backend / data agents

Read `METRIC_PROVENANCE_AND_VERIFICATION.md` before defining durable schemas.

Minimum rules:

- event timestamp != reporting period;
- measurement stage is first-class;
- source owner/provenance is first-class;
- transformation versions are retained;
- source-reported vs derived vs model-estimated states cannot collapse;
- an unresolved source conflict must be representable as `RECONCILIATION_REQUIRED`;
- operator decision and outcome need stable IDs for later verification.

---

# Research backlog ranked by expected decision value

## P0 — primary research, not more web browsing

1. Who owns daily production quantity and when is it frozen?
2. What portion of food waste is pre-consumer surplus vs plate/preparation waste?
3. What operational data are actually retained per service?
4. What happens when the kitchen under-produces?
5. What does the contractor get paid for: produced, delivered, accepted or served quantities?
6. Can the team access historical menu/served/waste data for a pilot?

## P1 — institutional expansion discovery

7. Which water decisions are currently made from the Water Management Commission's quarterly data?
8. Which energy anomalies/actions are already automated or manually reviewed under ISO 50001?
9. Who prepares THE/YÖK/GreenMetric evidence and where is reconciliation painful?
10. Does verification of savings affect capital budgets or procurement decisions?

## P2 — external market research

11. Repeat the workflow interviews at 2–3 Turkish public universities with materially different dining procurement structures.
12. Benchmark commercial campus/BMS/ESG/foodservice systems only after the decision gap is validated; otherwise competitor research will be too generic.

---

# One-page mental model for all agents

```text
PUBLIC SOURCE:
Boğaziçi has measurable sustainability operations and 48,251 kg reported 2025 food waste.

UNKNOWN:
How much is avoidable by better production decisions?

PMR:
Find the owner, timing, constraints, data, consequences and current workaround.

TECH TEST:
Can a baseline model improve a real decision without increasing shortage risk?

PILOT:
Measure normalized waste and service-level guardrails.

ONLY THEN:
Claim measured impact and consider broader campus expansion.
```
