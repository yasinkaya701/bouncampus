# Boğaziçi 2024–2025 Dining Contract — Historical Technical Precedent

**Research date:** 2026-10-01  
**Purpose:** Extract Boğaziçi-specific technical/contract structure from a 2023 Public Procurement Board decision that quotes the 2024–2025 tender documents, while keeping a strict firewall against treating historical clauses as current 2026–2027 facts.  
**Status:** Historical public-source precedent. **NOT current-contract evidence. NOT PMR. NOT legal advice.**

Canonical historical procurement:

- **İKN:** `2023/1144278`
- **KİK decision:** `2023/UH.I-1542`
- **decision date:** `13.12.2023`
- **service period:** 2024–2025

Source:  
https://arsiv.kikkararlari.com/index.php?Itemid=71&id=74668&option=com_content&task=view

---

# 0. Why this source matters

The decision is unusually valuable because it reproduces substantial text from:

- the Administrative Specification;
- the Technical Specification;
- the Draft Contract;
- the authority's responses to bidder objections.

That makes it much richer than a normal tender notice.

But it belongs to a **different contract period and İKN**. Every finding below is tagged `HISTORICAL BOĞAZİÇİ PRECEDENT` and may only be used to:

1. understand recurring Boğaziçi operating structures;
2. design current PMR questions;
3. identify variables that may still matter;
4. avoid reinventing known operational complexities.

It may **not** be copied into a claim about the current TEMAŞ 2026–2027 contract without current-document verification.

---

# 1. Historical production topology

## HIST-01 — North Campus was the designated production kitchen

`HISTORICAL BOĞAZİÇİ PRECEDENT`

The quoted Technical Specification states that the production kitchen was:

> Boğaziçi University North Campus

and defines the service as procurement, inspection, cooking, transport, service and pre/post-service cleaning for breakfast, lunch and dinner.

### Product implication

This supports the plausibility of a **central production → distributed service** topology at Boğaziçi.

Do not infer that the current 2026–2027 workflow is identical without current confirmation.

---

# 2. Six-campus central distribution was the dominant operating mode

## HIST-02 — About 99.7% of the historical tender volume was described as central-kitchen production for six Istanbul campuses

`HISTORICAL BOĞAZİÇİ PRECEDENT`

In its response quoted by KİK, the university stated that roughly **99.7%** of tendered meals would be produced in the central kitchen and distributed to six Istanbul campuses.

The same response described very small remote-unit demand outside Istanbul as only about **0.3%** of total tender volume.

Remote units included small staff populations in locations such as Ankara, İznik and Tarsus/Mersin, where local package-food procurement was permitted under defined equivalence conditions.

### Architecture implication

Historical Boğaziçi operations already contained two distinct channel topologies:

```text
A. central kitchen -> Istanbul campuses
B. local third-party package sourcing -> tiny remote units
```

Therefore future schemas should carry `production_origin` / `service_channel`, not assume every meal traverses the same physical chain.

---

# 3. Historical procurement scale

## HIST-03 — The 2024–2025 procurement line items were larger than the current 2026–2027 public quantities

`HISTORICAL BOĞAZİÇİ PRECEDENT`

The KİK decision quotes the historical line items:

- student breakfast: **735,000 meals**;
- student lunch/dinner: **3,465,000 meals**;
- staff lunch: **476,500 meals**.

Historical listed total: **4,676,500 meal units**.

This is useful for temporal context only. It does not prove that actual consumption fell from the historical contract to the current contract because procurement quantities, service definitions and planning assumptions can change.

---

# 4. Daily capacity semantics recur historically

## HIST-04 — Historical specification also used a 5,000-meal half-daily-requirement capacity criterion

`HISTORICAL BOĞAZİÇİ PRECEDENT`

The historical Administrative Specification required:

- meal capacity: **5,000 meals**, defined as half of the university's daily meal requirement;
- breakfast capacity: **500 breakfasts**, defined as half of the daily breakfast requirement.

The current 2026–2027 public notice independently retains the 5,000-meal half-requirement wording for meal production capacity.

### Research inference

