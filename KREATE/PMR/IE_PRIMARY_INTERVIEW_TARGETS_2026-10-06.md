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

### Source-backed routing note

Current public evidence supports the referral sequence:
`Dining Control Organization → Procurement branch → exact Spending Authority → Tahakkuk payment route`.

Aygül Demir is publicly listed as a principal member of the current dining control organization (`S-BU-014`). This makes the control role a high-information target, but **no outreach, scheduling or completed interview is claimed here**.

`S-BU-031` adds a formal question for this interview lane: how do the Food Service Executive Board + Inspection and Acceptance Commission duties for meal hakediş payment orders/accrual connect to the Control Organization → KİK56.0/H → Spending Authority flow in practice?

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
