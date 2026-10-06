# PMR Operational Contact & Role Map

**Updated:** 2026-10-06  
**Rule:** this is a **routing map**, not evidence that a person owns a decision or has agreed to an interview.

## First-party Boğaziçi routes

### Food Services branch

- Sources: `S-BU-010`, `S-BU-011`
- Public role surface includes the Food Services Branch Manager and office staff.
- Interview objective: reconstruct one recent service from quantity request → production → campus distribution → served/corrected counts → leftover/waste → acceptance/reporting.

Do not pre-assign "quantity owner", "buyer", "data owner" or "approver" from a job title.

### Dining cooking / distribution control organization

- Source: `S-BU-014`
- Public university governance page lists an official **Yemekhane, Yemek Pişirme ve Yemek Dağıtım Kontrol Teşkilatı**.
- Interview objective: learn what the control organization actually checks, which records it sees, what is accepted/rejected, and what happens when service quantity/quality differs from plan.

### BUCard / service-count reconciliation

- **S-BU-021:** current BİDB service inventory lists BUCard as a BİDB service and gives `bucard@bogazici.edu.tr`; cafeteria top-up/refund lists SKS + BİDB; turnstile/card-reader faults route to BİDB.
- **S-BU-022:** official BUCard portal confirms dining-hall use and BUCard Office/contact route.
- **S-BU-023:** BUCampus exposes user-facing turnstile/card-reader passage history.
- **S-BU-024:** institutional notice places BUCard among applications requiring BUVPN in that access context.

This moves the route from a generic "ask IT" hypothesis to a source-backed BİDB/BUCard + SKS reconciliation path. It still does not prove export approval.

### Existing Food Services correction context

- Source: `S-BU-015`
- Official FAQ references overcharge/refund issues with date, time, campus and turnstile information and notes BUCampus QR access.
- Interview objective: find the authoritative privacy-safe aggregate report and clarify retries, refunds/reversals, second meals, package meals, late corrections and report finalization.

Issue **#292** remains the active acquisition lane.

### TEMAŞ contractor operations

- Procurement anchor: `S-PROC-001`
- Public result identifies TEMAŞ as the 2026–2027 contractor.
- Interview objective: find local production-planning/operations and contract/acceptance counterparts.

Do not use generic company contacts as evidence of the Boğaziçi account owner; ask Food Services/control/procurement participants for the correct local referral.

### Procurement / contract document route

- **S-BU-026 — İhale ve Satınalma Şube Müdürlüğü**
  - official procurement/tender process route;
  - current public manager: Bahadır Şahin;
  - use: current IKN 2025/1727143 specification/document retrieval and procurement-process questions.
- **S-BU-027 — Tahakkuk Şube Müdürlüğü**
  - official branch states it performs hakediş payments;
  - current public manager: Yakup Korkmaz;
  - use: identify the payment package, required acceptance artifacts and payable-count source.
- **S-BU-030 — 2025 Administration Activity Report**
  - confirms Control Organization → KİK56.0/H → relevant Spending Authority → hakediş workflow.
- **S-BU-014 — current Control Organization roster**
  - Aygül Demir is publicly listed among principal members.
  - This is a **routing fact only**. No interview is marked completed without real notes.

### PMR referral sequence for #358

~~~text
Food Services / SKS
→ current Dining Control Organization
→ Procurement branch (specifications / tender documents)
→ relevant Spending Authority
→ Tahakkuk branch (hakediş payment package)
→ TEMAŞ local operations / planning
~~~

Ask each person to identify the next artifact owner rather than assuming job titles equal decision ownership.

## Signal-owner map

| Signal / artifact | Public clue | Actual owner/status |
| --- | --- | --- |
| menu | S-BU-004 | public; historical immutable snapshot process to verify |
| menu preference votes | S-BU-013 | BUCampus workflow exists; export owner/semantics unknown |
| service windows | S-BU-016 | public context |
| academic calendar | S-BU-019 | public/versioned context |
| student events | S-BU-018 | public context; attendance generally unknown |
| BUBizden entitlement | S-BU-017 | app workflow exists; not served-demand truth |
| BUCard/turnstile corrections | S-BU-015, S-BU-021, S-BU-023 | BİDB/BUCard technical route now source-backed; aggregate export + service semantics still pending #292 |
| production/allocation | — | pending PMR |
| stage-separated waste | — | pending PMR / measurement |
| acceptance/hakediş | S-BU-030 confirms KİK56.0/H → Spending Authority workflow; S-BU-027 is hakediş-payment route | payable count, exact food-contract Spending Authority and current clause semantics still pending #358 |
| contractor production planning | S-PROC-001 identifies TEMAŞ | local owner/workflow pending PMR |

## Interview order

1. Food Services operational lead / branch route.
2. Dining cooking/distribution control participant.
3. TEMAŞ local operations/production-planning referral.
4. BUCard/BİDB aggregate-report owner + Food Services semantic owner.
5. Procurement/contract/acceptance owner.
6. Waste measurement/sustainability owner.
7. Comparable second institution.

For every conversation, use [INTERVIEW_TEMPLATE.md](INTERVIEW_TEMPLATE.md) and promote only narrow supported/contradicted claims.

See [PRIMARY_EVIDENCE_ACQUISITION.md](PRIMARY_EVIDENCE_ACQUISITION.md) for the exact minimal artifact/request packet.
