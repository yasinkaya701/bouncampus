# CS2 PMR-85 Product Decision Delta

**Date:** 2026-10-06  
**Owner:** CS2 — Product Strategy, Evidence Synthesis & Application  
**Base:** `role/cs2-product-strategy@750000523e9b27ba780dc7f60f147ac0549e745e`  
**Evidence class:** product synthesis over current repository evidence. This document is **not** customer evidence, pilot evidence, measured impact, or a contract interpretation.

## Executive decision

**KEEP the institutional-dining wedge, but only as a conditional decision-support hypothesis. Do not broaden the product and do not promote stronger claims yet.**

The current product candidate is not "AI food forecasting", not a sustainability dashboard, and not a waste-measurement device.

The narrow product hypothesis is:

```text
privacy-minimized aggregate operational signals
→ semantically reconcile what each count means
→ identify a still-reversible quantity/allocation decision
→ compare operator/current practice against the cheapest transparent baseline
→ add richer modeling only if it earns lift
→ issue a bounded human-reviewed recommendation
→ preserve the final operator action separately
→ measure service, surplus/waste, and shortage outcomes prospectively
→ promote only traceable evidence
```

This remains a hypothesis because the highest-value unknowns are still external and operational.

## What changed after the current PMR consolidation

At the base role commit, the canonical PMR surface contains 85 sources and a materially sharper evidence boundary. Later IE fan-in may advance that count; the product consequences below depend on the evidence classes and unresolved gates, not on the raw source count. The information gain is not "we now know the product works." The information gain is that several previously fuzzy assumptions are now isolated into explicit gates.

### 1. The operational stakeholder map is more concrete

Public procurement research identifies a current 2026–2027 food-service procurement surface, IKN **2025/1727143**, with TEMAŞ as the current contractor.

This supports a concrete interview/acquisition route across university Food Services, control/acceptance, contractor operations, BUCard/report ownership and procurement.

It does **not** establish:

- who sets the daily quantity;
- who may revise it;
- the freeze time;
- who benefits economically from reducing excess;
- what quantity is accepted for payment;
- whether the university or contractor would buy a decision-support product.

**Product consequence:** the current wedge is more interviewable, not more validated.

### 2. BUCard/passages are now an explicit semantic-risk surface

Current first-party/public context shows correction/refund handling and turnstile context are operationally relevant. That makes it unsafe to rename a passage count to `actual_served` without owner reconciliation.

**Product consequence:** a data product that skips semantic reconciliation is not acceptable. The source-truth/reconciliation step is part of the product architecture, not back-office cleanup.

### 3. Public waste totals are context, not service truth

The public 2024–2025 aggregate food-waste series is useful for scale/context, but the canonical PMR hub preserves semantic inconsistencies and does not treat those rows as service-level labels.

**Product consequence:** do not train, benchmark or claim operational impact from the aggregate public series.

### 4. Broad novelty claims are already weakened

The current competitor/source matrix contradicts several broad claims:

- generic kitchen-demand forecasting is not novel;
- generic food-waste measurement/feedback is not novel;
- a campus sustainability dashboard is not a defensible novelty claim.

**Product consequence:** differentiation must live at the unresolved operational control point, evidence chain, workflow fit, privacy-minimized integration, and decision verification — if PMR confirms those are valuable.

### 5. Contract context is strategically useful only if it changes the decision

The public notice indicates a unit-price contract form, but current settlement/hakediş semantics remain unknown.

**Product consequence:** contract research is not a product feature by itself. It matters only if it changes decision authority, freeze semantics, incentives, buyer identity or measurable savings attribution.

## Product portfolio decision

| Surface | CS2 status | Why |
| --- | --- | --- |
| Human-reviewed pre-freeze quantity/allocation decision support | **KEEP — CONDITIONAL** | Best current wedge, but blocked on owner/freeze/data/outcome truth. |
| Generic "AI demand forecasting" positioning | **KILL as positioning** | Established category; no defensible novelty claim. Modeling may remain an implementation method later. |
| Generic sustainability dashboard | **KILL as wedge** | Too broad and already commoditized; weak link to a reachable operational action. |
| Waste tracking/feedback as the main product | **KILL as differentiation** | Incumbents already cover substantial measurement/feedback territory. |
| Reservation/menu/calendar/weather signals | **HOLD as candidate features** | May help only after timing, availability and incremental lift are verified. |
| BUCard/turnstile aggregate counts | **HOLD pending semantic admission** | Potentially valuable, but cannot equal served demand by assumption. |
| New sensing hardware / TrayGate | **HOLD behind measurement gap** | No evidence yet that existing operational records cannot answer the needed field. |
| Contract/procurement evidence layer | **SUPPORTING CAPABILITY** | Useful for authority/incentive/verification, not a standalone wedge. |
| Model complexity beyond transparent baseline | **DEFER** | Must beat current practice / simple baseline on admitted real data. |

## CS2 evidence-acquisition mapping

