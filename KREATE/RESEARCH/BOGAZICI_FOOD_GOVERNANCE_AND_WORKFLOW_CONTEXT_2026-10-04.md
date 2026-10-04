# Boğaziçi Food Governance & Workflow Context — 2026-10-04

**Purpose:** establish what official Boğaziçi sources actually prove about Food Services governance, service context and control responsibilities before PMR.  
**Status:** public institutional evidence only. **Daily production-quantity ownership remains UNKNOWN.**

## Executive conclusion

Official Boğaziçi sources establish that the Food Services Branch has substantial governance authority around:

- procurement preparation;
- technical specifications;
- contractor-service follow-up/control;
- menu preparation;
- contract/specification compliance;
- institutional food-service operations.

The university also operates a formal food-cooking/distribution control body and a multi-campus service regime with BUCard/QR turnstile operations.

What official sources do **not** establish is the critical BOUNCAMPUS control point:

> **who chooses tomorrow's production/allocation quantity, at what time, with what information, and until when it can change.**

That remains first-order PMR.

---

# 1. Official Food Services Branch responsibilities

Boğaziçi University's **2025 SKS Activity Report** lists the duties/powers of `Yemek Hizmetleri Şube Müdürlüğü`.

The official report states responsibilities including:

- preparing procurement work for student/personnel/guest food services;
- preparing technical specifications for dining halls subject to procurement;
- following and controlling food service provided by the contractor;
- handling institutional meal-price determination/approval processes;
- preparing and publishing menus;
- checking that food service complies with contract and technical-specification clauses;
- carrying out the secretariat of the Food Services Executive Board.

Official PDF:
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1526-saglik-kultur-ve-spor-daire-baskanligi-20260227-161845.pdf

Relevant section: `Yemek Hizmetleri Şube Müdürlüğü`, report page around 8.

### What this supports

Food Services Branch is a legitimate first governance/PMR route for:

- contract workflow;
- service oversight;
- menu/service rules;
- pilot escalation/referral.

### What it does not support

It does not explicitly say the branch manager personally calculates or approves daily production quantity.

---

# 2. 2025 operational activity language

The same official report describes 2025 Food Services activity as including:

- operation/management of food production and service processes in the central kitchen and associated units;
- kiosk/package-food access operations;
- food-safety and quality controls covering calorie values, portion/grammage compliance and HACCP-related hygiene;
- field control of contract/specification compliance.

Official PDF:
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/1526-saglik-kultur-ve-spor-daire-baskanligi-20260227-161845.pdf

Relevant section: `2025 Yılı Birim Bazlı Faaliyet Gerçekleşmeleri -> Yemek Hizmetleri Şube Müdürlüğü`.

### Product implication

Any pilot must fit an existing formal quality/control environment. It cannot treat the cafeteria as an unconstrained optimization system.

Food safety, gram standards, menu rules and contract terms are hard constraints.

---

# 3. Formal control body exists

Boğaziçi's current university board/commission page lists a:

> `Yemekhane, Yemek Pişirme ve Yemek Dağıtım Kontrol Teşkilatı`

with named members including Food Services representation.

Official source:
https://bogazici.edu.tr/tr/pages/universite-yonetim-kurulu-kurul-ve-komisyonla/246

### Implication

Dining oversight is not owned by a single informal operator. There is a formal control/governance layer that may become:

- an influencer;
- pilot reviewer;
- approval/veto route.

PMR should determine its actual role in daily quantity versus compliance oversight.

---

# 4. Current named branch contact

Official current staff sources list:

- **Aygül Demir Yolasığmazoğlu — Yemek Hizmetleri Şube Müdürü**.

Sources:

- https://yemekhane.bogazici.edu.tr/people
- https://sks.bogazici.edu.tr/tr/pages/kadromuz/2212

Branch contact:
https://yemekhane.bogazici.edu.tr/iletisim

### Evidence boundary

This identifies a real governance contact.

It does **not** establish:

- age;
- personal motivations;
- purchasing priorities;
- daily quantity ownership;
- willingness to adopt BOUNCAMPUS.

Do not invent these for the Persona.

---

# 5. Multi-campus service context

The official dining-service page publishes distinct breakfast/lunch/dinner windows across:

- North;
- South;
- Kilyos/Sarıtepe;
- Kandilli;
- Hisar;
- Anadolu Hisarı.

Source:
https://yemekhane.bogazici.edu.tr/yemek-servislerimiz

The page shows campus/service differences and weekend regimes.

### Modeling implication

Demand cannot safely be modeled as a single `university × day` total.

The natural operational unit is closer to:

```text
campus × meal_period × service_date × service_channel
```

subject to actual quantity/allocation workflow discovered in PMR.

---

# 6. Service-regime changes are frequent enough to matter

The official announcement archive includes operational changes such as:

- summer package-food service;
- summer meal-service changes;
- campus-specific service notices;
- Ramadan service hours;
- holiday package/service changes.

