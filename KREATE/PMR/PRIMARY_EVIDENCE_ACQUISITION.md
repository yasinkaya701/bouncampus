# Primary Evidence Acquisition Packet

**Updated:** 2026-10-06  
**Purpose:** convert the highest-value PMR unknowns into minimal, privacy-preserving artifact requests.  
**Boundary:** this packet is an acquisition plan. It is **not** evidence that access has been granted.

## Execution attachments

Use these focused execution sheets when contacting source owners:

- [IE_BUCARD_SKS_ACCESS_REQUEST_PACKET_2026-10-06.md](IE_BUCARD_SKS_ACCESS_REQUEST_PACKET_2026-10-06.md) — ready-to-send privacy-preserving BUCard/BİDB request, SKS reconciliation checklist, response classification and provenance log.
- [IE_CONTRACT_HAKEDIS_REQUEST_PACKET_2026-10-06.md](IE_CONTRACT_HAKEDIS_REQUEST_PACKET_2026-10-06.md) — current-contract artifact request, one-service reconstruction table, decision-rights map and #358 completion gates.

These are execution aids for this canonical packet, not new evidence registries.

## Lane A — BUCard / BİDB aggregate service truth

### Publicly verified routing

- **S-BU-021 — BİDB Service Inventory**
  - BUCard is listed as a BİDB service.
  - Official contact: `bucard@bogazici.edu.tr`.
  - Cafeteria BUCard top-up/refund services involve **SKS + BİDB**.
  - Turnstile/card-reader faults are routed to **BİDB**.
- **S-BU-022 — Kimlik BUCard**
  - BUCard is used as identity/payment infrastructure in dining halls and other campus services.
- **S-BU-023 — BUCampus Version Notes**
  - the user-facing app exposes passage history from turnstiles/card readers under **Geçişlerim**.
- **S-BU-015 — Food Services FAQ**
  - overcharge/refund troubleshooting asks for date, time, campus and turnstile;
  - QR can also be used at dining turnstiles.
- **S-BU-026 — Yemek Hizmeti Yürütme Kurulu Yönergesi**
  - Article 7 places the BUCard Office within BİDB and assigns operation/control of the dining BUCard system;
  - the BUCard Office is required to report to the Food Services Board and Food Services Branch and retain digital data;
  - Article 5(f) places meal-hakediş payment orders/accrual with the Food Services Board together with the Inspection/Acceptance Commission;
  - Article 9 identifies SKS + Administrative and Financial Affairs as the meal-service procurement route.

This now narrows the technical/report owner route beyond a service-contact hypothesis: the current university directive assigns dining-BUCard reporting/data-custody duties to the BUCard Office. It is **not** enough to mark any dataset `VERIFIED_EXPORTABLE`, determine report grain, or equate a turnstile/payment event with a physically served meal.

### Minimal first request

Ask BİDB / BUCard for a **privacy-safe aggregate report/export**, not transaction-level identities.

Target grain:

~~~text
service_date
campus_id
meal_period
reported_passage_or_meal_count
package_meal_count          # if represented
report_generated_at
source_report_id
~~~

Explicit exclusions:

~~~text
NO person name
NO T.C. identity number
NO student/personnel number
NO card identifier
NO account balance
NO row-level personal transaction history
~~~

### Technical questions for BİDB / BUCard

1. Which system stores the events shown in BUCampus **Geçişlerim**?
2. Can cafeteria readers/turnstiles be separated from library/gate/other readers?
3. What stable reader/campus identifiers exist?
4. Does one event record have event time, reader, result/status and correction/reversal state?
5. Is there an existing aggregate report by campus × meal period × service date?
6. Can that aggregate be exported without card/person identifiers?
7. Does a late correction mutate prior reports or create a new report/version?
8. What is the authoritative report/export identifier?
9. Who can approve release of an aggregate sample for a university research/pilot evaluation?
10. What retention window applies to the aggregate/report layer?

### Semantic questions for SKS / Food Services

1. What event actually means a meal was served?
2. Can one meal generate multiple card/QR events?
3. How do retries, duplicate charges, refunds and reversals appear?
4. How are second meals and staff/student/guest categories handled?
5. Does package-meal count mean requested, prepared, charged or physically collected?
6. Which count is treated as final for operational reporting?
7. At what time is a service considered reconciled/final?
8. What record is used when Food Services and BUCard counts disagree?

### Admission rule

Until both technical and semantic answers exist:

~~~text
reported_passage_count != actual_served
reservation_count != actual_served
meal_vote_count != actual_served
BUBizden_entitlement != actual_served
~~~

Issue **#292** remains the canonical live acquisition task.

---

## Lane B — IKN 2025/1727143 contract / hakediş truth

### Publicly verified facts

