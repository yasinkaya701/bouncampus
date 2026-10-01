# Türkiye Public-Service Hakediş Framework — Dining Decision Research

**Research date:** 2026-10-01  
**Purpose:** Narrow the current Boğaziçi 2026–2027 dining contract evidence gap by separating the general public-service payment/control framework from the tender-specific quantity semantics that still require a current contract artifact or owner confirmation.  
**Status:** Secondary legal/procurement research for product discovery. **NOT legal advice. NOT a statement of current Boğaziçi contract clauses.**

---

# 0. Executive conclusion

The general public-procurement framework materially narrows the Boğaziçi `hakediş` question, but does not finish it.

For unit-price service contracts, the general framework is built around this chain:

```text
service is performed
→ control organization keeps/validates performance records
→ quantities of performed work are established
→ established quantities × offered unit prices
→ progress-payment (hakediş) report
→ contract-defined deductions / penalties / payment process
```

For continuous services, records can be kept by service period and those records can feed both payment and acceptance.

This means the current Boğaziçi question is no longer:

> Does quantity matter in a unit-price public contract?

It clearly can.

The P0 question is now:

> **Which dining event or operational record is contractually recognized as the performed quantity for each Boğaziçi meal line item?**

Candidates that must be verified, not assumed:

```text
requested/called-off meals
produced meals
delivered meals
validated turnstile/QR meals
served/eaten meals
control-organization accepted meals
another specification-defined quantity
```

A current contract/specification excerpt or current progress-payment artifact is still required before any economic savings claim.

---

# 1. General framework: unit-price service payment

## HAK-GEN-01 — Performed quantities are multiplied by offered unit prices

KİK Board decisions quoting **Hizmet İşleri Genel Şartnamesi Article 42** state that, for total-price-over-unit-price service contracts, temporary progress-payment reports are generally prepared monthly unless the contract or annexes provide otherwise.

The work performed since commencement is calculated by the **control organization together with the contractor or representative**, and the resulting quantities are multiplied by the offered unit prices and entered into the progress-payment report according to the contract.

Official KİK decision examples quoting the rule:

- https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=d591bdf81890b2a85b173153899f9675a7fc653f7fbe53b784e5703dfd1053c7
- https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=57609f83cd6112f59b588ca530dc5ba7bf60ee2d3e580424a0eb3b3891455c9c

### Product implication

For a unit-price dining service, the relevant economic signal is not necessarily the tender's headline total quantity or kitchen output. It is the **quantity recognized as performed work under the current contract records**.

Therefore a model must not assume:

```text
produced_qty == hakedis_qty
served_qty == hakedis_qty
turnstile_qty == hakedis_qty
```

until the current Boğaziçi implementation is verified.

---

# 2. Contract-specific payment rules still matter

## HAK-GEN-02 — Type contract leaves payment plan/conditions to the administration within the general framework

KİK decisions quoting the **Hizmet Alımlarına Ait Tip Sözleşme** explain that the contract's `Ödeme yeri ve şartları` section is completed by the administration according to the nature of the work, within the General Conditions' payment rules.

Official KİK example:

https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=bfd148ff026799d21824d969497d951abff3c09a0c82c7a6866b3ee94506a6d8&KararMetni=92365fd3e7c8668776184277665d7fbb487eda0e362b33c7217090b1c1871c92

Another KİK decision notes that administrations prepare contract drafts using the Type Contract and may fill in work-specific terms or add other matters provided they remain consistent with procurement law:

https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=2af3873758eef6e870b62ce95f2917c2e0371df26152abee0897c360ebf68e71

### Consequence for Boğaziçi

The General Conditions tell us **how a unit-price progress-payment system is structured**, but the current Boğaziçi contract/specification must tell us what the relevant dining work quantity actually is and which records prove it.

P0 document sections therefore become finite and precise:

```text
Sözleşme / Sözleşme Tasarısı §12 — Ödeme yeri ve şartları
Sözleşme §19 — İşin yürütülmesine ilişkin kayıt ve tutanaklar
Sözleşme §20 — Teslim, muayene ve kabul işlemleri
Sözleşme §16 — Aykırılık / ceza / fesih
Teknik Şartname — meal-count / production / service / acceptance clauses
Birim Fiyat Teklif Cetveli — winning line items and unit prices
Hakediş eki — quantity evidence actually used in one month
```

The exact numbering should be verified in the current Boğaziçi documents; the Type Contract structure is a routing guide, not proof that every current clause has identical wording.

---

# 3. Continuous services create an operational record layer

## HAK-GEN-03 — Period records can become payment and acceptance evidence

KİK decisions quoting **Hizmet İşleri Genel Şartnamesi Article 34** state that, where a service is performed continuously in periods such as daily or weekly, relevant records are kept for those periods. They can record whether work conforms to the contract, defects or deficiencies, staffing/equipment and other matters required by the control organization. The records and objections can be used in progress payments and final acceptance.

Official KİK decision:

https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=96777df753c767a2638740f44e945daad76eb31ac4c79551c41613d75fcf3935

