# Boğaziçi Dining Aggregate-Data Feasibility — BUCard / BUCampus Reporting Surfaces

**Research date:** 2026-10-01  
**Purpose:** Close the technical-feasibility portion of P0-03 by determining whether Boğaziçi already has dining reporting/event surfaces that could plausibly produce privacy-safe aggregate demand counts.  
**Status:** Secondary/public-source research. **NOT proof of team access, retention period, export permission, completeness or suitability as the contract/hakediş source.**

---

# 0. Executive conclusion

Public evidence is now strong enough to move the P0-03 question from:

> Does Boğaziçi have any digital dining-event data?

into:

> **Can the institutional owner export the existing reporting surface at the exact aggregate grain and historical window needed for the production decision?**

The strongest current evidence is Boğaziçi BİDB's 2025 activity report, which states that:

- a **BUCard dining real-time report page** exists;
- **package-meal counts** were added to that real-time report;
- **daily passage reports** were updated to include package-meal information;
- a **staff meal report** was expanded with a breakfast field;
- BUCard MOBILE is used in dining halls/package distribution points;
- QR passage error/retry infrastructure was actively developed.

Separate public sources show that:

- personnel can inspect detailed meal usage through BUCard / BUCampus;
- dining overcharge investigations use **date + time + campus + turnstile** context;
- BUCampus QR can be used at dining turnstiles;
- older BİDB reports already referenced a `meal tracking screen`, manual meal passage records and reporting improvements;
- 2024 BİDB reporting describes dining access as part of the centrally managed BUCard system and QR-based passage tracking.

These sources establish **existing observability/reporting capability**, not research access.

The P0 artifact request should therefore be very small:

```text
ONE aggregate export sample
+ ONE-page data dictionary
+ retention/quality notes
```

No person-level logs are required.

---

# 1. Current strongest evidence — BUCard dining reporting already exists

## DATA-FEAS-01 — 2025 BİDB explicitly names a BUCard dining real-time report

Boğaziçi University BİDB's 2025 Activity Report, under BUCard system work, states that package-meal quantities were added to the **BUCard Yemekhane anlık rapor sayfası** and that **Günlük geçiş raporları** were updated to include package-meal information. It also states that a breakfast field was added to the staff-meal report.

Official report:

https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1503-bilgi-islem-daire-baskanligi-20260227-153040.pdf

### What this supports

There is a current institutional reporting layer that can represent at least some dining transaction/usage counts and distinguish some service classes.

This materially strengthens technical feasibility for an aggregate pilot.

### What this does not establish

- exact column schema;
- campus granularity;
- meal-window granularity;
- historical retention;
- whether student and staff counts are cleanly separable;
- whether QR and physical-card events are deduplicated;
- how reversals/refunds are represented;
- whether package sales equal consumed meals;
- whether the report is available before production freeze;
- whether the team will be granted access/export;
- whether the same report drives current contractor hakediş.

---

# 2. Current infrastructure supports multiple dining event channels

## DATA-FEAS-02 — Dining halls/package points use BUCard MOBILE and reader infrastructure

The same 2025 BİDB report states that BUCard MOBILE was deployed for dining halls and package-distribution locations, mobile meal-sale readers were updated, and QR passage retry behavior was improved.

Official source:

https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1503-bilgi-islem-daire-baskanligi-20260227-153040.pdf

### Implication

The first data inventory must distinguish channel semantics:

```text
DINING_HALL_TURNSTILE
PACKAGE_MEAL_SALE_OR_DISTRIBUTION
QR_PASSAGE
PHYSICAL_BUCARD_PASSAGE
STAFF_MEAL_USAGE
OTHER_OR_MANUAL_FALLBACK
```

Do not merge all events into one demand series until the source owner explains what each event means.

---

# 3. User-facing detailed usage confirms transactional history exists

## DATA-FEAS-03 — Personnel can view detailed meal usage

A Boğaziçi dining announcement on personnel meal charges states that meal fees are aggregated into the following month's payroll and that **detailed viewing** is available via BUCard and BUCampus.

Official source:

https://yemekhane.bogazici.edu.tr/node/225

