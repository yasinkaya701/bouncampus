# Bottom-Up Market Scale Sample — Turkish University Dining

**Research date:** 2026-10-05
**Status:** Public procurement / secondary research. This is an operational-scale sample, **not a TAM/SAM/SOM calculation** and not evidence of software willingness-to-pay.

## 1. Why institution count is misleading

Türkiye's higher-education ecosystem has hundreds of universities, but `number of universities × assumed SaaS price` would be a poor market estimate because dining operations vary materially in:
- contracted meal volume;
- number of dining/service sites;
- outsourced vs institution-operated production;
- quantity-decision ownership;
- reservation/card maturity;
- data availability;
- software stack;
- procurement route;
- economic-risk allocation.

A better first market lens is **service volume × repeated decision count × addressable workflow**.

## 2. Public procurement scale sample

### Boğaziçi University — large multi-campus operation

Current 2026–2027 procurement, IKN `2025/1727143`:
- 2,500,000 student-meal units;
- 380,000 breakfast/sahur units;
- 250,000 staff-meal units;
- **3,130,000 total contracted meal units** across the two-year procurement;
- six named campuses;
- contract value: 759,537,563.59 TRY;
- contractor: TEMAŞ Gıda.

Public source mirrors of EKAP:
- https://ekapveri.com/ihale/ekap-2025-1727143/
- https://www.ihaledetay.com/2025-1727143

### Karabük University — medium/large distributed operation

2026 procurement, IKN `2026/362557`:
- **500,000** four-course meal units;
- production across university kitchens;
- service to multiple campus/faculty/MYO/hospital-related dining locations.

Source:
https://ekapveri.com/ihale/ekap-2026-362557/

### Kırıkkale University — multi-site annual operation

2026 procurement, IKN `2026/1174924`:
- **350,000** meal units;
- roughly one-year service period;
- central preparation plus a long list of university dining locations;
- awarded contract value 54,127,500 TRY.

Sources:
- https://ekapveri.com/ihale/ekap-2026-1174924/
- https://www.ihaledetay.com/2026-1174924

### Gebze Technical University — annual lunch-service operation

2026 procurement, IKN `2025/1848289`:
- **300,000** student/personnel lunch meal units;
- one-year procurement.

Source:
https://ekapveri.com/ihale/ekap-2025-1848289/

### Sivas Cumhuriyet University — narrower staff-only example

Current personnel lunch procurement, IKN `2026/1549580`:
- **160,000** meal units;
- 24-month planned service;
- personnel dining-hall scope rather than whole student ecosystem.

Sources:
- https://www.ihaledetay.com/2026-1549580
- https://ekapveri.com/ihale/ekap-2026-1549580/

### Hacettepe University — small satellite-site example

2026 procurement, IKN `2026/1460303`:
- **16,200** prepared-meal units;
- two vocational-school dining sites;
- roughly Sep 2026–Feb 2027 service period;
- awarded contract value 2,645,946 TRY.

Source:
https://www.ihaledetay.com/2026-1460303

### Galatasaray University / schools — transported-meal example

2026 procurement, IKN `2026/130374`:
- transported prepared-food service covering Galatasaray University plus associated school sites;
- TEMAŞ Gıda awarded contract, public result value 20,717,350 TRY;
- public pages reviewed here do not expose a reliable meal-unit count, so do not infer one.

Sources:
- https://www.ihaletakip.com.tr/ihale/malzeme-dahil-tasimali-galatasaray-universitesi-galatasaray-lisesi-galatasaray-ortaokulu-ve-galatasaray-ilkokulu-yemek-hizmeti-alimi/4932230/
- https://www.ihaledetay.com/ihaleler/sayfa/3?okas=15894200

## 3. What the sample shows

The segment spans at least three operational scales:

### Large / multi-campus
Hundreds of thousands to millions of meal units, multiple dining halls/campuses, high integration potential.

Examples:
- Boğaziçi;
- Karabük;
- Kırıkkale.

### Medium / focused institution-wide
Hundreds of thousands of meal units with a smaller campus/site footprint.

Example:
- GTÜ.

### Small / satellite or subpopulation
Tens of thousands of meals, limited site coverage, lower likely integration headroom.

Example:
- Hacettepe satellite MYO contract.

### Strategic implication

`University dining` is not a uniform economic unit.

A high-priority beachhead should likely favor operations with:
- high repeated meal volume;
- several service points or meaningful daily demand variation;
- costly surplus/shortage trade-off;
- accessible decision owner;
- measurable actual consumption;
- enough recurring value to justify integration.

## 4. Decision-frequency lens

The product is potentially valuable because the decision repeats, not merely because annual procurement value is large.

For a dining operation serving most class days, a quantity decision may occur:
- once per service;
- multiple times per day for breakfast/lunch/dinner;
- per campus/site;
- per item or batch depending workflow.

Therefore one university can contain hundreds or thousands of **decision episodes** per year.

But exact episode counts must be derived from actual service schedules, not assumed from annual meal quantities.

## 5. Do not convert contract value into software value

Large food-service contract values do **not** imply a correspondingly large software budget.

Reasons:
- most contract value is food, labor, logistics and service;
- software may be bundled into incumbent operations;
- savings may accrue to contractor, institution, or neither depending settlement terms;
- procurement friction can dominate license price;
- the economic value of better forecasts depends on avoidable marginal cost, not total contract spend.

Therefore do not use:

```text
contract value × arbitrary 1%
```

as BOUNCAMPUS revenue potential.

## 6. Better value-sizing equation after PMR

Once real data exist, estimate site-level annual value from observed quantities such as:

```text
avoidable_surplus_cost
+ shortage / emergency-production cost
+ penalty / service-recovery cost
+ operator planning time saved
+ measurement/reporting value where genuinely incremental
```

Then apply:
- validated addressable share;
- realistic capture rate;
- integration/support cost.

## 7. Candidate ICP filter from scale research

A stronger first-customer screen is:

```text
high-volume recurring service
AND repeated pre-service quantity decision
AND measurable realized demand
AND meaningful surplus/shortage consequence
AND reachable decision owner
AND integration path
```

Not:

```text
is a university
```

## 8. Market-size research still missing

Before producing a serious TAM/SAM/SOM, collect:
- count of institutions matching the workflow filter;
- outsourced vs institution-operated split;
- number of major catering contractors and sites;
- typical software/procurement ownership;
- current forecasting/ERP penetration;
- realistic annual economic value of decision errors;
- price sensitivity / budget authority from PMR;
- sales-cycle length.

## 9. Bottom line

Public procurement data show that the target problem occurs in operations with material and repeated meal volumes, from tens of thousands to millions of contracted meal units. This supports selecting **high-volume, multi-site or operationally complex dining** as the likely initial ICP.

It does **not** yet support a monetary TAM or a SaaS pricing claim.