A separate KİK decision explains that period records jointly kept by the control organization and contractor can represent delivery of that period's performed service, and that records can be decisive if the contractor refuses to participate/sign under the specified procedure:

https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=25e0f77d116e7ee1dfd8897439f6c47079fbaeab24029f9dad7f8ddd6fa8a9a1&KararMetni=c7f1972c513ff324a59060cadbbf750e71f51531e512fc3c4671a494b2553589

### High-value Boğaziçi question

Ask for **one blank or anonymized example** of the current daily/monthly control record used to substantiate dining service.

Do not start by requesting the entire signed contract if a one-page operational record answers the product question faster.

Potential fields to inspect:

```text
service_date
campus
meal_type
requested_qty
produced_qty
served/validated_qty
accepted_qty
unit_price_line_item
penalty_or_deduction
control_officer_signoff
contractor_signoff
source_system
```

Even the column names can resolve more product uncertainty than another forecasting paper.

---

# 4. Food-service contracts demonstrate that “performed quantity” is contract-defined

## HAK-GEN-04 — Sector example: order/production quantity can differ from payable quantity

A 2023 KİK Board decision for a hospital meal service documents a workflow where:

1. the administration prepares next-day rations/needs;
2. the contractor learns the meals and quantities to produce;
3. staff meals are observed through chip-card/turnstile records plus controlled fallback records;
4. patient/companion quantities are recorded through the relevant systems;
5. the specification defines payment according to the **eaten/validated meal count**, not simply the prior production request.

The Board's assessment explicitly notes that estimated meal quantities can be communicated in advance but need not be exact, and that payment based on consumed meals is possible under that contract design.

Official KİK decision:

https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=a583bffcd454759389079584b79d72e1187522bb006e2cfdf8b8c56a45a76849&KararMetni=a764237d8d5b30dffbaa85925b7422af6b4bef5d4846dcf3945cf3a0ecb89a94

### Why this matters

This is not a Boğaziçi fact.

It demonstrates that a meal contract can legitimately contain two different quantities:

```text
Q_plan_or_ration
Q_payable_or_validated
```

with economic risk arising from their difference.

That distinction is exactly what the Boğaziçi P0 contract investigation must resolve.

---

# 5. Control records are likely more important than “AI accuracy” for initial economics

The product's economic chain should be represented as:

```text
Q_signal
→ Q_request / Q_plan
→ Q_produced
→ Q_delivered
→ Q_served / Q_validated
→ Q_accepted_for_hakedis
→ line_item_unit_price
→ deductions / penalties
→ contractor/university economic outcome
```

Every arrow can differ.

### Forbidden shortcut

```text
model predicts 100 fewer diners
× blended contract value per headline meal
= savings
```

is invalid until the contract-recognized quantity and marginal economic consequence are known.

---

# 6. Current Boğaziçi P0 artifact request — minimum viable version

Instead of asking vaguely for “the contract”, request the smallest artifact set that resolves the graph.

## Artifact A — current payment clause

Need only the current text answering:

```text
payment frequency
quantity calculation basis
who certifies it
```

Likely location: `Ödeme yeri ve şartları`.

## Artifact B — meal-count/acceptance clause

Need current wording answering:

```text
what counts as one payable student meal
what counts as one payable breakfast/sahur
what counts as one payable staff meal
```

## Artifact C — one redacted/anonymized hakediş quantity page

Need columns and totals, not financial/personally sensitive details.

Question:

> Which operational count is copied into the monthly meal line item?

## Artifact D — one service/control record

Need the actual record that links service operations to accepted quantity.

## Artifact E — penalty/deduction excerpt

Need only clauses relevant to:

```text
shortage / no meal available
late service
wrong menu/substitution
quality failure
quantity mismatch if defined
```

## Artifact F — winning unit-price line-item schedule

Required before any current TRY-per-meal or avoided-cost calculation.

This is especially important because the public tender index exposes more line items than the three headline meal categories.

---

# 7. PMR script: six questions that can resolve P0-02 without legal-document overload

Ask Food Services / Control Organization / contractor together or sequentially:

1. **For last month's hakediş, what exact number was multiplied by the student-meal unit price?**
2. Where did that number come from — BUCard/QR, dining-hall count, kitchen record, delivery record, manually signed list, or another source?
3. Who certified or signed that number?
4. If 1,000 meals were planned and 950 were actually served, what quantity normally enters hakediş?
5. If 1,000 were planned but 1,050 were needed, how are the extra 50 handled operationally and contractually?
6. Which document or report would let us verify that answer for one real month?

This is more informative than asking “how does procurement work?”

---

# 8. Economic archetypes to distinguish in PMR

These are hypotheses, not Boğaziçi facts.

## Archetype A — actual validated consumption payment

```text
hakedis_qty ≈ validated served count
```

Potential incentive:

- contractor bears some excess-production risk;
- university avoids paying unconsumed quantity depending on fixed/time-based line items;
- forecast value may accrue primarily to contractor operations.

## Archetype B — requested/accepted quantity payment

