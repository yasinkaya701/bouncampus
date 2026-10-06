# PMR Data Source Inventory

**Updated:** 2026-10-06  
**Role:** data-surface companion to [source_catalog.json](source_catalog.json). It does **not** replace the source catalog.

This file separates public context/features from source-owned operational truth required for measured product/pilot claims.

## Data classes

| Class | Benchmark eligibility | Typical use |
| --- | --- | --- |
| `PRIMARY_OPERATIONAL` | Eligible only after source, semantics, privacy and admission checks | measured service / production / waste truth |
| `PUBLIC_CONTEXT` | Feature/context only | menu, calendar, event signals |
| `PUBLIC_AGGREGATE_OUTCOME` | Aggregate context/sanity checks; not service labels | campus waste totals |
| `PUBLIC_PROCUREMENT` | Contract/market structure only; not operational labels | buyer, contractor, scope, procurement route |
| `ACCESS_EVIDENCE` | Not a benchmark dataset | owner route, event-surface and exportability questions |
| `PENDING_INTERNAL` | Ineligible until acquired and verified | production, settlement, service-level waste |
| `GENERATED_SANDBOX` | Never measured truth | demo/synthetic repo data |

## Current inventory

| ID | Surface | Grain / candidate fields | Class | Status | PMR / modeling use |
| --- | --- | --- | --- | --- | --- |
| DS-001 | Boğaziçi campus food-waste tracking (S-BU-002) | monthly/annual published totals/categories | PUBLIC_AGGREGATE_OUTCOME | available; semantics partial | scale/context; ask stage/boundary/date semantics |
| DS-002 | Dining menu (S-BU-004) | service date, meal period, dishes/options | PUBLIC_CONTEXT | available | candidate known-ahead feature; never a demand label |
| DS-003 | Academic calendar (S-BU-005 / S-BU-019) | dates, term/exam/break/holiday states | PUBLIC_CONTEXT | available | known-ahead context feature |
| DS-004 | Student events (S-BU-018) | date/type/name; attendance usually absent | PUBLIC_CONTEXT | available | anomaly feature candidate; effect unknown |
| DS-005 | BUCampus menu survey (S-BU-013) | authenticated weekly preference votes | PUBLIC_CONTEXT / PENDING_INTERNAL | public workflow known; export unknown | preference signal candidate only; not served demand |
| DS-006 | BUCard/SKS service truth (#292) | target: service_date × campus_id × meal_period, passage/served semantics, package meals, source report | PRIMARY_OPERATIONAL | **pending external acquisition** | required measured demand/service truth after reconciliation |
| DS-007 | Production/allocation record | requested/committed/produced/delivered quantities + timestamps | PENDING_INTERNAL | owner/system not yet verified | identifies actual controllable decision and counterfactual |
| DS-008 | Stage-separated waste record | service/campus/stage, waste_kg, method, timestamps, quality flag | PENDING_INTERNAL / PILOT | not yet acquired | causal outcome: surplus vs prep vs plate waste |
| DS-009 | Contract acceptance / hakediş | settlement unit, corrections, liability, penalties | PENDING_INTERNAL | public procurement scope known via S-PROC-001; clause semantics still missing | economic buyer / beneficiary / shortage-excess incentives |
| DS-010 | 2026–2027 public procurement (S-PROC-001) | IKN, listed meal quantities, campuses, contractor, contract period/value | PUBLIC_PROCUREMENT | available as public result context | interview target and contract-document acquisition route |
| DS-011 | Repo historical generated CSVs | synthetic/generated schemas | GENERATED_SANDBOX | available | demos/tests only; explicitly ineligible for measured claims |
| DS-012 | BİDB Service Inventory (S-BU-021) | service owner/responsible-unit/contact metadata | ACCESS_EVIDENCE | available | narrows BUCard/SKS/BİDB acquisition route; not data access |
| DS-013 | BUCampus Geçişlerim surface (S-BU-023) | user-facing turnstile/card-reader passage history | ACCESS_EVIDENCE | available | proves event-history surface exists; reader scope/exportability/reconciliation unknown |
| DS-014 | Intersession reservation workflow (S-BU-025) | reservation by service/date/campus special regime | PUBLIC_CONTEXT / PENDING_INTERNAL | public workflow known; snapshots/export unknown | decision-time intent signal candidate only |
| DS-015 | BUCard named dining report surfaces (S-BU-031) | BUCard dining live report, daily passage reports, personnel meal report; package-meal/breakfast fields documented | ACCESS_EVIDENCE | report surfaces verified first-party; grain/export/finality unknown | acquisition target names for #292; not service labels |

### Public ownership / event-surface evidence

The acquisition route is now narrower:

- **S-BU-021:** BİDB service inventory lists BUCard as a BİDB service; cafeteria BUCard top-up/refund includes SKS + BİDB; turnstile/card-reader faults route to BİDB.
- **S-BU-023:** BUCampus documents a user-facing history of turnstile/card-reader passages.
- **S-BU-026:** current university directive assigns dining BUCard operation/control, Food Services reporting and digital-data retention to the BUCard Office under BİDB.
- **S-BU-031:** BİDB 2025 activity report names existing BUCard dining live, daily-passage and personnel-meal report surfaces.

These sources support **owner routing and the existence of event/report surfaces only**. They do not establish research access, cafeteria-reader separation, report grain/finality, historical retention behavior, aggregate export, or `actual_served` semantics.

See [PRIMARY_EVIDENCE_ACQUISITION.md](PRIMARY_EVIDENCE_ACQUISITION.md).

## DS-006 — service truth contract

Active owner lane: issue **#292**; CS1 parent dependency: **#82**.

Preferred privacy-safe grain:

~~~text
service_date
campus_id
meal_period
reported_service_or_passage_count
package_meal_count
report_generated_at
source_report_id
~~~

No person/card/student identifier is required for the initial benchmark.

Before renaming any count to `actual_served`, reconcile: count-trigger event, retries/duplicates, refunds/reversals, second meals, package meals, staff/student channels, campus/meal-window boundaries, late corrections/backfills, retention, authoritative report/export and export ownership.

The official Food Services FAQ (S-BU-015) makes this reconciliation more important: overcharge/refund troubleshooting is tied to date, time, campus and turnstile context. That is evidence that correction/turnstile semantics matter, not evidence that the team has a clean export.

When a real artifact is obtained, route it through:

~~~text
scripts/cs1_service_truth_artifact_intake.py
~~~

## DS-007 — production/allocation truth

PMR must locate the record/system/person that can answer:

~~~text
what quantity was requested?
what quantity was committed?
what quantity was produced?
what quantity was delivered/allocated per campus/service?
when and by whom did the value change?
when did change become costly or impossible?
~~~

Served-count prediction without the actual decision/production record cannot prove a recommendation would have changed production.

## DS-008 — waste-stage truth

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

## DS-009 — contract / hakediş truth

The public procurement record (S-PROC-001) establishes a current two-year outsourced food-service contract and identifies the contractor. It does **not** answer the decision-economics questions needed for PMR.

Acquire or ask the responsible owner for:

~~~text
unit-price / settlement schedule
which quantity is accepted for payment
who signs acceptance / hakediş
how corrections are made
shortage / quality / delivery penalties
minimum or committed quantities, if any
how unused / overproduced food affects contractor vs university economics
whether campus allocation or total production can change after a cutoff
what report/document is authoritative for acceptance
~~~

Do not infer these from total contract value divided by listed meal counts.

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

1. #292 aggregate BUCard/SKS export + reconciliation using the now-verified BİDB/SKS owner route.
2. Current contract technical/admin specifications and settlement/hakediş semantics for IKN 2025/1727143.
3. Actual production/allocation record or at least owner/schema/timestamp semantics.
4. Service-level, stage-separated waste measurement.
5. Equivalent workflow/data map at a second institution for repeatability.

More scraped public pages have lower information value than these five.
