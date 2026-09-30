# Türkiye Public-University Dining Procurement Benchmark — 2026 Sample

**Research date:** 2026-10-01  
**Purpose:** Test whether the Boğaziçi food-service operating pattern is a one-off campus workflow or part of a repeatable public-university institutional-dining buyer/contract pattern in Türkiye.  
**Status:** Secondary/public-source research only. **NOT TAM. NOT exhaustive market sizing. NOT PMR. NOT customer validation.**

Related Boğaziçi packs:

- [`BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md`](./BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md)
- [`BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md)
- [`BOGAZICI_SOURCE_RECONCILIATION.md`](./BOGAZICI_SOURCE_RECONCILIATION.md)

---

# 0. Research question

> Is the current thesis — institutional dining quantities managed by a university authority and an outsourced food-service operator under explicit service/procurement constraints — repeatable beyond Boğaziçi?

The public procurement sample says **yes, as an operating archetype**, but not yet as a validated commercial beachhead.

The recurring pattern across the sampled universities is:

```text
university administrative / SKS authority
        ↓
public food-service procurement
        ↓
explicit meal / service line quantities
        ↓
contractor production and/or transport
        ↓
one or more campuses / dining halls
        ↓
student + staff service
```

What differs materially is **where food is produced, how it moves, what dietary/service channels are separate line items, how long contracts run, and how payment/acceptance is defined**.

---

# 1. Method and claim boundary

This benchmark is a **purposive convenience sample** of recent 2026 public-university food-service procurements found in public EKAP-derived records. It was selected to test operational repeatability and variation, not to estimate national market size.

Therefore:

- do **not** count the sample and extrapolate to all universities;
- do **not** sum contract values and label the result TAM/SAM/SOM;
- do **not** compare contract TRY values as if every tender covers the same scope, duration, labor, food composition, price-adjustment rules or VAT treatment;
- do **not** assume every listed tender uses the same payment semantics;
- do use the sample to identify repeated buyer roles, quantities, service modes and integration requirements that PMR can test.

---

# 2. Sample overview

## 2.1 Boğaziçi University — current reference case

From the existing Boğaziçi procurement research:

- **İKN:** 2025/1727143
- period: 2026–2027
- six campuses
- 2,500,000 student meals
- 380,000 breakfasts including sahur
- 250,000 staff meals
- **3,130,000 listed meal units**
- unit-price service contract structure in the public notice
- current contractor: TEMAŞ Gıda Sanayi ve Ticaret A.Ş.
- contract value: 759,537,563.59 TRY
- procurement capacity wording defines 5,000 meals as half the administration's daily food requirement, implying a **10,000-meal procurement design/capacity scale**, not measured average demand.

Primary research artifact: [`BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md)

---

## 2.2 Düzce University — on-campus kitchen + 400k meal units + event packages

`PUBLIC SOURCE`

- **İKN:** 2026/684643
- authority: Düzce University Rectorate, Health Culture and Sports Department
- service period: 01.07.2026–30.06.2027
- **400,000 meal units**
- **10,000 kumanya/package units** for sports, social and cultural activities
- work location: Konuralp Campus kitchen and all campus dining halls
- contract value: **57,822,400 TRY**
- contractor: Maya Grubu Catering
- open public tender / service procurement

Source:  
https://ekapveri.com/ihale/ekap-2026-684643/

### Pattern contribution

The same institution can have a normal dining stream and a separate event/package stream. This supports `service_channel` as a real schema dimension rather than a Boğaziçi-specific modeling detail.

---

## 2.3 Abdullah Gül University — transported institutional dining

`PUBLIC SOURCE`

- **İKN:** 2026/253113
- authority: Abdullah Gül University Rectorate, Health Culture and Sports Department
- service period: 04.05.2026–30.04.2027
- **210,000 meal units**
- explicitly described as **malzeme dahil taşımalı** personnel/student food service
- service location: Sümer Campus dining halls
- contract value: **27,972,000 TRY**
- contractor: Sevim Yemek ve Gıda Hizmetleri A.Ş.

Source:  
https://ekapveri.com/ihale/ekap-2026-253113/

### Pattern contribution

A forecasting/decision layer must not assume that every university owns the production kitchen on campus. In transported-service settings, the quantity freeze and logistics deadline may occur earlier and outside campus.

---

## 2.4 Türk-Alman University — breakfast + lunch/dinner as explicit demand classes

`PUBLIC SOURCE`

- **İKN:** 2026/296251
- authority: Türk-Alman University Rectorate, Administrative and Financial Affairs Department
- period: 01.05.2026–31.12.2026
- **210,000 total meal units**
  - 15,000 breakfasts
  - 195,000 lunch/dinner units
