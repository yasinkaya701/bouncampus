# KREATE for Climate — BOUNCAMPUS Application Pack

## One-line product

**BOUNCAMPUS is testing whether a human-reviewed, evidence-traceable decision layer can improve a reachable pre-service institutional dining decision and reduce avoidable food waste without increasing service risk.**

## Problem

Boğaziçi University publicly reports **48,251 kg of food waste for 2025**. That establishes a real institutional food-waste baseline, but it does **not** establish why the waste occurred or which intervention point is most important.

Our current hypothesis is narrower: some avoidable waste may be linked to decisions made before service, such as production quantity, batch release or campus allocation, when actual demand is still uncertain. We are actively testing whether such a decision is reachable, when it freezes, who controls it, and whether demand mismatch is material compared with alternatives such as plate waste, menu/quality effects, preparation loss or other operational causes.

## Solution hypothesis

BOUNCAMPUS is being developed as a food-waste prevention decision-and-evidence layer for institutional dining operations.

The current product contract is:

1. **Context and source health** — only use signals whose provenance and timing are known.
2. **Reachable decision** — target a quantity/batch/allocation decision only if PMR shows it can still be changed before a practical freeze point.
3. **Transparent baseline** — compare against the operator/status-quo heuristic and simple reproducible baselines before adding model complexity.
4. **Bounded recommendation** — expose uncertainty and service-risk tradeoffs rather than a false single-number certainty.
5. **Human gate** — an operator approves, modifies or rejects the recommendation; automatic kitchen dispatch is disabled.
6. **Prospective measurement** — measure the relevant outcome at service level with explicit waste-stage and shortage guardrails.
7. **Claim firewall** — only measured local evidence may support local impact claims.
8. **Learn / modify / kill** — if the hypothesized control point or causal mechanism is wrong, the product changes with the evidence.

## Why it can become climate tech

Food waste embeds agricultural inputs, water, energy, logistics and disposal impacts. Prevention can therefore have climate relevance, but the causal chain has to be earned:

reachable operational decision → less avoidable excess → measured waste reduction → transparent impact conversion

BOUNCAMPUS does **not** currently claim local CO2, water or cost savings. Climate accounting comes only after local operational effect is measured.

## Innovation / differentiation hypothesis

The defensible current wedge is **not** “AI predicts cafeteria demand,” generic food-waste tracking, computer vision, or another sustainability dashboard. Those capability classes already exist in research and commercial products.

The working differentiation hypothesis is the **decision-and-verification contract**:

- only decision-time-valid signals are admitted;
- signal semantics are reconciled against operational truth;
- uncertainty can force WITHHOLD;
- human approval is mandatory;
- the current operator baseline remains visible;
- surplus and shortage are measured together;
- evidence quality controls what claims can be promoted;
- a pilot can fail and force a product change.

Whether this workflow is valuable enough to adopt is still a PMR question.

## Current evidence

### What is real now

- official Boğaziçi public food-waste reporting, including the 2025 annual total;
- public dining-service, menu, calendar and procurement context;
- a current public food-service contractor/procurement surface;
- repository implementations for decision readiness, abstention/human review, baselines and pilot-evidence handling;
- a falsifiable pilot protocol and explicit claim/evidence boundaries;
- a cumulative PMR/source registry that distinguishes secondary research from real primary evidence.

### What remains unverified / blocked

- whether demand mismatch is a material cause of avoidable Boğaziçi food waste;
- the exact operational quantity/batch/allocation owner and freeze point;
- service-level produced/served/surplus/waste truth and its semantics;
- whether BUCard/turnstile/reservation signals can be exported and reconciled safely;
- contractor/payment/hakediş incentive mechanics;
- operator willingness to act on a recommendation;
- any local waste-reduction, cost, carbon or water impact;
- repeatability of the same product workflow at a second site.

## Proposed pilot design

The repository contains a **proposed**, falsifiable pilot design. It is not evidence that a pilot has occurred.

**Illustrative duration:** 14 days  
**Design:** matched CONTROL vs INTERVENTION services  
**Primary KPI:** waste kg / 100 served meals, if the served-meal denominator and waste boundary are verified  
**Minimum evidence concept:** at least 5 measured services per arm  
**Illustrative pre-registered target:** at least 10% lower normalized waste in INTERVENTION vs CONTROL  
**Service guardrail:** early-sellout incidence must not increase  
**Safety guardrail:** no food-safety process may be bypassed  
**Privacy:** prefer aggregate service-level data; no personal/student-level data is required for the intended analysis

The 10% figure is a **pilot target / protocol parameter, not an achieved or expected result**.

## Why normalize by served meals?

If served-meal semantics are verified, normalization can reduce service-volume confounding: a low-attendance day may show fewer kilograms of waste without any operational improvement. Until the denominator is reconciled, the metric remains a proposed measurement contract rather than a validated local KPI.

## Technical approach

The repository currently contains a transparent policy-heuristic prototype using candidate context classes such as:

- course schedule,
- weather,
- menu context,
- academic calendar.

Any existing fixed signal weights are **policy heuristics for prototype behavior**, not learned causal importance and not evidence of local predictive value.

After admitted real service labels exist, CS1 should evaluate in this order:

