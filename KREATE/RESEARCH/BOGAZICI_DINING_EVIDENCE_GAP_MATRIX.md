# Boğaziçi Dining Evidence Gap Matrix — Research Stop Rules & Next Proof

**Research date:** 2026-10-01  
**Purpose:** Convert the accumulated secondary research into a ranked evidence-acquisition plan so agents stop duplicating web research and target the few artifacts/interviews that can materially confirm, modify or kill the dining decision thesis.  
**Status:** Research synthesis. **NOT PMR. NOT evidence promotion. NOT proof that the product thesis is validated.**

Related packs:

- [`BOGAZICI_SUSTAINABILITY_2025.md`](./BOGAZICI_SUSTAINABILITY_2025.md)
- [`BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md`](./BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md)
- [`BOGAZICI_CONTRACT_SEMANTICS_EVIDENCE_MAP.md`](./BOGAZICI_CONTRACT_SEMANTICS_EVIDENCE_MAP.md)
- [`BOGAZICI_DINING_INCENTIVE_SUBSIDY_MAP.md`](./BOGAZICI_DINING_INCENTIVE_SUBSIDY_MAP.md)
- [`BOGAZICI_DINING_PRIVACY_DATA_MINIMIZATION.md`](./BOGAZICI_DINING_PRIVACY_DATA_MINIMIZATION.md)

---

# 0. Executive conclusion

Public/academic research is now **strong enough to justify targeted PMR and data requests**, but **not strong enough to validate the product**.

The remaining uncertainty is concentrated in a small set of questions:

```text
1. What exact quantity is decided?
2. Who decides it?
3. When does it freeze?
4. What data/signals exist before freeze?
5. What quantity drives contract acceptance / hakediş?
6. Who bears excess and shortage risk?
7. What share of measured waste is actually production-mismatch waste?
8. Can a privacy-safe pilot measure the outcome at useful granularity?
```

More generic web research on “food waste is bad” or “ML can forecast demand” now has low marginal value.

The next decisive evidence should come from **current Boğaziçi operational artifacts and real stakeholder conversations**.

---

# 1. Research maturity by question

| Question | Public-source maturity | PMR/data maturity | Current state | Next decisive proof |
| --- | --- | --- | --- | --- |
| Is food waste real/measured? | HIGH | NONE | Established problem-scale context | No more web research needed; owner verification only before final claim |
| Is dining centrally structured? | HIGH | NONE | Strongly plausible/current public support | Current TEMAŞ/Food Services workflow confirmation |
| Is production quantity controllable? | MEDIUM | NONE | Core hypothesis still unverified | Last-real-lunch decision walkthrough |
| Who owns quantity? | LOW | NONE | UNKNOWN | Food Services + TEMAŞ interviews |
| When does quantity freeze? | LOW | NONE | UNKNOWN | Operator timeline / current SOP |
| Is there a daily call-off/request? | LOW | NONE | UNKNOWN | Current contract/spec or daily request artifact |
| What drives hakediş/payment? | LOW | NONE | CRITICAL UNKNOWN | Current signed contract/spec + progress-payment owner confirmation |
| Who bears excess cost? | MEDIUM sector precedent, LOW Boğaziçi | NONE | UNKNOWN | Current contract + contractor interview |
| Who bears shortage risk? | MEDIUM historical/sector precedent, LOW current | NONE | UNKNOWN | Current penalty/acceptance clauses + operator incident |
| Are aggregate demand signals accessible? | MEDIUM existence, LOW access | NONE | UNKNOWN | BİD aggregate sample export + data dictionary |
| Is demand mismatch a material waste cause? | LOW | NONE | UNKNOWN | Waste-category breakdown + 6+ incident stories |
| Can pilot avoid personal data? | HIGH technical feasibility | NONE | Strong design hypothesis | Institutional approval of aggregate schema |
| Does intervention save university money? | LOW | NONE | UNKNOWN | Settlement semantics + verified economic owner |
| Does intervention save contractor money? | MEDIUM sector precedent, LOW current | NONE | UNKNOWN | Contractor variable-cost/risk interview |
| Is menu mix a separate problem? | MEDIUM historical/current context | NONE | PLAUSIBLE | Current menu-planning/production interview + option counts |
| Does reservation/intent beat forecasting? | MEDIUM sector precedent | NONE | UNKNOWN at Boğaziçi normal service | Current reservation practices + experiment/baseline comparison |

