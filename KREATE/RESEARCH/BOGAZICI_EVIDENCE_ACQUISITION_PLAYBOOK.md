# Boğaziçi Dining Evidence Acquisition Playbook

**Research date:** 2026-10-01  
**Purpose:** Convert the remaining P0 dining unknowns into the smallest possible artifact, aggregate-data or owner-confirmation requests so agents stop web speculation and acquire decision-grade evidence.  
**Status:** Research/acquisition plan. **No request has been sent. No document access, interview, approval or data availability is claimed. Not legal advice.**

## Executive conclusion

Secondary research has reached a useful stopping point for the highest-value dining questions.

Public sources establish:

- current TEMAŞ unit-price procurement and meal-volume scale;
- special-period reservation/cancellation capability;
- digital meal-access signals;
- a historical service-mode rule tied to reservation count;
- formal Food Services, Control Organisation, procurement/payment and sustainability-governance roles;
- a current governance obligation around production planning and monthly `produced / consumed / discarded` food reporting.

But public web sources do **not** establish the critical current operational facts:

```text
which quantity is chosen before service
who chooses it
when it freezes
which quantity is accepted as contractual truth
which quantity drives hakediş/payment
which aggregate signal exists before freeze
which physical waste stage changes after the decision
```

Those questions now require **artifact acquisition or primary research**, not another generic search.

---

# 1. Acquisition principles

## A. Ask for the smallest evidence object

Do not ask a unit to “send all dining data” or “share the contract”. Ask for the minimum artifact or field definition that resolves one decision gate.

Preferred pattern:

```text
unknown
→ narrow owner
→ minimum evidence object
→ source/definition/timestamp
→ downstream gate
→ stop
```

## B. Start with normal owner routes

Use a formal information-request route only after the operational/procurement owner cannot provide or direct the team to the relevant public/accessible artifact.

## C. Aggregate before transfer

For BUCard/reservation/service data, prefer **source-owner aggregation** by service episode. Do not request individual student histories where aggregate counts answer the question.

## D. Separate operational truth from money flow

Never infer contractor settlement from:

- student/personnel BUCard charge;
- published diner price;
- planned production;
- turnstile count;
- procurement contract total.

Each is a different economic/event object until reconciled.

## E. A refusal is evidence about feasibility

`Not retained`, `not exportable`, `cannot be shared`, or `owned by another unit` are valid findings. Record them; do not route around the owner by seeking unnecessary personal data.

---

# 2. Evidence acquisition ladder

Use the first route that can resolve the question.

## Level 1 — Food Services Branch

Best for:

- daily quantity/service workflow;
- reservation use;
- production/request freeze;
- contractor coordination;
- current technical-specification owner;
- which unit owns acceptance/hakediş records.

Minimum first question:

> For one normal lunch, what exact quantity is communicated before service, who sets it, when does it freeze, and what document/system records it?

Do not start by asking for an AI pilot.

## Level 2 — TEMAŞ local project / kitchen operator

Best for:

- production-plan transformation;
- buffer/safety-stock logic;
- batch/replenishment constraints;
- campus dispatch/allocation;
- internal produced/delivered/surplus records;
- latest timestamp at which a signal can still affect operations.

Minimum first evidence object:

> One redacted/example daily planning or production record with field definitions, not customer/user-level information.

## Level 3 — Dining/Cooking/Distribution Control Organisation

Best for:

- accepted operational truth;
- shortage/deviation/substitution records;
- contract-control evidence;
- which record is trusted when contractor/university counts differ;
- approval boundary for service changes.

Minimum first evidence object:

> Blank or redacted example of the service acceptance/control/deviation form, plus the meaning of each quantity field.

## Level 4 — Tahakkuk Şube Müdürlüğü

`PUBLIC SOURCE`

Boğaziçi University's Tahakkuk Branch publicly states that it performs university **tender, direct-procurement, transfer and progress-payment (`hak ediş`) payments** and archives expenditure files.

Primary source:
https://imid.bogazici.edu.tr/tr/pages/tahakkuk-sube-mudurlugu/2119

Best for:

- what document triggers current meal-service hakediş payment;
- whether quantity is visible in the payment packet;
- who provides/signs the underlying accepted quantity;
- where correction/adjustment records live.

**Do not request financial/personnel information that is not needed.**

Minimum question:

> For the current food-service contract, which aggregate service/acceptance quantity or document is the basis of the hakediş payment packet, and which unit originates that record?

Minimum artifact if available:

- blank/redacted hakediş summary template; or
- data dictionary / field names for quantity basis; or
- the exact current contract/specification clause defining payment quantity.

