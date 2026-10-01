# Boğaziçi Data & System Ownership Map — Agent Research Pack

**Research date:** 2026-10-01  
**Purpose:** Prevent agents from asking the wrong unit for data or silently treating a service-support owner as the authoritative data/decision owner.  
**Status:** Public-source routing research only. **NOT proof of database access, retention, schema, export permission or data-controller status.**

---

# 0. Core rule

Never collapse these roles:

```text
service support owner
!= application maintainer
!= database/data steward
!= business-process owner
!= decision owner
!= approval authority
```

A public service inventory tells us where a service/request is routed. It does **not** prove who owns every underlying table or whether historical data are retained/exportable.

---

# 1. Cross-system routing matrix

| System / data surface | Publicly visible service/authority route | Candidate business owner | What agents may safely infer | What still needs PMR/internal confirmation |
| --- | --- | --- | --- | --- |
| BUIS / ÖBİKAS | Öğrenci İşleri Daire Başkanlığı; BİD also appears in support route | Student Affairs / Registration | academic registration system exists and OIDB is authoritative service route | schema, history, exports, section enrollment snapshots, schedule-change logs |
| Course scheduling / classroom assignment | Kayıt İşleri Şube Müdürlüğü | Registrar / Registration Branch | general-use classroom scheduling is assigned to this unit | actual scheduler, algorithm/tool, freeze time, constraints, historical revisions |
| BUCampus | Bilgi İşlem Daire Başkanlığı | domain-dependent; BİD for software/support | BİD receives BUCampus development/support requests | event retention, analytics tables, feature-level domain owners, export rights |
| BUCard | BİD plus domain-specific units | domain-dependent; SKS for dining payment/load operations | campus identity/payment card service exists | transaction event semantics, timestamps, dining consumption mapping, refunds/duplicates |
| Cafeteria BUCard TL loading | SKS + BİD | SKS / Food Services candidate | dining payment workflow touches SKS and BİD | whether meal-service transaction history is suitable for demand modeling |
| Shuttle timetable surface | University shuttle site; BUCampus displays transport info | shuttle/transport operations owner unknown publicly | public routes/times exist | canonical schedule database, actual trip data, vehicle/ridership logs, approver |
| Wireless network | BİD | BİD infrastructure; use-case owner separate | university wireless service exists | AP telemetry retention, privacy approval, room mapping, historical client-count access |
| Water measurements | Water Management Commission + Yapı İşleri ve Teknik Daire + unit water admins | formal water governance | quarterly reporting/monitoring responsibility exists | meter topology, sampling cadence, raw granularity, anomaly workflow |
| Energy measurements | ISO 50001 Energy Management System + Energy Management Team | Energy management / facilities route | regular measurement/analysis is publicly stated | BMS/EMS granularity, alarms, controls, export/API, verification baseline |

---

# 2. BİD service inventory — strongest current routing source

**Source:** Boğaziçi University Information Technology Department, Service Inventory  
https://bilgiislem.bogazici.edu.tr/tr/pages/hizmet-envanteri/3513

The inventory publicly identifies, among other items:

- **Student Information Automation System (BUIS/ÖBİKAS)** — applicant/authorized unit: Student Affairs;
- **ÖBİKAS support** — Student Affairs + Information Technology;
- **BUCampus development/support requests** — Information Technology;
- **BUCard** — Information Technology, with domain-specific routes depending on card/user type;
- **BUCard TL loading for cafeteria** — Health, Culture and Sports (SKS) with Information Technology;
- **system/access authorization requests** — Information Technology;
- **wireless network services** — Information Technology;
- **turnstile/card-reader problems** — Information Technology.

### Agent implication

For dining data, a bounded request may need **both**:

```text
business approval from SKS/Food Services
+
technical extraction from BİD
```

For classroom data, the analogous path may be:

```text
business/process approval from OIDB/Registration
+
technical/system support from OIDB automation/BİD as appropriate
```

