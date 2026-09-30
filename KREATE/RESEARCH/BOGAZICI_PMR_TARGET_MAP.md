# Boğaziçi Food-Waste PMR Target Map

**Research date:** 2026-10-01  
**Purpose:** Route interviews to the roles that can actually answer quantity, contract, data, measurement and sustainability questions uncovered by the research packs.  
**Status:** Public professional-role mapping only. **No interview has occurred. No listed person implies endorsement, availability or validation.**

---

# 0. Use this map correctly

This is not a mass-outreach list.

Use the smallest number of interviews that resolve the highest-risk unknowns. Start with role-owned questions and ask for the next responsible person when the first interview reveals that the decision sits elsewhere.

Do not:

- treat public contact information as permission for repeated outreach;
- contact multiple people with the same generic message simultaneously;
- describe the product as deployed, validated or institutionally approved;
- ask IT for personal diner data;
- ask sustainability staff to validate a food-production workflow they do not own;
- treat a contractor corporate mailbox as proof that local Boğaziçi operations will respond.

---

# 1. P0 — Food Services Branch: production/contract workflow owner

## TARGET-BU-01 — Yemek Hizmetleri Şube Müdürlüğü

**Why first:** This is the strongest public-source owner for Boğaziçi's dining-service governance. The formal directive and current staff page place tender/specification work, contractor control, menus and meal-service administration in this branch.

### Public professional contact surface

- **Aygül Demir Yolasığmazoğlu** — Yemek Hizmetleri Şube Müdürü
- Public branch mailbox: `yemekhane@bogazici.edu.tr`
- Public branch phone: +90 212 359 4460 / 6729 / 6730
- Office: North Campus Administrative Building, 5th floor

Official sources:

- Staff: https://yemekhane.bogazici.edu.tr/people
- Branch contact: https://yemekhane.bogazici.edu.tr/iletisim
- SKS staff: https://sks.bogazici.edu.tr/tr/pages/kadromuz/2212

### P0 interview questions

1. Who determines tomorrow's student, breakfast and staff meal quantities under the current TEMAŞ contract?
2. What is the first forecast/requested quantity and when is it communicated?
3. When is the quantity frozen for production?
4. Can it be revised by campus, meal, package channel or batch?
5. Which historical/current signals are consulted today?
6. Is BUCard/QR usage seen before or only after service?
7. Are BUCampus menu votes or ratings ever used operationally?
8. Which quantity is used for contract acceptance/hakediş?
9. Who absorbs excess-food cost?
10. What happens contractually/operationally if food runs out?
11. Can they provide a privacy-safe 8–12 week aggregate pilot/history export?
12. Who at TEMAŞ owns the daily kitchen quantity if that decision is contractor-side?

### Evidence output required

A completed interview should produce a workflow of the form:

```text
role
→ input data
→ quantity decision
→ deadline/freeze point
→ adjustment rights
→ produced/delivered/served measurement
→ excess consequence
→ shortage consequence
→ payment/settlement signal
```

If the branch says the decision sits with TEMAŞ, that is a useful finding, not a failed interview.

---

# 2. P0 — Contractor operations: direct production user candidate

## TARGET-BU-02 — TEMAŞ Gıda / Boğaziçi project operations

**Why:** Public procurement research identifies TEMAŞ as the current 2026–2027 contractor. Sector precedents from Uşak and Kırıkkale show that in some university contracts the contractor is directly responsible for forecasting daily production while payment is tied to actual consumption.

### Public corporate contact surface

- Company: **TEMAŞ Gıda Sanayi ve Ticaret A.Ş.**
- Corporate collaboration/contact mailbox: `info@temasgida.com`
- Corporate phone: +90 212 886 41 41
- Public website: https://www.temasgida.com/
- Contact page: https://www.temasgida.com/iletisim

The public corporate page does **not** identify the current Boğaziçi project manager. Ask Food Services for the correct local operations contact rather than guessing a person.

### P0 interview questions

