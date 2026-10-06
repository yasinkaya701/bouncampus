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
