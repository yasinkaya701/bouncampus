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

### Procurement, payment and acceptance chain

- **S-BU-026:** current Food Services governance directive narrows the institutional process: meal hakediş payment-order/accrual work is carried out by the Food Services Board together with the Muayene Kabul Komisyonu; meal-service procurement is routed through SKS + İMİD.
- **S-BU-027:** official İhale ve Satınalma unit — authoritative procurement/tender-document routing.
- **S-BU-028:** official Tahakkuk unit — first-party payment/hakediş processing route.
- **S-BU-029:** official İMİD contact surface — fallback institutional routing.
- **S-BU-030:** 2025 Administration Activity Report — Control Organization performs preliminary service acceptance, prepares KİK56.0/H, and submits it to the relevant Spending Authority for hakediş preparation.

Interview/acquisition objective: identify the **exact food-contract Spending Authority**, actual hakediş artifact, payable/accepted quantity basis, and who can change production/allocation before the operational freeze.

Do not promote this institutional chain into a claim that any one unit is the software buyer, savings beneficiary, quantity owner or final contract signatory.

### TEMAŞ contractor operations

- Procurement anchor: `S-PROC-001`
- Public result identifies TEMAŞ as the 2026–2027 contractor.
- Interview objective: find local production-planning/operations and contract/acceptance counterparts.

Do not use generic company contacts as evidence of the Boğaziçi account owner; ask Food Services/control/procurement participants for the correct local referral.

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
| acceptance/hakediş | S-BU-026, S-BU-028, S-BU-030 narrow governance/payment/acceptance routing | exact food-contract Spending Authority + payable quantity + actual hakediş artifact pending #358 |
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