1. Who predicts tomorrow's quantity for the Boğaziçi project?
2. What heuristic is used today: same weekday, recent average, operator experience, reservation, university request, or another method?
3. What time do ingredient commitment and cooking become irreversible?
4. Is production split into batches that can react to early demand?
5. How is output allocated across six campuses and package/kiosk channels?
6. What does a 5% overforecast actually cost operationally?
7. What does a 5% underforecast cause — emergency cooking, service delay, penalty, complaint or other cost?
8. Which quantity is recorded for hakediş?
9. What fields are recorded internally: requested, produced, delivered, served, returned, leftover?
10. Would a range/shortage-risk recommendation be more usable than one scalar prediction?

### Critical commercial question

> If forecasting improves, **who captures the financial benefit — TEMAŞ, Boğaziçi, both, or neither under the contract?**

This determines whether the product is university SaaS, contractor operations software, shared decision support, or the wrong intervention altogether.

---

# 3. P0 — Data owner: BUCard / BUCampus / aggregate dining signals

## TARGET-BU-03 — Bilgi İşlem Daire Başkanlığı

**Why:** Public university pages establish that BİD operates BUCard as a service and BUCampus as a university digital product. Dining sources show QR/turnstile use and BUCampus menu/poll functionality. None of this proves historical data access; IT is the correct place to resolve that boundary.

### Public institutional contact surface

- Unit: **Bilgi İşlem Daire Başkanlığı**
- General mailbox: `bilgiislem@bogazici.edu.tr`
- General phone: 0 212 359 47 00
- Website: https://bilgiislem.bogazici.edu.tr/

Official service pages show BUCard and BUCampus among BİD services/products.

### P0 data questions

1. Are dining BUCard and QR events retained historically?
2. Can they be exported only as aggregate counts by `date × campus × meal window`, with no personal identifiers?
3. Are failed/duplicate/refund/second-meal events distinguishable?
4. Can turnstile events be reconciled to actual meal service?
5. What retention horizon exists?
6. Are BUCampus menu-vote totals stored historically?
7. Can ratings/menu polls be exported only in aggregate?
8. Is there a structured service-calendar or event feed that can be used without private user data?
9. What approval would be required for a bounded research pilot?

### Minimum acceptable result

Even `no, this cannot be exported` is valuable. CS1 should then design around operator spreadsheets/manual aggregate counts rather than fabricate telemetry access.

---

# 4. P1 — Zero Waste / sustainability measurement owner

## TARGET-BU-04 — Sürdürülebilir Yeşil Kampüs Uygulamaları Komisyonu

**Why:** The current university commission is formally tasked with reducing emissions/waste, improving natural-resource management and reducing campus ecological footprint. It is relevant to **measurement boundary and impact review**, but not automatically to kitchen quantity control.

### Current public role map

The university's current commission page lists:

- **Chair:** Prof. Dr. Mustafa Öztürk
- Members include Prof. Dr. Levent Kurnaz, Prof. Dr. Nilgün Cılız, Doç. Dr. Aslı Helvacıoğlu, Prof. Dr. Burak Demirel, Engin Köklü, Dr. Öğr. Üyesi Tamer Atabarut, Öğr. Gör. Bahar Özay, and Vehbi Meşin.

Official commission page:  
https://bogazici.edu.tr/tr/pages/universite-yonetim-kurulu-kurul-ve-komisyonla/246

### Research/technical sustainability option

Boğaziçi University's Sustainable Development and Cleaner Production Center (BU-SDCPC) publicly lists work on zero waste, cleaner production and life-cycle assessment.

Center:  
https://sdcpc.bogazici.edu.tr/tr/team.asp

### Questions

1. What is the exact boundary of the published food-waste total?
2. Which categories are weighed separately?
3. Is the date tied to waste generation or waste collection?
4. Can the waste stream be split by campus, meal, kitchen/pre-consumer and plate/post-consumer?
5. Which source is considered authoritative for internal reporting?
6. Which metric would they accept as a defensible pilot improvement?
7. What shortage/service guardrail must accompany a food-waste reduction claim?
8. Does the university already have an approved food-waste-to-CO2e/water methodology?