This maps the existing `EA-01..EA-06` queue onto current cross-role work so agents do not create duplicate lanes.

| CS2 gate | Current owner / issue | Minimum fact needed | CS2 consequence |
| --- | --- | --- | --- |
| **EA-01 REACHABLE_DECISION** | IE + #358 where contract/operations documents expose authority | Who changes quantity/allocation, what can change, and the last reversible freeze time for one recent service | If no meaningful post-signal action exists, modify/kill the wedge. |
| **EA-02 SOURCE_EXPORTABILITY** | IE #292 | Owner-generated privacy-preserving aggregate export/schema and availability time | If only unjustified person-level raw logs are available, reject that path for the pilot. |
| **EA-03 SEMANTIC_MAPPING_VERIFIED** | IE #292 + CS1 admission | Mapping from reported count to operational truth, including corrections/exceptions | Keep target fail-closed until reconciled. |
| **EA-04 PHYSICAL_OUTCOME_MEASURABLE** | EE via #322; EHB #119 only if a proven sensing gap remains | Stage boundary, unit, method, timing, QA and shortage/surplus outcome | No causal waste claim without credible prospective measurement. |
| **EA-05 REPORTING_RECONCILIATION** | IE + CS1 via #82 / #322 and the reporting owner | Current produced/consumed/discarded definitions and reporting frequency | Keep as governance context if it cannot reconcile to a service-level decision. |
| **EA-06 INCENTIVE_AND_AUTHORITY_MAP** | IE #358 | Accepted-service/hakediş quantity, approval/signature path, corrections, relevant penalties/flexibility | Do not claim savings/WTP/buyer incentive until this is real. |

### Latest IE route progress — route narrowing, not gate closure

The latest first-party IE routing reduces acquisition ambiguity without satisfying the underlying CS2 gates. CS2 follows the canonical namespace freeze from IE #430:

- **S-BU-026** remains the current Food Services governance directive. It narrows the institutional owner path for BUCard/reporting and the food-service acceptance/hakediş actor set. This improves who to ask; it does **not** establish export permission, payable quantity, freeze/change rights, penalties, buyer identity or economics.
- IE separately verified named BUCard dining report surfaces. Because that finding is still being reconciled into the canonical source namespace, CS2 records it only as a **pending routing observation**, not as an S-BU-027 claim. **EA-02 remains OPEN_EXTERNAL** until a real aggregate export/schema/grain/finality/access decision is obtained.
- Report existence is not service truth. Until real aggregate rows and SKS semantic reconciliation exist, **EA-03 remains OPEN_EXTERNAL** and BUCard/passages stay inadmissible as `actual_served` by assumption.
- **S-BU-027** is Tahakkuk, **S-BU-028** is the İMİD contact route, **S-BU-029** is İhale ve Satınalma, and **S-BU-030** is the 2025 Administration Activity Report acceptance-flow evidence. Together they narrow where to request the current tender/acceptance/hakediş artifacts, but they do not reveal the accepted/payable operational quantity, freeze point, correction rights, penalties, WTP or value capture. **EA-06 remains OPEN_EXTERNAL**.

CS2 consequence: spend the next primary-evidence cycle on retrieving and reconciling these named artifacts, not on broad new secondary research or on promoting stronger application claims.

### Application claim → IE owner/report route linkage

The route findings above are now tied explicitly to the submission claim ledger in `KREATE/APPLICATION_RUBRIC.md`; SAFE/BLOCKED/KILL policy remains governed by `KREATE/PMR/CS2_APPLICATION_CLAIM_GATE_2026-10-06.md`. These links narrow **who owns the next evidence request**; they do not upgrade the claim's evidence class or submission status.

| Application claim | Current claim state | Gate(s) | Canonical IE route evidence | What is now established | Still required before any promotion |
| --- | --- | --- | --- | --- | --- |
| **C-005** — a material, still-reversible pre-service quantity/batch/allocation decision exists | **HYPOTHESIS / DRAFT** | EA-01, EA-06 | S-BU-026 Food Services governance; S-BU-029 İhale ve Satınalma; S-BU-030 Control Organization / acceptance flow | Named governance, procurement and acceptance routes for reconstructing the decision chain | Actual daily decision owner, decision object, revision rights, freeze/cutoff and one recent service reconstruction |
| **C-007** — privacy-minimized service-level operational truth is exportable and semantically usable | **UNKNOWN / DRAFT** | EA-02, EA-03 | S-BU-026 narrows the BUCard/reporting owner path; named BUCard dining report surfaces remain a pending routing observation with no canonical source ID yet | The next owner/reporting route to request an aggregate export is narrower | Export permission, actual aggregate rows, schema, grain, availability/finality time, correction semantics and SKS reconciliation. **Do not bind this claim to S-BU-027; S-BU-027 is Tahakkuk.** |
| **C-008** — the intended operational user can safely act on a recommendation before freeze | **HYPOTHESIS / DRAFT** | EA-01, EA-06 | S-BU-026 Food Services governance; S-BU-030 acceptance-flow evidence | Candidate operational/acceptance actor path is narrower | Action authority, approval path, freeze time, override behavior, risk guardrails and observed willingness to use the recommendation |
| **C-010** — “BUCard/turnstile count equals meals physically served” | **CUT** | EA-03 | S-BU-026 plus the pending named BUCard report-surface observation | Only the owner/reporting path is narrower | Source-owner semantics, corrections/refunds/duplicates/second-meal handling and reconciliation. Route discovery can never by itself restore the forbidden equality claim |
| **C-014** — “public tender scale proves buyer WTP or favorable contract economics” | **CUT** | EA-06 | S-BU-027 Tahakkuk; S-BU-029 İhale ve Satınalma; S-BU-030 acceptance flow | Payment-processing, procurement/specification and acceptance routes are named | Accepted/payable quantity, unit-price mechanics, exact Spending Authority, penalties, freeze/change rights, economic beneficiary, buyer and WTP |