### What this establishes

The institution has enough meal-usage detail to expose account-level transaction history to an authorized user in at least the personnel workflow.

### What it does NOT establish

- that researchers/team members can access those records;
- the database retention period;
- that student transactions expose the same history;
- the exact event schema;
- that the detail is the same data source as the BİDB real-time report.

### Product rule

Do **not** request this person-level history.

Use its existence only to justify asking the owner to aggregate the relevant operational counts internally.

---

# 4. Support workflow exposes useful event dimensions

## DATA-FEAS-04 — BUCard dining issues are investigated using date/time/campus/turnstile

The current dining FAQ tells users who report a BUCard overcharge to provide:

```text
date
time
campus
turnstile
```

It also states that users without a physical card can use BUCampus to scan the QR code at the turnstile.

Official source:

https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0

### Inference boundary

This strongly suggests that operational troubleshooting can distinguish those dimensions.

It does not prove the exact database schema or export query.

### Pilot relevance

A privacy-safe aggregate grain such as:

```text
DATE × CAMPUS × MEAL_WINDOW × SERVICE_CHANNEL → VALIDATED_ENTRY_COUNT
```

is technically plausible enough to request from the owner.

---

# 5. 2024 BİDB report shows centrally managed dining passage infrastructure

## DATA-FEAS-05 — Dining passage is part of central BUCard support

BİDB's 2024 activity report describes BUCard as a centrally managed card-access system that covers dining passage and says QR-labelled passage control was implemented through BUCampus. It also records maintenance/support for dining turnstiles and duplicate meal-fee corrections.

Official report:

https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/540-bilgi-islem-ve-yayim-daire-baskanligi-20260109-142044.pdf

### What this strengthens

- BİDB/BUCard is a real technical owner route, not a speculative stakeholder;
- dining-passage data have an operational support lifecycle;
- duplicate/reconciliation issues are real enough to be corrected, so raw event count is not automatically a clean demand count.

### Data-quality implication

The pilot dataset needs explicit reconciliation semantics for:

```text
duplicate_charge_or_passage
refund_or_reversal
offline_event
QR_retry
manual_fallback
package_sale_vs_pickup
second_meal
staff_subsidized_meal
```

---

# 6. Historical reports show dining tracking/reporting is not new

## DATA-FEAS-06 — Older BİDB material references a meal tracking screen and reporting work

Historical BİDB/University activity material includes references to:

- `Yemek takip ekranı`;
- manual meal passage records;
- retrospective correction of meal passages;
- reporting-system improvements;
- food-fee configuration screens.

Historical source example:

https://sgdb.bogazici.edu.tr/sites/sgdb.boun.edu.tr/files/sgdbfiles/faaliyet_raporu/2016/2016_B%C4%B0DB_FAAL%C4%B0YET_RAPORU.pdf

### Correct use

This is historical architecture context only.

Do not assume old fields, retention or interfaces still exist today.

Its value is to show that meal-event reconciliation/reporting has long been an institutional system concern rather than a brand-new data request.

---

# 7. BUBizden and reservation data are separate signals

Current BUCampus/BUBizden sources show daily meal-support requests/rights inside the dining module, and separate Boğaziçi research packs document reservation workflows in special service regimes.

Sources:

- https://bilgiislem.bogazici.edu.tr/tr/announcements/bucampusun-yeni-versiyonu-yayinda/4373
- https://yemekhane.bogazici.edu.tr/bubizden-uygulamasi

### Important distinction

Do not collapse these signals into served demand:

```text
BUBIZDEN_APPLICATION_COUNT != MEAL_ENTRY_COUNT
RESERVATION_COUNT != SERVED_COUNT
MENU_VOTE_COUNT != DEMAND_COUNT
TURNSTILE_EVENT_COUNT may require reconciliation before it becomes VALIDATED_SERVED_COUNT
```

They can be candidate **pre-freeze explanatory/intent signals** only if owner-confirmed semantics and timing make them useful.

---

# 8. P0-03 is now two separate gates

## P0-03A — Technical aggregate-export feasibility

Public-source state: **STRONGLY PLAUSIBLE / PARTIALLY ESTABLISHED**.