- service locations: main dining hall + Foreign Languages dining hall
- contract value: **34,704,344 TRY**
- contractor: Okbay Unlu Mamülleri Gıda San. ve Tic. Ltd. Şti.

Source:  
https://ekapveri.com/ihale/ekap-2026-296251/

### Pattern contribution

Meal type is contractually visible and can carry different demand distributions. A reusable product data contract should model breakfast / lunch / dinner separately rather than flattening them into `daily meals`.

---

## 2.5 Marmara University — same buyer, two different operating modes in parallel

Marmara is especially useful because its 2026 procurement splits institutional dining into **on-site production** and **transported meals** under separate tenders.

### A. On-site production

`PUBLIC SOURCE`

- **İKN:** 2026/593793
- authority: Marmara University Health Culture and Sports Department
- period: 01.07.2026–30.06.2027
- four listed campuses/sites
- tender quantities include:
  - 700,000 standard four-course meals
  - 36,400 vegetarian meals
  - 1,000 gluten-free meals
  - 1,000 vegan meals
  - 1,000 kumanya
  - 600 sahur kumanya
- contract value: **177,352,151.28 TRY**
- contractor: ZCatering

Sources:  
https://ekapveri.com/ihale/ekap-2026-593793/  
https://www.ihaledetay.com/2026-593793

### B. Transported production

`PUBLIC SOURCE`

- **İKN:** 2026/603458
- authority: the same Marmara University SKS Department
- period: 01.07.2026–31.12.2026
- four different listed campuses/sites
- quantities:
  - 220,000 standard transported four-course meals
  - 19,000 vegetarian transported meals
  - 500 gluten-free transported meals
  - 500 vegan transported meals
- contract value: **64,980,000 TRY**
- contractor: Kapari Hazır Yemek Ltd. Şti.

Sources:  
https://www.ihaledetay.com/2026-603458  
https://ekapveri.com/ihale/ekap-2026-603458/

A KİK decision for this transported tender reproduces the line-item quantities in the unit-price bid schedule, providing direct evidence that the categories are contract line items.

Official KİK decision:  
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=e53bf685cc2908fe76abbf541eec9f9bd19b36dabe0cb1efb72281d2bc429276

### Pattern contribution

This is the strongest public-source evidence that `one university = one forecasting workflow` is a bad assumption.

The same buyer can simultaneously need:

```text
on_site_production_model
transported_food_model
campus_allocation
meal_type segmentation
dietary_variant segmentation
package / sahur exceptions
```

The durable product primitive should therefore be a **decision/data-contract layer around a quantity decision**, not a rigid model tied to one cafeteria architecture.

---

## 2.6 İstanbul University — large multi-site procurement, result not assumed

`PUBLIC SOURCE`

- **İKN:** 2026/1430432
- authority: İstanbul University Rectorate, Health Culture and Sports Department
- tender date: 16.09.2026
- listed quantity:
  - approximately **882,000 person/meal food units**
  - **30,000 student breakfast units**
- listed delivery/service footprint includes Beyazıt and connected units, İstanbul Medical Faculty/Çapa, AUZEF Maslak and child-care units.

Source:  
https://ekapveri.com/ihale/ekap-2026-1430432/

### Freshness rule

As of this research date, do not promote a winner/contract value unless an official result notice is rechecked. The tender is useful here only as evidence of **large, multi-site explicit quantity procurement**.

---

# 3. Cross-case operating patterns

## MKT-01 — A recurring institutional buyer role exists

Across the sample, food-service procurement repeatedly sits in one of two university administrative homes:

- **Health, Culture and Sports / Sağlık Kültür ve Spor (SKS)** — Boğaziçi, Düzce, Abdullah Gül, Marmara, İstanbul University;
- **Administrative and Financial Affairs / İdari ve Mali İşler** — Türk-Alman University in this sample.

### Product implication

The initial B2B buyer-discovery universe is substantially narrower than `university management`.

The team should map:

```text
contract owner / budget owner
food-service operational owner
contractor production owner
data owner
campus service owner
```

rather than interviewing generic sustainability personnel first.

This is an **outreach prioritization hypothesis**, not buyer validation.

---

## MKT-02 — Explicit meal quantities recur across institutions

Every sampled procurement defines service through explicit meal/food-service quantities or categories.

Examples include:

- Boğaziçi: 3.13M listed units across student/breakfast/staff classes over two years;
- Düzce: 400k meals + 10k kumanya;
- Abdullah Gül: 210k transported meals;
- Türk-Alman: 15k breakfasts + 195k lunch/dinner;
- Marmara: standard + vegetarian + gluten-free + vegan + kumanya/sahur or transported variants;
- İstanbul University: ~882k food units + 30k breakfasts in the public tender notice.

