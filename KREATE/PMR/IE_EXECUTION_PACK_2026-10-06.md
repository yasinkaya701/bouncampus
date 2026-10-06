# IE Execution Pack — Decision Rights, Economics, PMR, and Pilot

**Owner:** IE — Customer Discovery & Market  
**Date:** 2026-10-06  
**Status:** execution framework / repo artifact; **not** interview evidence, measured pilot evidence, or validated unit economics.

## Objective

Convert the current dining research base into a falsifiable operating plan for the IE workstream.

The IE workstream is not complete when the team can describe food waste or forecast demand. It is complete only when the team can answer, with primary evidence:

```text
who chooses quantity
→ when it freezes
→ what information exists before that point
→ what happens when quantity is too high / too low
→ who bears each consequence
→ who may approve a change
→ what record proves the outcome
→ who can buy / require / veto the intervention
```

This file separates what can be designed now from what remains blocked on external primary evidence.

## Current IE state

### Durable secondary/public evidence already available

The repository now has:
- a current Boğaziçi procurement surface and contractor anchor under IKN `2025/1727143`;
- official/public Boğaziçi food-service, food-waste, BUCard and operating-context sources;
- cross-university evidence that pre-service quantity planning, demand uncertainty, replenishment, card/turnstile counts and contextual forecasting recur in Türkiye;
- competitor evidence showing generic “AI demand forecasting” and broad waste dashboards are not defensible novelty claims;
- a provenance-first PMR source catalog and claim firewall.

### Source-backed owner/process narrowing — 2026-10-06

First-party Boğaziçi sources now narrow several routes:

- `S-BU-021`: BUCard is a BİDB service; cafeteria card services span SKS + BİDB; turnstile/card-reader support routes to BİDB.
- `S-BU-023`: BUCampus exposes a user-facing turnstile/card-reader passage-history surface.
- `S-BU-026`: Procurement branch is the source-backed tender/specification route.
- `S-BU-014`: current Dining Cooking/Distribution Control Organization roster; Aygül Demir is a principal member.
- `S-BU-030`: 2025 Administration Activity Report supports Control Organization review → KİK56.0/H → relevant Spending Authority → hakediş preparation.
- `S-BU-027`: Tahakkuk branch explicitly handles hakediş payments.

This reduces routing uncertainty only. Export access, exact food-contract Spending Authority, payable count, current unit-price schedule, quantity freeze and economic-risk allocation remain unverified.

### Still unknown and promotion-blocking

The following remain **UNKNOWN** until primary evidence exists:

1. Boğaziçi/TEMAŞ daily quantity owner.
2. Exact total-production, campus-allocation and batch/replenishment freeze points.
3. Current operator baseline / heuristic / system.
4. Local shortage vs surplus consequence and safety buffer.
5. Which party bears the economic cost of excess production.
6. Which quantity is authoritative for acceptance / hakediş.
7. Whether service-level planned/produced/served/surplus/waste data are exportable.
8. Economic buyer, champion, pilot approver and veto chain.
9. Same-product / same-sales-process repeatability at a second site.

Do not convert public procurement facts, aggregate waste totals, software capability, synthetic datasets, or team assumptions into answers to these questions.

---

## IE decision-rights map

For one recent meal service, reconstruct this chain with names/roles and timestamps.

| Stage | Question | Evidence to request | Status |
| --- | --- | --- | --- |
| Forecast / initial plan | Who first proposes a quantity? | production sheet, ERP/spreadsheet screenshot, verbal workflow | UNKNOWN |
| Approval | Who approves/changes the plan? | signed/approved form, system role, concrete incident | UNKNOWN |
| Total production freeze | When is total production expensive or impossible to change? | timestamp, kitchen cutoff, batch schedule | UNKNOWN |
| Campus allocation freeze | Can quantity still move between campuses after total production freezes? | allocation sheet / distribution plan | UNKNOWN |
| Replenishment | Can a later batch / substitute menu recover a shortage? | recent incident and lead time | UNKNOWN |
| Service count | Which record represents served demand? | BUCard/turnstile/QR report + correction semantics | UNKNOWN; see #292 |
| Surplus / waste | Which record separates edible surplus, prep loss and plate waste? | scale log / disposal form / manual sheet | UNKNOWN |
| Acceptance | Which record is accepted for contract performance? | acceptance / control / hakediş document | PARTLY NARROWED: KİK56.0/H → Spending Authority workflow known; exact food-contract fields/count remain UNKNOWN; see #358 |
| Settlement | Which quantity drives payment? | unit-price schedule + hakediş rule | UNKNOWN |
| Override | Who may reject a recommendation and why? | authority chain + recent override example | UNKNOWN |

### Interview method

Do not start with “Would you use our system?”

Start with a **recent concrete service** and ask the stakeholder to walk backward from the final served/accepted count to the first quantity decision. Capture documents, timestamps, corrections, handoffs and exceptions.

A role title is not proof of decision ownership.

---

## Decision-making unit

