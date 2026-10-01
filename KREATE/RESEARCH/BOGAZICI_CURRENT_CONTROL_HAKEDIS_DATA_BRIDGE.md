# Boğaziçi Current Control–Hakediş–Data Bridge

**Research date:** 2026-10-01  
**Purpose:** Connect the current Boğaziçi food-service governance, control/acceptance and BUCard reporting roles so the team asks for the *right operational record* when resolving `Q_HAKEDIS` and pilot data semantics.  
**Status:** Secondary/public-source research. **NOT a current meal-payment formula. NOT legal advice. NOT proof that BUCard counts are the current hakediş basis.**

---

# 0. Executive conclusion

Recent research resolves an important structural question:

Boğaziçi already has a formal chain connecting:

```text
DIGITAL DINING EVENTS / REPORTS
        ↓
BUCard Office / BİD
        ↓
Food Services + Yemek Hizmeti Yürütme Kurulu
        ↓
contract service / control records
        ↓
Yemekhane, Yemek Pişirme ve Yemek Dağıtım Kontrol Teşkilatı
        ↓
Muayene ve Kabul / hakediş process
        ↓
payment order / accrual
```

But the public sources do **not** establish that one specific BUCard count is copied directly into the current TEMAŞ meal-line hakediş.

The biggest methodological correction is:

> **KİK56.0/H (`Hizmet İşleri Kabul Teklif Belgesi`) is an acceptance-routing / readiness document, not the meal-quantity ledger.**

The standard form contains contract/service-identification and acceptance-readiness fields, but no meal-count table.

For continuous services such as **food service**, acceptance is instead based on the **records kept by the control organisation while the service is being performed**.

Therefore P0-02B should stop asking for KİK56.0/H as if it contains `Q_HAKEDIS`.

The highest-value artifact is now:

```text
one current PERIOD CONTROL RECORD / HAKEDIS ATTACHMENT
that connects operational meal counts to the quantity accepted for payment
```

paired with the relevant BUCard report/data dictionary only if BUCard is part of that chain.

---

# 1. Current Food Service Executive Board links hakediş and BUCard reporting

## BRIDGE-01 — Yemek Hizmeti Yürütme Kurulu participates in meal hakediş/payment execution

Boğaziçi's published **Yemek Hizmeti Yürütme Kurulu Yönergesi** defines the current governance around student/personnel/guest food-service payment and control.

The directive states that the Board carries out the **tahakkuk / ödeme emri** process for meal-service hakediş together with the **Muayene Kabul Komisyonu**.

Primary source:

https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/275-yemek-hizmetleri-yonergesi-20251103-152153.pdf

### What this establishes

The hakediş/payment workflow is not only a generic procurement-office process. A food-service-specific board and acceptance structure are formally involved.

### What remains unknown

- which count becomes the meal-line `Q_HAKEDIS`;
- which source system supplies that count;
- whether student/staff/breakfast lines use the same counting method;
- whether package meals have separate acceptance semantics;
- whether quantities are based on BUCard, production, delivery, manually signed records, or a combination.

---

# 2. Current directive explicitly assigns reporting/storage duties to BUCard Office

## BRIDGE-02 — BUCard Office provides reports to food-service governance and stores digital data

The same directive assigns the BUCard Office responsibilities around the dining system, including providing the necessary reports to the **Yemek Hizmeti Yürütme Kurulu** and **Yemek Hizmetleri Şube Müdürlüğü**, and preserving the relevant digital data.

Primary source:

https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/275-yemek-hizmetleri-yonergesi-20251103-152153.pdf

This aligns with BİDB's separate 2025 activity report that publicly describes:

- `BUCard Yemekhane anlık rapor sayfası`;
- daily passage reports;
- package-meal counts in those reports;
- staff meal reporting.

Source:

https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1503-bilgi-islem-daire-baskanligi-20260227-153040.pdf

### Critical boundary

The existence of a reporting duty does **not** prove:

```text
BUCARD_VALIDATED_ENTRY_COUNT == Q_HAKEDIS
```

It only makes BUCard/BİD a concrete source-system owner to inspect.

---

