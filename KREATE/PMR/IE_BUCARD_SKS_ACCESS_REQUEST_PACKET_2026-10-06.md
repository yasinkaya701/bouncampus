# IE BUCard / SKS Service-Truth Access Request Packet

**Updated:** 2026-10-06  
**Owner:** IE — Customer Discovery & Market  
**Coordinates with:** #292, #82, #322  
**Evidence status:** request specification only; no access, export, interview, or measured-service claim is implied.

## Objective

Obtain the smallest privacy-preserving, source-owned dataset that can establish campus × meal-period × service-date demand truth and the reconciliation rules required to interpret it.

The request must stay aggregate. Do not request or retain student/staff identity, BUCard/card number, account balance, personally identifiable transaction history, or raw access-control logs.

## Routing order

1. **BUCard / BİDB** — technical/report owner route. Official public material identifies BUCard as a BİDB service and lists `bucard@bogazici.edu.tr` as a contact route.
2. **Yemek Hizmetleri / SKS** — semantic owner for what dining passages/meal transactions mean operationally and which report is accepted/final.
3. **Dining control / contractor operations** — owner route for produced quantities, allocation, shortage/early-sellout and surplus/waste records.
4. **CS1 intake** — only after source provenance and reconciliation are explicit; canonical intake is `scripts/cs1_service_truth_artifact_intake.py`.

Public source IDs supporting the route: `S-BU-021`, `S-BU-022`, `S-BU-023`, `S-BU-026`, and `S-BU-031`. These sources do **not** prove export authorization or report semantics.

## Governance-backed owner-route refinement

The current official **Yemek Hizmeti Yürütme Kurulu Yönergesi** (`S-BU-026`, Article 7) goes beyond a contact-page inference: it places the BUCard Office inside BİDB, assigns operation/control of the dining BUCard system, requires reporting to the Food Services Board and Food Services Branch, and requires retention of digital data.

Operational consequence for #292:
- `S-BU-031` confirms named existing report surfaces: **BUCard Yemekhane anlık rapor**, **günlük geçiş raporları**, and **personel yemek raporu**;
- ask BUCard/BİDB first for those reports' exact grain, field dictionary, schema/version/finality semantics, stable identifiers and aggregate/export capability;
- ask whether the mandated retained digital data preserve historical report snapshots or only the latest corrected state;
- ask Food Services/SKS to reconcile what each reported count means and which report/version is operationally final.

Boundary unchanged: governance ownership is **not** permission to access/export data, and a dining turnstile/payment event is **not** automatically `actual_served`.

## Minimum aggregate export requested

Preferred grain: exactly one row per:

`service_date × campus_id × meal_period`

Minimum fields:

| Field | Required | Why |
| --- | --- | --- |
| `service_date` | yes | chronological service key |
| `campus_id` | yes | prevents university-wide totals from masquerading as service truth |
| `meal_period` | yes | breakfast/lunch/dinner/etc. must not be collapsed |
| reported served/passage count | yes | preserve source name until semantics are verified |
| `package_meal_count` | when applicable | separate package workflow from ordinary service |
| `report_generated_at` | yes | snapshot/finality audit |
| `source_report_id` | yes | immutable provenance / reconciliation |
| report status/version | preferred | distinguishes preliminary vs accepted/final/corrected reports |

Do **not** rename a source field to `actual_served` until SKS confirms what a counted event represents.

### Requested sample size

Ask first for a small chronological sample sufficient to validate semantics and pipeline compatibility, for example several consecutive service dates across at least one campus and meal period. If the source owner can safely provide a larger window, keep the same aggregate grain and privacy boundary.

No minimum row count should be represented as achieved until real rows are received.

## Reconciliation questions for BUCard / SKS

Record answers verbatim with role/owner and date where possible.

1. Does one accepted dining BUCard passage/meal transaction always correspond to one physically served meal?
2. Which readers/transaction types are included in the dining report? Could non-dining turnstiles/readers contaminate the same event surface?
3. How are retries, duplicate charges, reversals, refunds, corrections and manual overrides represented?
4. How are student, staff, guest, second-meal and other categories represented or aggregated?
5. Is package-meal count a reservation/sale, preparation count, or physical pickup count?
6. Which report state is considered authoritative/final by Food Services, and when does it become final?
7. Can corrected reports preserve a stable source ID and version/revision timestamp?
8. Can the report be exported at campus × meal-period × service-date granularity?
9. Are historical report snapshots retained, or only the latest corrected state?
10. Is there a source-owned field that directly denotes served meals, or must BUCard events be reconciled with another record?

