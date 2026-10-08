# IE Primary Interview Targets — 2026-10-06

**Owner:** IE — Customer Discovery & Market  
**Purpose:** convert the four IE PMR slots into non-overlapping, falsifier-driven interview missions.  
**Rule:** this file is a plan only. It does not change any tracker slot from `TODO` unless real outreach/scheduling occurs.

## IE-01 — Boğaziçi Food Services operational workflow

### Primary objective
Reconstruct one recent meal service from initial quantity planning through final service/reconciliation.

### Required questions
1. Who first enters or proposes the quantity?
2. Which role approves or changes it?
3. When is total production effectively frozen?
4. Can campus allocation still change after that point?
5. What data are visible before the decision?
6. What is the current heuristic/system/ERP/spreadsheet?
7. When was the last meaningful surplus incident?
8. When was the last shortage/early-sellout incident?
9. What happened operationally after each incident?
10. Which record is treated as the final service count?

### Artifact asks
- de-identified production request / production sheet;
- campus allocation sheet;
- example service report;
- referral to BUCard/report semantic owner;
- referral to contractor planning counterpart.

### Falsifiers
- no material pre-service quantity decision exists;
- quantity cannot be changed by a reachable actor;
- production mismatch is not a meaningful operational problem.

---

## IE-02 — Control / acceptance / procurement / hakediş

### Primary objective
Resolve who accepts service, which quantity/record matters contractually, and whether a recommendation can legally or operationally alter the relevant decision.

### Required questions
1. What record is authoritative for service acceptance?
2. What unit enters hakediş/payment?
3. Who signs/approves it?
4. Are quantities committed by day, meal period, campus, item, or another unit?
5. How are corrections, second meals, package meals and additional meals handled?
6. What happens when served/turnstile/production records disagree?
7. Who bears the consequence of excess production?
8. What happens under shortage / sellout / late service?
9. Which quantity can still change after an order/plan is issued?
10. Could a human-reviewed recommendation be used before the contractual/operational freeze?

### Artifact asks
- 2025/1727143 administrative specification;
- technical specification;
- unit-price bid schedule;
- relevant contract clauses;
- acceptance/control form;
- hakediş/reconciliation schema;
- penalty/SLA clauses;
- current daily production request/order form.

### Falsifiers
- there is no controllable quantity before the binding commitment;
- the party controlling quantity has no practical path to act on a recommendation;
- contract economics make the proposed value proposition irrelevant.

---

## IE-03 — TEMAŞ local operations / production planning

### Primary objective
Understand the contractor-side planning stack, risk ownership, operational buffers and buying authority.

### Required questions
1. Who decides the next service's production quantity?
2. What time is the decision made?
3. Which data are used?
4. What safety buffer is applied and why?
5. Who can revise the plan?
6. Is production centralized and then allocated?
7. How are shortages recovered?
8. What happens to edible surplus?
9. Which cost/risk does TEMAŞ actually bear?
10. Which software/system is already used?
11. Who can approve a pilot or software tool?
12. What would a new tool have to outperform to be worth changing process?

### Artifact asks
- de-identified production/allocation record;
- recent exception / shortage / surplus record;
- current planning system screenshot or field list if shareable;
- local → HQ software/procurement escalation path.

### Falsifiers
- current planning already solves the decision with no meaningful gap;
- local operations cannot change quantity or influence the buyer;
- required data/timing are unavailable before the decision.

---

## IE-04 — second-site repeatability / counter-archetype

### Primary objective
Test whether the same product and sales motion repeat outside Boğaziçi.

### Preferred archetypes
Choose one site that is deliberately informative:
- mature, data-informed university dining;
- reservation-first workflow;
- contractor-risk workflow;
- institution-operated kitchen.

Do not choose a second site merely because access is easy.

### Required questions
1. Who controls quantity?
2. When does it freeze?
3. Which pre-service signals are used?
4. How are surplus and shortage measured/handled?
5. Who bears cost/risk?
6. Who is the buyer?
7. Which system is already used?
8. What would trigger switching or adoption?
9. Is the same recommendation workflow usable?
10. Would the same procurement/sales process apply?

### Falsifiers
- same physical problem but materially different buyer/sales process;
- same buyer but materially different decision/control point;
- no measurable outcome or no safe intervention window.


## IE-04 target shortlist and routing — 2026-10-06

This shortlist is secondary-source routing evidence only. **No row in `INTERVIEW_TRACKER.md` may move from `TODO` until a message is actually sent or a call is actually placed.** Prepared Gmail drafts are not outreach evidence.

### P0-A — mature-operation second site: Bolu Abant İzzet Baysal University (BAİBÜ)

**Why this site is informative**
- official Beslenme Hizmetleri material describes a multi-site dining operation spanning the central campus and several district campuses;
- the service is delivered through a contracted private provider;
- the university publicly lists operational forms including `FR.015 Günlük Yemek Üretim Ve Tüketim Formu`, `FR.018 Tüm Birimlere Gönderilen Yemek Sayıları Formu`, and `FR.019 İlçelere Gönderilen Yemek Sayıları Formu`;
- its SKS site also shows a current 2026 reservation process, allowing comparison of reservation signals against an existing production/consumption record stack.

**Primary route**
- SKS: `saglikkultur@ibu.edu.tr`, +90 374 253 45 16.
- Beslenme Hizmetleri internal extensions publicly list food engineers Itır Fulya Savaşan Alaoğlu (2824) and Merve Gürsoy (2842).