# 3. Current dining transactions are routed through turnstile infrastructure

## BRIDGE-03 — Directive and public FAQ tie dining operations to turnstiles/BUCard/QR

The food-service directive defines meal-service transactions through dining-hall turnstile infrastructure, while the public dining FAQ states that physical BUCard or BUCampus QR can be used for turnstile access.

Sources:

- directive above;
- https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0

### Implication

A digital observed-service count exists as a plausible record class.

But it still needs reconciliation for:

- duplicate/retry events;
- package service;
- manual/offline service;
- failed transactions;
- second meals;
- reversals/corrections;
- sellout censoring;
- served meal without turnstile event.

The current product should call it `RECONCILED_VALID_PASSAGES` or `VALIDATED_SERVED_COUNT` only after the owner defines the semantics.

---

# 4. Control Organisation is explicitly tied to the current catering service

## BRIDGE-04 — Current General Secretariat reporting assigns a dedicated catering control organisation

Boğaziçi's General Secretariat Activity Report lists a specific:

> **Yemekhane, Yemek Pişirme ve Yemek Dağıtım Kontrol Teşkilatı**

for the contracted work described as:

> **Malzeme Dahil Kahvaltı ve Yemek Hazırlama, Servis, Dağıtım ve Dağıtım Sonrası Temizlik Hizmeti Alım İşi**

Current principal members listed in the report include:

- Ayhan Soylu — chair;
- Ahmed Musa Taş;
- Barış Pancar;
- Aygül Demir Yolasığmazoğlu;
- Mustafa Tunç.

Official source:

https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/564-genel-sekreterlik-20260112-095525.pdf

### Research value

This strengthens the Control Organisation as the correct owner route for:

```text
contract-performance truth
period service records
exceptions / deficiencies
accepted service evidence
```

It does **not** establish that the Control Organisation chooses daily production quantity.

---

# 5. Continuous food-service acceptance is record-based

## BRIDGE-05 — Repeating food services are accepted using Control Organisation records

The **Hizmet Alımları Muayene ve Kabul Yönetmeliği** states that for continuous services such as:

- cleaning;
- food service;
- transportation;

acceptance is performed using the records kept by the control organisation during performance of the service.

The same structure is reproduced in public procurement decisions and Boğaziçi's own institutional reporting.

Sources:

- consolidated regulation / public text: https://www.lexpera.com.tr/mevzuat/yonetmelikler/yr801y2002n24968p4/2
- KİK decision archive applying the rule: https://arsiv.kikkararlari.com/index.php?Itemid=9&id=59818&option=com_content&task=view
- Boğaziçi General Secretariat reporting: https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/564-genel-sekreterlik-20260112-095525.pdf

### Key consequence

The operational **period record** is likely a more direct place to resolve service-count semantics than the final acceptance-proposal form.

The specific current Boğaziçi period-record format remains unknown.

---

# 6. KİK56.0/H is not the quantity ledger

## BRIDGE-06 — Standard acceptance-proposal form contains no meal-count table

The standard **Hizmet İşleri Kabul Teklif Belgesi — KİK56.0/H** contains fields such as:

```text
work/service name
contractor
contract date
contract value
contract duration
required completion date
extensions
actual completion date
acceptance-readiness finding
signatures / titles
```

and allows a list of identified deficient/defective work to be attached.

Public standard-form reproduction:

https://www.hakedis.org/wp-content/uploads/2016/10/hizmet_muayene-kabul.pdf

The form does **not** contain a standard meal-count / unit-price line-item quantity table.

### Correction to research workflow

Do not ask:

> “Can we see KİK56.0/H to learn monthly meal counts?”

Ask instead:

> “Which period control record / hakediş attachment establishes the student-meal, breakfast and staff-meal quantities that feed the hakediş?”

KİK56.0/H can still help confirm the acceptance chain, but it is not enough to resolve `Q_HAKEDIS`.

---

# 7. Three record classes must remain separate

## Record A — source-system / operational digital event

Examples:

```text
BUCard successful passage
BUCampus QR passage
package meal sale/distribution event
manual fallback entry
```

Owner candidate: BUCard / BİD.

