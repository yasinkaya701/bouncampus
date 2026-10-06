# CS2 Application Claim Gate — 2026-10-06

**Owner:** CS2 — Product Strategy, Evidence Synthesis & Application  
**Task:** #361  
**Purpose:** convert the current PMR/research surface into an application-safe decision gate without creating another source registry.

Canonical evidence/research surfaces:
- [CLAIM_SOURCE_MATRIX.md](./CLAIM_SOURCE_MATRIX.md)
- [HYPOTHESIS_FALSIFICATION_MATRIX.md](./HYPOTHESIS_FALSIFICATION_MATRIX.md)
- [DATA_SOURCE_INVENTORY.md](./DATA_SOURCE_INVENTORY.md)
- [PROCUREMENT_CONTRACT_RESEARCH.md](./PROCUREMENT_CONTRACT_RESEARCH.md)
- [OPERATIONAL_CONTACT_ROLE_MAP.md](./OPERATIONAL_CONTACT_ROLE_MAP.md)
- [AGENT_HANDOFF.md](./AGENT_HANDOFF.md)
- [../EVIDENCE.md](../EVIDENCE.md)
- [../ASSUMPTIONS.md](../ASSUMPTIONS.md)

Open primary-evidence dependencies:
- #292 — BUCard / SKS aggregate service-truth acquisition and semantic reconciliation
- #358 — authoritative current tender/specification + hakediş / acceptance semantics
- #82 — service-level dining truth dataset / CS1 admission path
- #322 — PMR shared intake and cross-agent handoff

## Status vocabulary

- **SAFE_NOW** — defensible as a narrow repository/public-source fact with the current evidence boundary.
- **HYPOTHESIS_ONLY** — may be stated only as something the team is testing; not as a customer fact.
- **BLOCKED** — do not make the claim until the listed primary artifact/evidence exists.
- **KILL** — wording is already contradicted, overbroad, or structurally unsafe and should not appear.

## Executive claim gate

