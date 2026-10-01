# Boğaziçi Dining Incentive, Subsidy & Food-Access Map

**Research date:** 2026-10-01  
**Purpose:** Separate diner price, university subsidy/access policy, contractor economics and contract settlement so KREATE agents do not use menu price or procurement value as a false proxy for marginal waste savings.  
**Status:** Secondary/public-source research only. **NOT PMR. NOT current hakediş evidence. NOT a marginal-cost study.**

Related packs:

- [`BOGAZICI_CONTRACT_SEMANTICS_EVIDENCE_MAP.md`](./BOGAZICI_CONTRACT_SEMANTICS_EVIDENCE_MAP.md)
- [`BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`](./BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md)
- [`BOGAZICI_PMR_TARGET_MAP.md`](./BOGAZICI_PMR_TARGET_MAP.md)

---

# 0. Executive conclusion

The economic system has at least four different prices/cost concepts:

```text
STUDENT/PERSONNEL PRICE PAID AT ACCESS
        !=
UNIVERSITY'S PROCUREMENT / SERVICE COST
        !=
CONTRACTOR'S MARGINAL COST OF AN EXTRA MEAL
        !=
CONTRACT-ACCEPTED / HAKEDİŞ VALUE
```

They must never be merged without evidence.

The public record also shows that dining is an **access/welfare service**, not only a commercial food transaction:

- student meal prices are administratively subsidized;
- 1,091 meal-scholarship recipients were reported for 2025 and the scholarship was converted to in-kind support covering all meals;
- BUBizden launched in 2026 as a privacy-oriented free-meal support mechanism;
- current student lunch/dinner price is 75 TRY, far below a historical official university statement that at that earlier time put full meal cost at 210 TRY while student price was 40 TRY.

Therefore an optimization that saves food by increasing sellouts or reducing access can fail the university's mission even if it looks financially efficient.

The product objective should be:

> **reduce avoidable excess subject to food-access and service-level guardrails, and calculate economic benefit only from verified settlement/marginal-cost semantics.**

---

# 1. Current student prices are policy prices, not evidence of marginal cost

## INC-01 — Current student prices from 1 July 2026

`PUBLIC SOURCE`

Boğaziçi's official dining announcement states that from **01.07.2026**:

- student breakfast: **65 TRY**;
- student lunch: **75 TRY**;
- student dinner: **75 TRY**.

Source:  
https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi-2

The current dining homepage displays the same student prices.

Source:  
https://yemekhane.bogazici.edu.tr/

### Agent rule

`75 TRY` is the current student charge for lunch/dinner. It is **not**:

- current procurement unit price;
- contractor marginal cost;
- university marginal cost of one extra prepared meal;
- verified saving from preventing one excess meal.

---

# 2. Price regimes change over time and can change observed demand

## INC-02 — Student meal prices changed multiple times across 2024–2026

`PUBLIC SOURCE`

Official announcements show:

| Effective date | Breakfast | Lunch | Dinner |
| --- | ---: | ---: | ---: |
| 01.09.2024 | 20 TRY | 30 TRY | 30 TRY |
| 01.02.2025 | 30 TRY | 40 TRY | 40 TRY |
| 05.09.2025 | 40 TRY | 50 TRY | 50 TRY |
| 01.02.2026 | 50 TRY | 60 TRY | 60 TRY |
| 01.07.2026 | 65 TRY | 75 TRY | 75 TRY |

Sources:

- https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi-hakkinda
- https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi
- https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi-0
- https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi-1
- https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi-2

### Model implication

If historical demand data span these dates, `price_regime` is a candidate structural feature or regime flag.

Do not attribute a demand shift to menu/weather/calendar if a price change occurred simultaneously.

Recommended field:

```text
DINER_PRICE_REGIME_ID
DINER_PRICE_TRY
PRICE_EFFECTIVE_FROM
```

This does not imply price causally drives demand; it prevents silent confounding.

---

# 3. Historical official evidence shows substantial subsidy — but it is not a current-cost estimate

