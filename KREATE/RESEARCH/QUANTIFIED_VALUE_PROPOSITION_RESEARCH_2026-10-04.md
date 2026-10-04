# Quantified Value Proposition Research — 2026-10-04

**Method:** Disciplined Entrepreneurship Step 8 — https://www.d-eship.com/step8/  
**Status:** value-hypothesis design only. **No measured BOUNCAMPUS customer value exists yet.**

## Executive conclusion

BOUNCAMPUS should not lock its primary value proposition to `reduce food waste by X%` before the real Persona's highest-priority outcome is known.

Disciplined Entrepreneurship requires:

1. identify the Persona's #1 priority;
2. agree how that priority is measured;
3. map the customer's current `as-is` state in the same units;
4. describe the possible future state in those same units;
5. avoid aggressive promises before evidence.

For BOUNCAMPUS, the value currency may differ by DMU role.

---

# 1. Candidate value currencies by role

## Operational end user

Possible #1 priority:

```text
service continuity / avoiding operational failure
```

Candidate units:

- early-sellout events per 100 services;
- minutes of emergency replenishment/service delay;
- emergency substitutions per month;
- operator overrides/escalations;
- planning time per service;
- forecast/quantity revisions after commitment.

### Hypothesis

The operator may care more about avoiding visible service failure than about the absolute kilograms of waste.

This is consistent with the working asymmetric-risk hypothesis but must be validated behaviorally.

---

# 2. Food Services / university operations owner

Possible priorities:

- reliable service;
- lower avoidable surplus;
- better contractor oversight;
- lower operational friction;
- measurable sustainability performance.

Candidate units:

```text
edible_surplus_kg_per_100_served
early_sellout_rate
complaint/escalation count
manual reconciliation hours/month
services with documented decision/outcome chain
```

Do not assume monetary savings are the top priority until contract economics are known.

---

# 3. Contractor economic buyer

If the contractor bears marginal excess-production cost, possible value currencies include:

- avoidable ingredient cost;
- excess prepared portions;
- emergency production/replenishment cost;
- labor/time associated with corrections;
- penalty/service-risk exposure.

Candidate future QVP structure:

```text
as-is avoidable production cost per month
        ->
post-intervention avoidable production cost per month
```

But this cannot be calculated from Boğaziçi's contract total or average meal price.

Required data:

- actual marginal input cost or credible internal food-cost accounting;
- production/served/surplus records;
- shortage penalties or emergency response cost;
- who retains savings.

---

# 4. Sustainability champion

Possible priority:

```text
credible measured prevention rather than retrospective reporting
```

Candidate units:

- edible surplus kg avoided under a defensible measurement protocol;
- percentage of dining services with stage-specific waste measurement;
- evidence completeness / traceability;
- later derived CO2e/water estimate with documented factors.

### Boundary

This role may value the output but may not be the end user or economic buyer.

---

# 5. Why `10% waste reduction` is not yet the QVP

The repository currently uses a 10% lower normalized-waste threshold as a **pilot target**.

That target is useful for falsifiable experiment design.

It is not yet evidence that:

- the Persona's top priority is waste percentage;
- 10% is commercially meaningful;
- the product can achieve 10%;
- the operator would accept the associated service-risk tradeoff;
- the economic buyer would pay for that result.

Keep:

```text
10% = pre-registered pilot target
```

Do not silently promote to:

```text
10% = customer value proposition / expected saving
```

---

# 6. External benchmarks are context, not BOUNCAMPUS promises

Current commercial and academic sources report large ranges of effects in other contexts.

Examples include:

- Winnow university/commercial marketing claims food-cost reductions in the low-single-digit percentage range from cutting avoidable waste;
- Leanpath publishes individual university/operator case studies with substantial waste reductions;
- academic catering-demand studies report scenario/case-specific reductions in wasted meals or unmet demand.

These results demonstrate that operational value can be material, but their:

- baseline;
- intervention;
- customer type;
- waste definition;
- measurement period;
- pricing/cost structure;

are different.

Therefore they should be used for competitor/context research, not as BOUNCAMPUS expected performance.

Sources already tracked elsewhere:

- https://www.winnowsolutions.com/industries/universities
- https://www.leanpath.com/industries/college-university/
- `ACADEMIC_DEMAND_MODELING_EVIDENCE_2026-10-04.md`

---

# 7. QVP interview sequence

Only after the workflow and real Persona are identified:

## Step 1 — identify top priority through behavior

Ask:

- What result are you personally accountable for in meal service?
- What failure gets escalated fastest?
- What metric is reviewed with your manager/contractor?
- Which recent problem consumed the most time/money/attention?
- If you could improve only one outcome in this process, what would it be?

## Step 2 — quantify the as-is state

Ask for real recent records/examples:

- How often does this happen?
- What does one incident cost in time/material/service disruption?
- How many services/month are affected?
- What number do you currently track?
- Can we inspect the data definition?

## Step 3 — test conservative future state

Do not ask:

> Would 30% improvement be exciting?

Instead ask:

> If this metric moved from the current observed level to [conservative evidence-based possible level], what operational decision would change and who would care?

Until measured pilot data exist, keep future-state numbers as targets/scenarios.

---

# 8. Candidate QVPs by Persona outcome

These are templates, not claims.

## Reliability-first Persona

> Reduce avoidable overproduction **without increasing early-sellout rate**, measured service by service.

Quantification:

```text
waste/surplus metric
subject to sellout guardrail
```

## Time/friction-first Persona

> Reduce manual planning/reconciliation effort while preserving service quality.

Quantification:

```text
operator minutes/service
manual spreadsheet/reconciliation steps
```

## Cost-first contractor

> Reduce marginal cost of unnecessary production without increasing shortage penalties/emergency production.

Quantification:

```text
TRY avoidable cost/service or month
subject to shortage/service guardrail
```

## Sustainability-first champion

> Convert dining prevention from annual aggregate reporting into service-level measured intervention evidence.

Quantification:

```text
measured edible-surplus reduction
+ evidence coverage / provenance
```

---

# 9. Value creation and value capture are different

A reduction can create value for one actor while another controls payment.

Example split-incentive structure:

```text
university chooses quantity
contractor absorbs excess
sustainability office values waste reduction
procurement controls purchase
```

This is why the QVP must be paired with the DMU and buyer-economics research.

A strong end-user value proposition does not prove a viable business model.

---

# 10. Minimum evidence required before monetary ROI

Do not publish BOUNCAMPUS ROI until all of the following are known:

1. real Persona / buyer;
2. as-is metric baseline;
3. real marginal cost semantics;
4. measured intervention effect;
5. implementation/support cost;
6. who captures the benefit;
7. period over which savings persist;
8. additional risk/service costs.

A safe pre-pilot ROI statement is:

> `Economic value will be evaluated only after the contract/payment and marginal-cost structure is established.`

---

# 11. Current best application value language

Before PMR/pilot, prefer:

> **BOUNCAMPUS is designed to help operators reduce avoidable overproduction while protecting service continuity, and to make the result measurable.**

This is stronger and safer than:

> `BOUNCAMPUS saves universities X% of food cost.`

---

# 12. Research promotion gate

A QVP becomes application-ready when a real Persona can confirm:

```text
priority
+ metric/unit
+ current as-is value
+ why that value matters
+ conservative desired change
```

and later pilot evidence shows the product can move the metric.

Until then the QVP remains a hypothesis, not a customer result.