**Claim firewall:** all five mappings are routing progress only. They promote **zero** application claims. EA-02, EA-03 and EA-06 remain `OPEN_EXTERNAL`; C-010 and C-014 remain `CUT`; C-005/C-007/C-008 remain unverified until the primary artifacts or owner answers listed above are obtained.

### Cross-role dependency compression

For the next CS2 decision cycle, the six gates effectively compress into three external truth packages:

1. **Decision rights package** — owner, change rights, freeze time, current planning record.
2. **Service truth package** — aggregate export, field semantics, corrections/reconciliation, authoritative report.
3. **Outcome + economics package** — surplus/waste/shortage measurement plus accepted-service/hakediş semantics.

This should reduce duplicate PMR work. New secondary browsing is lower value than closing these packages.

## What CS2 should ask each role for next

### IE

Return artifacts/facts, not generic opinions:

- one recent service-day swimlane;
- initial quantity/request;
- every material revision;
- who approved each revision;
- final freeze/cutoff;
- current planning heuristic/system;
- current production/allocation record;
- one surplus incident and one shortage incident;
- source owner for aggregate service truth;
- current accepted-service / hakediş semantics.

Route real service-truth work through **#292** and contract/acceptance work through **#358**.

### CS1

Do not spend the next cycle optimizing model architecture before admitted data exist.

Prepare for the moment real data arrive:

- preserve the service-truth intake gate;
- keep operator/current practice as a baseline;
- define the cheapest transparent benchmark;
- preserve decision-time feature availability;
- represent uncertainty/abstention;
- keep recommendation separate from final human action;
- reject leakage and unreconciled targets.

### EE

Define the lightest prospective measurement protocol that can distinguish:

- preparation waste;
- unserved surplus;
- service/holding discard;
- plate waste;
- shortage / early sellout / emergency replenishment.

Do not assume a new device is needed. First identify whether existing records + direct weighing can close the pilot truth loop.

### EHB

Remain downstream of an explicit missing physical field.

Only advance hardware toward a pilot when EE/IE show:

- which field is missing;
- why existing systems cannot provide it;
- required unit/range/timing;
- calibration/QA requirement;
- operational placement;
- how that field changes a decision or evidence gate.

## Claim-policy alignment

Application claim wording is owned by the now-integrated canonical CS2 claim gate:

- `KREATE/PMR/CS2_APPLICATION_CLAIM_GATE_2026-10-06.md`

This product-delta artifact must not create a second SAFE/BLOCKED/KILL claim vocabulary. Its responsibility is narrower: product portfolio decisions, acquisition priority, cross-role dependencies, and wedge keep/modify/kill logic.

When wording in this file and the canonical claim gate appear to overlap, the claim gate controls application wording; this file controls the product-strategy consequence.

## Product kill / modify triggers

The dining wedge should be modified or killed if primary evidence shows any of the following:

1. useful signals arrive after the material quantity decision is already irreversible;
2. the real operator has little or no discretion to change quantity/allocation;
3. demand mismatch is not a material cause of avoidable surplus/waste;
4. there is no trustworthy service-level outcome or prospective measurement path;
5. shortage risk makes the proposed intervention unacceptable under realistic guardrails;
6. current practice/simple rules perform adequately and richer modeling adds no decision value;
7. the user, economic beneficiary and approval/buyer chain cannot be aligned;
8. privacy-minimized aggregate data are insufficient and the only workable design requires unjustified person-level tracking;
9. the operational burden of recording/approving recommendations exceeds plausible value.

## Current CS2 recommendation

**Do not expand scope. Do not start another generic research dump. Do not build a new model/hardware layer to create the appearance of progress.**

The highest-value next move is to close #292 and #358 enough to answer:

```text
Can a named operator change a named quantity
before a named cutoff
using a privacy-minimized signal
and can we measure the consequence prospectively?
```

If yes, CS2 should convert that concrete workflow into the pilot specification and application narrative.

If no, CS2 should modify or kill the current dining wedge rather than weakening the evidence bar.