| Application claim | Gate | What can be said now | What unlocks a stronger claim | Falsifier / downgrade trigger | Owner |
| --- | --- | --- | --- | --- | --- |
| BOUNCAMPUS targets institutional dining operations before avoidable food waste occurs. | SAFE_NOW | This is the team's current product wedge and repository direction. | Real PMR showing the pre-service decision is both reachable and valuable. | PMR shows the actionable decision lies elsewhere or the wedge is not material. | CS2 + IE |
| Boğaziçi has a current outsourced food-service/procurement surface and identifiable operational routing. | SAFE_NOW | Public sources identify current procurement/contract context and relevant operational roles. | Authoritative current specifications, acceptance and settlement documents. | Current authoritative documents contradict the assumed contract/role interpretation. | IE / #358 |
| A reachable quantity-control decision exists before demand is realized. | HYPOTHESIS_ONLY | We are testing whether quantity, batch release, allocation or a related pre-service decision remains adjustable. | One recent service reconstructed end-to-end from decision owner + contractor/production participant, with freeze time and revision rights. | Quantity is fixed too far upstream, not revisable, or the actionable object is different. | IE |
| Demand mismatch materially causes avoidable Boğaziçi food waste. | BLOCKED | Public waste totals establish waste exists, not its cause. | Recent mismatch incidents plus stage-separated service truth linking cause → decision → surplus/shortage outcome. | Plate waste, quality/menu, preparation loss, safety rules or other causes dominate the addressable waste. | IE + EE |
| Operators intentionally maintain a shortage-risk buffer. | HYPOTHESIS_ONLY | Other institutions/literature make asymmetric shortage risk plausible; Boğaziçi behavior is unverified. | Recent surplus and shortage incidents plus explicit current buffer/heuristic and consequence chain. | No intentional buffer, shortage risk is negligible, or contract fixes the quantity independently of operator judgment. | IE + CS1 |
| Service-level operational data are available for model training/evaluation. | BLOCKED | Candidate public signals exist; service truth access and semantics are unverified. | Real aggregate export or prospective measurement artifact with data dictionary, timestamps, source owner and reconciliation rules. | Required fields are unavailable, semantically incompatible, too delayed, or too burdensome/privacy-sensitive to collect. | #292 + #82 + EE |
| BUCard/turnstile counts equal meals served. | KILL | Do not make equivalence claims. Official workflows already imply corrections/refunds/QR/turnstile semantics that require reconciliation. | A source-owner data dictionary and reconciled aggregate export may support a narrower proxy relationship. | Any unresolved retry/refund/duplicate/second-meal/late-correction semantics. | #292 |
| Weekly menu preference votes are demand labels. | KILL | Treat them only as a candidate preference feature. | Timestamp/version semantics plus measured incremental value against real service labels. | Votes do not map to attendance/pickup or are unavailable before the decision cutoff. | CS1 |
| Reservation intent reduces demand uncertainty at the target workflow. | HYPOTHESIS_ONLY | A reservation workflow exists in some contexts; campus-wide/current coverage is not established. | Current workflow, cutoff, cancellation/no-show and served reconciliation evidence. | Reservation is exceptional, late, weakly coupled to pickup, or unavailable at the decision point. | IE + CS1 |
| Generic AI demand forecasting is BOUNCAMPUS's novelty. | KILL | Forecasting is an established method and is commercially available. | No unlock; novelty must be narrower than generic forecasting. | Existing competitors continue to provide forecasting capability. | CS2 |
| Food-waste measurement/feedback alone is differentiated. | KILL | Measurement/feedback is already served by incumbents. | No unlock; differentiation must focus on an unresolved decision/workflow gap. | Existing incumbent capability remains broad enough to cover the proposed value. | CS2 + EE |
| A broad campus sustainability dashboard is novel. | KILL | Do not use broad novelty language. | No unlock; retain only a narrower operations/evidence wedge if PMR supports it. | Existing campus sustainability platforms already cover broad dashboard/evidence functionality. | CS2 |
| Human-reviewed decision support can fit operations safely. | HYPOTHESIS_ONLY | The repository implements human-gated/abstaining decision logic; workflow adoption is unvalidated. | Evidence that operators already revise plans based on new information, plus trust threshold, timing and non-negotiable guardrails. | Required approval/food-safety/contract constraints make recommendations too late or unusable. | IE + CS1 |
| BOUNCAMPUS can reduce Boğaziçi food waste. | BLOCKED | The repository contains a falsifiable pilot design; no measured local effect exists. | Pre-registered control/intervention measurement with stage-separated outcomes and shortage/service guardrails. | No measurable improvement, displacement into another waste stage, or service harm. | EE + CS1 + CS2 |
| BOUNCAMPUS can reduce climate impact. | BLOCKED | Prevention frameworks support the causal direction in principle; no local measured effect exists. | Measured food-waste reduction first, then a transparent impact conversion with boundary/uncertainty. | Food-waste reduction is not measured or the conversion boundary is not defensible. | CS2 + EE |
| A buyer will pay because current food volume/waste is large. | KILL | Public scale is not willingness-to-pay evidence. | Economic-buyer interview, current process/software cost, purchase criteria, budget/procurement route. | Benefit accrues to a party that does not control purchase or savings are not economically material to buyer. | IE + #358 |
| TEMAŞ/SKS economics favor lower production. | BLOCKED | Current public contract context exists; incentive direction is unknown. | Hakediş/payment basis, unit-price mechanics, waste/excess cost bearer, shortage/penalty responsibility. | Contract structure rewards/neutralizes volume reduction or shifts savings away from the buyer/user. | #358 + IE |
| The same product/workflow repeats beyond Boğaziçi. | BLOCKED | Other institutions show analogous practices, not repeatable same-product demand. | At least one second-site workflow reconstruction with same control point, buyer path and evidence needs. | Second site uses materially different governance, contract, timing or data semantics requiring a different product. | IE + CS2 |

## Application wording firewall

### Safe wording now

Use language of the form:

> We are testing a pre-service institutional dining decision-support wedge at Boğaziçi. Public and repository evidence establishes that food waste exists, that operational planning and procurement surfaces are real, and that forecasting/measurement technologies already exist. Our current unanswered question is narrower: whether a reachable production or allocation decision, combined with reliable service-level truth and operator guardrails, creates a useful prevention workflow.

This wording:
- does not claim local causal validation;
- does not claim measured savings;
- does not claim unique AI;
- does not imply access to private university telemetry;
- makes the key uncertainty explicit.

### Unsafe wording until primary evidence exists

Do not write:
- “Boğaziçi overproduces because demand is unpredictable.”
- “Our AI predicts cafeteria demand accurately.”
- “BUCard data tells us exactly how many meals were served.”
- “The contractor saves money when fewer meals are produced.”
- “We reduce food waste / carbon by X%.”
- “Operators want this.”
- “BOUNCAMPUS is the first AI food-waste platform.”
- “Competitors only measure waste after it happens.”
- “The university is ready to pilot/buy.”

## Primary-evidence unlock queue

### P0 — decision owner + freeze point
**Required artifact:** one recent service reconstruction with:
- quantity/batch/allocation decision object;
- decision timestamp;
- named role;
- revision rights;
- practical freeze point;
- last real change and trigger;
- approval/override path.

