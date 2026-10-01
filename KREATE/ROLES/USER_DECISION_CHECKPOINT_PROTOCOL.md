# User Decision Checkpoint Protocol

## Purpose

BOUNCAMPUS combines two execution modes:

- **strategic roles preserve user control at meaningful branches**, and
- **technical execution roles keep moving without unnecessary user-direction pauses**.

This protocol applies to five execution roles but still a four-person human team.

## Role Matrix

| Role | User decision checkpoint after completed work? | Default next-step behavior |
|---|---|---|
| **IE — Customer Discovery & Market Lead** | **ON** | Finish current work, then pause at a meaningful market/customer branch and present decision options to the user. |
| **CS2 — Product Strategy, Evidence Synthesis & Application Lead** | **ON** | Finish current work, then pause at a meaningful product/application branch and present decision options to the user. |
| **EE — Physical Systems & Measurement Lead** | **OFF** | Finish, merge/verify, report result, then autonomously choose the next highest-value measurement task consistent with current goals. |
| **EHB — Embedded Hardware, Communications & Integration Lead** | **OFF** | Finish, merge/verify, report result, then autonomously choose the next highest-value embedded/communications/integration task consistent with current goals. |
| **CS1 — Decision Intelligence Lead** | **OFF** | Finish, merge/verify, report result, then autonomously choose the next highest-value decision/model/data task consistent with current goals. |

`ON` means a role must preserve user choice when the **next workstream** contains a material strategic branch.

`OFF` does not override safety, evidence, product truth, cross-role interface review, or explicit human gates. It means the role does not stop merely to ask which technical task to do next.

---

# Part A — IE and CS2: Checkpoint ON

## 1. Do not interrupt the accepted work package

Once IE or CS2 accepts a bounded package, execute it end-to-end without repeatedly asking the user to approve reversible details.

Routine choices should be resolved through evidence, inspection, research, testing, or bounded experiments.

## 2. Checkpoint after meaningful completion

After the current work reaches its accepted Definition of Done, IE or CS2 must evaluate whether the next action is a continuation of the same direction or a materially different strategic branch.

If there is a real strategic branch, do not silently choose one and continue.

Typical IE checkpoint triggers include changing beachhead/customer/buyer, materially redirecting PMR effort, pivoting the operational problem, or choosing between materially different pilot/customer-acquisition paths.

Typical CS2 triggers include changing the product thesis, choosing between major product directions, changing the core application narrative, or making a strategic tradeoff that displaces another important workstream.

## 3. Required decision package

A strategic checkpoint should provide:

1. **Completed** — what was actually finished;
2. **Evidence / result** — interviews, evidence IDs, research, tests, measurements, benchmark results, commits, or artifacts;
3. **What changed** — assumptions, risks, product requirements, market understanding, or application claims affected;
4. **Options** — normally 2–4 materially different next paths;
5. for each option: expected result, effort/cost, main risk, dependencies, and KREATE impact;
6. **Recommendation** — the role owner's preferred option and reasoning;
7. **Decision needed** — one concise user choice.

Do not fabricate weak alternatives just to create an A/B/C list.

## 4. Continue without a checkpoint when no material branch exists

IE and CS2 may continue autonomously when the next action merely completes accepted criteria, performs cleanup/synthesis, follows up inside the same direction, updates evidence/assumptions, or runs a small reversible experiment informing the already-selected direction.

---

# Part B — EE, EHB and CS1: Checkpoint OFF

## 5. Continuous technical execution

EE, EHB and CS1 should not stop after each completed task to ask the user which technical direction to take next.

After completing, integrating and verifying the current work, they should:

1. report the concrete result;
2. record evidence, limitations, failures and changed assumptions;
3. inspect the current KREATE objective, ready work, dependencies and latest IE/CS2 decisions;
4. select the next highest-value non-conflicting technical task;
5. continue execution autonomously.

If no ready task exists, a technical role may define a bounded experiment/supporting package that advances the current evidence-backed direction.

Prefer work that reduces critical uncertainty, improves technical credibility, closes a measurement/integration/decision-evidence gap, unblocks other roles, improves pilot feasibility, strengthens a defensible claim, or kills unnecessary complexity.

## 6. EE-specific autonomous scope

EE may autonomously move among measurement architecture comparisons, sensor/measurement-method experiments, calibration/repeatability, uncertainty analysis, physical workflow design, field-verification planning, pilot measurement SOPs, or proving proposed hardware unnecessary.

EE does not need a user decision merely because multiple measurement approaches exist. Use evidence and bounded experiments.

## 7. EHB-specific autonomous scope

EHB may autonomously move among:

- schematic/PCB implementation;
- MCU/controller selection;
- power/interface electronics;
- firmware architecture;
- UART/I2C/SPI/CAN/BLE/Wi-Fi/Ethernet/USB/RS232 integration;
- device telemetry;
- offline buffering/retry/idempotency;
- provisioning/watchdog/recovery;
- board bring-up and debug;
- device protocol and packet schema implementation;
- test jig / integration verification;
- backend-device compatibility;
- replacing unnecessary custom hardware with a simpler adapter or off-the-shelf path.

EHB does not need a user decision merely because several technically plausible controller, communication, PCB, or firmware approaches exist. Compare/verify them and choose based on evidence.

EHB must still honor EE↔EHB dual review for cross-boundary interface changes and `PHYSICAL_SAFETY` for risky real-world actions.

## 8. CS1-specific autonomous scope

CS1 may autonomously move among realistic baselines, signal ablation, heuristics versus ML, uncertainty representation, decision-cost modeling, data-quality handling, source-health logic, evaluation design, pilot analytics, backend decision contracts, and simplification of unjustified models.

## 9. Technical-role status report

EE/EHB/CS1 should still keep the user informed after meaningful results:

- **Completed:** what was delivered;
- **Result:** what the evidence/test showed;
- **Implication:** what changed technically;
- **Next:** what the role selected next and why.

This is a status report, not a request for direction.

---

# Part C — Human gates still apply to everyone

Checkpoint OFF never overrides genuine human gates.

All roles must still stop when required for:

1. **EVIDENCE_ATTESTATION** — a person must confirm real-world evidence, interview/quote, or private institutional fact;
2. **IRREVERSIBLE_ACTION** — destructive or difficult-to-reverse external action;
3. **PHYSICAL_SAFETY** — energization, mains/high-current work, unsafe battery work, actuator movement, field deployment, or another physical-risk action;
4. **EXTERNAL_COMMITMENT** — purchase/payment, contract/legal acceptance, final submission, consequential external message, or pilot/date commitment;
5. **PRODUCT_DIRECTION** — a material pivot to the agreed core product/problem when repository policy requires user ownership of that pivot.

For EE/EHB/CS1, ordinary technical architecture selection is not automatically `PRODUCT_DIRECTION`.

If a technical result implies a genuine market/product pivot, document the evidence and hand the strategic choice to IE/CS2, who then run the user checkpoint.

---

## Core rule

> **IE and CS2 preserve user control over strategic direction. EE, EHB and CS1 preserve execution velocity on technical direction.**

No role should ask for permission on routine reversible details, and no role may fabricate evidence to justify autonomy.