---

# 2. P0 evidence acquisitions — highest information gain

These items can materially change the product direction. Do them before adding model complexity or application claims.

## P0-01 — One current quantity-workflow interview

**Target:** Food Services operational owner and/or North Campus/TEMAŞ production lead.

Ask them to reconstruct **yesterday's actual lunch**:

```text
when first quantity was estimated
who estimated it
what number was sent
what data were used
who approved it
what changed after approval
when changes became costly/impossible
how production was batched
how campuses were allocated
what happened to excess
what happened to shortage
```

### Evidence gained

Resolves or strongly narrows:

- quantity owner;
- freeze time;
- current heuristic;
- adjustment window;
- batch flexibility;
- campus allocation control;
- user persona.

### Kill condition

If no meaningful production/allocation decision exists before service, the current wedge must be modified or killed.

---

## P0-02 — Current signed-contract / specification quantity semantics

**Target artifact:** smallest current document excerpt that answers:

- daily requested/called-off quantity mechanics;
- acceptance quantity;
- progress-payment (`hakediş`) quantity;
- excess treatment;
- shortage/substitution/delay penalty;
- minimum/tolerance rules.

Preferred sources:

1. signed 2026–2027 contract relevant pages;
2. current technical specification relevant pages;
3. current administrative specification / hakediş procedure;
4. owner-confirmed progress-payment summary if clauses are not shareable.

### Evidence gained

Resolves whether economic value sits with:

- university;
- contractor;
- both;
- neither directly.

### Stop rule

Do not continue inferring payment mechanics from procurement total, student price or other universities once a current artifact is obtainable.

---

## P0-03 — One privacy-safe aggregate demand sample

**Target:** BİD / BUCard / BUCampus data owner.

Ask for a small sample such as:

```text
DATE | CAMPUS | MEAL_WINDOW | AGGREGATE_ENTRY_COUNT
```

for a limited period, plus a one-page data dictionary.

No identifiers.

### Evidence gained

Tests:

- export feasibility;
- temporal granularity;
- campus labeling;
- missingness;
- service-window alignment;
- QR/BUCard semantics;
- whether useful demand signal exists before/after production decision.

### Kill/modify condition

If aggregate entry data are unavailable, unreliable or only available after the decision with no historical utility, the model/input strategy must change.

---

## P0-04 — Waste boundary decomposition

A university-wide monthly waste total is not enough.

Need at least a short-period breakdown of:

```text
preparation waste
unserved cooked surplus
service-line leftovers
plate waste
edible donated/transferred surplus
compost/recovery
other
```

Prefer campus/meal granularity for a bounded sample.

### Evidence gained

Directly tests core causal hypothesis:

> Is production mismatch a material share of avoidable waste?

### Kill condition

If almost all relevant waste is plate waste/menu-consumption behavior with negligible unserved surplus, production-quantity optimization should be downgraded.

---

## P0-05 — Current operator baseline

Before an ML benchmark, record the actual current rule.

Examples to test, not assume:

- previous same weekday;
- historical average;
- reservation/intent;
- manual judgment;
- fixed quantity;
- contractor heuristic;
- university call-off;
- menu-specific adjustment.

### Evidence gained

Defines the true baseline to beat.

### Technical rule

A model is not useful merely because it beats a naive mean if the operator already uses a stronger heuristic.

---

# 3. P1 evidence acquisitions — pilot design

Do after the P0 control point is confirmed.

## P1-01 — Menu-option / mix counts

Needed if total demand and option mix are separate decisions.

Potential fields:

```text
MENU_ID
OPTION_ID
PLANNED_OPTION_QTY
SERVED_OPTION_QTY
SUBSTITUTION_EVENT
```