Keep these roles separate even if one person eventually fills multiple roles.

| Role | Definition | Current Boğaziçi status |
| --- | --- | --- |
| End user | Reviews/acts on production or allocation recommendation | UNKNOWN |
| Champion | Has enough pain/influence to push a pilot | UNKNOWN |
| Economic beneficiary | Captures avoided cost / service benefit | UNKNOWN |
| Economic buyer | Has budget/procurement authority | UNKNOWN |
| Pilot approver | Can authorize a bounded test | UNKNOWN |
| Data owner | Can provide required service-level record | BİDB/BUCard technical route source-backed; release/export authority still UNKNOWN |
| Semantic owner | Can explain what fields/counts actually mean | UNKNOWN |
| Veto holder | Can block for contract, food safety, privacy, IT or operations | UNKNOWN |

### Buyer test

A useful interview must distinguish:
- who suffers from excess;
- who suffers from shortage;
- who pays the contractor;
- who pays for ingredients/labor/emergency replenishment;
- who can purchase software/services;
- who can require a contractor to use a tool;
- who can approve access to operational records.

Do not infer buyer from university ownership of the cafeteria or from the headline contract value.

---

## Contract / incentive scenarios

Use scenarios only as a questioning framework until authoritative Boğaziçi clauses are retrieved.

### Scenario A — contractor quantity-risk dominant

```text
contractor materially chooses quantity
+ contractor absorbs surplus cost
+ contractor faces shortage/service penalties or recovery cost
+ settlement depends on realized/accepted service
```

Likely implication: contractor operations may be the primary user and economic beneficiary.

### Scenario B — institution-led plan, contractor execution

```text
institution sets/notifies plan
→ contractor executes
→ contractor may still bear execution / shortage / excess consequences
→ settlement follows an accepted quantity rule
```

Likely implication: adoption may require a two-sided university + contractor workflow.

### Scenario C — institution bears most quantity economics

```text
institution controls production quantity
+ institution pays for or directly bears surplus
+ institution bears service/reputation risk from shortage
```

Likely implication: SKS / food-services / procurement may be closer to buyer and beneficiary.

### Kill / modify condition

If the actor who can change quantity neither bears a meaningful consequence nor can influence the party who does, the proposed product may have a broken incentive chain. Modify buyer, workflow, or beachhead before adding features.

---

## IE optimization objective

The product should not optimize point-forecast accuracy in isolation.

For a service with demand `D` and chosen quantity `q`, the decision layer should reason about an asymmetric loss:

```text
L(q, D) =
  C_over  × max(q - D, 0)
+ C_under × max(D - q, 0)
+ operational guardrail penalties
```

Where:

- `C_over` = evidence-backed marginal consequence of one excess portion;
- `C_under` = evidence-backed marginal consequence of one unmet portion;
- guardrails can include early sellout, emergency substitution, unacceptable delay, capacity or food-safety constraints.

Neither cost may be populated with invented “meal cost”, contract-value division, or guessed penalties.

If the classical single-period assumptions are approximately valid and both costs are known, the newsvendor critical fractile is:

```text
P(D ≤ q*) = C_under / (C_under + C_over)
```

This is a **decision rule**, not proof that Boğaziçi should use it. PMR must establish whether the assumptions, timing and control rights hold.

### Safe implementation before cost evidence

Until real costs/consequences are known:
- run sensitivity scenarios across a clearly labeled range;
- expose the consequence of different under/over ratios;
- keep the output advisory;
- preserve human approval;
- never label scenario values as “savings” or “optimized cost”.

---

## Bounded recommendation contract

An IE-acceptable recommendation should include:

1. target service and decision cutoff;
2. point estimate / baseline estimate;
3. recommended quantity or bounded range;
4. explicit overage/underage scenario assumption;
5. capacity / batch constraints;
6. readiness state;
7. missing-information reasons;
8. operator override and reason;
9. source snapshot IDs;
10. no automatic kitchen dispatch.

The system should **WITHHOLD** when the actual decision cutoff, required input semantics, or authority chain is not established strongly enough for safe action.

---

## Primary interview queue for IE

The IE-owned four slots should test different failure modes rather than repeat the same persona.

### IE-01 — Boğaziçi Food Services operations

**Goal:** reconstruct one recent service end-to-end.  
**Must learn:** quantity owner, freeze time, current heuristic/system, last surplus/shortage incident, referral to contractor/data/acceptance owners.  
**Artifact request:** current production request / planning sheet / anonymized example if shareable.  
**Falsifier:** no meaningful pre-service quantity decision exists or the team cannot reach it.

### IE-02 — Control / acceptance / procurement route

**Goal:** establish acceptance, change rights and hakediş semantics.  
**Must learn:** accepted quantity, sign-off chain, penalty/service clauses, unit-price item semantics, who can authorize workflow changes.  
**Artifact request:** authoritative contract/spec clause, acceptance form/schema, daily reconciliation form.  
**Falsifier:** recommendation cannot legally/operationally alter any relevant quantity before freeze.