```text
hakedis_qty ≈ university call-off / accepted delivered qty
```

Potential incentive:

- university quantity accuracy may directly affect quantity-linked payment;
- contractor may have less excess risk if accepted quantity is paid.

## Archetype C — mixed contract economics

```text
meal_qty × meal_unit_price
+ fixed/monthly service line items
± price adjustment
− penalties/deductions
```

Potential incentive:

- physical waste savings and contract-payment savings differ;
- not all avoided food creates equal avoided contract spend.

## Archetype D — minimum/fixed commitments or tolerance bands

Potential implication:

- production reduction may save contractor ingredients but not university payment within the band.

Do not select an archetype without current evidence.

---

# 9. Data schema update for economic verification

If an operational pilot proceeds, add contract provenance without exposing unnecessary financial documents:

```text
SERVICE_ID
CONTRACT_LINE_ITEM_ID
CONTRACT_LINE_ITEM_CLASS

Q_OPERATOR_PLAN
Q_FINAL_APPROVED
Q_PRODUCED
Q_DELIVERED
Q_VALIDATED_SERVED
Q_HAKEDIS

Q_HAKEDIS_SOURCE_RECORD
Q_HAKEDIS_CERTIFIER_ROLE

SHORTAGE_EVENT
PENALTY_EVENT
DEDUCTION_EVENT

UNIT_PRICE_VERIFICATION_STATUS
SETTLEMENT_RULE_VERSION
```

### Security/privacy rule

For model development, unit-price values do not need to be widely distributed. A verified economic owner can apply them downstream after physical outcomes are calculated.

---

# 10. Claim firewall

## Safe before current artifact verification

> Türkiye's general public-service framework provides for performed quantities in unit-price service contracts to be established through the contract/control process and multiplied by offered unit prices for progress payments. Food-service contracts can define the payable meal count using different operational records. The team is verifying which count the current Boğaziçi dining contract uses.

## Unsafe

> `Boğaziçi pays TEMAŞ for every meal scanned at the turnstile.`

> `TEMAŞ is paid only for meals actually eaten.`

> `Boğaziçi pays for production quantity.`

> `Every avoided meal reduces university spend by the meal unit price.`

> `The current monthly hakediş is definitely BUCard-derived.`

None is established without the current Boğaziçi artifact.

---

# 11. How this changes the evidence-gap matrix

P0-02 can now be split into three smaller confirmations:

```text
P0-02A  What is Q_HAKEDIS for each meal line item?
P0-02B  Which record/source system establishes Q_HAKEDIS?
P0-02C  Who signs/certifies and what penalties/deductions alter payment?
```

Once those are answered, economics can be evaluated separately from forecast accuracy.

### Research stop rule

Do not collect more generic public-procurement commentary after this point.

Next useful evidence must be one of:

- current Boğaziçi contract/spec clause;
- current anonymized hakediş/control record;
- current owner interview confirming the record chain;
- current winning unit-price schedule.

---

# 12. Sources

Primary/official KİK Board decisions used to quote/apply the public-service framework:

1. General Conditions Article 42 / unit-price progress-payment mechanism:  
   https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=d591bdf81890b2a85b173153899f9675a7fc653f7fbe53b784e5703dfd1053c7
2. Type Contract payment section and work-specific payment terms:  
   https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=bfd148ff026799d21824d969497d951abff3c09a0c82c7a6866b3ee94506a6d8&KararMetni=92365fd3e7c8668776184277665d7fbb487eda0e362b33c7217090b1c1871c92
3. Contract-draft flexibility within statutory/type-contract framework:  
   https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=2af3873758eef6e870b62ce95f2917c2e0371df26152abee0897c360ebf68e71
4. General Conditions Article 34 / period records used in progress payment and acceptance:  
   https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=96777df753c767a2638740f44e945daad76eb31ac4c79551c41613d75fcf3935
5. Control records / period delivery and acceptance context:  
   https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=25e0f77d116e7ee1dfd8897439f6c47079fbaeab24029f9dad7f8ddd6fa8a9a1&KararMetni=c7f1972c513ff324a59060cadbbf750e71f51531e512fc3c4671a494b2553589
6. Food-service example with next-day ration, chip-card/other consumption records and eaten-meal payment basis:  
   https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=a583bffcd454759389079584b79d72e1187522bb006e2cfdf8b8c56a45a76849&KararMetni=a764237d8d5b30dffbaa85925b7422af6b4bef5d4846dcf3945cf3a0ecb89a94

---

# 13. Bottom line

General procurement law does **not** close the Boğaziçi business case, but it tells us exactly where the truth must live.

```text
CURRENT CONTRACT/SPEC
        ↓
CURRENT CONTROL RECORD
        ↓
Q_HAKEDIS
        ↓
WINNING UNIT PRICE
        ↓
DEDUCTIONS / PENALTIES
        ↓
ECONOMIC CONSEQUENCE
```

Until that chain is verified, BOUNCAMPUS should optimize and claim **physical decision outcomes** — excess, shortage, service quality and measured waste — rather than invented financial savings.