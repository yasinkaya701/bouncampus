# IE External Acquisition Runbook

**Updated:** 2026-10-06  
**Owner:** IE — Customer Discovery / Operations  
**Active issues:** #292, #358  
**Parent data dependency:** #82  
**Evidence rule:** this runbook prepares and records acquisition. A prepared request, scheduled call, public contact page, or public procurement summary is **not** primary operational evidence.

## 1. Why this lane exists

Generic PMR browsing is no longer the bottleneck. The remaining high-value IE unknowns require source-owner evidence:

1. a privacy-preserving service-level BUCard/SKS export with reconciled count semantics;
2. current IKN 2025/1727143 contract/specification and acceptance/hakediş semantics;
3. the real production/allocation record and the person/system that can change it before freeze.

Until these are obtained, do not claim measured forecast lift, pilot readiness, savings, controllable overproduction reduction, or contract-economic benefit.

## 2. Confirmed first-party routing surface

These routes were rechecked against official Boğaziçi pages on 2026-10-06.

| Route | First-party contact / location | Use | Does not prove |
| --- | --- | --- | --- |
| BUCard / BİDB | `bucard@bogazici.edu.tr`; BUCard Office under Bilgi İşlem Daire Başkanlığı | ask for privacy-safe aggregate reporting owner/export path | that an export exists or is accessible |
| Food Services | `yemekhane@bogazici.edu.tr`; +90 212 359 4460 / 6729 / 6730 | semantic owner for dining service, production, package-meal and served-count reconciliation | exact quantity owner or hakediş signer |
| Food Services branch manager | Aygül Demir Yolasığmazoğlu — public role page | route one concrete recent-service reconstruction and referrals | that the role personally owns every decision |
| SKS | `sks@bogazici.edu.tr`; +90 212 359 4515 | escalation / organizational routing | contract interpretation by itself |
| Dining control organization | official University Management Board page lists the `Yemekhane, Yemek Pişirme ve Yemek Dağıtım Kontrol Teşkilatı` | identify acceptance/control workflow and record owners | current clause semantics without the actual documents |

Official source pages:
- https://bucard.bogazici.edu.tr/
- https://bilgiislem.bogazici.edu.tr/tr/pages/hizmet-envanteri/3513
- https://yemekhane.bogazici.edu.tr/iletisim
- https://yemekhane.bogazici.edu.tr/people
- https://sks.bogazici.edu.tr/tr/contact
- https://bogazici.edu.tr/tr/pages/universite-yonetim-kurulu-kurul-ve-komisyonla/246

## 3. Acquisition sequence

Use the sequence below. Do not shotgun the same long questionnaire to every contact.

### Step A — Food Services first

Objective: reconstruct **one real recent service** end-to-end and identify the exact record owners.

Ask:
1. For a recent campus × meal-period service, what quantity was first requested/planned?
2. Who entered it, where, and when?
3. What could still be changed after that point: total production, campus allocation, batch size?
4. What record contains produced portions?
5. What record contains delivered/allocated portions?
6. Which record is treated as final served/accepted count?
7. How are leftovers/surplus and shortages recorded?
8. Which person/unit can explain BUCard count corrections?
9. Which person/unit owns hakediş/acceptance?
10. Which local TEMAŞ operations counterpart should be interviewed?

Output: owner + system/document + grain + timestamp semantics for each field. Do not infer ownership from job titles.

### Step B — BUCard/BİDB aggregate export

Objective: obtain only the minimum aggregate service-level data needed for #292/#82.

**Requested grain:** one row per `campus_id × meal_period × service_date`.

Preferred fields:

```text
service_date
campus_id
meal_period
reported_service_or_passage_count
package_meal_count
report_generated_at
source_report_id
```

Privacy guardrail — explicitly do **not** request:
- card number;
- student/person identifier;
- T.C. identity number;
- name;
- balance;
- individual transaction history;
- per-person meal history;
- row-level personal timestamps when unnecessary for the aggregate export.

Required reconciliation questions:

1. What event increments the reported count?
2. Does an accepted passage/payment always mean one physically served meal?
3. How are retries, duplicate charges, reversals and refunds represented?
4. Are second meals distinguishable?
5. Are student/staff/guest channels combined or separable?
6. What exactly does package-meal count represent: reservation, sale, preparation, handoff or pickup?
7. How are campus and meal-period boundaries assigned?
8. Can late corrections/backfills change past rows?
9. Which report state is final/reconciled?
10. Can each export carry stable `source_report_id` and `report_generated_at`?

Do not rename the count to `actual_served` until Food Services confirms the semantics.

### Step C — current contract / acceptance / hakediş

Anchor: IKN **2025/1727143**.