Why:

- real-time dining report exists;
- daily passage reports exist;
- staff meal reporting exists;
- passage troubleshooting has operational dimensions;
- package channel has been added to reports.

Remaining proof:

> Data owner generates one aggregate sample.

## P0-03B — Decision usefulness

State: **UNKNOWN**.

Need to know:

- whether the count is available historically;
- whether it is timestamped accurately;
- whether it can be mapped to meal windows/campuses;
- whether it represents served demand adequately;
- whether it is available before freeze as a live/pacing signal or only after service as history;
- whether historical context spans comparable service regimes.

A technically exportable dataset can still be useless for the decision.

---

# 9. Minimum viable export request

Do not ask for a database dump.

Ask BİDB/BUCard for a tiny sample such as 14–28 service days:

```text
SERVICE_DATE
CAMPUS_CODE
MEAL_WINDOW
SERVICE_CHANNEL
VALIDATED_ENTRY_COUNT
PACKAGE_COUNT_IF_SEPARATE
STAFF_COUNT_IF_SEPARATE
STUDENT_COUNT_IF_SEPARATE
MANUAL_OR_OFFLINE_COUNT_IF_AVAILABLE
REVERSAL_OR_CORRECTION_COUNT_IF_AVAILABLE
SOURCE_REPORT_NAME
EXTRACTED_AT
```

No card/user identifiers.

### If meal-window field does not exist

Ask whether the owner can derive meal windows from event timestamps **inside the source environment** and export only aggregates.

### If campus field is turnstile-based

Request a lookup table:

```text
TURNSTILE_OR_DEVICE_GROUP → CAMPUS → SERVICE_POINT
```

without device/user-sensitive fields that are unnecessary for analysis.

---

# 10. One-page data dictionary request

For each field, request:

```text
field_name
business_definition
source_system
unit
aggregation_rule
included_event_types
excluded_event_types
correction_rule
timezone
retention_start
known_missing_periods
owner
```

For `VALIDATED_ENTRY_COUNT`, the most important questions are:

1. Does a QR retry create duplicate raw events?
2. Are failed/declined passages excluded?
3. Are refunds/reversals represented?
4. Does one successful event equal one meal received?
5. Can a valid user enter without consuming the meal?
6. Can a meal be distributed without a recorded turnstile event?
7. How are package meals counted?
8. How are manual/offline passages reconciled?

---

# 11. Demand label hierarchy

The model should not call every count `actual_demand`.

Use explicit states:

```text
RAW_PASSAGE_EVENTS
RECONCILED_VALID_PASSAGES
VALIDATED_SERVED_COUNT
OBSERVED_SALES_OR_DISTRIBUTION_COUNT
CENSORED_DEMAND_LOWER_BOUND_IF_SELLOUT
TRUE_UNCONSTRAINED_DEMAND = generally unobserved
```

### Sellout rule

If production sells out, validated served count can be a lower bound on true demand.

This links directly to the pilot red-team pack: do not score forecast error as if the served count were uncensored demand on a sellout service.

---

# 12. Data-source precedence for a pilot

Prefer the smallest source that is operationally authoritative.

Candidate order to test:

```text
1. control/hakediş accepted meal count, if it is semantically suitable and timely enough for history
2. reconciled BUCard/BUCampus dining report count
3. manually verified service count
4. raw passage aggregate after owner-defined reconciliation
```

This is a test order, not an assertion that the contract source is superior for forecasting.

The label should be selected based on **business meaning**, not convenience.

---

# 13. Aggregate data can also reveal regime changes

The 2025 BİDB report shows package meal counts were added to reporting, while SKS sources show package service expanded and BUCampus/BUBizden/menu features changed over time.

Therefore historical data require a regime table:

```text
DATE_RANGE
SERVICE_POINT
SERVICE_REGIME
REPORTING_VERSION
PACKAGE_CHANNEL_ACTIVE
BUBIZDEN_ACTIVE
PRICE_REGIME
RESERVATION_REQUIRED
KNOWN_SYSTEM_CHANGE
```

### Why

A model can mistake a reporting-system upgrade for a demand shift.