## Parallel production/outcome request

For the same service grain, ask the operational owner whether the following source-owned records exist:

- `produced_portions`
- campus/service allocation
- `actual_surplus_portions` and/or accepted `waste_kg`
- `shortage_or_early_sellout`
- pre-service operator/status-quo quantity
- quantity request/order version + timestamp
- accepted/reconciled outcome flag
- source record/report ID

The first priority is an existing owner-generated record. New sensing is fallback work for EE/EHB only after an existing record path is shown insufficient.

## Ready-to-send request text — technical/data owner

> Merhaba, Boğaziçi Üniversitesi yemekhane operasyonlarında talep/üretim kararını anlamaya yönelik öğrenci projemiz için yalnızca anonim ve toplulaştırılmış bir rapor örneği talep ediyoruz. Kişi, öğrenci/personel kimliği, kart numarası, bakiye veya kişisel işlem geçmişi istemiyoruz. Mümkünse her satırın tarih × kampüs × öğün düzeyinde olduğu; raporda kullanılan servis/geçiş sayısı, varsa paket yemek sayısı, rapor üretim zamanı ve sabit rapor kimliği alanlarını içeren küçük bir kronolojik örnek yeterlidir. Ayrıca bu sayıların hangi işlem tiplerini kapsadığı ve düzeltme/iptal/iade durumlarının rapora nasıl yansıdığı bilgisini teyit etmek istiyoruz. Bu verinin paylaşımı mümkün değilse, hangi birimin/veri sahibinin değerlendirmesi gerektiğini ve uygun anonimleştirilmiş alternatif granülerliği belirtmeniz de bizim için çok değerli olacaktır.

This wording is a request draft, not proof that it was sent.

## Ready-to-use SKS semantic checklist

For one specific recent service, reconstruct:

`planned/requested quantity → produced quantity → campus allocation → BUCard/passage report → physically served → surplus/waste → correction/finality`

Capture for each step:

- owner role;
- system/form/report name;
- timestamp;
- unit;
- when it becomes final;
- correction path;
- whether the record is exportable in aggregate;
- whether it is accepted for operational/financial reconciliation.

## Response classification

Every outreach attempt or source-owner answer should be classified as one of:

- `GRANTED`
- `DENIED`
- `UNAVAILABLE`
- `FOLLOW_UP_REQUIRED`
- `WRONG_OWNER_REFERRED`
- `PENDING`

Do not use `VERIFIED_EXPORTABLE` until the owner confirms exportability and an export/sample or equivalent source-owned evidence exists.

## Provenance log template

| Field | Value |
| --- | --- |
| request date/time | |
| requesting team member | |
| contacted role/unit | |
| contact route | |
| response date/time | |
| access status | |
| artifact/report title | |
| source_report_id semantics | |
| report_generated_at semantics | |
| grain confirmed | |
| reconciliation owner | |
| privacy constraints | |
| received artifact location/checksum | |
| next action | |

## Handoff gates

### To CS1

Only hand off a candidate `SERVICE_TRUTH_V1` package when:

- source privacy is aggregate and acceptable;
- service grain is explicit;
- chronological rows are real and source-owned;
- report timestamp/source ID semantics are known;
- BUCard/passages are reconciled enough to determine whether they can represent served demand;
- no missing field is silently fabricated.

### To CS2

Hand off only verified facts about:

- who owns the report;
- who controls the quantity decision;
- what can change before freeze;
- whether the workflow can host a human-reviewed recommendation.

Do not infer willingness-to-pay or savings.

### To EE/EHB

Escalate a missing measurement field only after confirming that no existing source-owned operational record can supply it with acceptable timing/quality.

## Stop conditions

Stop and record the blocker rather than inventing evidence if:

- only person/card-level raw data is offered and aggregation cannot be performed by the owner;
- only university-wide daily/monthly totals are available;
- report semantics cannot distinguish dining events from unrelated passages;
- only reservation intent exists without served/reconciled outcome;
- production/waste records are incomparable in time or unit and the owner cannot reconcile them.

The correct result may be a documented `DENIED` or `UNAVAILABLE` outcome. That is still valuable PMR because it changes product/data architecture.
