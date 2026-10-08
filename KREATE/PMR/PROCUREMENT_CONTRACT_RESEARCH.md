# PMR Procurement & Contract Research

**Updated:** 2026-10-06  
**Status:** public/secondary procurement research — **not** interview evidence and **not** contract interpretation.

## Current procurement anchor

The current public procurement trail identifies **IKN 2025/1727143** for Boğaziçi University's 2026–2027 "Malzeme Dahil Kahvaltı, Yemek Hazırlama ve Dağıtım Hizmeti Alımı".

Public tender/result mirrors report:

- administration: Boğaziçi University Health, Culture and Sports Department;
- service period: 01.01.2026–31.12.2027;
- service footprint: North, South, Kilyos, Kandilli, Hisar and Anadolu Hisarı campuses;
- listed quantities: **2,500,000 student meals + 380,000 breakfasts + 250,000 staff meals**;
- result: **TEMAŞ Gıda Sanayi ve Ticaret A.Ş.**;
- public result reports a contract dated 25.12.2025.

Canonical PMR source: `S-PROC-001`.

### What this materially changes

The PMR buyer/workflow map is no longer a generic "university cafeteria" abstraction. At minimum there are distinct roles/interfaces to test:

~~~text
Boğaziçi SKS / Food Services
→ contract / procurement / acceptance authority
→ official dining control organization
→ TEMAŞ contractor operations / production planning
→ BUCard / digital-report owner
→ campus/service execution
~~~

The key product question is therefore:

> Which party can change which quantity, before which freeze point, using which source-owned record, and who economically benefits or bears risk when quantity is wrong?

## Historical contractor continuity / clause provenance

Public procurement history shows TEMAŞ also appears as the awarded contractor for the preceding **2024–2025** Boğaziçi food-service procurement (IKN 2023/1144278).

Source: `S-PROC-003`.

An archived procurement-decision record for that prior tender (`S-PROC-004`) exposes useful historical technical-specification context, including North Campus kitchen production and continuity/backup-kitchen requirements.

This changes PMR targeting in two ways:

1. TEMAŞ appears to be an **incumbent across consecutive contract periods**, so the team should ask about an existing working relationship and established planning/acceptance routines rather than assuming a new-vendor onboarding context.
2. Historical specifications show that production location, continuity capacity and operational control can be contractually explicit.

Strict boundary: **do not copy prior-period clauses into the current contract model**. They are question generators only until the 2025/1727143 technical/admin specifications are retrieved.

## Tender mechanics visible in the public notice

The public notice/result mirror additionally records:

- bidder qualification included a capacity report threshold sufficient for **5,000 meals/day**;
- award criterion was stated as **price-based**;
- result record reports **14 bids / 7 valid bids**.

Interpretation boundary:

- the 5,000-meal figure is a **bidder capacity qualification**, not the university's actual daily production, a guaranteed order, or a service-level target;
- price-based award does not tell us who captures operational savings after award;
- bid counts do not establish switching willingness or software budget.

These facts sharpen PMR around where a decision-support tool would enter: university-side contract/acceptance, contractor-side operations, or a future procurement/specification cycle.

### Unit-price contract form

The public notice states that bids are formed from **each work item's quantity × offered unit price** and that the resulting agreement is a **unit-price contract**.

This is a major PMR constraint, but not yet a settlement answer.

We still need to learn:

- the actual unit-price schedule by work item;
- which quantity becomes payable/accepted;
- whether payment follows produced, delivered, served, accepted or another reconciled count;
- how package/second/additional meals and corrections enter hakediş;
- whether daily/campus allocations can change without changing the contractual item quantity.

The same notice describes a 5,000-meal/day bidder-capacity threshold as one-half of the administration's stated daily meal need. Treat that as **procurement capacity context only**, not measured actual daily demand.

### Public schedule mirror: line-item ambiguity

A second EKAP-derived public mirror (`S-PROC-005`) confirms the current tender's **unit-price contract** form and exposes three identifiable meal rows:

- 380,000 student breakfasts;
- 2,500,000 student meals;
- 250,000 staff meals.

The same public schedule surface also exposes **additional monthly rows** whose descriptions are not sufficiently visible in the mirror to determine what they represent. The public surface is therefore **not complete enough to reconstruct the awarded unit-price schedule or settlement model**.

Operational implication:

- do not assume the three meal rows are the only priced work items;
- do not infer that campus allocation, staffing, service, equipment or other monthly obligations are absent merely because their descriptions are not visible in the mirror;
- do not use the public schedule to derive awarded unit prices, contractor margin, meal cost or savings;
- retrieve the authoritative EKAP administrative/technical specification, unit-price bid schedule and contract/acceptance documents before clause-level or economic claims.

This ambiguity strengthens, rather than closes, #358.

### Retrieval attempt status

The public tender mirror exposes links that redirect to the official EKAP tender-document route for **IKN 2025/1727143**. The current environment can resolve the route but cannot retrieve the underlying document bundle.

Record this as:

~~~text
current announcement/result: VERIFIED_PUBLIC
current admin specification: RETRIEVAL_REQUIRED
current technical specification: RETRIEVAL_REQUIRED
current unit-price schedule: RETRIEVAL_REQUIRED
current contract/acceptance clauses: RETRIEVAL_REQUIRED
~~~

Do not backfill current clauses from the 2023/2024–2025 procurement.

#### Resolved official EKAP acquisition route — 2026-10-06

A fresh retrieval pass resolved the mirror's document buttons to the official EKAP citizen-document endpoint and exposed the stable tender document identifier:

~~~text
IKN: 2025/1727143
official EKAP ihaleId:
8a0a0df8b81eaca6a907dc1db667be87d30732baf3af5797db5e5db12c7b3edc
~~~

Resolved routes:

- current tender document bundle (`İhale Dokümanı`):
  `https://ekap.kik.gov.tr/EKAP/Ortak/VatandasIlanGoruntuleme.aspx?ddac=true&aramaDownload=true&ihaleId=8a0a0df8b81eaca6a907dc1db667be87d30732baf3af5797db5e5db12c7b3edc&wots=false&Iszylnm=false`
- bundle exposed by the mirror as `Teknik Şartname Hariç Doküman`:
  `https://ekap.kik.gov.tr/EKAP/Ortak/VatandasIlanGoruntuleme.aspx?ddac=true&aramaDownload=true&ihaleId=8a0a0df8b81eaca6a907dc1db667be87d30732baf3af5797db5e5db12c7b3edc&wots=true&Iszylnm=false`
- current EKAP search route:
  `https://ekapv2.kik.gov.tr/ekap/search/2025_1727143`

Discovery route:
`https://ekapveri.com/ihale/ekap-2025-1727143/`

The browser environment could resolve the redirect target but could not fetch the official document payload. Therefore this is a **routing improvement**, not artifact retrieval. Keep the authoritative documents at `RETRIEVAL_REQUIRED` until a human/authorized environment successfully downloads the bundle and records title/version/checksum.

The mirror also explicitly labels the current tender with `Düzeltme İlanı: Var`. Do not infer the affected clause. The correction/zeyilname history remains a separate required acquisition artifact.

### Predecessor cancellation is now explicit

For **IKN 2025/1335958**, the public cancellation notice states that objections to the tender documents required changes to some specification provisions, but an EKAP addendum could not be issued at the tender date, so the tender was cancelled.

That gives a concrete next desk artifact task: obtain both predecessor and current authoritative specification bundles and make a clause-level diff. The cancellation notice does **not** identify the changed clauses.

See [PRIMARY_EVIDENCE_ACQUISITION.md](PRIMARY_EVIDENCE_ACQUISITION.md).

## Do not infer settlement from the headline contract

The public result is sufficient for **scope, contractor and procurement-route context**. It is not sufficient for:

- unit prices;
- accepted/paid quantity;
- daily committed quantity;
- minimum purchase;
- production-loss allocation;
- shortage penalties;
- quality penalties;
- acceptance/hakediş workflow;
- campus-allocation change rights;
- invoice/reconciliation fields.

Never divide total contract value by total listed meals and call the result "meal cost" or "hakediş price".

## Predecessor procurement signal

The public trail for **IKN 2025/1335958** indicates an earlier procurement with the same headline meal quantities was cancelled after objections required specification changes and a zeyilname could not be issued in time.

Source: `S-PROC-002`.

Use this only as a prompt to retrieve both sets of authoritative procurement documents and ask:

- what specification clauses changed?
- did any changed clause concern production, delivery, staffing, food safety, acceptance, penalties or quantity?
- which constraints are operationally binding today?

Do not claim the cancellation was caused by forecasting, waste, technology or data requirements.

## Official operational routing

Useful first-party routes now in the catalog:

- Food Services contact: `S-BU-010`;
- Food Services staff/role page: `S-BU-011`;
- dining cooking/distribution control organization: `S-BU-014`;
- Food Services FAQ / BUCard correction context: `S-BU-015`;
- service windows: `S-BU-016`.

These are **interview-routing evidence**, not proof that any named public role owns the specific decision.

## Canonical first-party procurement and hakediş routes

The current IE source map separates four first-party routing/evidence surfaces instead of overloading one source ID:

- **S-BU-029 — İhale ve Satınalma Şube Müdürlüğü:** procurement/tender document ownership and referral route.
- **S-BU-027 — Tahakkuk Şube Müdürlüğü:** tender/direct-procurement/transfer/hakediş payment route.
- **S-BU-028 — İMİD contact:** general fallback routing.
- **S-BU-030 — 2025 Administration Activity Report:** institutional Control Organization → KİK56.0/H acceptance proposal → relevant Spending Authority → hakediş-preparation flow; explicitly includes food-service procurement among recurring service works.

The current Food Services directive remains **S-BU-026** and is a distinct governance source. Do not reuse S-BU-026 for an İMİD page.

Decision boundary:
- these sources narrow **where to ask** and the generic institutional acceptance path;
- they still do not reveal the current IKN 2025/1727143 payable meal count, accepted quantity, exact Spending Authority, signer chain, daily freeze/change rights, penalties, unit prices, economic-risk owner or software buyer;
- the authoritative current tender bundle and real acceptance/hakediş artifact remain required.

## Contract-PMR question set

Ask for one recent concrete service first, then reconstruct the documents and decisions:

1. Who entered/requested the first quantity and in which system/document?
2. Who approved or accepted it?
3. When could TEMAŞ still change total production? Campus allocation? Batch size?
4. Which quantity/record is used for acceptance and hakediş?
5. Which party loses economically if excess remains? Who bears shortage/early-sellout consequences?
6. Are quantities committed per day, meal period, campus, menu item or another unit?
7. How are additional meals, second meals, package meals, cancellations and corrections handled?
8. Which report is authoritative when BUCard/turnstile counts disagree with production/acceptance records?
9. What penalty/quality/service-level clauses make underproduction riskier than overproduction, if any?
10. Could a human-reviewed recommendation legally/operationally change the accepted quantity before freeze?

## Artifact acquisition backlog

Highest-value contract artifacts:

- authoritative EKAP administrative specification;
- technical specification;
- unit-price bid schedule;
- contract / acceptance language;
- penalty/service-level clauses;
- acceptance/hakediş forms or schema;
- current production request/order form;
- current daily reconciliation report.

Store canonical links/checksums where redistribution permits. If documents are access-controlled, record only the IKN, requested artifact, owner, retrieval status and the narrow fact needed.

## Evidence firewall

Public procurement establishes a real current contractor relationship and procurement surface. It does **not** establish product-market fit, willingness to buy, accessible APIs/data, forecast error, quantity flexibility or savings.