### IE-03 — TEMAŞ local operations / production planning

**Goal:** map contractor-side planning, risk and economics.  
**Must learn:** who plans, what data are used, buffer logic, shortage recovery, surplus ownership, software/procurement authority.  
**Artifact request:** de-identified production/allocation record and one recent exception story.  
**Falsifier:** planning is already solved to the point that the proposed intervention adds no material operational value.

### IE-04 — second-site counter-archetype

**Goal:** test whether the same problem, product language and buying process repeat outside Boğaziçi.  
**Target:** a mature data-informed university operation or reservation-first/contractor-risk operation.  
**Must learn:** same control point? same buyer? same data? same decision timing?  
**Falsifier:** repeatable kernel exists but buyer/workflow differs enough to require a separate segment/product.

Do not mark any tracker slot `OUTREACH`, `SCHEDULED` or `COMPLETED` without a real corresponding event.

---

## Minimum data handoff from IE to CS1

For every real service record, IE should attempt to secure the semantic owners and provenance for:

### Decision-time
- `service_id`
- `campus_id`
- `meal_period`
- `service_date`
- `decision_cutoff_at`
- `operator_status_quo_quantity`
- reservation/intent count where truly applicable
- menu snapshot ID
- calendar/context snapshot IDs
- any other signal known before cutoff

### Outcome / reconciliation
- reported served/passages with exact semantic name
- `produced_portions`
- `actual_surplus_portions` and/or accepted `waste_kg`
- `shortage_or_early_sellout`
- substitutions / emergency production
- finalization timestamp
- source report ID
- reconciliation/acceptance state

### Decision audit
- recommendation version
- recommended quantity/range
- operator action
- override reason
- evidence/provenance IDs

Do not rename an unreconciled passage count to `actual_served`.

---

## Pilot KPI hierarchy

Primary IE outcome should connect the quantity decision to waste **without sacrificing service**.

### Primary outcome candidate
`edible_surplus_kg_per_100_served_meals` or another stage-specific upstream waste metric if that is what the accepted measurement can support.

### Guardrails
- early-sellout incidence;
- unmet demand / rejected diners where measurable;
- emergency substitution incidence;
- service delay;
- food-safety or quality nonconformance;
- operator override rate and reasons.

### Decision-quality metrics
- asymmetric decision loss;
- absolute/signed quantity error;
- excess portions per 100 served;
- shortage portions per 100 served;
- calibration/coverage only if a genuinely calibrated interval exists.

### Commercial/process metrics
Only after buyer PMR:
- time spent planning;
- time to approve/override;
- integration burden;
- procurement/pilot approval cycle;
- economic value using evidence-backed unit consequences.

Do not use aggregate 2025 campus waste as the denominator for an intervention claim.

---

## IE acceptance gates

### Gate 1 — control point
**PASS** only if a reachable actor can change or approve a relevant quantity before a real freeze point.

### Gate 2 — causal target
**PASS** only if production mismatch is shown to be material enough to justify intervention, or the product is explicitly modified to the dominant waste stage.

### Gate 3 — data truth
**PASS** only if service-level outcome semantics and provenance are adequate for comparison.

### Gate 4 — incentive chain
**PASS** only if the beneficiary / buyer / user relationship is coherent enough for adoption.

### Gate 5 — safe pilot
**PASS** only if a bounded human-reviewed trial can measure improvement without relaxing shortage, quality or food-safety guardrails.

### Gate 6 — repeatability
**PASS** only if at least one second-site workflow is similar enough to support the same product and sales motion; otherwise segment explicitly.

---

## What IE can claim now

Safe:
- the repository has identified a current Boğaziçi procurement/contractor surface;
- similar pre-service quantity-planning mechanisms recur across multiple Turkish university dining operations;
- the team has a falsifiable framework for decision ownership, asymmetric risk, data truth and pilot measurement;
- the remaining high-value uncertainty is primary operational/customer evidence.

Not safe:
- demand mismatch causes most Boğaziçi waste;
- Boğaziçi currently overproduces by a quantified amount;
- TEMAŞ or the university will buy/use the product;
- a specific unit meal cost, penalty or savings;
- a verified quantity freeze time;
- model lift, pilot impact or measured waste reduction.

## Cross-role handoff

- **CS1:** consume decision cutoff, operator baseline, under/over consequence semantics and admitted service truth; optimize decision loss only after evidence exists.
- **CS2:** use only supported buyer/workflow facts in application language; do not promote scenario economics into value claims.
- **EE:** measure only the waste stage / field that PMR shows is decision-critical and unavailable from current operations.
- **EHB:** hardware remains downstream of a proven measurement gap.

## Immediate unresolved blockers

- #292 — privacy-preserving BUCard/service truth + semantic reconciliation.
- #358 — authoritative contract/spec/hakediş mechanics.
- #322 — primary PMR handoffs and second-site interview.
- Real IE interview slots — still not evidence until actual outreach/scheduling/completion is documented.
