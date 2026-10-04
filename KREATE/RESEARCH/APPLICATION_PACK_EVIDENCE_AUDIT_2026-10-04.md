# KREATE Application Pack — Evidence Audit — 2026-10-04

**Audited artifact:** `docs/kreate-application-pack.md`  
**Purpose:** Identify which application statements are currently supported, hypothetical, misleading, or too broad after the October 4 research pass.  
**Status:** Research audit. This file does **not** claim PMR has occurred.

---

# Executive conclusion

The current pack has a strong evidence/falsifiability philosophy, but it still contains several places where a product hypothesis is phrased too close to a current fact.

Highest-risk issues:

1. annual food waste is allowed to imply production-planning causality;
2. the operational quantity decision is described before its real owner/timing is verified;
3. target user list is too broad and weakens persona specificity;
4. exact signal weights are policy heuristics, not validated model importance;
5. a 5-service-per-arm pilot gate can be mistaken for causal/statistical proof;
6. course schedule is described as the backbone even though schedule != observed dining demand;
7. broad climate-tech/expansion language is stronger than current PMR evidence.

---

# 1. One-line product

Current concept:

> BOUNCAMPUS turns measured institutional food waste into an uncertainty-aware, human-approved production decision...

## Risk

`measured institutional food waste -> production decision` can imply that the measured waste is already causally connected to production mismatch.

## Evidence-safe interpretation

The public waste baseline establishes **problem scale**, while the product **tests** whether a pre-service production decision can prevent an addressable part of it.

## Research-safe category

`PROPOSED PRODUCT`, not measured outcome.

---

# 2. Problem section — causal leap

Current sentence:

> "A meaningful part of the campus sustainability challenge therefore sits before composting or recovery: how much food should be prepared..."

## Issue

The word `therefore` overstates what the 48,251 kg baseline proves.

Current evidence establishes:

- total published food waste;
- service scale;
- central production context;
- analogous Turkish contracts where demand/quantity uncertainty is operationally material.

It does **not** establish:

- how much Boğaziçi waste is edible overproduction;
- whether quantity planning is the dominant cause;
- whether the quantity decision can be changed.

## Safer research logic

```text
public waste baseline
+
production-demand mechanism exists in comparable institutional dining
+
Boğaziçi has central/contracted high-volume service
        ↓
production planning is a high-value hypothesis to test
```

not:

```text
public waste baseline
        ↓
production mismatch caused a meaningful share
```

---

# 3. "Today the operational decision can be made with incomplete context"

## Issue

This is a PMR claim currently phrased as fact.

We do not yet know:

- who makes it;
- which data they use;
- whether context is incomplete;
- whether a specialist system already exists;
- when the decision freezes.

## Correct label

`HYPOTHESIS` until interview evidence.

---

# 4. Solution loop — mostly defensible as design

The following are valid **repo/product-design claims**:

- planning band rather than one magic number;
- `PILOT_READY / REVIEW_REQUIRED / WITHHOLD` states;
- operator approval;
- claim firewall;
- matched-pilot protocol;
- normalized outcome metric;
- failure allowed.

These are supported as repo artifacts (`E-REP-001`–`E-REP-004`).

## Boundary

Do not turn the fact that the software implements these controls into a claim that operators value them.

Human review, WITHHOLD, explanation and evidence provenance remain **adoption hypotheses**.

---

# 5. Climate-tech section — prevention framing is strong, causal target remains hypothesis

EPA/UNEP support prevention/source reduction as environmentally preferable to managing food after it becomes waste.

Useful sources:

- https://www.epa.gov/sustainable-management-food/wasted-food-scale
- https://www.epa.gov/sustainable-management-food/prevent-wasted-food-through-source-reduction
- https://www.unep.org/resources/publication/food-waste-index-report-2024

## Safe

> The proposed intervention acts before waste is created and should be evaluated on measured food reduction before climate conversions.

## Not safe yet

> BOUNCAMPUS currently prevents Boğaziçi waste.

---

