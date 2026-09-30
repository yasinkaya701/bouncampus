# Boğaziçi Procurement Cost Denominator Warning

**Research date:** 2026-10-01  
**Purpose:** Prevent agents from dividing the current dining contract value by the three headline meal quantities and presenting the result as a current meal cost, savings rate or marginal waste value.  
**Status:** Secondary public-source research. **NOT a winning unit-price bid schedule. NOT hakediş evidence.**

---

# 0. Executive conclusion

The current 2026–2027 procurement publicly lists three headline meal quantities:

- 2,500,000 student meals;
- 380,000 breakfasts including sahur;
- 250,000 staff meals.

But a public tender-index page labels the procurement as having **15 bid-schedule (`İhale Cetveli`) items**, and its rendered schedule shows the three meal rows plus multiple rows measured in **months (`Ay`)**.

Sources:

- https://www.ihaletakip.com.tr/ihale/2026-2027-yili-01-01-2026-31-12-2027-malzeme-dahil-kahvalti-yemek-hazirlama-ve-dagitim-hizmeti-alimi/4374218/
- https://www.ihaledetay.com/2025-1727143

The open-web parser does not expose the month-based row descriptions reliably enough to name them. Therefore do **not** infer whether they are labour, management, equipment, service-support or another category.

What can safely be said is narrower:

> The procurement schedule appears to contain more priced/quantity rows than the three headline meal categories, so the total contract value is not safely interpretable as a pure three-meal-line cost pool from public summary data alone.

---

# 1. The tempting calculation is not a defensible cost metric

Current contract value:

```text
759,537,563.59 TRY
```

Headline meal quantity:

```text
2,500,000 + 380,000 + 250,000 = 3,130,000 meal units
```

A mechanical division would produce a blended figure of roughly:

```text
759,537,563.59 / 3,130,000 ≈ 242.66 TRY per headline meal unit
```

This arithmetic is mathematically correct but the **economic interpretation is not established**.

Do not label `242.66 TRY` as:

- current student-meal cost;
- current average meal production cost;
- contractor variable cost;
- marginal cost of one additional meal;
- amount saved by preventing one excess meal;
- current university subsidy per meal;
- current hakediş unit price.

Reasons:

1. breakfast, student meal and staff meal almost certainly do not have identical economic structures;
2. the public tender schedule reports 15 items, not only the three headline meal rows;
3. month-based rows are present in the rendered schedule, with descriptions unresolved in the public parser;
4. price adjustment is provided in the procurement;
5. actual payment depends on current settlement/hakediş semantics that remain unverified;
6. fixed and variable cost components may differ materially.

---

# 2. This strengthens the existing economic claim firewall

The repository already separates:

```text
DINER PRICE
!= PROCUREMENT / SERVICE COST
!= CONTRACTOR MARGINAL COST
!= CONTRACT ACCEPTED / HAKEDİŞ VALUE
```

Add another distinction:

```text
TOTAL CONTRACT VALUE / HEADLINE MEAL COUNT
!= VERIFIED MEAL UNIT PRICE
```

The blended quotient can be stored only as a **derived procurement-scale ratio** if there is a specific analytical reason, with a warning that it is not an operational cost metric.

For most KREATE application and pilot work, it is better not to use it at all.

---

# 3. P0 artifact request becomes more specific

Instead of asking vaguely for “cost per meal,” request the minimum current documents/fields needed to separate components:

```text
WINNING_UNIT_PRICE_BID_SCHEDULE
LINE_ITEM_ID
LINE_ITEM_DESCRIPTION
UNIT
CONTRACT_QUANTITY
AWARDED_UNIT_PRICE
PRICE_ADJUSTMENT_RULE_OR_INDEX
ACTUAL_ACCEPTED_QUANTITY
HAKEDIS_QUANTITY
```

If the full bid schedule cannot be shared, ask the contract/budget owner to confirm only:

1. whether meal line items and month-based service items are priced separately;
2. current awarded unit prices for the relevant pilot meal class, if releasable;
3. which line-item quantity drives monthly payment;
4. whether a reduced produced quantity changes the payable amount;
5. which cost components are fixed regardless of quantity.

---

# 4. Model economics should separate fixed and variable components

Once verified, economic modeling should distinguish:

```text
FIXED_OR_TIME_BASED_COST
+ QUANTITY_LINKED_SETTLEMENT
+ CONTRACTOR_VARIABLE_INPUT_COST
+ WASTE_HANDLING_COST
+ SHORTAGE / SERVICE PENALTY
+ INTERVENTION_COST
```

A forecast/recommendation can only create direct financial value through components that actually change when the operational decision changes.

Therefore:

```text
avoided physical waste != automatically avoided contract spend
```

and:

```text
better demand forecast != automatically budget saving
```

---

# 5. Why this matters for buyer/persona research

Different economics imply different beneficiaries.

## University may value

- reduced payable quantity, if settlement is quantity-linked;
- reduced disposal/handling burden;
- sustainability outcomes;
- service reliability;
- budget predictability.

## Contractor may value

- lower unrecoverable ingredient/production cost;
- lower emergency-production cost;
- fewer shortage penalties;
- better labour/batch planning.

## Both may value

- fewer disputes/reconciliations;
- clearer operational evidence;
- improved allocation accuracy.

PMR must identify which of these actually moves under the current Boğaziçi–TEMAŞ contract.

---

# 6. Current evidence grade

## High-confidence public facts

- IKN `2025/1727143`;
- contract value `759,537,563.59 TRY`;
- headline quantities total `3,130,000` meal units;
- current contractor TEMAŞ;
- unit-price contract structure at procurement level;
- price adjustment is indicated;
- public tender-index page identifies **15 schedule items**;
- rendered schedule includes three meal rows and multiple `Ay`-unit rows.

## Still unknown

- descriptions of all month-based rows from a reliable current primary document;
- awarded unit price for each meal class;
- awarded price for each non-meal line;
- fixed vs variable economics;
- current accepted/hakediş quantity definition;
- how price adjustment changes realized payment;
- marginal avoidable cost of one excess meal.

---

# 7. Agent rule

If any application, dashboard or model code computes:

```text
contract_value / total_meals
```

and labels it `meal cost`, `cost saved per meal`, `subsidy`, `unit price` or equivalent, reject the claim unless a current verified contract/bid artifact proves that interpretation.

A safer field name, if the ratio must exist for an internal scale comparison, is:

```text
DERIVED_CONTRACT_VALUE_PER_HEADLINE_MEAL_UNIT
```

with:

```text
CLAIM_CLASS = DERIVED_CONTEXT_ONLY
NOT_FOR_SAVINGS_CALCULATION = true
```

---

# 8. Bottom line

The new public schedule evidence makes a simple conclusion stronger:

> **Do not monetize food-waste reduction from the headline contract total.**

First obtain the current winning line-item schedule and payment semantics. Until then, measure physical food waste and service outcomes directly, and keep economic impact `UNKNOWN` or explicitly modeled as a scenario rather than achieved savings.
