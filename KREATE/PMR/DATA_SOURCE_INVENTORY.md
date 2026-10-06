# PMR Data Source Inventory

**Updated:** 2026-10-06  
**Role:** data-surface companion to [source_catalog.json](source_catalog.json). It does **not** replace the source catalog.

This file separates public context/features from the source-owned operational truth required for a measured product/pilot claim.

## Data classes

| Class | Benchmark eligibility | Typical use |
| --- | --- | --- |
| `PRIMARY_OPERATIONAL` | Eligible only after source, semantics, privacy and admission checks | measured service / production / waste truth |
| `PUBLIC_CONTEXT` | Feature/context only | menu, calendar, event signals |
| `PUBLIC_AGGREGATE_OUTCOME` | Aggregate context/sanity checks; not service labels | campus waste totals |
| `PENDING_INTERNAL` | Ineligible until acquired and verified | production, settlement, service-level waste |
| `GENERATED_SANDBOX` | Never measured truth | demo/synthetic repo data |

## Current inventory

| ID | Surface | Grain / candidate fields | Class | Status | PMR / modeling use |
| --- | --- | --- | --- | --- | --- |
| DS-001 | Boğaziçi campus food-waste tracking (S-BU-002) | monthly/annual published totals/categories | PUBLIC_AGGREGATE_OUTCOME | available; semantics partial | scale/context; ask stage/boundary/date semantics |
| DS-002 | Dining menu (S-BU-004) | service date, meal period, dishes/options | PUBLIC_CONTEXT | available | candidate known-ahead feature; never a demand label |
| DS-003 | Academic calendar (S-BU-005/S-BU-010) | dates, term/exam/break/holiday states | PUBLIC_CONTEXT | available | known-ahead context feature |
| DS-004 | Student events (S-BU-009) | date/type/name; attendance usually absent | PUBLIC_CONTEXT | available | anomaly feature candidate; effect unknown |
| DS-005 | BUCard/SKS service truth (#292 / S-INT-005) | target: `service_date × campus_id × meal_period`, passage/served semantics, package meals, source report | PRIMARY_OPERATIONAL | **pending external acquisition** | required measured demand/service truth after reconciliation |
| DS-006 | Production/allocation record | requested/committed/produced/delivered quantities + timestamps | PENDING_INTERNAL | owner/system not yet verified | identifies actual controllable decision and counterfactual |
| DS-007 | Stage-separated waste record | service/campus/stage, waste_kg, method, timestamps, quality flag | PENDING_INTERNAL / PILOT | not yet acquired | causal outcome: surplus vs prep vs plate waste |
| DS-008 | Contract acceptance / hakediş | settlement unit, corrections, liability, penalties | PENDING_INTERNAL | not yet acquired | economic buyer / beneficiary / shortage-excess incentives |
| DS-009 | Repo historical generated CSVs | synthetic/generated schemas | GENERATED_SANDBOX | available | demos/tests only; explicitly ineligible for measured claims |

## DS-005 — service truth contract

The active owner lane is issue **#292**; CS1 parent dependency is **#82**.

Preferred privacy-safe grain:

~~~text
service_date
campus_id
meal_period
reported_service_or_passage_count
package_meal_count          # if applicable
report_generated_at
source_report_id
~~~

No person/card/student identifier is required for the initial benchmark.

### Semantic reconciliation before `actual_served`

Resolve with the source owner:

- what event increments the count;
- retries/duplicates;
- refunds/reversals;
- second meals;
- package meals;
- staff/student channels if semantically material;
- campus and meal-window boundaries;
- late corrections/backfills;
- retention and authoritative report/export;
- export approval / ownership.

When a real artifact is obtained, route it through:

~~~text
scripts/cs1_service_truth_artifact_intake.py
~~~

Preserve exact input hash/source identity/admission result. Do not hand-edit a synthetic or ambiguous count column into `actual_served`.

## DS-006 — production/allocation truth

The PMR has to locate the record/system/person that can answer:

~~~text
what quantity was requested?
what quantity was committed?
what quantity was produced?
what quantity was delivered/allocated per campus/service?
when and by whom did the value change?
when did change become costly or impossible?
~~~

Served-count prediction without the actual decision/production record cannot prove a recommendation would have changed production.

## DS-007 — waste-stage truth

A useful schema must preserve stage:

~~~text
service_date
campus_id
meal_period
measurement_stage   # preparation | unserved surplus | holding/service discard | plate | mixed/unknown
waste_kg
measurement_method
measurement_started_at
measurement_ended_at
source_or_device_id
quality_flag
~~~

`mixed/unknown` must never be silently reinterpreted as production surplus.

## Dataset promotion gate

A dataset is eligible for measured claims only when all are true:

- [ ] source owner is known;
- [ ] collection/export method is known;
- [ ] grain and time coverage are explicit;
- [ ] critical field semantics are reconciled;
- [ ] privacy boundary is acceptable;
- [ ] missingness/corrections are represented;
- [ ] source report/export identity is preserved;
- [ ] generated/demo data are excluded;
- [ ] applicable CS1 admission/validation passes.

## Highest-value next acquisitions

1. #292 aggregate BUCard/SKS export + reconciliation.
2. Actual production/allocation record or at least owner/schema/timestamp semantics.
3. Service-level, stage-separated waste measurement.
4. Current contract settlement/economic-beneficiary semantics.
5. Equivalent workflow/data map at a second institution for repeatability.

More scraped public pages have lower information value than these five.
