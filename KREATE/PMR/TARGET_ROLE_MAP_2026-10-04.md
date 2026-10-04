# PMR Target Role Map — 2026-10-04

**Status:** Public role/contact mapping only. **No interview has occurred and no listed person implies endorsement or availability.**

## Principle

Contact the smallest number of people needed to resolve the highest-risk unknowns. Ask the first stakeholder to route you to the real owner when the decision sits elsewhere.

Do not blast generic outreach to every listed person.

---

# P0 — Food Services governance / workflow discovery

## Boğaziçi Yemek Hizmetleri Şube Müdürlüğü

Current public staff page lists:

- **Aygül Demir Yolasığmazoğlu — Şube Müdürü**
- Hakan Deniz — Büro Personeli
- İsmet Gündoğan — Büro Personeli
- Mustafa Melep — Bilgisayar İşletmeni

Official source:
https://yemekhane.bogazici.edu.tr/people

SKS directory also lists Aygül Demir Yolasığmazoğlu as **Yemek Hizmetleri Şube Müdürü**.

Official source:
https://sks.bogazici.edu.tr/tr/pages/kadromuz/2212

## Why first

This branch is the strongest public institutional route for:

- current dining workflow;
- contractor relationship;
- menu/service administration;
- identifying the actual quantity owner;
- identifying the TEMAŞ local project/production owner;
- pilot permission/escalation route.

## Questions this role should resolve

1. Who determines each meal's planned quantity?
2. Which side owns the forecast: university, TEMAŞ, or joint?
3. When is the first quantity communicated?
4. When does it freeze?
5. Can it be revised by campus/channel/batch?
6. What records are used today?
7. Which quantity is accepted/paid under the contract?
8. Who bears excess-production cost?
9. What happens when food runs out?
10. Who is the correct local contractor operator to interview next?

## What not to ask this role to prove alone

- detailed IT retention/schema;
- exact waste-accounting semantics owned elsewhere;
- technical ML performance.

---

# P0 — Current contractor production operations

## TEMAŞ Gıda Sanayi ve Ticaret A.Ş.

Current Boğaziçi procurement publicly identifies TEMAŞ as contractor for the 2026–2027 service.

Public corporate contact:

- phone: +90 (212) 886 41 41
- general email: `info@temasgida.com`

Source:
https://www.temasgida.com/iletisim

## Important routing rule

Do **not** assume the corporate mailbox/person is the Boğaziçi project owner. The preferred route is:

> Food Services interview -> ask for the local Boğaziçi TEMAŞ project/production contact.

## Questions only contractor operations can answer reliably

- current daily forecasting heuristic;
- who converts expected demand into batches;
- ingredient/cooking commitment timeline;
- whether production is batch-reactive;
- campus allocation timing;
- recorded requested/produced/delivered/served/returned fields;
- operational cost of 5% over/under forecast;
- shortage recovery mechanisms;
- whether better forecasts financially help the contractor.

---

# P0/P1 — Daily operational / data workflow inside Food Services

The public dining staff page lists operational/office roles inside the branch.

These roles may know:

- actual spreadsheets;
- monthly reconciliation;
- BUCard issue workflow;
- where contractor reports live;
- what quantities are manually reconciled.

They are **not automatically the persona/buyer** by title.

Use after the branch manager identifies the person closest to the actual record/process.

---

# P1 — BUCard / aggregate dining-event data owner

Boğaziçi BİD's public service inventory states:

- BUCard is a BİD service;
- `bucard@bogazici.edu.tr` is listed for BUCard communication;
- SKS and BİD are both associated with dining-related BUCard load/refund services.

Sources:

- https://bilgiislem.bogazici.edu.tr/tr/pages/hizmet-envanteri/3513
- https://bilgiislem.bogazici.edu.tr/tr/pages/bu-card/2389

General BİD contact:

- `bilgiislem@bogazici.edu.tr`
- 0 212 359 47 00

## Questions

1. Are dining entry events retained historically?
2. Can they be exported only as aggregate `date x campus x meal-window` counts?
3. What does one valid event represent?
4. Are failed/duplicate/refund events distinguishable?
5. What retention period exists?
6. Are QR and card entry events reconciled?
7. Is there a structured calendar/service feed?
8. What approval path would be needed for a bounded research pilot?

## Privacy boundary

The first pilot does not need names, IDs, individual histories, demographics, or student-level tracking.

---

# P1 — Waste / sustainability measurement owner

## Sürdürülebilir Yeşil Kampüs Uygulamaları Komisyonu

Current university governance page lists a commission tasked with improving energy/natural-resource management, reducing emissions/waste and the ecological footprint.

Official current governance source:
https://bogazici.edu.tr/tr/pages/universite-yonetim-kurulu-kurul-ve-komisyonla/246

Current page lists **Prof. Dr. Mustafa Öztürk** as chair and members including sustainability, administration and institutional-data roles.

A separate legacy/green-campus page contains older/inconsistent chair information; for current governance, prefer the university governance page above and preserve date/source if using names.

Sustainable Development and Cleaner Production Center public contact also exists:

- `sdcpc@bogazici.edu.tr`

Source:
https://yesilkampus.bogazici.edu.tr/tr/pages/sera-gazi-envanteri-ve-karbon-ayak-izi-calism/6910

## Questions

- What exactly is included in the published food-waste total?
- Generation date or collection date?
- Pre-consumer / edible surplus / plate waste separation?
- Which scale/record is authoritative?
- What campus/meal granularity exists?
- What KPI would be accepted for a pilot?
- What evidence is required before a sustainability reduction claim is defensible?

## Boundary

This role cannot validate that better demand forecasting is the root cause/intervention unless it directly owns that production workflow.

---

# P1 — Senior SKS administrative / approval route

Current SKS directory lists:

- **Eshabil Yıldız — Sağlık Kültür ve Spor Daire Başkanı**

Source:
https://sks.bogazici.edu.tr/tr/pages/kadromuz/2212

Use after workflow discovery if needed for:

- permission;
- contractor access;
- bounded pilot approval;
- cross-unit data approval;
- senior procurement/governance clarification.

Do not begin with a generic innovation pitch if branch-level discovery can answer the operational question.

---

# Interview sequence

```text
1. Food Services Branch
   -> identify real quantity owner + local TEMAŞ owner

2. TEMAŞ local production/project operator
   -> reconstruct forecasting, freeze time, economics, batch process

3. daily food engineer / production-adjacent operator
   -> current heuristic, buffer, incidents, records

4. BİD / BUCard data owner
   -> aggregate signal access + semantics

5. waste/sustainability measurement owner
   -> waste boundary + pilot KPI

6. same decision role at another Turkish university
   -> beachhead repeatability
```

---

# Evidence discipline

A scheduled meeting is not PMR evidence.

A person's public title is not proof that they own the production decision.

After each real interview, create a separate record from `INTERVIEW_TEMPLATE.md` and promote only narrow supported/contradicted claims into `EVIDENCE.md` with `E-INT-*` IDs.