## INC-03 — Official university response: at that historical point, meal cost 210 TRY vs student price 40 TRY

`HISTORICAL PUBLIC SOURCE`

In an official Boğaziçi University Rectorate response transmitted through the Turkish Grand National Assembly system, the university stated that under the food-service procurement contract:

- the cost of one meal was **210 TRY including VAT**;
- the student meal price was **40 TRY**;
- only a small portion of total cost was borne by the student;
- students needing financial support also received in-kind meal scholarships.

Official TBMM-hosted document:  
https://cdn.tbmm.gov.tr/KKBSPublicFile/D28/Y3/T7/WebOnergeMetni/fbbc0f26-dcbf-41ef-b353-576cb61b7d4d.pdf

### Critical time-boundary rule

The document refers to a period when the student meal charge was 40 TRY. Current 2026 student lunch/dinner price is 75 TRY.

Therefore **210 TRY must not be used as the current 2026 meal cost**.

### What the historical statement safely establishes

- student menu price can be materially below full service cost;
- the university explicitly treats dining as subsidized student support;
- retail/user price is an unsafe proxy for system cost.

### What it does not establish

- today's full meal cost;
- today's subsidy ratio;
- current contract line-item unit prices;
- marginal avoidable cost of one excess portion;
- contractor margin.

---

# 4. Personnel pricing follows a separate subsidy rule

## INC-04 — Personnel pricing is tied to public-sector food-aid rules

`PUBLIC SOURCE`

Boğaziçi's 29 January 2026 personnel/guest price announcement cites the public-sector food assistance rule that, in Istanbul, budget appropriations may cover no more than two-thirds of meal cost, with the portion not covered by the budget collected from diners.

The announcement set, from 01.02.2026, personnel charges by salary band and separate guest/second-meal charges.

Source:  
https://yemekhane.bogazici.edu.tr/personel-ve-misafir-yemek-ucretlerinin-guncellenmesi-hakkinda-0

The current dining homepage now displays a later personnel/guest price snapshot, including salary-band prices and a **320 TRY** second-meal/tabldot guest price.

Source:  
https://yemekhane.bogazici.edu.tr/

### Implication

Student, staff and guest meal classes have different pricing/access semantics. A single blended `revenue per meal` metric is likely misleading.

Keep meal classes separate in any economic model.

---

# 5. Meal scholarships make access a first-class guardrail

## INC-05 — 1,091 meal-scholarship recipients reported for 2025

`PUBLIC SOURCE`

The 2025 SKS Activity Report lists:

- **1,091 meal-scholarship recipients**;
- conversion of the meal scholarship from cash to in-kind support;
- the statement that all meals became free for recipients under the in-kind meal scholarship.

Source:  
https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096

### Product implication

A shortage is not simply a lost sale. It may prevent a supported student from accessing a meal entitlement.

Therefore a pilot should treat service/access failure as a hard guardrail, not a soft secondary metric.

### Privacy rule

Do not request or model individual scholarship status.

If an aggregate access-equity check is operationally necessary, use privacy-safe aggregate counts and only with institutional approval.

---

# 6. BUBizden adds a second support mechanism and a demand-regime event

## INC-06 — BUBizden launched 26 February 2026

`PUBLIC SOURCE`

Boğaziçi launched **BUBizden** as a campus support mechanism for free student meals from **26.02.2026**.

The official announcement states that:

- students can apply through the university mobile application;
- meal-support rights are tracked in the same system;
- a defined right can be used once per day;
- the right is valid for that day;
- applications are evaluated under confidentiality principles.

Source:  
https://yemekhane.bogazici.edu.tr/bubizden-uygulamasi

The SKS activity page reports a `BUBizden` figure of **3,350**, but the public page does not define that number sufficiently for modeling; preserve it as a source label rather than assuming users, meals or applications.

Source:  
https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096

### Model implication

The BUBizden launch is a potential **structural intervention date** in historical demand.

Do not model individual support use. At most, consider an aggregate regime flag if PMR/data owners confirm material operational relevance.