## P1-02 — Campus allocation records

Needed if central production is allocated before local demand is known.

Potential fields:

```text
TOTAL_PRODUCED
CAMPUS_PLANNED_ALLOCATION
CAMPUS_DELIVERED
CAMPUS_RETURNED_OR_SURPLUS
```

## P1-03 — Batch timing

Needed to know whether intrameal signals can change outcomes.

```text
BATCH_ID
START_TIME
COMMIT_TIME
QTY
ADJUSTABLE_UNTIL
```

## P1-04 — Service failure logs

Shortage must be measurable, not anecdotal.

```text
sellout
substitution
late batch
queue spike
complaint
operator override
```

Use aggregate/operational records, not personal complaint identities.

---

# 4. Evidence that should NOT be pursued now

Low marginal value unless a P0 question requires it.

## Stop researching generic global food-waste statistics

Already enough to establish climate relevance.

## Stop collecting random university case-study reduction percentages

They do not validate Boğaziçi impact.

## Stop model-shopping before data semantics

No need to compare dozens of architectures until target, baseline and decision deadline are known.

## Stop expanding TAM from tender-search counts

Market sizing waits for buyer/workflow repeatability and commercial PMR.

## Stop scraping person-level campus activity

The pilot can be designed on aggregates.

---

# 5. Evidence acquisition scorecard

Scoring is a **research prioritization heuristic**, not a statistical confidence score.

Scale: 1 low, 5 high.

| Evidence item | Product-direction impact | Ease | Uncertainty removed | Urgency | Priority |
| --- | ---: | ---: | ---: | ---: | --- |
| Quantity-workflow incident interview | 5 | 4 | 5 | 5 | P0 |
| Current contract/hakediş semantics | 5 | 2 | 5 | 5 | P0 |
| Aggregate demand sample | 5 | 3 | 5 | 5 | P0 |
| Waste boundary decomposition | 5 | 3 | 5 | 5 | P0 |
| Current operator baseline | 5 | 4 | 4 | 5 | P0 |
| Menu mix counts | 4 | 3 | 3 | 3 | P1 |
| Campus allocation records | 4 | 3 | 4 | 3 | P1 |
| Batch timing | 4 | 4 | 4 | 3 | P1 |
| Current penalty table | 4 | 2 | 4 | 4 | P0/P1 |
| Additional generic ML paper | 1 | 5 | 1 | 1 | DEFER |
| More global food-waste headline stats | 1 | 5 | 1 | 1 | DEFER |

---

# 6. Minimum evidence bundle to justify a pilot

Do not call a technical pilot `PILOT_READY` until at least:

1. a named current decision owner is confirmed;
2. a freeze/decision deadline is known;
3. current operator baseline is documented;
4. one privacy-safe aggregate demand source is feasible **or** a manual aggregate collection alternative exists;
5. produced/served/surplus outcome can be measured;
6. shortage/service guardrail can be measured;
7. waste boundary relevant to production mismatch is defined;
8. human approval/override is part of the workflow;
9. contract/economic claims remain excluded unless settlement semantics are verified.

---

# 7. Minimum evidence bundle to justify an economic claim

In addition to pilot readiness:

1. current line-item unit price or settlement rule verified;
2. `CONTRACT_ACCEPTED_QTY` / `HAKEDIS_QTY` semantics verified;
3. excess meal payment/risk owner verified;
4. shortage deduction/penalty verified if applicable;
5. intervention operating cost measured;
6. calculation reviewed by contract/budget owner.

Without these, only physical waste/service outcomes are claimable.

---

# 8. Minimum evidence bundle to justify a climate claim

1. measured physical food-waste reduction;
2. clear waste category/boundary;
3. no unacceptable shortage/service regression;
4. documented conversion method and factor source;
5. `MODEL ESTIMATE` label for CO2e/water/resource conversion;
6. uncertainty/range where appropriate.

Never jump from forecast accuracy to climate impact.

---

# 9. Evidence-to-decision map