### Role boundary

Do not ask this group to prove that demand forecasting causes the existing waste. That remains a production/workflow hypothesis.

---

# 5. P1 — Senior administrative owner / escalation path

## TARGET-BU-05 — Sağlık, Kültür ve Spor Daire Başkanlığı

**Why:** SKS is the contracting/administrative umbrella for Food Services. Use this route if branch-level PMR shows that pilot/data/contract approval sits above the branch.

### Public professional contact surface

- **Eshabil Yıldız** — Sağlık Kültür ve Spor Daire Başkanı
- General SKS mailbox: `sks@bogazici.edu.tr`
- General phone: (0212) 359 45 15

Official source:  
https://sks.bogazici.edu.tr/tr/pages/kadromuz/2212

### Ask only after workflow discovery

Do not start with generic innovation-pitch questions. Escalate with a concrete request such as:

- permission for a privacy-safe aggregate data pilot;
- approval to interview the contractor project operator;
- clarification of contract owner/quantity approval;
- approval of a measurement protocol.

---

# 6. P2 — Food-service operational staff / data dictionary support

## TARGET-BU-06 — Yemek Hizmetleri branch operational staff

The public staff directory also lists:

- Hakan Deniz — Büro Personeli
- İsmet Gündoğan — Büro Personeli
- Mustafa Melep — Bilgisayar İşletmeni

Official source:  
https://yemekhane.bogazici.edu.tr/people

### Why P2

These roles may know actual spreadsheets, reporting workflows, BUCard issue handling, monthly contractor records and where data live. They should not be treated as the buyer/persona by title alone.

Use after the branch manager identifies the relevant operational/data owner.

---

# 7. Useful evidence of an existing feedback culture

## TARGET-BU-07 — Menu voting, daily tasting and feedback channels

Public sources show several feedback mechanisms already exist:

- BUCampus menu selection/voting;
- satisfaction survey with 2,386 participants reported for 2025;
- daily pre-service tasting with volunteer students and evaluation forms;
- web request/complaint channel;
- planned daily meal rating through BUCampus in the 2026–2027 goals.

Sources:

- SKS 2025 activity report: https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096
- Tasting program: https://sks.bogazici.edu.tr/tr/announcements/yemek-tadim-etkinligi/2565

### Product implication

Do **not** propose another generic feedback app as the core innovation. The harder unanswered problem is whether existing feedback/preference/attendance signals reach the production decision before the freeze point.

---

# 8. Recommended interview order

The fastest sequence is:

```text
1. Food Services Branch manager
   ↓ identify actual quantity owner + settlement rule
2. TEMAŞ local project/production operator
   ↓ identify heuristic, freeze time, risk and internal records
3. BİD data owner
   ↓ test privacy-safe aggregate signal availability
4. Zero Waste / sustainability measurement owner
   ↓ validate waste boundary and impact claim rules
5. SKS senior owner only for permissions/escalation
```

This sequence avoids spending interviews on peripheral personas before the core decision is understood.

---

# 9. Interview artifact requirements

Every interview should record:

```text
interviewee_role
organization/unit
role_in_decision
last_real_incident
current_process
input_signals
decision_owner
freeze_time
adjustment_rights
excess_consequence
shortage_consequence
settlement_measure
data_system
privacy/access_constraint
what_changed_in_our_hypothesis
follow_up_owner
```

A contact or scheduled meeting is **not evidence**. Only completed interview notes may enter the PMR evidence pipeline.

---

# 10. Highest-value outcome

The single most useful PMR result is a verified answer to:

> **Under the current Boğaziçi–TEMAŞ workflow, who chooses each meal's production/allocation quantity, at what exact time does that choice become costly to change, what aggregate signals exist before that moment, and who bears the cost of excess versus shortage?**

Everything else — model choice, app UI, carbon conversion and market story — should remain downstream of that answer.