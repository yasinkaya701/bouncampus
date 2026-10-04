# Boğaziçi Dining Source Reconciliation — 2026-10-04

**Purpose:** Prevent public Boğaziçi values with similar labels from being silently merged into one modeling/market dataset.  
**Status:** Public-source reconciliation. **Not PMR, not internal-data validation.**

---

# Executive conclusion

Official/public Boğaziçi sources are strong enough to establish:

- material dining scale;
- six-campus dining footprint;
- centralized/structured food operations;
- measured annual/monthly waste;
- digital access/menu infrastructure.

They are **not internally consistent enough to act as a single operational ground-truth dataset**.

The product/data layer must retain:

```text
source
publication_year
measurement_period
scope
unit
counting_semantics
event_time vs reporting_time
known_conflicts
```

rather than selecting whichever public number is most convenient.

---

# 1. Dining-hall capacity conflict — 1,734 vs 1,652

## Source A — Campus Food Waste Tracking / sustainability page

Official university page:
https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

The 2025-facing page lists:

| Campus | Capacity |
| --- | ---: |
| North | 660 |
| South | 159 |
| Kilyos | 118 |
| Kandilli | 200 |
| Hisar | 124 |
| Anadolu Hisarı | 473 |
| **Total** | **1,734** |

## Source B — 2025 University Administration Activity Report

Official 2025 report:
https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Bo%C4%9Fazi%C3%A7i%20%C3%9Cniversitesi%202025%20Y%C4%B1l%C4%B1%20%C4%B0dare%20Faaliyet%20Raporu%283%29.pdf

Table 5, printed page 37, lists:

| Campus | Capacity |
| --- | ---: |
| North | 692 |
| South | 114 |
| Hisar | 118 |
| Kandilli | 120 |
| Anadolu Hisarı | 486 |
| Sarıtepe/Kilyos | 122 |
| **Total** | **1,652** |

## Difference

Total difference:

```text
1,734 - 1,652 = 82 seats/capacity units
```

But the disagreement is not a simple uniform offset; individual campuses differ in both directions.

### Possible explanations — NOT established

- different source dates/layouts;
- renovation/configuration changes;
- seating-definition differences;
- capacity vs operational capacity;
- stale page content around current waste data.

Do not select one explanation without owner confirmation.

### Modeling rule

Do **not** use either public capacity table as a hard demand cap.

Even a correct seat capacity is not equivalent to meal throughput because a dining hall can turn seats multiple times during a service window.

---

# 2. Service-regime descriptions conflict across current official sources

## Sustainability/food-waste page

The food-waste page states that, except Hisar (weekday lunch only), North, South, Anadolu Hisarı, Kandilli and Kilyos serve breakfast, lunch and dinner seven days per week.

Source:
https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

## 2025 Administration Activity Report

The report's dining section says, in summary:

- personnel receive weekday lunch at South, North, Kandilli, Anadolu Hisarı and Kilyos;
- students at South and North receive three meals on weekdays and breakfast+dinner on weekends;
- students at Kandilli and Anadolu Hisarı receive weekday lunch;
- breakfast/dinner references in the following sentences are tied to academic-calendar periods.

Source:
https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Bo%C4%9Fazi%C3%A7i%20%C3%9Cniversitesi%202025%20Y%C4%B1l%C4%B1%20%C4%B0dare%20Faaliyet%20Raporu%283%29.pdf

## Operational announcements introduce further time-varying exceptions

Dining announcements document temporary regimes such as:

- summer suspension of breakfast/dinner/weekend service;
- campus-specific reduced schedules;
- Ramadan/special-hour changes;
- packaged-service changes.

Examples:

- https://yemekhane.bogazici.edu.tr/yaz-donemi-yemek-hizmeti-hakkinda
- https://yemekhane.bogazici.edu.tr/saritepe-kilyos-kampus-yemek-hizmeti-hakkinda
- https://yemekhane.bogazici.edu.tr/duyurular

### Data rule

There is no safe timeless variable:

```text
campus_default_service_hours
```

without effective dates and source precedence.

Build instead:

```text
campus
meal_period
service_available
valid_from
valid_to
source_id
source_priority
reconciliation_state
```

and treat announcements as possible overrides of general/default pages.

---

# 3. Population/service-audience numbers are not interchangeable

## Source A — sustainability page

Approximate dining audience:

- ~13,000 students;
- ~2,000 staff.

Source:
https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

## Source B — 2025 Administration Activity Report

Table 83 reports people **benefiting from food services**:

- students: **17,466**;
- personnel: **2,478**;
- total: **19,944**.

Source:
https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/Bo%C4%9Fazi%C3%A7i%20%C3%9Cniversitesi%202025%20Y%C4%B1l%C4%B1%20%C4%B0dare%20Faaliyet%20Raporu%283%29.pdf

### Rule

Do not compute meal participation/penetration by dividing one source into the other.

The labels likely refer to different populations/periods/beneficiary semantics; public sources do not resolve the exact counting definition.

---