Purpose:

- observed service activity;
- reporting;
- candidate demand label.

## Record B — contract-control period record

Examples to request, not assume:

```text
daily/weekly/monthly service control record
meal-count reconciliation
campus/service deviation record
shortage/substitution exception record
contractor + control signatures
```

Owner candidate: Control Organisation / Food Services.

Purpose:

- accepted truth for continuous service;
- compliance / exception evidence;
- likely bridge toward hakediş.

## Record C — formal acceptance/payment artifact

Examples:

```text
KİK56.0/H acceptance proposal
Kabul Tutanağı
hakediş report/payment attachment
payment order/accrual documents
```

Owner candidates:

- Muayene Kabul;
- Yemek Hizmeti Yürütme Kurulu;
- spending/payment chain.

Purpose:

- formal acceptance/payment workflow.

### Hard rule

Never collapse A, B and C into a single field named `actual_meals`.

They may disagree for legitimate operational reasons.

---

# 8. Current truth graph to verify

The minimum useful current graph is:

```text
RAW / RECONCILED DINING EVENTS
              ↓
? does control organisation consume these ?
              ↓
PERIOD CONTROL RECORD
              ↓
Q_CONTROL_ACCEPTED
              ↓
? same as Q_HAKEDIS ?
              ↓
HAKEDIS LINE-ITEM QTY
              ↓
YHYK + MUAYENE/KABUL + payment workflow
```

Every `?` is still a current evidence gap.

### Do not assume

```text
BUCard count == control accepted quantity
control accepted quantity == hakediş quantity
hakediş quantity == produced quantity
hakediş quantity == served quantity
```

---

# 9. Best next artifact — one real month, four documents maximum

A targeted document review can resolve the chain without requesting the full procurement archive.

## Artifact 1 — BUCard dining aggregate/report extract

Need only columns/aggregate numbers for one service period.

Purpose:

```text
identify digital observed-service count
```

## Artifact 2 — one period control record

Ask specifically for the record kept by the catering Control Organisation for the same period.

Purpose:

```text
identify accepted operational truth
```

## Artifact 3 — one hakediş quantity page/attachment

Need only:

```text
meal line item
monthly quantity
unit
source/reference
```

Financial values may be redacted if necessary.

Purpose:

```text
identify Q_HAKEDIS
```

## Artifact 4 — relevant payment/acceptance signoff page

Purpose:

```text
confirm who certifies / approves
```

### Reconciliation test

For one month:

```text
Q_BUCARD
Q_CONTROL
Q_HAKEDIS
```

If equal:

- determine whether equality is a formal rule or coincidental for that month.

If unequal:

- document the reconciliation rule.

This is more valuable than collecting another year of high-level sustainability data.

---

# 10. Six exact questions for a joint owner meeting

1. **What is the name of the record your Control Organisation keeps each month for this catering service?**
2. Which meal counts appear in it — requested, delivered, served, BUCard, package, staff, other?
3. Does the Control Organisation receive a BUCard dining report? If yes, which report and how is it reconciled?
4. Which quantity from the period record is copied into the current TEMAŞ hakediş meal line?
5. Who signs the period record, and who signs/approves the hakediş/payment order?
6. Can we inspect one redacted month where BUCard report, control record and hakediş are shown side by side?

These questions should be routed primarily to:

```text
Food Services Branch
+ catering Control Organisation
+ BUCard/BİD data owner
```

with YHYK/Muayene-Kabul as needed for formal payment confirmation.

---

# 11. Data model update

The product/research schema should distinguish:

```text
Q_DIGITAL_EVENTS_RAW
Q_DIGITAL_EVENTS_RECONCILED
Q_OPERATOR_PLAN
Q_PRODUCED
Q_DELIVERED
Q_SERVE_OBSERVED
Q_CONTROL_ACCEPTED
Q_HAKEDIS
```

plus:

```text
SOURCE_RECORD_ID
SOURCE_SYSTEM
RECONCILIATION_RULE_VERSION
CONTROL_SIGNOFF_ROLE
HAKEDIS_CERTIFIER_ROLE
EXCEPTION_CODE
```