This is higher value than requesting an invoice total.

## Level 5 — İhale ve Satınalma Şube Müdürlüğü

Official IMID materials describe the Procurement Branch as carrying out tenders/EKAP processes and preparing hakediş-related documents for procured work.

Primary sources:

- https://imid.bogazici.edu.tr/
- https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/50-bogazici-universitesi-idari-ve-mali-isler-dai-20250407-160510.pdf

Best for:

- current signed contract/specification provenance;
- which document/version is authoritative for İKN `2025/1727143`;
- quantity/order/acceptance/payment clauses;
- whether public access exists to the relevant contract sections.

Minimum artifact request:

> The current authoritative clause(s) defining requested/accepted meal quantity, hakediş basis, excess/shortage treatment and revision authority for İKN `2025/1727143`, rather than the entire procurement file if unnecessary.

## Level 6 — BİD / BUCard source owner

Best for:

- whether reservation-created/cancelled/active-at-cutoff events exist;
- privacy-safe aggregate BUCard/QR service counts;
- timestamps/retention;
- source-owner aggregation feasibility.

Minimum dataset request:

```text
service_date
campus
meal_period
reservation_created_count
reservation_cancelled_before_cutoff
active_reservations_at_cutoff
aggregate_validated_entry_count
```

No user identifier is needed for Pilot 0.

## Level 7 — Safe & Sustainable Food / monthly reporting owner

Best for:

- data source behind directive-required `produced / consumed / discarded` monthly reporting;
- definitions and granularity;
- reconciliation with contractor/BUCard/waste data;
- which report reaches Rectorate/governance.

Minimum artifact:

> A blank/redacted monthly food-flow reporting template or data dictionary showing definitions and source systems for `produced`, `consumed` and `discarded`.

## Level 8 — Formal Bilgi Edinme fallback

`PUBLIC SOURCE`

Boğaziçi's official Information Acquisition page states that formal requests are handled by the Yazı İşleri Branch through the online request form or fax. It states the requested information/document is normally notified before **15 business days**, with a **30-business-day** window when multiple institutions/units are involved and the extension is communicated.

Primary source:
https://bilgiedinme.bogazici.edu.tr/tr/pages/bilgi-edinme-basvuru-sayfasi/5333

Use this only for **narrow public-document access** after the normal owner route fails or points here.

Good fallback target:

- authoritative current publicly releasable contract/specification clause;
- public institutional directive/report template;
- information on which unit/document contains the requested definition.

Bad use:

- fishing for all transaction data;
- requesting personal/student histories;
- treating formal access deadlines as product execution timelines;
- using the process to bypass a legitimate data-access restriction.

---

# 3. P0 acquisition queue by product gate

## AQ-01 — Current quantity owner + freeze time

**Unknown resolved:** who sets the operational quantity/action before service and when it becomes costly to change.

Primary owner route:

1. Food Services;
2. TEMAŞ local operations;
3. Control Organisation for approval/accepted-record boundary.

Minimum evidence:

```text
one real recent service example
quantity field name
owner role
first communication timestamp
final revision/freeze timestamp
allowed adjustment dimensions
source system/document
```

Acceptable evidence:

- owner-confirmed workflow tied to a named current artifact; or
- redacted planning/request record + data dictionary.

Stop condition:

If quantity/service mode/allocation is not adjustable before usable signals arrive, stop quantity-forecast product work and test another control surface.

## AQ-02 — Current hakediş / accepted quantity

**Unknown resolved:** which quantity is economically/contractually accepted and paid.

Primary route:

1. Food Services / Control Organisation for accepted service;
2. Tahakkuk for payment packet/basis;
3. Procurement for authoritative current clause;
4. formal Information Acquisition only for narrow public-document fallback.

Minimum evidence:

```text
field_or_clause_name
quantity_semantics
source_document
who_originates_it
who_approves_it
monthly_or_daily_aggregation
correction_policy
```

Do **not** ask for bank/payment details or person-level data.

Promotion gate:

No `TRY saved per avoided meal` or contractor-P&L claim before this is resolved together with verified unit-price/variable-cost semantics.

## AQ-03 — Historical reservation → realized service reconciliation

**Unknown resolved:** whether explicit intent leaves material residual uncertainty.

Primary route:

1. Food Services for special-period context;
2. BİD/BUCard for source-owner aggregates;
3. Control Organisation/service record for realized truth.

Minimum historical sample:

```text
service_date
campus
meal_period
active_reservations_at_cutoff
reservation_cancellations
aggregate_validated_served_or_entry_count
service_regime
```

Ideal first periods:

- 2024 inter-semester reservation regime;
- 2026 Kilyos holiday reservation regime;

only if records still exist and owners allow aggregate use.

Stop condition:

If reservation is already within accepted operational tolerance and no other decision remains, do not build residual ML for its own sake.

## AQ-04 — Physical surplus/waste boundary

**Unknown resolved:** whether the decision changes an addressable waste stage.

Primary route:

- Food Services / kitchen;
- waste-measurement owner;
- Control Organisation when service records matter.

Minimum data dictionary:

```text
produced
served
edible_unserved_surplus
preparation_waste
plate_waste
collected_waste
measurement_method
measurement_timestamp
campus_meal_linkability
```

Stop condition:

If addressable pre-consumer surplus cannot be distinguished or measured at the decision boundary, claim only demand/service optimization until a prospective measurement protocol exists.

## AQ-05 — Directive-required monthly food-flow report

**Unknown resolved:** whether existing governance already reconciles production/consumption/discarded data and whether a product gap exists.

Primary route:

- current Safe & Sustainable Food governance/report owner;
- Food Services for source records;
- Corporate/administrative data owner only if current owner routes there.

Minimum artifact:

```text
blank_report_template_or_schema
metric_definitions
source_systems
reporting_granularity
reporting_period
manual_steps
review_owner
```

Product consequence:

- if already fully automated and decision-useful → provenance/reporting is not the wedge;
- if manual but low pain → also not necessarily a market;
- if reconciliation materially delays/errors operational decisions → test value separately.

---

# 4. Acquisition request template

Keep first requests short and artifact-specific.

```text
Context:
We are mapping the current dining planning workflow for a bounded research/hackathon study.

Question:
[one narrow decision/definition question]

Minimum evidence requested:
[one document/template/aggregate field set]

Data-minimization boundary:
No student/person-level information is requested. Aggregate or redacted material is sufficient.

Why needed:
This determines [specific product/pilot gate].

If your unit does not own this:
Which unit/document is authoritative?
```

Do not bundle AQ-01 through AQ-05 into one initial message.

---

# 5. Evidence promotion contract

## PUBLIC_SOURCE

Promote only a claim directly supported by an inspected public/current artifact.

## INTERVIEW

Requires completed interview notes and a narrow claim tied to the speaker's role/knowledge.

## CURRENT_CONTRACT_EVIDENCE

For payment/order/penalty claims, require current signed contract/current technical-admin specification or direct current-owner confirmation tied to the authoritative artifact.

## TECH_TEST

Requires actual run output, method version, dataset provenance, test split/period and limitations.

## MODEL_RESULT

Never becomes measured impact by itself.

---

# 6. Evidence-stop rules

Stop public web research for a P0 question when:

- the authoritative current document is not publicly indexed;
- multiple public sources only repeat tender metadata without the needed clause;
- a current owner/data dictionary is required to resolve semantics;
- further search results are derivative mirrors rather than stronger evidence.

Then move the item to the acquisition queue.

This prevents a common failure mode:

```text
lack of evidence
→ more searching
→ weaker derivative sources
→ accidental certainty
```

Correct flow:

```text
lack of C1/current evidence
→ mark UNKNOWN
→ acquire minimum artifact / owner confirmation
→ update evidence registry
→ only then implement economic/decision claim
```

---

# 7. Current highest-value acquisition sequence

If the team can only do four things, do these:

1. **Food Services:** identify current quantity/service-mode owner and freeze time from one recent meal service.
2. **TEMAŞ:** identify how `R/history/request → produced quantity` works and what can still change after initial planning.
3. **Control + Tahakkuk/Procurement:** identify accepted service record and the quantity/clause that drives hakediş.
4. **BİD + reporting owner:** acquire aggregate reservation/served sample and the produced/consumed/discarded data dictionary.

These four results are more valuable than another competitor scan or another model paper.

---

# 8. Source notes

Official public routing evidence used in this playbook:

- Tahakkuk Branch: https://imid.bogazici.edu.tr/tr/pages/tahakkuk-sube-mudurlugu/2119
- IMID / Procurement governance: https://imid.bogazici.edu.tr/
- IMID duties directive: https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/50-bogazici-universitesi-idari-ve-mali-isler-dai-20250407-160510.pdf
- Current administrative organisation: https://bogazici.edu.tr/tr/pages/bogazici-universitesi-idari-organizasyon-sema/813
- Formal Information Acquisition: https://bilgiedinme.bogazici.edu.tr/tr/pages/bilgi-edinme-basvuru-sayfasi/5333

Related repo packs are indexed in `RESERVATION_DECISION_INDEX.md`.