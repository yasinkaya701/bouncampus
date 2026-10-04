# Bottom-Up Turkish University Dining Market Sample — 2026-10-04

**Purpose:** build a reality-based market/sample frame from actual 2026 university food-service procurements rather than `number of universities × invented SaaS price`.  
**Status:** public procurement sample only. **Not TAM/SAM/SOM, not willingness-to-pay evidence, and contract values are not marginal food-waste savings.**

## Executive conclusion

Real 2026 public-university dining procurements show very large heterogeneity in:

- annualized meal volume;
- number of service locations;
- central vs transported production;
- contract duration;
- administrative owner;
- likely data/integration complexity.

Observed sample spans roughly:

```text
~210k contracted meals/year-equivalent
        to
>1.7M meals/year-equivalent in very large operations
```

and from:

```text
single campus / 1–2 dining halls
        to
18+ service locations across central and district campuses
```

This supports segmentation by **operational architecture**, not institution count alone.

---

# 1. Sample table

| Institution / procurement | IKN | Published quantity | Approx. service horizon | Site pattern | Contract/result context | Research use |
| --- | --- | ---: | --- | --- | --- | --- |
| Türk-Alman University | `2026/296251` | 210,000 meals (15k breakfast + 195k lunch/dinner) | May–Dec 2026 | main dining hall + School of Foreign Languages dining hall | awarded at 34.704M TRY | lower-volume, compact-campus archetype |
| Abdullah Gül University | `2026/253113` | 210,000 meals | ~12 months | Sümer Campus dining halls | awarded at 27.972M TRY | lower-volume transported-service/public-SKS archetype |
| Bandırma Onyedi Eylül University | `2026/1117946` | 300,000 meals | Sep 2026–Jun 2027 | central + Bandırma MYO + Erdek + Gönen + Manyas sites | transported ready-meal procurement | distributed medium-volume archetype |
| Düzce University | `2026/684643` | 400,000 meals + 10,000 packed meals | Jul 2026–Jun 2027 | Konuralp kitchen + campus dining halls | awarded at 57.822M TRY | central-kitchen / medium-volume archetype |
| Çanakkale Onsekiz Mart University | `2026/473016` | 600,000 meals | contract service period | 9 central + 9 district dining sites | awarded at 99.600M TRY | highly distributed multi-site archetype |
| İstanbul University | `2026/1430432` | ~882,000 meal units + 30,000 breakfasts | procurement period | Beyazıt, Çapa, Maslak, affiliated units/creches | 2026 procurement | large multi-campus urban archetype |
| Boğaziçi University | `2025/1727143` | 2.5M student meals + 380k breakfast/sahur + 250k staff meals = 3.13M listed units | Jan 2026–Dec 2027 | six campuses | awarded to TEMAŞ; 759.538M TRY contract | beachhead reference / large coordinated operation |
| Ankara University | `2026/1774040` | 3.48M regular lunch/dinner + 15k vegetarian + 5k celiac meals | Jan 2027–Dec 2028 | large network of central and district campuses | tender announced Oct 2026; result not yet published at research date | very-large distributed public-university archetype |

### Sources

- Türk-Alman: https://www.ihaledetay.com/2026-296251 and https://ekapveri.com/ihale/ekap-2026-296251/
- Abdullah Gül: https://www.ihaledetay.com/2026-253113
- Bandırma Onyedi Eylül: https://www.ihaledetay.com/2026-1117946
- Düzce: https://www.ihaledetay.com/2026-684643 and https://ekapveri.com/ihale/ekap-2026-684643/
- Çanakkale Onsekiz Mart: https://ekapveri.com/ihale/ekap-2026-473016/ and https://ihale.diyosis.com/ihale/2026-473016-canakkale-onsekiz-mart-universitesi-ogrenci-ve-personeli-icin-malzeme
- İstanbul University: https://www.ihaledetay.com/2026-1430432 and https://ekapveri.com/ihale/ekap-2026-1430432/
- Boğaziçi: https://ekapveri.com/ihale/ekap-2025-1727143/ and https://www.ihaledetay.com/2025-1727143
- Ankara University: https://www.ihaledetay.com/2026-1774040 and https://ihale.diyosis.com/ihale/2026-1774040-universitemiz-ogrenci-ve-personellerinin-01-01-2027-31-12-2028

---

# 2. What the sample establishes

## A. Meal volume varies by more than an order of magnitude

A product/support model that is sensible for a 210k-meal single-campus operation may not fit a 3M+ meal, multi-campus operation.

Potential segmentation variable:

```text
annualized service volume
```

not simply:

```text
university = one customer
```

## B. Site count and distribution complexity matter

Examples range from:

- compact campus with 1–2 dining halls;
- one central kitchen serving multiple campus halls;
- transported meal service across district sites;
- very large urban/multi-campus networks.

