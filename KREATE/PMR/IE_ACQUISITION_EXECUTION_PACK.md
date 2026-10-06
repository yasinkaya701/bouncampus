# IE Acquisition Execution Pack

**Updated:** 2026-10-06  
**Owner:** IE — Customer Discovery & Market  
**Primary issues:** #292, #358  
**State:** READY_TO_REQUEST — no external request or interview is claimed as sent/completed by this document.

## Objective

Convert the two remaining IE external dependencies into bounded, privacy-preserving acquisition flows:

1. **#292 — BUCard/SKS service truth:** obtain the smallest aggregate chronological sample that CS1 can admit without person/card identifiers.
2. **#358 — contract/hakediş semantics:** obtain authoritative current-contract artifacts or source-owner answers sufficient to identify the payable quantity, freeze/change rights, acceptance/reconciliation flow and economic-risk owner.

Public/secondary research is routing evidence only. It does not satisfy either issue.

## Execution order

### Lane A — Food Services / operations reconstruction

Start with the first-party Food Services route in `S-BU-010` / `S-BU-011`. Ask for one **recent concrete service** rather than hypothetical product feedback.

Reconstruct, in order:

`quantity request → approval → production → campus allocation → service → correction/reconciliation → leftover/waste → acceptance/reporting`

For every step record:

- role that creates the record;
- record/system name;
- grain: university / campus / meal period / service date / item;
- when it becomes final;
- whether it is exportable;
- correction/reversal semantics;
- whether the value is known before the decision cutoff.

Do not infer ownership from job title.

### Lane B — BUCard/BİDB aggregate export (#292)

Use the technical/data-steward route via BUCard/BİDB and the semantic route via Food Services/SKS.

#### Minimum request

Request **aggregate rows only**, one row per:

`campus_id × meal_period × service_date`

Requested fields:

- `service_date`
- `campus_id`
- `meal_period`
- reported accepted passage / meal count under its source-native field name
- `package_meal_count`, if applicable
- `report_generated_at`
- stable `source_report_id`

Do **not** request person, student, staff, card, balance, transaction identifier, biometric or face data.

#### Reconciliation questions

1. Does one accepted BUCard passage/meal transaction equal one physically served meal?
2. How are retries, reversals, refunds, duplicate charges and turnstile/report corrections represented?
3. How are student/staff/guest/second-meal categories represented or aggregated?
4. Does package-meal count mean reservation, sale, preparation or pickup?
5. Which report state is accepted/final/reconciled and when?
6. Can the export be produced at exact campus × meal-period × service-date grain with stable report IDs?
7. Who owns `produced_portions`, accepted surplus/waste and shortage/early-sellout records at the same service grain?
8. Is there a pre-service operator/status-quo quantity snapshot with timestamp/version?

#### Evidence state

Use only these statuses:

- `NOT_REQUESTED`
- `REQUEST_READY`
- `FOLLOW_UP_REQUIRED`
- `ACCESS_GRANTED`
- `ACCESS_DENIED`
- `UNAVAILABLE`
- `ARTIFACT_RECEIVED_UNRECONCILED`
- `ARTIFACT_RECEIVED_RECONCILED`
- `HANDED_TO_CS1`

Never self-label `VERIFIED_EXPORTABLE` without source-owner/export evidence.

#### CS1 handoff

Preserve the original received artifact and provenance. Build one `SERVICE_TRUTH_V1` package and pass it through:

`scripts/cs1_service_truth_artifact_intake.py`

Do not rename a source-native passage/count field to `actual_served` until reconciliation is evidence-backed.

### Lane C — current contract / hakediş (#358)

Procurement anchor: `S-PROC-001`, IKN **2025/1727143**.

Retrieve, preferably from authoritative EKAP / university / source-owner copies:

- administrative specification;
- technical specification;
- unit-price bid schedule;
- current contract / acceptance clauses;
- penalty / SLA clauses;
- acceptance / hakediş form or schema;
- daily production request/order form;
- daily reconciliation / acceptance report.

If an artifact cannot be copied into the repository, record:

- exact title/version;
- IKN;
- source/owner;
- canonical retrieval route;
- access status;
- the narrow fact needed.

#### Contract questions to resolve

1. What unit/quantity is accepted for payment?
2. Who approves/signs acceptance and hakediş?
3. At what grain are quantities committed?
4. How are additional, second and package meals handled?
5. Who bears the economic cost of excess production?
6. What are shortage/early-sellout/quality consequences?
7. When can total production, campus allocation or batch size still change?
8. Is there a minimum/committed quantity?
9. Which record wins when BUCard, production and acceptance records disagree?
10. Can a human-reviewed recommendation legally and operationally change quantity before freeze?

The public unit-price contract form is **not** an answer to the payable-count question.

## Copy/paste request — BUCard / Food Services

> We are documenting the cafeteria planning workflow for a university sustainability project. We only need privacy-preserving aggregate operational records; we do not request any person/card/student/staff identifiers or balances. Could you confirm whether an export exists with one row per campus × meal period × service date containing the source-native served/passage count, package-meal count if applicable, report generation time and a stable report ID? We also need the report semantics: retries/refunds/reversals/corrections, second meals, package meals and which report state is considered final/reconciled. If possible, a small chronological sample covering several services is sufficient.

## Copy/paste request — procurement / acceptance

> For IKN 2025/1727143, we are trying to understand only the operational quantity and acceptance workflow. Could you point us to the authoritative current administrative/technical specifications, unit-price schedule, relevant acceptance/hakediş clauses and, if shareable, the daily production request and reconciliation/acceptance form? Our key questions are which quantity is payable/accepted, who approves it, when quantity changes freeze, and how excess/shortage/corrections are handled. If the documents cannot be shared, a source-owner answer to those narrow questions is sufficient.

## 20-minute interview flow

**0–3 min:** pick one recent service and identify campus + meal period.  
**3–8 min:** reconstruct quantity request, approval, freeze and contractor change rights.  
**8–13 min:** reconstruct served/passage, production, surplus/waste, shortage and corrections.  
**13–17 min:** identify acceptance/hakediş record and who bears excess/shortage risk.  
**17–20 min:** ask for the smallest shareable artifact/sample and the correct next owner/referral.

Do not spend the first interview pitching the product. First establish the decision and evidence chain.

## Cross-role handoff

### CS1

IE unlock condition:

- privacy-safe chronological service-level artifact;
- field provenance;
- report timing/finality;
- reconciliation semantics.

CS1 should continue to fail closed until those exist.

### CS2

IE unlock condition:

- confirmed buyer/approver/contract owner;
- payable quantity and economic-risk owner;
- actual freeze/change-right semantics.

Do not turn public contract value or generic sustainability goals into willingness-to-pay or savings claims.

### EE / EHB

IE unlock condition:

- map what production/waste/reconciliation records already exist;
- identify the exact missing measurement field/stage.

Do not introduce a new sensor before confirming the missing operational truth cannot be obtained from existing records.

## Stop conditions

Stop and record the blocker rather than inventing evidence when:

- the route refuses/does not own the data;
- only personal/transaction-level records are offered;
- only university-wide daily/monthly aggregates are available;
- current contract artifacts cannot be verified;
- a public/historical clause is being used as if current;
- the source cannot explain correction/finality semantics.

## Definition of done for this execution pack

This pack is complete when it makes #292/#358 directly executable without further research design.  
The issues themselves remain open until real source-owner evidence or artifacts are obtained.