**Product consequence:**
- if supported → keep pre-service decision wedge;
- if different control point appears → modify product around that control point;
- if no reachable control point → kill current wedge.

**Owner:** IE.  
**Consumers:** CS1, CS2, EE.

### P1 — waste-stage causality
**Required artifact:**
- recent mismatch event;
- waste stage;
- cause;
- what was recorded;
- what decision could have changed the outcome;
- preparation / unserved edible surplus / plate waste separation where feasible.

**Product consequence:**
- if demand mismatch is material → continue forecasting/decision-support test;
- if another cause dominates → redirect product to the actual controllable cause.

**Owner:** IE + EE.  
**Consumers:** CS1 + CS2.

### P2 — shortage asymmetry
**Required artifact:**
- last shortage incident;
- last surplus incident;
- current buffer/heuristic;
- complaint/substitution/emergency production/penalty consequences;
- who bears each consequence.

**Product consequence:** define decision loss and guardrails before model optimization.

**Owner:** IE.  
**Consumer:** CS1 + CS2.

### P3 — service truth and semantics
**Required artifact:**
- privacy-safe date × campus × meal sample;
- field dictionary;
- produced / served / surplus / waste semantics;
- source owner;
- before/after-service timestamps;
- corrections/refunds/duplicates/second-meal handling where card data is involved.

**Dependency:** #292 → #82.

**Product consequence:**
- if viable → benchmark current heuristic before richer models;
- if not viable → use a minimal prospective measurement protocol for the missing field only.

**Owner:** CS1 + IE + EE.

### P4 — contract economics / buyer
**Required artifact:**
- authoritative current specs/contract documents;
- payment/hakediş basis;
- acceptance quantity;
- who bears excess ingredient/labor cost;
- who bears shortage/recovery/penalty cost;
- software purchase/requirement authority;
- contract-renewal technical-specification owner.

**Dependency:** #358.

**Product consequence:** buyer, value proposition and procurement strategy may change even if end-user workflow is attractive.

**Owner:** IE.  
**Consumer:** CS2.

### P5 — second-site repeatability
**Required artifact:** one mature institutional dining operation outside the immediate Boğaziçi workflow, tested using the same H1–H6 structure.

**Product consequence:**
- same control point + similar buyer path → stronger beachhead repeatability;
- materially different process → segment more narrowly instead of claiming a broad institutional market.

**Owner:** IE + CS2.

## Cross-role handoff

### IE
Highest-value next evidence is not another generic source. Deliver:
1. recent service owner/freeze reconstruction;
2. one surplus and one shortage incident;
3. contract/economic owner chain;
4. second-site same-workflow test.

Do not convert “sounds useful” or sustainability enthusiasm into promotable evidence.

### CS1
Do not optimize richer models before:
1. #292/#82 produce admitted service truth;
2. naive/operator baseline exists;
3. all historical features pass decision-cutoff timing checks;
4. shortage/surplus asymmetry is explicit.

Return to CS2:
- what is technically implemented now;
- what is only simulated/sandboxed;
- what measured result, if any, is actually promotable.

### EE
Prioritize the measurement boundary, not a new sensor:
1. which stage/outcome is decision-critical;
2. which field already exists reliably;
3. which missing field truly requires prospective measurement;
4. calibration/quality metadata required to make that field promotable.

### EHB
No hardware novelty claim is application-critical unless IE/EE prove a missing field that existing operational data cannot satisfy.

### CS2
Until primary evidence changes the gate:
- own truthful application wording;
- keep generic AI / dashboard / measurement novelty claims killed;
- keep local savings, causal root cause, WTP and climate impact blocked;
- change the product thesis when evidence changes the reachable control point.

## Decision rules

1. **Primary evidence outranks narrative coherence.**
2. **Contradictions are preserved, not averaged away.**
3. **A public source can motivate a hypothesis; it cannot validate a Boğaziçi customer claim.**
4. **A repository implementation proves implementation state only.**
5. **No model metric becomes customer value without real service truth and a decision baseline.**
6. **No measured food-waste reduction means no measured climate reduction.**
7. **No buyer/economic-chain evidence means no WTP claim.**
8. **If H1 or H2 fails, change the wedge rather than defending sunk work.**

## Next CS2 checkpoint

CS2 should revisit this gate immediately when any of these lands:
- #292 real aggregate export / semantic reconciliation;
- #358 authoritative current procurement/settlement documents;
- a completed real workflow interview that produces promotable evidence;
- a second-site same-workflow interview;
- stage-separated service measurement;
- a leakage-safe benchmark on admitted real labels.

Until then, the strongest application story is an evidence-disciplined problem thesis with explicit falsifiers — not a fabricated “validated AI solution” story.