This affects:

- campus-level allocation decisions;
- data joins;
- service-regime heterogeneity;
- measurement burden;
- hardware economics;
- local-vs-central decision ownership.

## C. The procurement owner often sits in SKS / administrative units

Many public procurements are run by Health, Culture and Sports Departments or equivalent administrative units.

This supports these actors as part of the DMU, but **does not prove they are the daily production end user or economic buyer for BOUNCAMPUS**.

## D. Contract values are economically material but semantically unsafe for ROI

Examples in the sample involve contracts in tens to hundreds of millions of TRY.

Safe use:

> institutional dining is an economically material outsourced operation.

Unsafe use:

```text
contract value / meals = true marginal cost per portion
```

or:

```text
X% less waste × average contract unit price = BOUNCAMPUS savings
```

Contract totals include labor, service, materials, risk, logistics, inflation provisions and other obligations. Marginal avoidable food cost must come from the real operator/buyer accounting.

---

# 3. Operational archetypes emerging from the sample

## Archetype 1 — compact centralized operation

Characteristics:

```text
~200k–400k annual meal volume
few sites
single main campus or kitchen
lower allocation complexity
```

Potential advantage:

- faster bounded pilot;
- lower integration burden;
- easier measurement.

Potential disadvantage:

- smaller economic upside;
- fewer site-allocation problems.

Examples in sample:

- Türk-Alman;
- Abdullah Gül;
- Düzce partly fits.

## Archetype 2 — distributed medium-scale operation

Characteristics:

```text
300k–900k meals
multiple dining halls / district sites
transport or distribution planning
```

Potential decisions:

- total quantity;
- site allocation;
- batch/replenishment;
- package/dine-in split.

Examples:

- Bandırma Onyedi Eylül;
- Çanakkale Onsekiz Mart;
- İstanbul University.

## Archetype 3 — very large coordinated network

Characteristics:

```text
>1M annualized meals
multiple campuses
formal contractor/governance structure
higher data/procurement complexity
```

Potential upside:

- repeated decisions at scale;
- larger operational effect;
- stronger cross-campus allocation use case.

Potential burden:

- slower procurement;
- more veto roles;
- harder data reconciliation;
- incumbent-system likelihood higher.

Examples:

- Boğaziçi;
- Ankara University.

---

# 4. Important procurement evidence beyond volume

Çanakkale Onsekiz Mart's 2026 procurement dispute states that:

- 600,000 meal need is estimated using previous-year information;
- exact need cannot be determined with certainty in advance;
- production/transport/service/cleaning/waste management are part of an integrated service;
- technical staffing includes dietitian/food engineer, head cook and coordinator roles.

Source:
https://ihale.diyosis.com/ihale/2026-473016-canakkale-onsekiz-mart-universitesi-ogrenci-ve-personeli-icin-malzeme

### Implication

Uncertainty is not unique to Boğaziçi and can appear in a large, distributed outsourced-service specification itself.

It still does not prove demand forecasting is the highest-value intervention.

---

# 5. Market sizing framework — what to collect next

A defensible bottom-up SAM should classify institutions by:

```text
annualized_meal_volume
number_of_service_sites
production_architecture
outsourced_vs_inhouse
quantity_owner
settlement_basis
actual_demand_measurement
waste_measurement_maturity
pilot_accessibility
incumbent_specialist_system
procurement_cycle
whole_product_burden
```

Then count only institutions matching the validated beachhead profile.

---

# 6. Do not monetize the market yet

To convert an institution count into monetary SAM/SOM, we still need real PMR for:

- buyer role;
- annual budget available for this category;
- acceptable pilot price;
- implementation/support cost;
- full-product requirements;
- sales cycle;
- renewal logic;
- whether software is purchased directly, through contractor, or embedded in food-service procurement.

Until then:

```text
meal/service volume = operational market context
```

not:

```text
meal volume × assumed fee = revenue market size
```

---

# 7. Beachhead-selection implication

The best first customer may **not** be the largest university.

Disciplined Entrepreneurship speed-to-win and whole-product criteria imply an attractive first site should maximize:

```text
pain × reachable control point × measurable outcome × pilot accessibility
```

while minimizing:

```text
integration burden × procurement delay × incumbent lock-in
```

A 300k–600k meal operation with a clear operator and easy service-level data can be a better beachhead than a 3M-meal system with a two-year integration cycle.

This must be tested, not assumed.

---

# 8. Next market-research sample expansion

To reduce public-university selection bias, add:

- foundation-university dining operations;
- in-house production models;
- contractor-managed models where contractor independently controls quantity;
- institutions already using specialist waste/forecasting software;
- hospitals / factory cafeterias later as adjacent-market comparison.

The purpose is **segmentation**, not collecting as many tender examples as possible.