# 6. Innovation section — direction is strong, novelty wording still needs discipline

Current pack already says the novelty is **not** another dashboard or complex forecasting model. This is aligned with competitor research.

However even:

> "closed-loop decision and evidence contract"

should be presented as the product's **design differentiation**, not an unqualified market-first claim.

Current public research does not prove competitors cannot implement similar loops.

## Safe language class

> "We are designing the product around..."

> "Our differentiation hypothesis is..."

Avoid:

> "No other system..."

unless comparative product evidence exists.

---

# 7. Current evidence section — public monthly waste history needs reconciliation warning

The pack lists:

> `2025 monthly food-waste/recovery history`

as current evidence.

That is true as **published history**, but the October 4 reconciliation found an important semantic inconsistency: some monthly İSTAÇ-delivery values exceed the same month's published total although the page says the former is included in the latter.

See:

`KREATE/RESEARCH/BOGAZICI_SOURCE_RECONCILIATION_2026-10-04.md`

## Application implication

Use the **annual 48,251 kg total** as the clean opening fact.

Avoid deriving monthly recovery ratios or causal trends until source semantics are resolved.

---

# 8. Pilot design — valid falsification plan, not statistical proof

The pack states:

- 14 days;
- matched CONTROL vs INTERVENTION;
- minimum 5 services/arm;
- 10% target;
- sellout and safety guardrails.

This is good pre-registration discipline.

## Risk

`controlled pilot` can be read as a sufficiently powered controlled experiment.

The research standard now explicitly distinguishes:

- hackathon promotion gate;
- preliminary matched operational evidence;
- statistically/generalizably validated effect.

See:

`KREATE/RESEARCH/PILOT_MEASUREMENT_AND_EVIDENCE_STANDARD_2026-10-04.md`

## Safe description

> bounded matched pilot / preliminary field evaluation

until sample size/design justifies stronger causal language.

---

# 9. Technical approach — exact signal weights are policy heuristics

Current pack says:

```text
course schedule: 50%
weather: 20%
menu: 20%
academic calendar: 10%
```

## Risk

A judge can reasonably ask:

> Why 50/20/20/10?

There is no measured Boğaziçi target dataset showing these are empirical feature importances.

## Correct classification

`POLICY HEURISTIC / DEMO POLICY`

not:

`validated model weights`.

## Research recommendation

Externally, emphasize:

- baseline-first modeling;
- feature availability/readiness;
- future ablation on real data;
- simple baseline must be beaten before richer model promotion.

If the exact weights are shown, label them explicitly as a transparent demo heuristic pending calibration.

---

# 10. "Course schedule is the backbone signal" — too strong

## Current evidence

Academic/calendar state can be predictive context and is publicly available.

## Missing evidence

No real Boğaziçi service-level demand dataset has established that course schedule contributes more predictive value than:

- recent meal counts;
- reservation/intent;
- turnstile history;
- menu;
- service regime;
- weather;
- event context.

## Rule

Schedule != occupancy != dining attendance.

Describe course schedule as a **candidate context signal**, not validated demand backbone.

---

# 11. Target users — current list is too broad

Current list:

- dining-service operations;
- sustainability offices;
- campus facility/operations teams.

## Problem

This reads like multiple unrelated personas.

Research now points toward one primary persona family:

> **the operational owner of the meal production/allocation quantity under uncertain demand.**

Possible actual role:

- Food Services manager;
- cafeteria manager/director;
- food engineer/production planner;
- contractor project/production manager.

Secondary DMU roles:

- economic buyer;
- data owner;
- sustainability champion;
- senior approver.

## Application implication

Use one primary persona. Mention other stakeholders only as the decision-making unit.

---

# 12. Scalability — institutional kitchens first is stronger than campus-everything

The pack's portability to other institutional kitchens is more defensible than immediate cross-domain campus claims because the core job is more similar:

```text
forecast/release institutional meal quantity
-> serve
-> measure surplus/shortage
```

Candidate adjacent markets:

- hospitals;
- factory/staff cafeterias;
- schools;
- municipal kitchens;
- catering operators.

Campus energy/mobility/water/space remain plausible architecture expansions but require separate customer discovery.

See:

`KREATE/RESEARCH/CAMPUS_EXPANSION_DECISION_MAP_2026-10-04.md`

---

# 13. "Why can win KREATE" — separate fact from team judgement

Current claim:

> real, quantified climate problem backed by institution's own data.

This is safe if `problem` means **food waste exists at scale**.

It is unsafe if interpreted as:

> production mismatch has been quantified as the cause.

Recommended internal distinction:

```text
quantified outcome problem = YES
validated root cause = NO
proposed intervention = TESTING
```

---

# 14. 15-second answer audit

Current:

> "starts from a real 48-ton food-waste baseline..."

Strong.

> "turns campus context into an uncertainty-aware production band..."

Valid as current product behavior if model/demo estimate is clearly labeled.

> "decision layer before the waste happens"

Valid as proposed intervention timing, but actual decision owner/freeze point remains PMR unknown.

No achieved-saving language appears; retain this discipline.

---

# 15. 45-second answer audit

Strong points:

- official 48,251 kg baseline;
- human control;
- WITHHOLD;
- pilot target not result;
- normalized waste + sellout guardrail.

Main correction needed:

> "We focus on a decision made before that waste exists: how much should be prepared..."

This should be framed as the **decision we are testing as the first control point**, not a verified description of current Boğaziçi workflow.

---

# 16. Judge-answer audit

## "Is this just forecasting?"

Good answer direction. Add that forecasting itself is a mature category; BOUNCAMPUS only earns its place if the surrounding university workflow creates incremental value.

## "Why not last week's meal count?"

Strong answer. Preserve. A simple baseline must be allowed to win.

## "Where is the AI?"

Current answer risks defending complexity. Better research framing:

> complexity is conditional; first prove that context beats transparent baselines.

## "Why human?"

Strong and evidence-disciplined.

## "What if APIs fail?"

Strong as technical safety behavior, but do not imply currently authorized production APIs exist.

## "What proves you wrong?"

Add earlier business falsifiers:

- quantity cannot be changed;
- production mismatch not material;
- wrong persona/buyer;
- data too costly/inaccessible;
- incumbent sufficiently solves the problem.

A model failing a 10% gate is only one way the company thesis can be wrong.

---

# 17. Submission-safe claim stack

## FACT / PUBLIC SOURCE

- Boğaziçi reports 48,251 kg 2025 food waste.
- large multi-campus dining operation exists.
- North Campus central-kitchen context exists.
- current formal contractor relationship exists.
- comparable Turkish university contracts demonstrate meal-demand/quantity uncertainty can be operationally and contractually material.
- UI GreenMetric/YÖK increase institutional digital-sustainability context.

## REPO FACT

- human-reviewed recommendation policy exists;
- WITHHOLD/readiness design exists;
- pilot protocol exists;
- no automatic kitchen dispatch;
- claim firewall exists.

## HYPOTHESIS / PMR

- Boğaziçi demand mismatch is a material cause of avoidable surplus;
- exact quantity decision is reachable;
- safety buffer exists and is painful;
- operator values planning bands/uncertainty;
- data can be accessed with acceptable effort;
- university or contractor will sponsor/pay;
- same workflow repeats across beachhead.

## FUTURE MEASURED RESULT

- waste reduction;
- shortage change;
- cost savings;
- CO2e/water effects;
- model performance on actual operational data.

---

# 18. Research recommendation before submission

The application should be frozen only after:

1. real PMR interview records replace at least some of the core unknowns;
2. every causal/persona statement is re-labelled against `EVIDENCE.md`;
3. exact demo signal weights are labelled heuristic or removed from market-facing narrative;
4. primary persona is narrowed;
5. small-pilot language does not imply statistical proof;
6. competitor novelty claims are checked against the October 4 matrix;
7. source-reconciliation conflicts are not used as model facts.