Current procurement source: **S-PROC-001**.

Public notice/result establish:

- current service period: 01.01.2026–31.12.2027;
- six-campus service footprint;
- listed contract quantities by breakfast/student/staff meal;
- unit-price bid / unit-price contract form;
- bidder capacity threshold of 5,000 meals/day, described as half the administration's stated daily need;
- price-only economically most advantageous offer criterion;
- TEMAŞ as awarded contractor.

None of these reveals the payable operational count or hakediş formula.

### Document retrieval status

| Artifact | Public route | Status | What it can resolve |
| --- | --- | --- | --- |
| current announcement/result | EKAP / S-PROC-001 mirrors | VERIFIED_PUBLIC | scope, contract form, contractor, dates, qualification |
| current administrative specification | EKAP IKN 2025/1727143 document bundle | **RETRIEVAL_REQUIRED** | contract administration, acceptance, price-difference and document rules |
| current technical specification | EKAP IKN 2025/1727143 technical specification | **RETRIEVAL_REQUIRED** | production/distribution/service constraints, staffing, measurement/control details |
| unit-price bid schedule | EKAP tender document | **RETRIEVAL_REQUIRED** | actual work-item structure and offered unit-price basis |
| contract / draft contract | EKAP / source owner | **RETRIEVAL_REQUIRED** | payment, acceptance, penalties, change rights |
| hakediş / acceptance form | SKS/procurement/control owner | **SOURCE_OWNER_REQUIRED** | which measured count becomes payable |
| daily production/order record | SKS/TEMAŞ operations | **SOURCE_OWNER_REQUIRED** | actual controllable quantity and freeze/revision timestamps |
| daily reconciliation report | SKS/TEMAŞ/BUCard | **SOURCE_OWNER_REQUIRED** | production–served–accepted linkage |

Public document links were traced to the official EKAP tender-document route, but the current environment cannot retrieve the underlying bundle. Record this as an **access/retrieval status**, not as missing evidence silently filled from prior contracts.

### Predecessor diff target

**S-PROC-002** records why IKN 2025/1335958 was cancelled:

- objections to the tender documents were evaluated;
- changes to some specification provisions were deemed necessary;
- an EKAP addendum could not be issued at the tender date;
- the tender authority cancelled the procurement.

Therefore the highest-value contract desk task is:

~~~text
2025/1335958 specs
        ↓ structured diff
2025/1727143 specs
        ↓
changed clauses → operational consequence → interview question
~~~

Do **not** assume any clause changed until the two authoritative bundles are compared.

### Current owner-route refinement

**S-BU-026** adds first-party governance facts for #358:
- meal-service procurement is carried out through **SKS + Administrative and Financial Affairs**;
- meal-hakediş payment orders/accrual are carried out by the **Food Services Board together with the Inspection/Acceptance Commission**.

Route current specification/service-control questions through Food Services/SKS, and route the exact acceptance/hakediş artifact and quantity basis through the Board + Inspection/Acceptance path. Keep payable quantity, exact signer sequence, freeze/change rights, penalties, economic beneficiary and software buyer authority unresolved until source-owned evidence confirms them.

### Contract-owner questions

1. Which work-item quantity is accepted for payment?
2. Who prepares, verifies and signs the hakediş?
3. Is payment tied to produced, delivered, served, accepted or another reconciled quantity?
4. What timestamp freezes the order/production quantity?
5. Can total production, campus allocation or batch size change after that point?
6. How are package, second, additional and corrected meals handled?
7. What underproduction / late-service / quality penalties apply?
8. Who economically bears unused production?
9. Which record wins when production, BUCard and acceptance counts differ?
10. Is a human-reviewed demand recommendation operationally admissible before freeze?

Issue **#358** remains the canonical acquisition task.

---

## Lane C — reservation signal boundary

Two official cases are now preserved:

- **S-BU-006** — May 2026 Kilyos holiday workflow, reservation by prior-day cutoff.
- **S-BU-025** — Jan–Feb 2024 intersession workflow across multiple campuses; published rule allowed packaged service when reservation counts were below 15.

This shows reservation workflows recur under special operating regimes. It still does **not** establish an always-on reservation system.

PMR must ask:

- which calendar/service states activate reservation;
- whether the operator sees counts before production freeze;
- whether reservation snapshots are retained/exportable;
- cancellation/no-show semantics;
- whether reservations alter production or only service packaging/distribution.

---

## Stop rule

Do not spend another research cycle on broad food-waste literature unless it resolves a named decision.

The next evidence promotion requires at least one of:

1. real aggregate BUCard/SKS sample;
2. authoritative current procurement/specification artifact;
3. source-owner answer on hakediş/acceptance;
4. real production/allocation record;
5. stage-separated service-level waste measurement;
6. completed operational interview.
