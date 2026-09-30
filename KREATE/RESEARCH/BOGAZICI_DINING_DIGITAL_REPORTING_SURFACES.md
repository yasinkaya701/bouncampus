# Boğaziçi Dining Digital Reporting Surfaces — BUCard, Live Reports & Aggregate-First Integration

**Research date:** 2026-10-01  
**Purpose:** Identify existing Boğaziçi digital dining-report surfaces that can reduce pilot integration cost and privacy risk, and test whether they expose a reachable same-day operational control loop.  
**Status:** Secondary/public-source research. **No report access, export permission, API availability, historical retention, team access or live operational usage is claimed.**

## Executive conclusion

Boğaziçi's 2025 Bilgi İşlem Daire Başkanlığı activity report materially changes the dining-data feasibility picture.

The report states that during 2025:

- the **BUCard dining real-time report page** was extended to include **packaged-meal counts**;
- **daily passage reports** were updated to include packaged-meal information;
- the **personnel meal report** gained a breakfast field and related calculation updates;
- a BUCard mobile application used at dining halls and packaged-food distribution points was deployed;
- a dedicated mobile packaged-meal sales application was deployed across packaged-meal sales points;
- BUCard / QR and related software infrastructure continued to receive operational support.

Primary official source:

https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1503-bilgi-islem-daire-baskanligi-20260227-153040.pdf

Relevant section: **BUCARD SİSTEMİ ÇALIŞMALARI → Yemekhane ve Paket Yemek Sistemleri Geliştirmeleri**, report pages 25–27.

### Why this matters

The first pilot no longer needs to assume that aggregate dining counts must be created from raw person-level logs.

A better acquisition order is:

```text
existing BUCard dining report / daily passage report
→ understand report schema + semantics
→ ask whether bounded aggregate export already exists
→ reconcile against Food Services / Control accepted truth
→ only then request any additional source-owner aggregation
```

This is simpler and more privacy-minimized than requesting raw BUCard events.

---

# DR-01 — A BUCard dining **real-time report page** exists

`PUBLIC SOURCE`

The 2025 BİD report says:

- the BUCard dining **anlık rapor** page was updated;
- packaged-meal counts were added to that page.

Primary source:
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1503-bilgi-islem-daire-baskanligi-20260227-153040.pdf

### What this establishes

- A dining-specific reporting surface exists in the BUCard environment.
- The report was capable of exposing at least packaged-meal counts in 2025.
- The system distinguishes packaged-meal activity enough for dedicated reporting.

### What this does **not** establish

- who can view the report;
- whether Food Services, TEMAŞ or the Control Organisation actually uses it;
- refresh latency;
- historical retention;
- export/API support;
- whether counts are campus-specific or meal-window-specific;
- whether counts represent sale, entry, distribution, charge or consumed meal;
- whether the report is available before a useful operational decision freezes.

Those are PMR/data-dictionary questions.

---

# DR-02 — Daily passage reports already carry packaged-meal information

`PUBLIC SOURCE`

The same report says **daily passage reports** were updated to include packaged-meal information.

This is strategically stronger than a generic statement that turnstile logs exist.

It implies there is already a report-level abstraction above raw transactions.

### Acquisition implication

Before requesting raw events, ask BİD for:

1. the current report/data-dictionary fields;
2. the natural aggregation grain;
3. a privacy-safe example/export for a bounded period;
4. the difference between a `passage`, `meal sale`, `package meal`, `QR entry` and `served meal`.

A blank report or field list may be enough to decide pilot feasibility before any data transfer.

---

# DR-03 — Personnel meal reports distinguish breakfast

`PUBLIC SOURCE`

The BİD report states that a **breakfast field** was added to the personnel meal report with necessary calculation changes.

### Product implication

Meal-period segmentation is not merely a modeling preference; at least part of the existing reporting system distinguishes breakfast explicitly.

Do not assume the same dimensionality exists for students or every campus.

### Data-model rule

Retain:

```text
actor_class_if_aggregate
meal_period
service_channel
report_source
counting_semantics
```

But do not import person-level staff identity unless a decision genuinely requires it.

---

# DR-04 — Packaged service has its own digital operational surface

`PUBLIC SOURCE`

The report describes:

- a BUCard mobile application used in dining halls and packaged-food distribution points;
- a packaged-meal sales mobile application deployed across packaged-meal sales points;
- related service/integration preparation;
- offline sales capability work.

Primary source:
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1503-bilgi-islem-daire-baskanligi-20260227-153040.pdf