### Product implication

`quantity` is not an artificial ML abstraction. It is already part of the procurement/operating vocabulary.

What remains to validate is whether **daily/meal-level quantity decisions are adjustable** and whether better predictions change physical or financial outcomes.

---

## MKT-03 — Service architecture varies enough that the product must be configurable

The sample contains:

- central/on-site production;
- transported food service;
- multi-campus delivery;
- regular meals;
- breakfast;
- vegetarian/vegan/gluten-free variants;
- packaged/kumanya service;
- sahur variants;
- event-related package demand.

A single output field such as `tomorrow_total_demand` would lose operational meaning.

Recommended reusable key:

```text
institution
site_or_campus
meal_type
service_channel
menu_or_dietary_class
service_regime
quantity_decision
quantity_freeze_time
```

---

## MKT-04 — Procurement is part of the product architecture, not only sales paperwork

Marmara's KİK material reproduces explicit bid line items. Boğaziçi's current tender also uses a unit-price structure. Other sampled notices similarly publish formal quantities even when this benchmark does not assert identical payment semantics.

This means a deployment can fail even with an accurate forecast if:

- the contract quantity cannot be revised;
- the contractor is paid in a way that removes incentive to reduce output;
- shortages carry strong penalties;
- quantity acceptance is tied to a different source than dining entries;
- campus allocation is fixed before useful demand signals arrive.

### Product implication

The solution needs a **contract-aware decision policy**:

```text
forecast distribution
+ service constraints
+ contract/payment constraints
+ shortage guardrail
+ human approval
= recommended quantity
```

---

## MKT-05 — Existing data integration requirements are likely heterogeneous

The public procurement records say little about university data systems. Boğaziçi provides unusual public clues around BUCard/QR and BUCampus menu voting, but other institutions may use different cards, turnstiles, POS, reservation systems or manual records.

Therefore the product architecture should separate:

### Canonical internal schema

```text
served_demand
requested_quantity
produced_quantity
delivered_quantity
accepted_quantity
waste_boundary
menu_context
service_regime
```

from:

### Institution-specific adapters

```text
card_or_turnstile_export
POS export
contractor spreadsheet
meal reservation export
manual daily form
waste log
```

This supports portability without pretending every university has Boğaziçi's signals.

---

# 4. Candidate beachhead refinement

## Current broad framing

`universities / institutional dining`

is too broad for PMR and product design.

## Better candidate beachhead

`HYPOTHESIS`

> **Turkish public universities with outsourced material-included dining services where explicit meal quantities are managed across one or more campuses/channels and an administrative food-service owner can influence contractor quantities.**

This definition is stronger because the public sample establishes a repeatable procurement architecture.

It is still unvalidated because public notices do **not** establish:

- frequency/cost of forecast errors;
- current forecasting method;
- discretion to alter quantities;
- buyer willingness to adopt software;
- data access;
- procurement path for the software itself;
- operator willingness to act on a recommendation.

---

# 5. Candidate qualification screen for IE

This is a **POLICY HEURISTIC for PMR prioritization**, not market truth.

Prioritize institutions where at least three of these are true:

1. outsourced material-included food service;
2. explicit high-volume meal-unit contract;
3. multiple campuses or service channels;
4. transported and/or distributed production creates an allocation decision;
5. multiple meal/dietary categories create segmentation;
6. administrative food-service/SKS owner is identifiable;
7. historical aggregate serving/entry data plausibly exist;
8. contract allows meaningful quantity changes before production;
9. excess/shortage consequences are measurable.

The first six can often be pre-screened publicly. Items 7–9 require PMR/data access.

Do not invent a numerical annual-meal threshold until interviews show where the pain/economics change materially.

---

# 6. PMR expansion plan derived from market research

## P0 — buyer/workflow interviews

Target **three institutions** with different operating modes:

1. Boğaziçi — centralized multi-campus reference case;
2. one transported-service institution such as Abdullah Gül or the transported Marmara group;
3. one on-site / multi-category case such as Marmara on-site or Düzce.

For each, answer the same canonical questions:

```text
Who owns quantity?
When is it frozen?
What is today's forecast method?
What data are visible before freeze?
Can quantity be revised?
What is the shortage cost?
What is the excess cost?
Which quantity is payable/accepted?
What is measured after service?
```

## P0 — contractor-side interviews

At least two institutional caterers should be interviewed because the buyer and operational user may have different incentives.

Do not frame the interview as `would you use AI?`.

Ask:

- last day demand differed materially from plan;
- what decision failed;
- what data were available;
- when ingredients/cooking became irreversible;
- whether a better quantity would save money/labor/waste or simply transfer risk;
- what recommendation could realistically be acted on.