Do not send a generic “give us all data” request to BİD before the business owner defines a legitimate field-level request.

---

# 3. Student Affairs / course-system boundary

## DS-S01 — BUIS/ÖBİKAS is routed to Student Affairs

The BİD service inventory lists the Student Information Automation System under the **Öğrenci İşleri Daire Başkanlığı**.

## DS-S02 — Classroom scheduling is explicitly owned by Registration Branch

Source:  
https://oidb.bogazici.edu.tr/tr/pages/derslikler-hakkinda/4422

General-use classroom scheduling is performed by **Kayıt İşleri Şube Müdürlüğü**.

## DS-S03 — Public organizational material exposes automation/reporting roles

A public Student Affairs organizational document shows an **Otomasyon ve Raporlama Şube Müdürlüğü** with subordinate functions including **ÖBİKAS** and **Ders Programları** responsibilities.

Source:  
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/567-ogrenci-isleri-daire-baskanligi-20260112-095818.pdf

### Important boundary

This supports a more precise PMR route, but it still does not prove which unit stores the authoritative room-assignment revision history or can export it.

### Field-level request for classroom pilot

Ask only for the minimum needed:

```text
term
course_code
section_id
meeting_pattern
assigned_room
room_capacity
registered_count_or_snapshot
course_quota
assignment_version_or_change_if_available
```

Then separately ask whether room-type/equipment/accessibility constraints exist in structured form.

---

# 4. BUCampus boundary

BİD publicly accepts **BUCampus Support and Development Requests** and the product exposes services such as transport and dining/menu interfaces.

Sources:

- https://bilgiislem.bogazici.edu.tr/tr/pages/hizmet-envanteri/3513
- https://bilgiislem.bogazici.edu.tr/tr/pages/ulasim/8597

### Safe inference

BUCampus is a real university digital surface and BİD is a technical route.

### Unsafe inference

Do not claim that:

- every BUCampus interaction is logged historically;
- menu votes/ratings are available as timestamped exports;
- transport screen views equal travel intent;
- app identity can or should be used for individual prediction.

### Preferred data request

Privacy-safe aggregate first:

```text
date_or_service_day
context_id (meal / route / campus)
event_type
aggregate_count
available_at
```

Before any user-level data request, prove aggregate signals are insufficient and obtain the appropriate privacy/legal approval.

---

# 5. BUCard dining boundary

The service inventory identifies **BUCard** as the campus identity/payment card and routes cafeteria TL loading through **SKS + BİD**.

Source:  
https://bilgiislem.bogazici.edu.tr/tr/pages/hizmet-envanteri/3513

### Research hypothesis

A privacy-safe aggregate of successful dining transactions may be useful as a historical **served-demand proxy**.

### What must be established before use

- what event means a consumed meal;
- whether QR/card modes share semantics;
- transaction timestamp meaning;
- refunds/cancellations/duplicates;
- second-meal/multi-use behavior;
- campus/terminal identity;
- retention window;
- whether historical export is permitted;
- when aggregate data become available relative to production freeze.

### Agent rule

Use the label:

```text
CANDIDATE_SERVED_DEMAND_PROXY
```

until a business + technical owner confirms event semantics.

---

# 6. Wireless data boundary

The BİD inventory exposes wireless network services and BİD as the technical unit.

### What this supports

Only that managed wireless infrastructure exists.

### What it does not support

- AP-level historical telemetry is retained;
- telemetry can be used for occupancy analytics;
- APs map cleanly to classrooms;
- raw client count equals occupancy;
- privacy approval exists.

Academic research already indexed in `BOGAZICI_CLASSROOM_ALLOCATION_AND_OCCUPANCY.md` shows why raw Wi-Fi device counts need calibration in dense campuses.

### EE/CS1 rule

Existing administrative data first. Wi-Fi occupancy is a fallback sensing path, not the first data dependency.

---

# 7. Shuttle data boundary

Public sources expose routes and scheduled departure times:

- https://bogazici.edu.tr/tr/pages/ulasim-park/138
- https://mekik.bogazici.edu.tr/
- https://bilgiislem.bogazici.edu.tr/tr/pages/ulasim/8597

What remains unknown:

```text
canonical_timetable_owner
actual_trip_timestamp_source
vehicle_assignment
vehicle_capacity
boarding_count
queue_or_left_behind_count
historical_retention
```

Do not build a forecasting pipeline around scraped scheduled times alone; the prediction target requires observed ridership/service outcomes.

---

# 8. Water data boundary

Boğaziçi's Water Management Directive states that unit water administrative officers are responsible for measurement/monitoring/control and that water consumption/recovery data are presented to the Water Management Commission every three months. Yapı İşleri ve Teknik Daire is also explicitly part of the governance/data flow.

Source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/1541-water-discharge-guidelines-and-standards/1972

### Data request sequence

Ask for metadata before values:

```text
meter_id_or_measurement_point
physical_scope
unit
sampling_frequency
aggregation_frequency
reporting_owner
quality_checks
missing_data_policy
```

Only then request a bounded historical extract for one decision hypothesis.

---

# 9. Energy data boundary

Boğaziçi publicly states that energy consumption is regularly measured/analyzed under an ISO 50001 Energy Management System and that an Energy Management Team coordinates the system.

Source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/724-plan-to-reduce-energy-consumption/1367

### PMR/data questions

- building vs campus vs meter granularity;
- electricity/gas/diesel source systems;
- sampling interval;
- BMS/EMS availability;
- existing thresholds/alarms;
- action tickets/work orders;
- normalized baseline method;
- verification owner.

Public evidence of measurement is not evidence of API access or controllability.

---

# 10. Standard field-level access request template

Agents should prepare requests in this format rather than asking for an entire database:

```text
Decision being tested:
Business owner:
Why the field is needed before decision time:
Requested date range:
Aggregation level:

field | semantic definition | minimum granularity | needed_at | personal data? | fallback

Expected output format:
Retention needed after pilot:
Who can validate semantics:
Who can approve access:
```

### Preferred progression

```text
public aggregate
-> owner-validated internal aggregate
-> pseudonymous/event-level only if necessary
-> individual-level only if strictly justified and approved
```

---

# 11. Agent routing

## IE

Find the **business decision owner first**. Ask them which system is authoritative and who can explain the fields.

## CS1

Do not train before a data dictionary exists. Every feature needs `source`, `available_at`, `semantic_definition`, `quality`, and `leakage_risk`.

## EE

Map physical truth to system fields. Determine which data are genuinely measured vs administrative estimates.

## EHB

Only propose sensors when the ownership map proves the required physical variable is absent or too poor in existing systems.

## CS2

Use this pack to keep access claims bounded. “The university operates BUCard/BUCampus/BUIS” is safe; “we have access to their data” is not.

## Backend

Represent owner and provenance explicitly:

```text
source_system
business_owner
technical_owner
semantic_validator
access_authority
observed_at
available_at
transformation_version
privacy_class
```

---

# 12. Source register

- BİD Service Inventory: https://bilgiislem.bogazici.edu.tr/tr/pages/hizmet-envanteri/3513
- BİD / BUCampus product surface: https://bilgiislem.bogazici.edu.tr/
- BUCampus Transport: https://bilgiislem.bogazici.edu.tr/tr/pages/ulasim/8597
- Student Affairs classroom scheduling: https://oidb.bogazici.edu.tr/tr/pages/derslikler-hakkinda/4422
- Student Affairs organizational document: https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/567-ogrenci-isleri-daire-baskanligi-20260112-095818.pdf
- Shuttle system: https://mekik.bogazici.edu.tr/
- Water Management Directive: https://kurumsalveri.bogazici.edu.tr/tr/pages/1541-water-discharge-guidelines-and-standards/1972
- Energy Management System: https://kurumsalveri.bogazici.edu.tr/tr/pages/724-plan-to-reduce-energy-consumption/1367