Historical backtests must distinguish:

```text
real demand change
vs
channel shift
vs
reporting-schema change
```

---

# 14. Exact BİDB interview / artifact request

A 20-minute technical meeting can answer P0-03.

Ask:

1. Can you show the current **BUCard Yemekhane anlık rapor** without exposing individual user rows?
2. What dimensions can it aggregate by today?
3. What is contained in **Günlük geçiş raporları**?
4. How far back are comparable records retained?
5. How are QR retry, duplicate charge, correction and offline/manual events handled?
6. Are package-meal counts separate from dining-hall passage counts?
7. Is there a stable campus / service-point identifier?
8. Can you export 2–4 weeks of aggregate counts to CSV/XLSX or provide a one-time anonymized aggregate query result?
9. Which institutional approval is required for a pilot extract?
10. Which count does Food Services currently trust operationally?

### Desired output

```text
one screenshot/schema walkthrough
+ one 20-row aggregate sample
+ one-page data dictionary
```

No raw transaction export is necessary.

---

# 15. Falsification conditions

## Keep aggregate-data architecture if

- report fields can identify campus/service window;
- history is available across enough comparable days;
- correction semantics are understood;
- aggregate export is institutionally feasible;
- count is a useful served-demand proxy.

## Modify if

- package and hall events cannot be reconciled;
- historical schema changed heavily;
- campus/meal grain is unavailable;
- turnstile count is not meaningfully related to meals served.

Possible fallback:

```text
manual service count
+ production log
+ waste measurement
```

## Defer model-heavy pilot if

- no reliable aggregate history exists;
- manual collection burden is prohibitive;
- event semantics cannot be reconciled;
- output arrives too late to train/evaluate a useful operational baseline.

---

# 16. Safe KREATE language

### Safe

> `PUBLIC SOURCE` Boğaziçi BİDB reports an existing BUCard dining real-time report and daily passage reports, including package-meal reporting. `RESEARCH GAP` The team is validating whether a privacy-safe aggregate extract can be produced at campus/meal granularity and whether those counts are semantically suitable for the production decision.

### Unsafe

> `We have access to BUCard data.`

> `BUCard provides clean actual demand.`

> `Every turnstile scan equals a meal consumed.`

> `The current model trains on university transaction history.`

> `BUCard is the current hakediş source.`

None of those is established.

---

# 17. Sources

1. Boğaziçi University BİDB — 2025 Activity Report, BUCard dining report / daily passage / package system development:  
   https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1503-bilgi-islem-daire-baskanligi-20260227-153040.pdf
2. Boğaziçi University BİDB — 2024 Activity Report, central BUCard / dining passage / QR infrastructure context:  
   https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/540-bilgi-islem-ve-yayim-daire-baskanligi-20260109-142044.pdf
3. Dining FAQ — date/time/campus/turnstile troubleshooting + QR passage:  
   https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0
4. Personnel meal payroll announcement — detailed BUCard / BUCampus meal-usage viewing:  
   https://yemekhane.bogazici.edu.tr/node/225
5. BUCard usage areas:  
   https://bucard.bogazici.edu.tr/tr/pages/bucard-kullanim-alanlari/5942
6. BUBizden current support flow:  
   https://yemekhane.bogazici.edu.tr/bubizden-uygulamasi
7. Historical BİDB activity report — meal tracking/reporting context only:  
   https://sgdb.bogazici.edu.tr/sites/sgdb.boun.edu.tr/files/sgdbfiles/faaliyet_raporu/2016/2016_B%C4%B0DB_FAAL%C4%B0YET_RAPORU.pdf

---

# 18. Bottom line

P0-03 is no longer primarily a software-existence question.

Boğaziçi publicly documents dining reports and event infrastructure.

The remaining proof is operational and institutional:

```text
EXISTING REPORT
→ DATA DICTIONARY
→ PRIVACY-SAFE AGGREGATE SAMPLE
→ RECONCILIATION / QUALITY CHECK
→ DECISION-USEFUL LABEL
```

If that chain works, the first model can be built without person-level tracking and without inventing a new campus data-collection platform.