### Product implication

`PACKAGE` should not be treated as a cosmetic UI label.

It is a distinct operational/service channel with digital infrastructure.

The decision dataset should preserve at least:

```text
service_channel = HALL | PACKAGE | OTHER
```

where the source owner can support those semantics.

This matters because public Boğaziçi evidence already shows service mode can change with reservation level in a historical special regime.

---

# DR-05 — Dining reporting should be reused before building a parallel telemetry stack

Boğaziçi's BİD report also describes institution-wide API standardization work (`BUAPI`) and integrated institutional-data initiatives (`BUHUB`).

Primary source:
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1503-bilgi-islem-daire-baskanligi-20260227-153040.pdf

### Architecture implication

The preferred order is:

```text
existing institutional report/export/API surface
→ source-owner aggregation
→ narrow BOUNCAMPUS adapter
→ decision model
```

not:

```text
new sensors
+ duplicated identity/event database
+ new campus data lake
```

### Boundary

The report does **not** say BUCard exposes an API for dining reports or that BUHUB contains dining data. Those remain unknown.

Do not claim integration availability until BİD confirms it.

---

# DR-06 — New candidate control surface: **intra-service adaptive decision**

`HYPOTHESIS — NOT PUBLICLY VALIDATED`

A real-time dining report may create a different decision opportunity from next-day forecasting.

Potential loop:

```text
pre-service quantity / reservation / historical expectation
        ↓
service begins
        ↓
aggregate live passage count
        ↓
compare realized pace vs expected pace
        ↓
if kitchen/service still has a reachable action:
    adjust second batch
    adjust reserve release
    reallocate package/hall stock
    reallocate campus/channel supply
        ↓
measure shortage + surplus outcome
```

### Why this could matter

If the next-day production quantity freezes too early for a better forecast, the real product wedge may be a **same-day adaptive control point**.

### Hard falsifier

This control surface dies if:

- cooking/dispatch is fully irreversible before live counts arrive;
- there is no reserve/second batch/reallocation mechanism;
- the report latency is too high;
- the operator who can act does not see the report;
- counts do not correspond reliably enough to remaining demand.

Do not build this feature until TEMAŞ/Food Services confirms a reachable action.

---

# DR-07 — Existing reports reduce privacy burden but do not automatically remove it

The parallel privacy architecture already recommends owner-controlled aggregation.

This new evidence makes that recommendation more concrete: an institutional dining report layer already exists.

Preferred request:

```text
existing report schema or owner-generated aggregate export
```

rather than:

```text
raw BUCard transaction history
```

### Minimum fields to ask whether they already exist

Do not assert these fields exist. Ask whether the current reports contain them:

```text
report_date
report_generated_at
campus_or_location
meal_period
service_channel
package_meal_count
passage_or_entry_count
actor_class_aggregate   # only if already report-level and necessary
```

For interval data, ask only if a same-day decision exists:

```text
15_or_30_minute_bucket
aggregate_entry_count
```

No user/card identifier is needed for the first test.

---

# DR-08 — Reporting semantics must still be reconciled to accepted service truth

A BUCard passage report is not automatically the same as:

- actual demand;
- kitchen-served portions;
- accepted contract quantity;
- contractor hakediş quantity;
- consumed meal;
- package distributed.

Potential reasons include:

- duplicate/failed/retried passage events;
- package sale without a hall turnstile event;
- guests or service channels using different flows;
- refunds/corrections;
- second meals or special entitlements;
- offline package sales synchronization.

### Required reconciliation

Before using a report field as `Y`/ground truth, identify:

```text
report_field
physical/business event represented
source timestamp
correction semantics
scope
owner
relationship to Control Organisation accepted record
```

---

# 1. Updated acquisition request for BİD

Old generic question:

> Can you export aggregate dining entry counts?

Better current question:

> The 2025 BİD activity report references a BUCard dining real-time report, daily passage reports with packaged-meal information, and personnel meal reporting. For a bounded dining pilot, can the source owner provide the current **report schema/data dictionary or an existing privacy-safe aggregate export**, rather than raw user transactions?

Then ask:

1. What does each count represent physically/operationally?
2. Which dimensions exist: date, campus/location, meal period, channel, actor class?
3. Is the real-time report historical or only current-state?
4. How often does it refresh?
5. Can a bounded historical report be exported CSV/Excel/API or generated by the owner?
6. Are package sales/entries distinct from dining-hall passages?
7. How are duplicates, corrections, refunds or offline package transactions handled?
8. Can the report be joined to a `service_id` without person-level data?
9. Which institutional role currently consumes the report?
10. Does anyone act on it during service?