---

# 7. Promotions can also alter observed demand independently of menu quality

## INC-07 — A dining payment promotion existed in late 2025

`PUBLIC SOURCE`

A Boğaziçi–Garanti BBVA campaign announced on 30 October 2025 offered university personnel a bonus equal to one meal amount after four qualifying dining payments.

Source:  
https://sks.bogazici.edu.tr/tr/announcements/4-yemek-odemesine-1-yemek-tutarinda-bonus/2547

### Data implication

If staff demand history is used, campaign periods should not be silently treated as normal demand.

Candidate field:

```text
PROMOTION_REGIME_ID
```

Again, this is a confounder-control recommendation, not a claim that the campaign changed demand materially.

---

# 8. Incentive map: buyer, user, payer, beneficiary are different roles

The public system suggests at least five economically distinct actors.

| Actor | Publicly visible role | Potential incentive | Critical unknown |
| --- | --- | --- | --- |
| University / SKS | service owner, subsidy/access mission, procurement authority | reduce physical waste and budget pressure without harming access | Does lower production reduce university expenditure under current settlement? |
| Food Services Branch | operational governance / contractor control | stable service, quality, no shortage, less waste | Does it control daily quantity? |
| TEMAŞ contractor | current service provider | avoid unrecoverable food/labor cost while meeting service obligations | Which excess costs remain contractor risk? Which shortages trigger deductions? |
| Students / scholarship recipients | service beneficiaries | affordable/reliable meal access | What shortage/sellout level is unacceptable? |
| Staff / guests | separate price classes | reliable service, different subsidy/payment rules | Does their demand need separate forecasting? |

### Product implication

The **economic buyer**, **daily decision user**, **data owner** and **beneficiary** may be four different personas.

The application must not collapse them into “cafeteria manager.”

---

# 9. Economic objective must be settlement-aware

Before current contract semantics are verified, do **not** optimize:

```text
student_price * avoided_portions
```

or:

```text
contract_value / total_meals * avoided_portions
```

Both can be wrong.

A defensible future economic model is:

```text
verified_economic_effect =
    change_in_contract_settlement
  + change_in_verified_contractor_variable_cost   # only if relevant/available
  + verified_disposal_or_handling_change
  - verified_shortage_or_service_penalty
  - incremental_intervention_cost
```

Each term must have an identified owner/source.

Physical waste reduction can be measured before monetary attribution.

---

# 10. Social/service objective must be explicit

A quantity recommendation should satisfy a service constraint such as:

```text
minimize expected excess
subject to
P(shortage) <= approved threshold
AND access/service guardrails remain satisfied
```

Potential pilot guardrails:

- shortage event count;
- sellout minutes;
- queue/service delay;
- forced substitution;
- unserved entitled/support meals, if a privacy-safe aggregate can be measured;
- operator override rate.

The threshold must be chosen by the operational owner, not invented by the model team.

---

# 11. Demand features created by policy/intervention regimes

If long historical data become accessible, construct a regime table instead of forcing everything into generic date features.

```text
DATE
STUDENT_PRICE_REGIME
STAFF_PRICE_REGIME
MEAL_SCHOLARSHIP_POLICY_REGIME
BUBIZDEN_ACTIVE
PAYMENT_PROMOTION_REGIME
SERVICE_REGIME
ACADEMIC_CALENDAR_STATE
MENU_CONTEXT
```

### Why

Observed attendance can change because the institution changed access, price, entitlement, service availability or promotion policy — not because the forecasting model's usual temporal features changed.

---

# 12. PMR questions upgraded by incentive research

## University / SKS / Food Services

1. If 100 fewer meals are produced and nobody goes hungry, **who financially benefits and through which ledger/contract line?**
2. Does university payment change with served/accepted quantity, or are some costs fixed/minimum-guaranteed?
3. Which dining outcomes are treated as public-service obligations rather than cost variables?
4. How are scholarship/support rights protected when quantities are tight?
5. Who decides the acceptable shortage/sellout risk?
6. Are price changes considered when planning quantities?