### Why this matters

A product that stores only:

```text
actual_meals
```

cannot distinguish demand forecasting error from:

- digital logging error;
- package-channel omission;
- manual reconciliation;
- control adjustment;
- contract acceptance rule;
- payment-rule difference.

---

# 12. Product implications

## If BUCard reconciled count == control accepted == hakediş quantity

Potentially powerful single source-of-truth path:

```text
aggregate digital usage
→ decision history
→ contract outcome
```

Still verify timing and excess economics.

## If BUCard is only reporting but control uses another count

Use BUCard for demand/history, not financial claims.

## If control/hakediş count is delivered quantity

University and contractor incentives may differ from served-demand optimization.

## If control/hakediş count is actual validated consumption

Contractor excess-production risk may be more important than university invoice reduction.

## If counts cannot be reconciled reliably

Run physical operational pilot first and defer economic claims.

---

# 13. Current governance facts vs unresolved facts

## Strong current/public facts

- a food-service-specific Board participates in hakediş payment/accrual workflow;
- BUCard Office has formal food-service reporting/storage duties;
- dining turnstile/QR infrastructure exists;
- BİDB publicly reports dining real-time/daily report surfaces;
- a current catering-specific Control Organisation is appointed;
- continuous food services are accepted using control-period records;
- KİK56.0/H is an acceptance-proposal form rather than a meal-quantity table.

## Still unresolved

- exact current period-control form name/schema;
- whether BUCard report feeds that record;
- exact current `Q_CONTROL_ACCEPTED`;
- exact current `Q_HAKEDIS`;
- whether package/turnstile/manual counts reconcile;
- current line-item unit prices;
- current excess/shortage economic allocation.

---

# 14. Safe application language

### Safe

> `PUBLIC SOURCE` Boğaziçi already has formal dining digital-report, contract-control and payment/acceptance roles. Current university rules require BUCard reporting to food-service governance, while continuous service acceptance relies on records maintained by the Control Organisation. `RESEARCH GAP` We are validating which operational count bridges those records into the current TEMAŞ meal-line hakediş before making financial claims.

### Unsafe

> `BUCard is the hakediş source.`

> `Every QR/turnstile entry is paid to TEMAŞ.`

> `KİK56.0/H contains the monthly meal quantities.`

> `The Control Organisation decides tomorrow's production quantity.`

> `Digital count, accepted count and paid count are identical.`

None is established yet.

---

# 15. Sources

1. Boğaziçi — Yemek Hizmeti Yürütme Kurulu Yönergesi:  
   https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/275-yemek-hizmetleri-yonergesi-20251103-152153.pdf
2. Boğaziçi BİDB 2025 Activity Report — BUCard dining real-time/daily reports:  
   https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1503-bilgi-islem-daire-baskanligi-20260227-153040.pdf
3. Boğaziçi General Secretariat Activity Report — catering Control Organisation/current assignment:  
   https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/564-genel-sekreterlik-20260112-095525.pdf
4. Boğaziçi dining FAQ — BUCard/QR turnstile context:  
   https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0
5. Hizmet Alımları Muayene ve Kabul Yönetmeliği / continuous-service records:  
   https://www.lexpera.com.tr/mevzuat/yonetmelikler/yr801y2002n24968p4/2
6. KİK decision archive quoting continuous meal-service acceptance from Control Organisation records:  
   https://arsiv.kikkararlari.com/index.php?Itemid=9&id=59818&option=com_content&task=view
7. Public reproduction of standard KİK56.0/H form:  
   https://www.hakedis.org/wp-content/uploads/2016/10/hizmet_muayene-kabul.pdf

---

# 16. Bottom line

The next decisive research object is **not** another forecast model or another sustainability report.

It is one same-period reconciliation:

```text
BUCard / digital aggregate
        ↕
Control Organisation period record
        ↕
Hakediş meal-line quantity
```

Once those three numbers and their definitions are known, the team can finally separate:

- observed demand;
- accepted service;
- payable quantity;
- contractor risk;
- university financial effect.

Until then, keep the product's claim layer on physical operational outcomes rather than invented settlement economics.