## P1 — data-owner interview

At one institution, identify the card/turnstile/POS/reservation owner and test whether privacy-safe aggregate counts can be exported without PII.

---

# 7. Product consequences for CS1 / CS2

## CS1

Do not optimize a universal `university demand model`.

Build the technical contract around:

```text
ForecastContext
  institution
  campus
  meal_type
  service_channel
  menu_class
  service_regime
  history

DecisionConstraints
  freeze_time
  min_max_quantity
  contract_rules
  shortage_cost_or_guardrail
  production_batch_rules
  source_health

Recommendation
  quantity
  uncertainty
  reasons
  abstain_or_review
```

The forecasting engine can vary underneath this interface.

## CS2

The market story should not be:

> every university wastes food because demand is unpredictable.

A defensible pre-PMR story is:

> `PUBLIC SOURCE` Recent Turkish public-university food-service tenders repeatedly define large institutional dining operations through explicit meal quantities, outsourced contractors and campus/service-specific delivery models. `HYPOTHESIS` Across this segment, quantity is often set before all demand information is available, creating a repeatable decision point where better aggregate demand signals may reduce mismatch without increasing service failures. The team is validating that workflow with operators before claiming market demand or impact.

---

# 8. What the sample does **not** prove

This benchmark does not prove:

- a national market size;
- that all universities outsource dining;
- that all contracts are unit-price contracts with identical payment rules;
- that the universities suffer meaningful overproduction;
- that software procurement is easy;
- that card/turnstile data are accessible;
- that contractors welcome lower production quantities;
- that one model transfers across institutions without recalibration;
- that contract value is addressable software value.

Any application claim broader than the repeated procurement pattern should remain `HYPOTHESIS` until PMR or a more systematic market dataset supports it.

---

# 9. Sample source table

| Institution | IKN | Public quantity signal | Operating form | Public result status used here |
| --- | --- | --- | --- | --- |
| Boğaziçi University | 2025/1727143 | 3.13M listed units / 2 years | Central production + multi-campus distribution | Contracted; see Boğaziçi procurement pack |
| Düzce University | 2026/684643 | 400k meals + 10k kumanya | Campus kitchen + dining halls | Contracted |
| Abdullah Gül University | 2026/253113 | 210k meals | Transported | Contracted |
| Türk-Alman University | 2026/296251 | 15k breakfast + 195k lunch/dinner | Campus dining halls | Contracted |
| Marmara University — on-site | 2026/593793 | 700k standard + dietary/package classes | On-site production across listed sites | Contracted |
| Marmara University — transported | 2026/603458 | 220k standard + dietary classes | Transported to four listed sites | Contracted |
| İstanbul University | 2026/1430432 | ~882k meals + 30k breakfast | Multi-site | Tender notice only for this research; result not promoted |

---

# 10. Sources

1. Düzce University, İKN 2026/684643:  
   https://ekapveri.com/ihale/ekap-2026-684643/
2. Abdullah Gül University, İKN 2026/253113:  
   https://ekapveri.com/ihale/ekap-2026-253113/
3. Türk-Alman University, İKN 2026/296251:  
   https://ekapveri.com/ihale/ekap-2026-296251/
4. Marmara University on-site production, İKN 2026/593793:  
   https://ekapveri.com/ihale/ekap-2026-593793/  
   https://www.ihaledetay.com/2026-593793
5. Marmara University transported meals, İKN 2026/603458:  
   https://www.ihaledetay.com/2026-603458  
   https://ekapveri.com/ihale/ekap-2026-603458/
6. Official KİK decision reproducing Marmara transported line items:  
   https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=e53bf685cc2908fe76abbf541eec9f9bd19b36dabe0cb1efb72281d2bc429276
7. İstanbul University, İKN 2026/1430432:  
   https://ekapveri.com/ihale/ekap-2026-1430432/
8. Boğaziçi current procurement: see [`BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md).

---

# 11. Bottom line

The cross-university research materially improves the thesis:

> Boğaziçi is **not** the only public university where meal quantity is a formal operational/procurement object. Recent tenders show a repeatable institutional-dining architecture across universities, but with different production, transport, campus and meal-category structures.

That suggests the scalable product should be:

```text
institution-specific data adapters
        ↓
canonical demand + service context
        ↓
forecast / uncertainty
        ↓
contract + operational constraints
        ↓
human-reviewed quantity recommendation
        ↓
measured excess + shortage + service outcomes
```

The next market-validation step is not a larger desk-research TAM estimate. It is **same-question PMR across 3 different university operating modes plus 2 contractor operators** to determine whether the quantity-decision pain and willingness to act actually repeat.