| New evidence | Likely decision |
| --- | --- |
| Quantity is discretionary + mismatch incidents frequent | KEEP production-decision wedge |
| Quantity fixed externally / no discretion | MODIFY intervention point |
| Unserved surplus is material | KEEP quantity optimization hypothesis |
| Waste mostly plate waste | MODIFY toward menu/service/behavior intervention |
| Contractor bears excess and uses heuristic | Strengthen contractor-operator persona |
| University settlement decreases with actual accepted quantity | Strengthen university budget-owner case |
| Aggregate data inaccessible but manual pilot feasible | Keep pilot, simplify tech stack |
| Aggregate data inaccessible and manual measurement prohibitive | KILL/DEFER model-heavy pilot |
| Reservation removes most uncertainty cheaply | MODIFY from passive ML to reservation/hybrid workflow |
| Existing forecast already near operational ceiling | Shift to allocation/mix/batch or another domain |

---

# 10. Suggested 60-minute evidence sprint

If a stakeholder gives only one hour, use it to produce an artifact — not a broad conversation.

## 0–15 min

Walk through yesterday's lunch quantity decision.

## 15–30 min

Draw state machine:

```text
request -> produce -> deliver -> serve -> accept/pay -> surplus/waste
```

Write owner + timestamp + data source on every arrow.

## 30–45 min

Inspect one anonymized/aggregate example of:

- demand/entry count;
- production record;
- waste/surplus record.

## 45–60 min

Agree on:

- baseline;
- one candidate intervention;
- primary physical outcome;
- shortage guardrail;
- next artifact owner.

This one session can remove more uncertainty than another week of generic desk research.

---

# 11. Agent routing

## IE

Own:

- P0-01 quantity workflow;
- current operator baseline;
- decision-owner/persona validation;
- concrete mismatch incidents.

## CS2

Own:

- current contract/hakediş semantics routing;
- claim boundary;
- buyer/user/payer distinction;
- application narrative changes after PMR.

## EE

Own:

- waste boundary decomposition;
- produced/served/surplus measurement feasibility;
- manual fallback measurement protocol.

## CS1

Own only after P0 semantics:

- baseline implementation;
- forecast/uncertainty evaluation;
- asymmetric decision policy;
- service guardrails.

## BİD/data-owner route

Own/confirm:

- aggregate demand export feasibility;
- event semantics;
- retention;
- privacy-safe aggregation.

---

# 12. Current evidence confidence summary

## Strong public facts

- food waste is publicly reported;
- current dining is a formal six-campus service procurement;
- current contract is unit-price at procurement-line level;
- current contractor is TEMAŞ;
- current student dining is subsidized/access-supported;
- BUCard/QR and BUCampus dining-related systems exist;
- Food Services has specification/contractor-control duties;
- other Turkish university contracts demonstrate real historical-demand / actual-consumption / excess-risk mechanisms.

## Strong historical Boğaziçi precedents, not current facts

- North Campus central production;
- six-campus distribution dominance;
- menu-mix uncertainty;
- backup production continuity;
- payment-linked service penalties.

## Still unvalidated core claims

- demand mismatch materially causes current Boğaziçi food waste;
- current operator quantity decision is adjustable;
- current quantity freeze time;
- current payment/hakediş basis;
- current excess/shortage risk allocation;
- current aggregate data access;
- measured pilot effect;
- willingness to pay.

---

# 13. Research stop rule

Secondary research on the dining wedge should now expand only when it answers a **named P0/P1 gap**.

A new source should be rejected as low value if it merely says:

- food waste is globally important;
- AI can forecast demand;
- universities care about sustainability;
- another institution reduced waste by some percentage.

The next research cycle should be triggered by **new operational evidence** and ask narrower questions around the contradiction or mechanism discovered.

---

# 14. Bottom line

The repository now has enough secondary research to stop guessing broadly.

The highest-value next proof is:

```text
CURRENT REAL WORKFLOW
+
CURRENT CONTRACT SEMANTICS
+
CURRENT AGGREGATE DATA SAMPLE
+
CURRENT WASTE BOUNDARY
```

Until those exist, more model sophistication is premature.
