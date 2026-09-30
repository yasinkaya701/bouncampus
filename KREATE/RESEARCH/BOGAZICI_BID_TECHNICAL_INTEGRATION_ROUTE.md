# Boğaziçi BİD Technical Integration Route — From Business Sponsor to Aggregate Adapter

**Research date:** 2026-10-01  
**Purpose:** Convert public BİD ownership/service evidence into a realistic technical request path for a dining pilot without bypassing business ownership or requesting raw personal data.  
**Status:** Secondary/public-source research + proposed implementation routing. **No BİD approval, report access, work-order submission, export capability or API access is claimed.**

## Executive conclusion

The current public ownership pattern argues against a direct `hackathon team -> BUCard database` request.

Boğaziçi's official service inventory shows:

- **BUCard identity/card system** is a BİD-owned service;
- **BUCard dining TL-loading/refund services** involve **SKS as the responsible business unit** with BİD as a technical participant;
- **system/access requests** are handled through BİD's `İş Takip Sistemi` (`istakip.bogazici.edu.tr`);
- BİD's **Yazılım Şube Müdürlüğü** officially handles requirements analysis, digital-project development, integration-gap analysis, application/database design and improvement proposals;
- the Software Branch lists a **Rezervasyon Sistemi** among managed applications;
- BİD already operates dining-specific real-time/daily reporting surfaces documented in the 2025 activity report.

Primary official sources:

- BİD Service Inventory: https://bilgiislem.bogazici.edu.tr/tr/pages/hizmet-envanteri/3513
- Software Branch responsibilities: https://bilgiislem.bogazici.edu.tr/tr/pages/yazilim-sube-mudurlugu/3247
- BİD support / İş Takip: https://bilgiislem.bogazici.edu.tr/tr/pages/bilgisayar-destegi/2373
- BİD 2025 Activity Report: https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1503-bilgi-islem-daire-baskanligi-20260227-153040.pdf

### Recommended routing principle

```text
Food Services / SKS validates the business question and sponsor
        ↓
BİD source owner confirms existing report/schema and minimum data path
        ↓
formal internal technical request / work item if needed
        ↓
source-owner aggregate export or narrow adapter
        ↓
BOUNCAMPUS decision layer
```

Not:

```text
student team asks for raw BUCard tables
→ duplicates institutional systems
→ creates avoidable privacy/security scope
```

---

# BID-01 — BUCard service ownership is split by domain

`PUBLIC SOURCE`

The BİD service inventory lists **Kimlik BUCard** as a BİD service. It separately lists `BUCard TL Yükleme Seçenekleri (Yemekhane)` and `BUCard Para İadesi` with **Sağlık, Kültür ve Spor Daire Başkanlığı** as the responsible service unit and BİD participating technically.

Primary source:
https://bilgiislem.bogazici.edu.tr/tr/pages/hizmet-envanteri/3513

### Product implication

Do not ask BİD to decide dining semantics that belong to Food Services/SKS.

The ownership split should be treated as:

```text
BUSINESS SEMANTICS / PURPOSE
Food Services / SKS

SYSTEM / SOFTWARE / ACCESS / REPORTING
BİD / BUCard / Software Branch
```

A good data request should be co-owned by the business unit that can define what the event means.

---

# BID-02 — System/access requests already have a formal internal channel

`PUBLIC SOURCE`

The service inventory lists `Sistem / Erişim Yetkisi Talebi` under BİD and points to the online **İş Takip Sistemi** (`istakip.bogazici.edu.tr`). BİD support pages also instruct university personnel to open work requests through this system for supported technical work.

Sources:

- https://bilgiislem.bogazici.edu.tr/tr/pages/hizmet-envanteri/3513
- https://bilgiislem.bogazici.edu.tr/tr/pages/bilgisayar-destegi/2373

### Implementation implication

If PMR/pilot sponsorship reaches the point where a technical request is appropriate, agents should prepare a **minimal technical request package** for the institutional sponsor to route through the proper internal channel.