Request authoritative copies or source-owner answers for:
- administrative specification;
- technical specification;
- unit-price bid schedule;
- final contract / relevant acceptance clauses;
- penalty / SLA clauses;
- acceptance / hakediş form or schema;
- daily production request/order form;
- daily reconciliation / acceptance report.

If a document cannot be shared, record:
- exact artifact title/version;
- IKN;
- owner;
- canonical retrieval route;
- access status;
- the narrow fact that must be answered.

Questions that must be resolved:

1. What unit/quantity is accepted for payment?
2. Who signs/approves acceptance and hakediş?
3. Is the payable/accepted quantity produced, delivered, served, ordered, reconciled, or another quantity?
4. At what grain is quantity committed: day, meal period, campus, menu item, contractual line item, other?
5. When can total production still change?
6. When can campus allocation still change?
7. Is there a minimum/committed quantity?
8. Who bears the economic consequence of overproduction?
9. What happens on shortage/early sellout/late delivery/quality failure?
10. Which record is authoritative when BUCard, production and acceptance records disagree?
11. Can a human-reviewed recommendation operationally alter the relevant quantity before the freeze point?

Never derive a unit meal price by dividing headline contract value by listed quantities.

### Step D — contractor local operations referral

Do not treat a generic company inbox as proof of the Boğaziçi account owner.

Ask Food Services/control/procurement contacts for the local TEMAŞ counterpart responsible for:
- daily production planning;
- batch/replenishment decisions;
- campus allocation;
- operational reconciliation;
- contract acceptance/hakediş coordination.

Then reconstruct the same recent service from the contractor side and compare the two accounts.

## 4. Ready-to-send request text

### 4.1 BUCard/BİDB routing request

**Subject:** Boğaziçi Yemekhane için kişisel veri içermeyen toplu BUCard raporu hakkında

Merhaba,

Boğaziçi Üniversitesi kampüs yemekhanelerinde talep/üretim planlamasına yönelik öğrenci projesi kapsamında, kişisel veri içermeyen **toplu** bir BUCard raporunun mevcut olup olmadığını ve doğru veri sorumlusunu öğrenmek istiyoruz.

İhtiyacımız kişi/kart/öğrenci bazlı işlem değildir. Tercih edilen çıktı yalnızca her **kampüs × öğün × hizmet tarihi** için toplam geçiş/servis sayısı; varsa paket yemek sayısı; rapor üretim zamanı ve kararlı bir rapor kimliğidir.

Özellikle kart numarası, isim, öğrenci/personel kimliği, bakiye veya kişisel işlem geçmişi istemiyoruz.

Böyle bir toplu rapor varsa, raporun teknik sahibi ve erişim/izin süreci konusunda bizi doğru kişiye yönlendirebilir misiniz? Ayrıca sayımın iade, tekrar deneme, ikinci yemek ve sonradan düzeltmeleri nasıl ele aldığına ilişkin semantik doğrulama için Yemek Hizmetleri ile birlikte çalışacağız.

Teşekkürler.

### 4.2 Food Services operational reconstruction request

**Subject:** Yemekhane üretim–servis kayıt akışını anlamak için kısa görüşme talebi

Merhaba,

Boğaziçi yemekhanelerinde bir öğünün planlanan miktardan üretim, kampüs dağıtımı, servis ve kalan/atık kaydına kadar nasıl ilerlediğini doğru anlamaya çalışıyoruz.

Hipotetik ürün soruları yerine tek bir yakın tarihli öğünü örnek alarak şu kayıt akışını anlamak istiyoruz: ilk planlanan miktar → değişiklik/freeze noktası → üretilen miktar → kampüslere ayrılan/teslim edilen miktar → servis/BUCard sayımı → kalan/atık → kabul/hakediş.

15–20 dakikalık kısa bir görüşmede bu kayıtların hangi sistem/formlarda tutulduğunu ve doğru sorumluların kim olduğunu öğrenebilirsek yeterli olacaktır. Kişisel öğrenci/veri talep etmiyoruz.

Uygun kişiye yönlendirebilir misiniz?

Teşekkürler.

### 4.3 Contract/specification request

**Subject:** İKN 2025/1727143 teknik/idari şartname ve kabul-hakediş kayıtları hakkında

Merhaba,

Boğaziçi Üniversitesi 2026–2027 yemek hizmeti kapsamında **İKN 2025/1727143** için operasyonel miktar planlama ve kabul/hakediş akışını doğru anlamaya çalışıyoruz.

Mümkünse aşağıdaki belgelerin erişim yolunu veya bu maddeleri açıklayabilecek doğru birimi rica ediyoruz: teknik şartname, idari şartname, birim fiyat teklif cetveli, ilgili kabul/hakediş hükümleri, ceza/SLA maddeleri ve günlük üretim/kabul mutabakat formu.