---

# 2. Updated Pilot 0 data path

Preferred path:

```text
reservation aggregate if available
+ existing BUCard report aggregate
+ Food Services / Control accepted service record
+ production/surplus measurement
```

Reconciliation table:

| Layer | Candidate evidence | Semantics status |
| --- | --- | --- |
| Intent | active reservations at cutoff | special-period existence proven; normal-term unknown |
| Live service | BUCard dining real-time report | report existence proven; dimensions/meaning unknown |
| Daily service | BUCard daily passage report | report existence proven; package dimension proven; exact meaning unknown |
| Package channel | package sales/mobile/report fields | digital channel existence proven; operational definition unknown |
| Accepted truth | Control Organisation/Food Services record | owner/artifact still P0 unknown |
| Physical outcome | produced/served/surplus/waste | measurement granularity still P0 unknown |
| Settlement | current contract hakediş | P0 unknown |

No model should silently choose one layer as ground truth.

---

# 3. Agent-specific implications

## IE

Add two questions to Food Services / TEMAŞ / Control:

1. **Who currently looks at the BUCard dining real-time report?**
2. **What operational decision, if any, can still change after that report begins moving during service?**

This determines whether the same-day control loop is real or imaginary.

## CS1

Before richer forecasting, compare possible clocks:

```text
T-1 day reservation/history estimate
T-freeze final pre-service plan
T+service-start live aggregate pace
T+service-end realized accepted count
```

A model must be evaluated at the timestamp where its action can actually change.

Do not use final daily report data in a pre-service prediction.

## Backend/Data

Design adapter interfaces around **aggregate report outputs**, not BUCard identity rows.

Candidate interface:

```text
DiningAggregateObservation {
  source_report
  generated_at
  service_id
  campus_or_location
  meal_period
  service_channel
  interval_start?
  interval_end?
  aggregate_count
  counting_semantics
  quality_state
}
```

`service_id` may need to be created by reconciliation; do not assume BUCard already has it.

## EE

Determine whether production/batch/distribution state can be measured at comparable timestamps to the live count.

A live demand signal has no value without a reachable physical action.

## Frontend

Do not build a real-time operations screen until workflow validation.

If validated, the useful surface is not a decorative live counter. It is:

```text
expected vs realized pace
remaining planned quantity
reachable action
shortage/surplus risk
operator approve/override
```

## CS2

Safe claim:

> Boğaziçi's 2025 BİD activity report documents existing BUCard dining real-time and daily reporting enhancements, including packaged-meal counts. We are testing whether these existing aggregate reporting surfaces can support a privacy-minimized operational decision before a relevant control point closes.

Unsafe claim:

> We have live BUCard data / API access / real-time demand integration.

---

# 4. Evidence-acquisition changes

The BİD acquisition task should now prefer:

1. current BUCard dining-report **schema/data dictionary**;
2. blank/redacted screenshot/report template if appropriate;
3. owner-generated bounded aggregate export;
4. export/API capability only after semantics are understood;
5. raw events only if aggregate report genuinely cannot answer the decision and institutional approval supports it.

This is a meaningful reduction in data-access risk compared with starting from raw transaction logs.

---

# 5. Claim firewall

Do **not** claim:

- the team has access to the BUCard real-time report;
- the report is visible to TEMAŞ/Food Services/Control;
- the report refreshes at a specific latency;
- the report contains campus or meal-period dimensions beyond what the source explicitly states;
- a passage equals a consumed/served/accepted meal;
- package-meal count means produced packages rather than sold/distributed/passed units;
- historical report retention exists;
- a dining report API exists;
- BUHUB currently includes dining data;
- same-day production/reallocation is operationally possible.

What is safe:

> `PUBLIC SOURCE` The 2025 BİD activity report documents a BUCard dining real-time report page, daily passage reporting with packaged-meal information, personnel meal-report enhancements, and digital packaged-meal sales/distribution infrastructure. `HYPOTHESIS` The team is testing whether existing aggregate reporting can be reused for a privacy-minimized pre-service or intra-service decision loop.

---

# 6. Bottom line

This finding changes the integration question from:

```text
Can we somehow get raw BUCard data?
```

into:

```text
What existing dining report already represents the smallest useful aggregate signal,
what exactly does each field mean,
and which decision is still reachable when that report is available?
```

That is a much stronger starting point for a hackathon pilot and a production architecture.