# Buyer Economics & Procurement Route — 2026-10-04

**Status:** Secondary/public-source research. **Boğaziçi daily settlement economics remain UNKNOWN until the active contract/specification or direct PMR resolves them.**

## Executive conclusion

The core commercial risk is not whether forecasting can reduce production error in principle. It is whether the actor who can change quantity also captures enough operational/economic value to adopt BOUNCAMPUS.

Comparable Turkish university procurements show that daily meal planning can place risk/value on different parties:

```text
university defines quantity
contractor produces
actual consumption measured electronically
excess risk may sit with contractor
```

or

```text
contractor forecasts quantity
contractor bears shortage/excess exposure
actual consumption drives payment
```

Therefore the economic buyer cannot be inferred from the phrase `university dining`.

---

# 1. Boğaziçi current procurement — what is public

Current procurement IKN: `2025/1727143`.

Public result/notice sources show:

- 2026–2027 service term;
- six Boğaziçi campuses;
- 2,500,000 student-meal units;
- 380,000 breakfast/sahur units;
- 250,000 staff-meal units;
- 3,130,000 listed meal units total;
- winning contractor TEMAŞ Gıda;
- contract value 759,537,563.59 TRY;
- open procurement under Law 4734.

Sources:

- https://ekapveri.com/ihale/ekap-2025-1727143/
- https://www.ihaledetay.com/2025-1727143

## Publicly unresolved

The indexed result does **not** establish:

- daily quantity instruction process;
- whether payment is based on requested, produced, delivered, accepted or actually served meals;
- whether electronic turnstile/BUCard count is a settlement basis;
- who absorbs ingredient/labor cost of unnecessary production;
- shortage penalties or emergency replenishment requirements;
- whether the university or contractor controls batch-level adjustments;
- whether pilot-generated recommendations could legally/operationally affect contracted quantity.

### Rule

Do not infer Boğaziçi unit economics by dividing contract value by meal units and calling that `waste cost per meal`.

The contract includes service, labor, materials, inflation/risk and other obligations; marginal avoidable production cost is not equal to contract unit price without evidence.

---

# 2. Comparable mechanism A — university determines quantity, electronic realized demand drives payment

İzmir Katip Çelebi University decision `2025/UH.II-2367` reproduces a workflow where expected daily production uses reservation information plus expected guests/walk-ins. The administration determines the daily quantity and the contractor produces it. Electronic-card/turnstile passage is used to determine the daily diner count for payment, while excess-production risk is not shifted to the administration.

Source:
https://herpoz.com/kamu-ihale-kararlari/2025UH.II-2367-kamu-ihale-karari-kik

### Commercial implication

Potential roles:

```text
end user / quantity owner = university operations
production executor = contractor
realized-demand evidence = turnstile
excess-cost exposure = contractor-side at least in part
```

This creates possible incentive misalignment: the actor specifying quantity and the actor absorbing excess may not be the same party.

---

# 3. Comparable mechanism B — contractor forecasts and bears forecast risk

Kırıkkale University decision `2026/UH.I-2269` states that the contractor is expected to determine daily quantities using previous meal counts. Payment is tied to meals actually eaten, insufficient production can lead to penalties, and the administration does not bear responsibility for leftover food.

Official KIK source:
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=0b6db2bdc4dcba60ddf7cb70334f72bf03b482e26ad51295bd12345ea082c52b

### Commercial implication

Potential structure:

```text
end user = contractor production planner/project operator
champion = contractor operations manager
primary economic beneficiary = contractor
university = service-quality / oversight stakeholder
```

If Boğaziçi resembles this model, a university-only SaaS GTM thesis may be wrong even when the technical problem is real.

---

# 4. Comparable mechanism C — actual electronic consumption as settlement evidence

İTÜ decision `2026/UH.II-740` describes cafeteria automation/turnstile records being jointly confirmed by administration and contractor and used in payment determination.

Source:
https://herpoz.com/kamu-ihale-kararlari/2026UH.II-740-kamu-ihale-karari-kik

The same procurement includes operational requirements around additional food when service is at risk of running out.