## Contractor / TEMAŞ

1. Which costs of an excess meal are unrecoverable to the contractor?
2. Which inputs are committed before the quantity can be revised?
3. Does a lower accepted/served quantity reduce contractor payment?
4. Are shortages/substitutions/delays penalized?
5. Would the contractor use a recommendation that reduces expected excess but slightly increases shortage probability?

## Data owner

1. Can aggregate served counts be separated by student/staff/guest meal class?
2. Can historical price/policy regime dates be joined without individual identity?
3. Can support mechanisms be represented only as aggregate regime variables rather than personal attributes?

---

# 13. Falsifiers / strategic branches

The “economic savings” narrative must be weakened if:

- university contract payments do not decline with avoidable production;
- all variable excess cost is borne by contractor but contractor is not a reachable/user/buyer stakeholder;
- savings are too small relative to operational complexity;
- service/access risk makes quantity reductions practically unusable.

The product can still have a sustainability/measurement value proposition, but the economic buyer story would need modification.

Conversely, contractor-as-user becomes stronger if PMR shows:

- excess food is contractor financial risk;
- actual accepted/served quantity drives payment;
- shortages create penalties or costly emergency production;
- operator currently uses simple heuristics and has discretion before freeze time.

---

# 14. Safe application language

A defensible formulation now is:

> `PUBLIC SOURCE` Boğaziçi operates a subsidized dining system: current student lunch/dinner price is 75 TRY, the university provides in-kind meal scholarships and additional free-meal support mechanisms, and current dining is delivered through a large unit-price service procurement. `HYPOTHESIS` The team is testing where avoidable excess cost actually sits — university settlement, contractor variable cost, or both — and will treat meal access and shortage as hard service guardrails rather than assuming every reduced portion is a financial saving.

Do not write:

- `Every prevented meal saves 75 TRY.`
- `Every prevented meal saves 210 TRY.`
- `The university subsidizes exactly 135 TRY per meal today.`
- `The current subsidy rate is 81%.`
- `The contractor loses the full cost of every excess meal.`

Current evidence does not establish those claims.

---

# 15. Sources

1. Current student prices from 01.07.2026:  
   https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi-2
2. Current dining homepage / current displayed prices:  
   https://yemekhane.bogazici.edu.tr/
3. Student price history:  
   https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi-hakkinda  
   https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi  
   https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi-0  
   https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi-1  
   https://yemekhane.bogazici.edu.tr/ogrenci-yemek-ucretlerinin-guncellenmesi-2
4. Personnel/guest pricing and public-sector food-aid rule:  
   https://yemekhane.bogazici.edu.tr/personel-ve-misafir-yemek-ucretlerinin-guncellenmesi-hakkinda-0
5. Official Rectorate response via TBMM — historical 210 TRY cost / 40 TRY student price:  
   https://cdn.tbmm.gov.tr/KKBSPublicFile/D28/Y3/T7/WebOnergeMetni/fbbc0f26-dcbf-41ef-b353-576cb61b7d4d.pdf
6. 2025 SKS Activity Report — 1,091 meal scholarships and in-kind all-meal support:  
   https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096
7. BUBizden free-meal support:  
   https://yemekhane.bogazici.edu.tr/bubizden-uygulamasi
8. Garanti BBVA personnel dining bonus campaign:  
   https://sks.bogazici.edu.tr/tr/announcements/4-yemek-odemesine-1-yemek-tutarinda-bonus/2547

---

# 16. Bottom line

The product should not be sold as:

```text
forecast better -> cook less -> price per meal × saved meals = savings
```

The defensible chain is:

```text
verify contract settlement
+ verify who bears marginal excess cost
+ preserve subsidized food access
+ recommend quantity under asymmetric shortage/excess risk
+ measure physical outcome prospectively
+ only then calculate verified economic impact
```

This turns “AI food waste” into a real institutional incentive problem rather than a superficial cost calculator.