Do not assume a student can independently submit or authorize an access request.

---

# BID-03 — BİD Software Branch is the relevant technical integration function

`PUBLIC SOURCE`

BİD's current Software Branch page describes responsibilities including:

- digital project development;
- requirements/current-state analysis;
- integration and gap analysis;
- technical solution proposals;
- application and database design;
- user/documentation support.

It also lists a `Rezervasyon Sistemi` among managed applications.

Primary source:
https://bilgiislem.bogazici.edu.tr/tr/pages/yazilim-sube-mudurlugu/3247

### Architecture implication

If the product wedge validates, the most institution-compatible integration is likely a **small adapter or report export** designed with the existing software owner — not a new shadow identity/transaction system.

### Boundary

The generic `Rezervasyon Sistemi` listing does **not** prove that special-period meal reservation uses that exact application. Current meal reservation source/system ownership must still be confirmed.

---

# BID-04 — Existing dining reports should be the first technical object discussed

The 2025 BİD activity report publicly documents:

- a BUCard dining real-time report page;
- daily passage reports with packaged-meal information;
- a personnel meal report with breakfast support;
- packaged-meal mobile sales/distribution tooling.

See:
`BOGAZICI_DINING_DIGITAL_REPORTING_SURFACES.md`

### Correct first technical request

Not:

> Give us BUCard logs/API access.

Prefer:

> We have a Food Services-approved bounded dining decision question. Which existing BUCard dining report already contains the smallest aggregate signal needed, what does each field mean, and can the source owner generate a bounded aggregate export or approved adapter without person-level data?

---

# BID-05 — Minimal sponsor package before a technical work request

Before any BİD implementation/access request, the product team should be able to supply:

```text
business_owner
named_decision
why_current_report_is_needed
information_cutoff / decision_freeze
minimum_required_fields
aggregation_grain
period_requested
no_PII_statement
retention_requirement
output_format_preference
who_will_receive_output
pilot_end_date / deletion rule if applicable
accepted_truth_reference
```

If these fields cannot be filled, the request is premature.

### Example minimal pilot request

```text
Business owner:
Food Services / SKS [must be validated]

Decision:
retrospective reservation-vs-realized service reconciliation

Period:
one bounded owner-approved historical special-service period

Preferred existing source:
BUCard dining daily/real-time aggregate report

Minimum fields:
service date
location/campus if already report-level
meal period if already report-level
service channel / package count if already report-level
aggregate passage count
report generated timestamp
counting semantics

Excluded:
student ID
card ID
name/email
raw transaction history
QR token/device ID
```

---

# BID-06 — Access, export and integration are different asks

Agents must distinguish:

## A. Schema understanding

Lowest-cost ask.

```text
field names
field definitions
aggregation grain
report screenshot/template if releasable
correction semantics
```

No data export required.

## B. Owner-generated bounded export

Preferred Pilot 0 path if current reports support it.

```text
aggregate rows
bounded period
approved purpose
```

## C. Recurring export / integration

Only after the pilot proves value.

Possible mechanisms may include:

- scheduled report export;
- owner-controlled file handoff;
- approved internal API/adapter;
- reporting view.

None is currently confirmed.

## D. Raw event/system access

Highest scope/risk. Avoid by default.

Use only when aggregate surfaces cannot answer a validated decision and institutional approval supports it.

---

# BID-07 — Business owner and technical owner must jointly define event semantics

Example:

BİD may know exactly how `package_count` is generated technically, while Food Services/Control may know whether that count means:

- package sold;
- package distributed;
- package collected;
- meal entitlement charged;
- accepted service.

A valid data dictionary needs both dimensions:

```text
technical_generation_semantics
+
operational_business_semantics
```

Do not let software field names substitute for operational truth.

---

# BID-08 — Same-day control requires a different technical requirement than retrospective Pilot 0

If PMR confirms a reachable intra-service action, the technical request changes.

### Retrospective / next-day experiment

Daily aggregate report may be enough.