operator/status-quo baseline → reproducible naive baseline → timing-safe single-signal ablations → richer model only if it clears the registered decision-loss gate

Forecast accuracy is not the product KPI by itself. Decision utility, coverage, overrides, shortage risk and physical outcome matter.

## Target user hypothesis

The current user/persona hypothesis is an institutional dining role that can actually change or approve the relevant pre-service decision.

Candidate stakeholders include:
- Food Services / dining operations,
- contractor production or local operations,
- operational data / acceptance owners,
- procurement or pilot approvers.

“Sustainability office” alone is not treated as the validated operational persona. The actual user, influencer, buyer and veto roles remain to be established through PMR.

## Beachhead / scalability hypothesis

Boğaziçi is the current learning environment, not automatically a validated market segment.

The institutional-dining beachhead becomes defensible only if:
1. a reachable control point is confirmed;
2. the problem is material and repeated;
3. the buyer/approval path is coherent;
4. the same product boundary repeats at another site.

Expansion to other universities or institutional kitchens is therefore a **repeatability hypothesis**, not a current scalability fact.

## Why this can be a strong KREATE project

The current strength is not a fabricated claim of market validation. It is the combination of:

1. **A real public institutional baseline** that justifies investigation.
2. **A falsifiable product thesis** with explicit kill/modify conditions.
3. **A working technical prototype** whose limitations are visible.
4. **Human control and abstention** rather than pretending an unvalidated model should automate production.
5. **An evidence discipline** that keeps public sources, PMR, technical tests, model outputs and measured impact separate.

The project becomes materially stronger only as primary evidence closes the current unknowns.

## What we want from the accelerator

The next milestones are:

1. reconstruct one real service from initial planning through final outcome;
2. verify the actual decision owner, freeze point and revision rights;
3. obtain privacy-safe service-level truth or establish a minimal prospective measurement path;
4. resolve current contract/acceptance/hakediş mechanics and the economic beneficiary;
5. benchmark the operator/status-quo heuristic before richer modeling;
6. run a bounded shadow/advisory pilot only after data and workflow gates are satisfied;
7. measure surplus and shortage together;
8. calculate climate impact only after local waste reduction is measured;
9. test the same product boundary at a second institutional site.

## 15-second answer

> Boğaziçi publicly reports 48,251 kilograms of food waste for 2025. We are testing a narrower question: is there a reachable pre-service dining decision where better, semantically verified context can reduce avoidable excess without increasing shortages? BOUNCAMPUS keeps the operator in control and only promotes claims after prospective measurement.

## 45-second answer

> Boğaziçi University publicly reported 48,251 kilograms of food waste in 2025, but that number does not tell us the cause. Our current hypothesis is that part of avoidable waste may be linked to a reachable pre-service production, batch or allocation decision. BOUNCAMPUS is designed to combine only decision-time-valid signals, compare against simple operator baselines, expose uncertainty, and let a human approve or reject the recommendation. The important part is the evidence loop: we want to measure surplus and shortage prospectively and change or kill the product thesis if the control point or causal mechanism is wrong. We are not claiming local savings or model impact before that evidence exists.

## Common judge questions

### “Is this just forecasting?”
No. Generic forecasting already exists. Our hypothesis is that value comes from integrating a reachable decision, reconciled operational truth, a baseline, human approval, prospective outcome measurement and a strict evidence gate. PMR still has to prove that workflow matters locally.

### “Why not just use last week's meal count?”
That may be the best baseline. We will not add model complexity unless timing-safe context improves decision utility against the operator/status-quo and simple baselines without increasing service risk.

### “Where is the AI?”
The current repository contains transparent decision logic and candidate contextual signals. We are deliberately not presenting an unvalidated black-box model as production-ready. Richer ML is downstream of real chronological service labels and a baseline it must beat.

### “Why do you need a human?”
Because the operational and causal assumptions are still being tested, and shortage/food-safety/contract constraints matter. Human approval is part of the intended operating contract.

### “Do BUCard or turnstile counts give you actual demand?”
Not yet. They are candidate aggregate signals whose event semantics, corrections, duplicates, refunds, second-meal handling and relation to physically served meals must be reconciled with the source owner before they can become labels.

### “Have you already reduced waste by 10%?”
No. Ten percent appears only as an illustrative pre-registered pilot target in the current protocol. It is not an achieved or expected result.

### “Does the contractor save money if production falls?”
Unknown. We need authoritative acceptance/hakediş and cost-responsibility evidence before making that claim.

### “How do you stop the model gaming waste by underproducing?”
Any pilot must measure shortage/early-sellout alongside waste. A lower waste number is not success if service deteriorates.

### “What would prove you wrong?”
Any of these would force a material change: no reachable control point; demand mismatch is not a material cause; reliable outcome truth is unavailable at acceptable burden; operators cannot safely act before freeze; the current baseline is already good enough; or prospective measurement shows no useful improvement or worse service.

### “Why should this scale beyond Boğaziçi?”
We are not claiming that yet. We need at least one second-site reconstruction showing the same owner/freeze/signal/action/buyer topology. If that topology differs materially, we should segment more narrowly instead of claiming broad institutional portability.