### Commercial implication

A contract can contain both:

- a measurable realized-demand signal;
- a service-continuity obligation.

This is structurally aligned with BOUNCAMPUS's proposed dual objective:

```text
reduce avoidable surplus
subject to shortage / service guardrail
```

But it is not evidence that İTÜ wants BOUNCAMPUS.

---

# 5. Comparable mechanism D — forecast uncertainty can be procurement-material

Gebze Technical University decision `2026/UH.II-962` describes a specification where the university would not provide daily student meal counts in advance and the contractor would determine quantities by estimation. The Board found the absence of sufficient daily distribution/reference information material to healthy bid preparation.

Source:
https://herpoz.com/kamu-ihale-kararlari/2026UH.II-962-kamu-ihale-karari-kik

### Commercial implication

Demand/reference uncertainty is not merely an analytics inconvenience; in some institutional contracts it is material enough to affect bidder risk.

This supports the mechanism class, not willingness to pay.

---

# 6. Buyer-economics scenarios for Boğaziçi PMR

Do not choose one until evidence exists.

## Scenario A — university bears marginal excess cost

Possible product route:

- university/SKS economic buyer;
- contractor/operator as end user or implementer;
- waste reduction creates direct budget value for university.

Need to prove:

- payment/acceptance semantics;
- avoidable cost actually changes with production quantity;
- university can change the production plan.

## Scenario B — contractor bears marginal excess cost

Possible product route:

- contractor as economic buyer / major champion;
- university as approver/data partner/service-quality stakeholder.

Need to prove:

- contractor can retain savings;
- no contract mechanism neutralizes the savings;
- contractor has decision authority.

## Scenario C — university specifies quantity, contractor bears excess

This creates split incentives.

Possible product requirements:

- shared decision audit trail;
- recommendation visible to both parties;
- evidence explaining who approved a quantity;
- pilot agreement that defines outcome ownership.

Sales can be harder because the actor with authority and actor with economic pain differ.

## Scenario D — payment largely fixed / quantity savings do not change near-term economics

Then immediate value may shift toward:

- sustainability target;
- contractor performance/risk;
- service quality;
- future procurement specification;
- waste-disposal burden.

If none is compelling, the commercial wedge may be weak despite environmental relevance.

---

# 7. Economic-value questions that must be answered in PMR

For each institution:

1. Which number determines what the contractor is paid for?
2. Who decides the first production quantity?
3. Who can revise it?
4. Who pays for ingredients/labor associated with unused production?
5. What happens to unserved edible surplus?
6. What happens contractually when food runs out?
7. Are there penalties, complaints, emergency production, substitution or other shortage costs?
8. Which party's P&L/budget changes if 100 unnecessary portions are avoided?
9. Does waste disposal/recovery create a measurable cost?
10. Who owns the budget for software/pilot/integration?
11. Can a bounded pilot be approved separately from a full service procurement?
12. What procurement/security/legal step can veto the pilot?

---

# 8. Do not confuse four economic quantities

Keep distinct:

```text
contract_unit_price
marginal_food_input_cost
marginal_operational_cost
avoidable_waste_cost
```

They are not interchangeable.

Also keep distinct:

```text
financial savings
avoided food mass
avoided environmental impact
reported sustainability value
```

Climate and water conversions require separate documented factors after measured physical reduction.

---

# 9. Economic-buyer promotion gate

Do not name a primary economic buyer in application copy as validated until a real stakeholder confirms:

```text
budget authority
+ captured benefit / avoided risk
+ pilot approval path
+ willingness to allocate resources
```

A person who likes the concept or uses the tool is not necessarily the buyer.

---

# 10. Commercial research outcome

The strongest current commercial hypothesis is not:

> `universities will pay for AI food-waste software`

It is:

> **Within a subset of high-volume institutional dining contracts, forecast error creates measurable excess/shortage exposure for a reachable operator or sponsor; if BOUNCAMPUS improves that decision before the freeze point and proves the result, one of the parties may have a compelling operational/economic reason to adopt.**

Every clause after `if` remains to be tested through PMR/pilot evidence.