### Same-day adaptive experiment

Need to know:

```text
refresh_latency
interval_granularity
report_availability_during_service
correction_delay
location/channel dimensions
```

Only then can CS1 evaluate `expected vs realized pace`.

Do not request interval/high-frequency reporting unless the physical decision can still change.

---

# 1. Institutional routing map

| Need | Business owner candidate | Technical/source route | Evidence still needed |
| --- | --- | --- | --- |
| Define meal-demand/service semantics | Food Services / SKS | — | current owner confirmation |
| Define accepted contract truth | Food Services + Control Organisation | — | accepted record/artifact |
| Understand current BUCard report fields | Food Services semantic input | BİD / BUCard / Software | report dictionary |
| Request aggregate bounded export | Food Services/SKS sponsor | BİD source owner / formal internal request | approval + export capability |
| Integrate recurring report after pilot | Food Services/SKS sponsor | BİD Software Branch | validated value + integration design |
| Request system/access permission | authorized institutional sponsor | BİD İş Takip / access process | exact authorization path |
| Raw personal data | **avoid by default** | only if separately justified/approved | necessity + lawful institutional basis |

---

# 2. New questions for BİD / Food Services PMR

## Food Services / SKS

1. Which BUCard dining report do you currently use, if any?
2. Who in your unit is authorized to request report changes or exports from BİD?
3. What business meaning do `passage`, `package`, `breakfast`, `meal charge` fields have?
4. Is an owner-generated aggregate export sufficient for the pilot?
5. If a recurring integration were useful later, who would sponsor the BİD request?

## BİD / Software / BUCard

1. Which technical unit owns the current dining report implementation?
2. Is the report already exportable, or can the source owner generate a bounded aggregate report?
3. Is there a field/data dictionary or report specification?
4. Does the report keep historical snapshots or recompute from event data?
5. What is the current access-control model for the report?
6. What is the institutional route for an SKS-sponsored report/export request?
7. Could a validated pilot use an existing report view/export rather than new DB access?
8. For future integration, what is the preferred institutional pattern: report, file, view, approved internal API or another mechanism?

---

# 3. Agent handoff

## IE

Do not interview BİD first about `AI`. Obtain a named Food Services decision and business sponsor first.

## Backend

Build adapters against a documented aggregate contract, not assumptions about BUCard tables.

Example interface:

```text
DiningAggregateReportRow {
  source_report
  report_generated_at
  service_date
  location?
  meal_period?
  service_channel?
  aggregate_count
  counting_semantics
  correction_state?
}
```

## CS1

Design experiments so they can run on bounded aggregate rows. Person-level modeling should not be required for the primary hypothesis.

## CS2

This institutional route is evidence for **integration feasibility direction**, not evidence that integration has been approved.

## Frontend

No live-report UX until the business/technical loop is validated. The first UI can run from offline aggregate pilot data.

---

# 4. Claim firewall

Do **not** claim:

- the hackathon team can submit an authorized BİD work order today;
- BİD will approve/export the requested report;
- meal reservation is implemented by BİD's generic Reservation System;
- a dining API exists;
- BUCard report access can be granted to external/student users;
- Food Services has already agreed to sponsor integration;
- `istakip` is the direct mechanism for this exact pilot before the institutional owner confirms it.

Safe statement:

> `PUBLIC SOURCE` Boğaziçi's BİD service inventory and Software Branch materials show an established institutional split between BUCard technical services, SKS-owned dining functions, formal system/access request processes, and software integration responsibilities. Combined with the existing BUCard dining-report evidence, this supports an aggregate-first, business-sponsored integration path to test — not a claim of approved access.

---

# 5. Bottom line

The technical path should be designed as an institutional integration, not a hackathon data scrape:

```text
validated Food Services problem
→ business sponsor
→ existing BUCard report semantics
→ minimum aggregate export
→ offline/shadow pilot
→ only if value is proven:
   formal integration request + narrow adapter
```

This is both more realistic and more production-grade.