Özellikle şu sınırlı soruları netleştirmek istiyoruz: hangi miktarın ödeme/kabul için esas alındığı; miktarın hangi seviyede ve ne zaman kesinleştiği; fazla üretim ve eksik servis riskinin hangi tarafta olduğu; kampüs dağılımının hangi noktaya kadar değiştirilebildiği; BUCard/üretim/kabul kayıtları uyuşmazsa hangi kaydın esas olduğu.

Belge paylaşımı mümkün değilse yalnızca doğru belge adı, sahip birim ve erişim prosedürü de yeterlidir.

Teşekkürler.

## 5. Evidence-status ledger

Update this table after each **real** external action. Do not convert `READY_TO_SEND` into `SENT` without a real send/call.

| Lane | Artifact / question | Owner route | Status | Evidence ID / link | Next action |
| --- | --- | --- | --- | --- | --- |
| #292 | aggregate BUCard service report | BUCard/BİDB | READY_TO_SEND | — | send routing request |
| #292 | count semantics / finality | Food Services | READY_TO_SEND | — | reconstruct one real service + reconcile |
| #292 | produced / allocated / surplus record | Food Services + TEMAŞ | OWNER_UNKNOWN | — | obtain record owner/referral |
| #358 | technical specification | SKS/procurement owner | REQUEST_READY | — | obtain authoritative document/status |
| #358 | administrative specification | SKS/procurement owner | REQUEST_READY | — | obtain authoritative document/status |
| #358 | unit-price schedule | SKS/procurement owner | REQUEST_READY | — | obtain authoritative document/status |
| #358 | hakediş / acceptance schema | control + procurement owner | OWNER_UNKNOWN | — | identify signer/system |
| #358 | penalty / shortage / quality mechanics | authoritative contract owner | UNRESOLVED | — | resolve from current docs/owner |
| cross | TEMAŞ local operations counterpart | Food Services/control referral | REFERRAL_NEEDED | — | request local named role |

## 6. Intake and evidence promotion

### BUCard/service truth

When a real aggregate artifact is obtained:
1. preserve original bytes unchanged;
2. record source owner, export method, retrieval time and access/privacy decision;
3. record reconciliation answers;
4. construct the canonical `SERVICE_TRUTH_V1` package without inventing missing fields;
5. route through:

```text
scripts/cs1_service_truth_artifact_intake.py
```

6. hand the exact artifact/checksum/result to #82 and #292.

A failed CS1 admission is useful evidence. Do not weaken the validator to admit the file.

### Contract documents

For each real document:
1. preserve authoritative URL/source and version/date;
2. store a checksum if bytes are legally/operationally retained;
3. extract only narrow operational claims with page/section provenance;
4. update `PROCUREMENT_CONTRACT_RESEARCH.md` and `CLAIM_SOURCE_MATRIX.md`;
5. keep historical 2024–2025 clauses separated from current 2026–2027 clauses.

## 7. Cross-role handoff contract

**CS1**
- may add a missing minimum field/reconciliation condition;
- must not infer service truth from public BUCard pages;
- owns canonical intake after acquisition.

**CS2**
- may add a contract question only if it changes buyer, beneficiary, procurement, WTP or go-to-market reasoning;
- must not infer unit economics from public headline values.

**EE/EHB**
- should ask for new sensing only after current operational records are mapped;
- if a field is absent from current records, specify the minimum measurement boundary, not a hardware solution first.

**Quality/release**
- treat `READY_TO_SEND`, `REQUEST_READY`, `OWNER_UNKNOWN` and `UNRESOLVED` as non-evidence states;
- only provenance-backed external artifacts/interviews can advance evidence claims.

## 8. Completion gates

### #292 closes only when
- access decision is recorded;
- real aggregate rows are obtained or authoritative unavailability/denial is recorded;
- count semantics and finality are reconciled;
- export granularity/exportability are explicitly confirmed;
- production/outcome record ownership is recorded;
- any received artifact is handed to CS1 without fabrication.

### #358 closes only when
- authoritative current specification retrieval status is recorded;
- settlement/hakediş unit and owner are confirmed or explicitly unresolved by the responsible owner;
- quantity freeze/change rights are recorded;
- acceptance/penalty mechanics are recorded;
- production/allocation owner is identified;
- current-vs-historical clause provenance is preserved.

## 9. Current retrieval note — 2026-10-06

A focused public-web check re-confirmed the official BUCard, Food Services, SKS and dining-control routing surfaces above. It did **not** yield the authoritative current IKN 2025/1727143 technical/admin specification text in the publicly indexed official pages checked in this run. Therefore #358 remains an acquisition task rather than a secondary-research inference task.