**Interview mission**
1. Reconstruct one recent day from reservation / expected demand → production → campus allocation → service/take-up → remaining quantity.
2. Identify which of FR.015 / FR.018 / FR.019 is operationally authoritative versus retrospective paperwork.
3. Establish the last reversible production/allocation cutoff.
4. Test whether reservation counts materially change production, merely improve information, or are operationally ignored.
5. Ask for one recent surplus and one shortage/early-sellout incident and the actual corrective action.
6. Compare central versus district-campus planning and contractor handoff.

**Falsifier value**
- if a mature operation already has timely production, allocation and consumption truth but still cannot act before freeze, BOUNCAMPUS's current pre-service recommendation wedge weakens;
- if the same records support a reachable intervention, this is a strong same-product repeatability test.

**Official sources**
- https://sksdb.ibu.edu.tr/tr/page/beslenme-hizmetleri/9713
- https://sksdb.ibu.edu.tr/tr/page/beslenme-hizmetleri-kullanilan-formlar/9853
- https://sksdb.ibu.edu.tr/tr/page/dahili-iletisim/9732

**Execution state:** Gmail draft prepared; **NOT SENT**.

### P0-B — reservation-first counter-archetype: Bandırma Onyedi Eylül University (BANÜ)

**Why this site is informative**
- an official notice updated 2 October 2026 states that, effective 5 October 2026, dining at all vocational schools **outside the central campus** is completely reservation-based;
- the notice explicitly says users without a reservation will not receive meal service;
- the university frames the change around more accurate daily planning, effective resource use and reducing food waste.

This makes BANÜ a deliberately adversarial counter-archetype: demand is partially converted from forecast uncertainty into explicit pre-service commitment.

**Primary route**
- SKS: `sks@bandirma.edu.tr`, +90 266 717 01 17.
- The SKS structure separately exposes Beslenme Hizmetleri and an Akıllı Kart ve Yemek Hesapları unit, so the interview should request the actual operational owner rather than infer ownership from titles.

**Interview mission**
1. Establish reservation cutoff, cancellation/release semantics, no-show handling and any exception path.
2. Determine exactly how reservation counts become kitchen/order quantities.
3. Identify whether a safety buffer is still added after reservations and why.
4. Compare pre-reservation and post-reservation surplus/shortage measurement.
5. Determine what uncertainty remains after mandatory reservation.
6. Test whether BOUNCAMPUS has any useful decision left to improve, or whether the reservation workflow largely substitutes for it.

**Kill test**
- if mandatory reservation in the announced off-central-campus MYO scope makes final demand known early enough and operational variance is negligible, a generic forecasting wedge should be killed for this archetype;
- any remaining opportunity must be narrower (no-show uncertainty, cross-site allocation, menu/preference effects, late operational exceptions, or another demonstrated control point).

**Official sources**
- https://sksdb.bandirma.edu.tr/tr/sksdb/d/UNIVERSITEMIZ-MERKEZ-YERLESKE-DISINDAKI-TUM-MESLEK-YUKSEKOKULLARINDA-REZERVASYONLU-YEMEK-HIZMETINE-GECIYOR-94035
- https://sksdb.bandirma.edu.tr/

**Execution state:** Gmail draft prepared; **NOT SENT**.

### P1 backup / comparative migration case — Kayseri University

**Why keep it as backup**
- the reservation system already used at the 15 Temmuz campus was expanded university-wide from 6 April 2026;
- the official dining-unit page states that the central campus produces meals in its own kitchen while district campuses use prepared-meal procurement, creating a useful within-institution operating-model contrast.

**Direct public route**
- Fatih Koç — Sosyal İşletmeler ve Yemekhaneler Şube Müdürü: `fatihkoc@kayseri.edu.tr`, 0352 504 38 38 / 10807.
- General SKS: `sksd@kayseri.edu.tr`.

**Interview mission**
- compare reservation behavior before/after university-wide expansion;
- compare own-kitchen versus purchased-meal planning;
- locate the production/order freeze in both models;
- ask which mismatch or service problem remained after reservation adoption.

**Official sources**
- https://sksd.kayseri.edu.tr/tr/duyuru-detay/10301/yemekhane-rezervasyon-sistemi-duyurusu
- https://sksd.kayseri.edu.tr/tr/i/12-1/sosyal-isletmeler-ve-yemekhaneler-sube-mudurlugu
- https://sksd.kayseri.edu.tr/tr/akademik-personel

**Execution state:** Gmail draft prepared; **NOT SENT**.

### Promotion rule for IE-04

Public pages may justify target selection and interview questions, but **cannot** prove:
- reservation-to-production coupling;
- actual surplus/shortage reduction;
- current decision owner/freeze time;
- buyer or economic beneficiary;
- adoption willingness;
- same-product repeatability.

Only a real source-owner response, completed interview or primary operational artifact may promote those facts.

---

## Interview scoring rubric

After each **real completed** interview, score only supported facts.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Concrete incident | none | vague example | recent specific example with sequence |
| Decision owner | unknown | likely role | verified actor + authority |
| Freeze point | unknown | approximate | explicit timestamp/event |
| Current baseline | unknown | described | artifact / reproducible rule |
| Surplus consequence | unknown | qualitative | quantified or contract-backed |
| Shortage consequence | unknown | qualitative | quantified or contract-backed |
| Data source | unknown | source named | semantics + sample/export path |
| Buyer/approver | unknown | likely role | verified authority path |
| Falsifier pressure | none | weak | clear evidence changing decision |

Do not add scores to the evidence ledger without the underlying notes/artifacts.

## Promotion rule

A completed interview can promote a narrow claim only when:
- a real conversation occurred;
- date and stakeholder role are recorded;
- reported fact and team interpretation are separated;
- no identifying/sensitive personal data are unnecessarily stored;
- contradictions are preserved;
- the claim links to the appropriate `E-INT-*` or operational evidence item.

Interview count is not a substitute for information value.