# 4. "6,000 daily meals" is not a daily observation series

The 2025 SKS activity report publishes:

- 6 dining halls;
- 6,000 daily meals;
- 2,000 packaged meals as another published figure.

Source:
https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096

The 2024 Administration Activity Report separately reports annual meal-service counts:

- 157,697 student breakfasts;
- 1,157,911 student meals;
- 96,838 staff meals.

Official 2024 report:
https://sgdb.bogazici.edu.tr/sites/sgdb.bogazici.edu.tr/files/2024_bu_idare_faaliyet_raporu_.pdf

### Rule

Do not derive training labels such as:

```text
6000 meals / day
```

from the summary badge.

A production-demand model requires timestamped actual service counts with defined campus/meal/channel semantics.

---

# 5. Food-waste monthly table contains a direct semantic contradiction

Official 2025 food-waste page:
https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310

The page states:

> delivered amounts are included within total amounts.

Yet the monthly table contains rows where the reported amount delivered to İSTAÇ exceeds the same month's total food waste:

| Month | Total food waste kg | Delivered to İSTAÇ kg |
| --- | ---: | ---: |
| August | 1,502 | 3,550 |
| October | 1,334 | 4,850 |

Under a same-period subset interpretation, those rows cannot both be true.

### Plausible but unverified explanations

- collection date differs from generation date;
- backlog from earlier months;
- different measurement boundaries;
- table/reporting error.

### Strong rule

Do **not** calculate monthly recovery/recycling rates from these columns until the source owner clarifies:

```text
generation_date
collection_date
reporting_period
included_streams
```

Do not train a service-level model against these monthly totals.

---

# 6. Waste stage is missing from public total

The public waste figure does not provide a clean service-level decomposition into:

```text
preparation waste
unserved edible surplus
plate/post-consumer waste
other food waste
```

This is the most important causal measurement gap.

### Implication for PMR/pilot

The first waste-owner interview should ask:

1. What is weighed?
2. At which physical point?
3. When is it attributed to a date/month?
4. Is edible surplus separate?
5. Is plate waste separate?
6. Can it be resolved by campus/service?
7. Which device/log is authoritative?

Without this distinction, the statement:

> "better demand forecasting will reduce the reported 48,251 kg"

remains a hypothesis.

---

# 7. Menu preference is not demand

The authenticated BUCampus Wednesday-menu poll provides a real preference signal.

Source:
https://yemekhane.bogazici.edu.tr/menu-anketi

It does **not** identify:

- whether a voter attends;
- campus used;
- service channel;
- quantity consumed.

### Model rule

Use poll aggregates only as a candidate exogenous preference feature after ablation.

Never use vote count as ground-truth served demand.

---

# 8. Turnstile event is not automatically one consumed meal

Dining FAQ confirms date/time/campus/turnstile context in BUCard issue handling and QR turnstile entry.

Source:
https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0

Public material does not specify:

- retention horizon;
- duplicate attempts;
- failed passages;
- refunds;
- staff/manual exceptions;
- package-channel semantics;
- one-to-one reconciliation with meals physically served.

### Data rule

Before using entry count as target:

```text
aggregate turnstile count
↔ serving / contractor record
```

must be reconciled on a bounded sample.

---

# 9. Canonical reconciliation state

Every durable imported metric should support:

```text
VERIFIED_SOURCE
SOURCE_REPORTED
RECONCILIATION_REQUIRED
DERIVED
MODEL_ESTIMATE
MISSING
WITHHELD
```

The two capacity tables and 2025 monthly waste contradiction are examples where `RECONCILIATION_REQUIRED` is preferable to silently choosing a number.

---

# 10. Source precedence should be domain-specific, not global

Do not define one rule such as:

> latest source always wins.

Instead:

- operational announcement may override a generic hours page for a specific date;
- administrative annual report may be stronger for year-specific capacity but still require owner confirmation;
- food-waste page is authoritative for its published total but not necessarily for service-level cause;
- turnstile/contractor operational exports, if obtained and defined, should outrank annual public summaries for service-level modeling.

---

# 11. Minimum data dictionary required before pilot modeling

For every core field document:

| Field | Definition to resolve |
| --- | --- |
| planned portions | requested by whom, at what time? |
| produced portions | final cooked output or batch total? |
| delivered portions | central-kitchen dispatch or campus receipt? |
| served portions | turnstile, POS, plate count, contractor acceptance? |
| edible surplus | unserved safe food only? |
| prep waste | what stage? |
| plate waste | tray return only? |
| collected food waste | generation date or collection date? |
| campus | serving site vs production site? |
| service channel | dine-in/package/kiosk/special? |

A CSV without this dictionary is not clean ground truth.

---

# 12. Strategic conclusion

The public-source inconsistencies strengthen one part of the BOUNCAMPUS product thesis:

> **provenance and metric semantics are operational requirements, not dashboard decoration.**

But this should not be exaggerated into a market claim that universities will pay for provenance. PMR must still test whether reconciliation friction is painful enough to affect the target production decision or pilot verification.