Source:
https://yemekhane.bogazici.edu.tr/duyurular

Example summer package regime:
https://yemekhane.bogazici.edu.tr/yaz-donemi-paket-yemek-hizmeti-hakkinda

### Modeling implication

A historical model needs explicit `service_regime` states rather than interpreting a closure/restricted service as naturally low demand.

This reinforces the existing repo rule to build a dated regime table.

---

# 7. BUCard / QR creates a real transaction context, but not yet a usable dataset

Official FAQ states:

- dining access uses BUCard;
- users can enter using BUCAMPUS QR if they do not yet have their card;
- support cases reference date, time, campus and turnstile information.

Source:
https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0

### What this supports

Operational systems have event context including at least some combination of:

```text
date
time
campus
turnstile
```

### What remains unknown

- retention horizon;
- data owner/schema;
- historical export availability;
- duplicates/refunds/failed attempts;
- whether entry equals one served meal;
- whether privacy-safe aggregate export can be approved;
- whether current contractor sees it before the production freeze.

Do not call BUCard a live demand feed until these are resolved.

---

# 8. Service audience / scale evidence

The 2025 SKS Activity Report reports `Yemek Hizmetinden Yararlanan Sayısı` values of:

- students: 17,466;
- personnel: 2,478;
- total: 19,944.

The exact counting semantics should not be treated as unique active daily diners without clarification.

The same ecosystem also separately reports a `6,000 daily meals` scale indicator in public SKS reporting.

### Reconciliation rule

Do not calculate daily participation or utilization by dividing one public metric into another unless source definitions align.

See:
`BOGAZICI_SOURCE_RECONCILIATION_2026-10-04.md`.

---

# 9. Demand pressure is institutionally acknowledged in historical reporting

Boğaziçi's 2024 SKS report describes the Food Services Branch mission as meeting growing dining demand without sacrificing quality, and discusses central-kitchen capacity improvements.

Official source:
https://sgdb.bogazici.edu.tr/sites/sgdb.bogazici.edu.tr/files/saglik_kultur_ve_spor_daire_baskanligi_2024_faaliyet_raporu.pdf

### Boundary

`growing demand` does not prove forecast error, waste or shortage.

It supports operational scale/capacity context only.

---

# 9A. Active tender uses a 10,000-meal/day capacity-reference need

The public EKAP-derived notice for active procurement `2025/1727143` states under production/manufacturing capacity that bidders must submit a valid capacity report able to cover **5,000 meals/day**, explicitly described as **one half (1/2) of the administration's daily meal need**.

Source:
https://ekapveri.com/ihale/ekap-2025-1727143/

This implies the tender's **capacity-qualification reference daily need is 10,000 meals/day**.

### What this supports

- the procurement is designed around high daily production capacity;
- the operation is large enough that daily quantity planning is operationally consequential;
- a 5,000-meal/day production capacity is only half the tender's stated daily-need reference.

### What this does NOT support

Do **not** relabel `10,000` as:

- actual daily meals served;
- average attendance;
- the production target for every service/day;
- the quantity communicated to TEMAŞ each day;
- a BUCard/turnstile count;
- the hakediş/payment quantity.

It is a **procurement qualification/planning-capacity reference** only.

This also should not be silently reconciled with the separate SKS `6,000 daily meals` indicator; they may use different scopes/definitions/time periods.

---

# 10. Governance-to-PMR map

## Food Services Branch

Can likely answer/referral-route:

- contract/specification ownership;
- contractor oversight;
- menu/service rules;
- current data/reporting processes;
- pilot approval/escalation.

Must ask rather than assume:

- daily quantity owner;
- freeze point;
- buffer policy;
- settlement/payment semantics.

## Contractor project/production team

Likely strongest route for:

- actual daily production calculation;
- ingredient/cooking commitment;
- batch flexibility;
- surplus/shortage consequence;
- internal ERP/forecast process.

## Food-cooking/distribution control body / technical food roles

Potential route for:

- compliance;
- portion/gram standards;
- service quality;
- measurement acceptance;
- food-safety constraints.

## BİD / BUCard data owner

Route for:

- aggregate event export;
- retention;
- semantics;
- privacy/security approval.

---

# 11. Strongest remaining workflow unknown

After extensive secondary research, the single most important unanswered Boğaziçi question remains:

> **Under the active 2026–2027 TEMAŞ service workflow, who sets each campus/meal's production or allocation quantity, when does that number become costly/impossible to change, what information is available before that time, and which party bears the consequence of excess versus shortage?**

Further public web research is unlikely to answer this as reliably as a direct workflow interview or active technical specification.

---

# 12. Application consequence

Safe:

> Boğaziçi has a formal Food Services governance structure overseeing contractor service, menus and contract compliance across a multi-campus dining operation, and its current procurement references a high daily production-capacity requirement.

Still hypothesis:

> This branch directly makes daily quantity decisions.

The Persona should remain the **production-quantity decision actor** until PMR identifies the actual person/role.