The 10,000-meal/day **design-capacity concept** appears persistent across procurement generations.

This does not prove measured average daily demand is 10,000.

---

# 5. Continuity / backup-kitchen risk was contractually material

## HIST-05 — Backup production capability was tied to contract non-compliance risk

`HISTORICAL BOĞAZİÇİ PRECEDENT`

Historical tender documents required the contractor to provide documentation for a backup kitchen in Istanbul for situations such as:

- earthquake;
- fire;
- flood;
- university-kitchen renovation or other production-blocking conditions.

The quoted Draft Contract treated failure to provide the required documentation after contract signature as a serious contractual non-compliance case that could lead to termination.

### Product implication

Decision support for this domain cannot optimize only demand. The operating system has a **service-continuity constraint**.

A robust schema should support states such as:

```text
production_site = normal_central_kitchen | backup_kitchen | external_package_source
capacity_state
service_disruption_reason
```

Current applicability must be re-verified.

---

# 6. Historical menu choice created a second forecasting problem: mix, not only total meals

## HIST-06 — Etli vs vegan main-course choice existed within the same meal count

`HISTORICAL BOĞAZİÇİ PRECEDENT`

The historical Technical Specification provided both meat-based and vegan main-course options. A diner could choose one of the alternatives.

The KİK decision notes that the bid schedule contained **total meal quantity**, while a separate vegan-meal quantity was not listed as an independent procurement line.

The authority nevertheless provided example menus, ingredients and gram quantities so bidders could price the service.

### Decision implication

Even when total demand is known perfectly, the kitchen can still face **composition uncertainty**:

```text
total meals = q_total
meat choice = q_meat
vegan choice = q_vegan
q_total = q_meat + q_vegan
```

This is a distinct decision problem from total attendance forecasting.

CS1 should keep separate potential targets:

- total production quantity;
- main-course mix;
- campus allocation;
- batch timing.

Do not assume the same choice architecture exists unchanged in the current contract.

---

# 7. Selectable items created pricing/production uncertainty

## HIST-07 — A bidder challenged unspecified ratios of selectable meals

`HISTORICAL BOĞAZİÇİ PRECEDENT`

One bidder objection argued that the proportions of selectable meal alternatives were not specified, creating uncertainty for pricing/cost estimation.

The KİK decision ultimately found the tender documentation sufficiently specified when considering total meal counts, sample menus, ingredients and gram weights.

### Research value

The dispute itself is informative:

> **mix uncertainty can be economically material even when aggregate meal counts are fixed.**

This strengthens the need to ask current operators:

- Which menu components are substitutable?
- Which components have high cost differences?
- Is mix planned using historical preference?
- Can kitchen batches rebalance during service?
- Does BUCampus menu voting reduce or merely shift this uncertainty?

---

# 8. Historical specification used explicit menu and gram-weight structure

## HIST-08 — A 14-day example menu and raw-input gram quantities were part of cost formation

`HISTORICAL BOĞAZİÇİ PRECEDENT`

The historical procurement included a two-week example menu with food components and associated raw-input quantities/gram weights.

The KİK reasoning emphasizes that food-service bidders need total meal quantities together with menu contents and raw-input quantities to form objective prices.

### Data-model implication

Menu context should not be a free-text afterthought.

Potential canonical structure:

```text
menu_date
meal_class
course_slot
option_id
option_category
raw_ingredient_group
portion_or_recipe_grams
substitution_group
```

Public current menu pages may provide part of this schema, while private recipe/cost data should be requested only if needed.

---

# 9. Contract penalties were financially connected to payments

## HIST-09 — Historical draft-contract penalties could be deducted from contractor payments

`HISTORICAL BOĞAZİÇİ PRECEDENT`

The KİK decision quotes historical Draft Contract language stating that contract penalties were deducted from payments, with separate collection if payment amounts were insufficient.

It also describes general/specific non-compliance penalty rates and termination mechanics.

### Important boundary

This does **not** tell us the current 2026–2027 shortage penalty, food-waste penalty or hakediş calculation.

It does establish that historical Boğaziçi catering operations were governed by a real **service-performance/financial enforcement layer**.

### PMR upgrade

Do not ask only:

> What happens operationally when you run short?

Also ask:

> Does a shortage, delay, substitution or other service failure create a formal deduction/penalty in the current contract, and which event record triggers it?

---

# 10. Historical renovations changed production origin

## HIST-10 — North Campus kitchen renovation temporarily forced contractor-side production

`HISTORICAL BOĞAZİÇİ PRECEDENT`

The KİK record notes that the North Campus kitchen underwent renovation around the start of the 2024 service period, so part of the service initially had to be produced outside the university kitchen until renovation completion.

### Modeling implication

Historical demand/production data may contain regime shifts caused by **infrastructure state**, not demand.

If older data are ever used for model training, add context such as:

```text
kitchen_state
production_site
renovation_or_disruption_flag
```

Without this, a model can mistake operational relocation effects for demand behavior.

---

# 11. What survives as a strong current research hypothesis

The historical precedent plus current public material supports these **questions**, not current facts:

| Hypothesis | Historical support | Current verification needed |
| --- | --- | --- |
| Boğaziçi still operates a central-production, multi-campus allocation workflow. | Strong historical evidence + current central-kitchen public context. | Current TEMAŞ workflow interview/specification. |
| Total demand and menu mix are separate decisions. | Historical meat/vegan selectable menu structure. | Current menu-production process and current choice data. |
| Service continuity/backup production affects feasible recommendations. | Historical backup-kitchen contract requirements. | Current contract continuity clauses. |
| Contract penalties make underproduction/service failure asymmetric. | Historical payment-linked penalties. | Current shortage/substitution/delay penalty clauses. |
| Historical service data require regime flags. | Kitchen renovation changed production location. | Current data span + known service changes. |

---

# 12. Current-vs-historical firewall

## Allowed

> `HISTORICAL PUBLIC SOURCE` In Boğaziçi's 2024–2025 dining procurement, the quoted technical specification used North Campus as the production kitchen, distributed the dominant service volume across six Istanbul campuses, offered meat/vegan main-course alternatives, and included formal service-continuity/contract-penalty mechanisms. The team is verifying which of these mechanisms remain in the current 2026–2027 TEMAŞ contract.

## Forbidden

Do not write from this source alone:

- `TEMAŞ must maintain a 5,000-meal backup kitchen.`
- `Current shortages are penalized at the historical rate.`
- `The current contract pays the same way as 2024–2025.`
- `Current vegan mix is unspecified.`
- `Current remote sites represent 0.3% of volume.`
- `The 2026–2027 contract contains the same penalty table.`

---

# 13. Agent handoffs

## IE / PMR

Add these current-verification prompts:

1. Has production remained centered at North Campus under TEMAŞ?
2. Which production/service topology differs from 2024–2025?
3. Are total quantity and menu-option mix separately planned?
4. Which menu alternatives create the largest waste/shortage risk?
5. What current contract event produces a penalty/deduction?
6. What backup-production rule exists today?

## CS1

Model only after separating:

```text
TOTAL_DEMAND_HEAD
MENU_MIX_HEAD
CAMPUS_ALLOCATION_HEAD
SERVICE_REGIME
PRODUCTION_SITE_STATE
```

A single scalar demand predictor is likely too coarse if current operations retain even part of the historical structure.

## EE / measurement

When tracing waste and production, record:

- production site;
- batch;
- campus destination;
- menu option;
- quantity produced;
- quantity served;
- surplus/waste boundary.

## CS2

Use this source to demonstrate **operational complexity and continuity**, not to make current-contract claims.

---

# 14. Bottom line

The strongest historical Boğaziçi lesson is:

```text
meal demand is not one number

it can decompose into:
TOTAL QUANTITY
+ MENU MIX
+ CAMPUS ALLOCATION
+ PRODUCTION SITE / CONTINUITY STATE
+ SERVICE-LEVEL / PENALTY CONSTRAINTS
```

That is a much better product-research frame than generic cafeteria forecasting.

The current contract must now be tested against this historical structure rather than assumed to match it.
