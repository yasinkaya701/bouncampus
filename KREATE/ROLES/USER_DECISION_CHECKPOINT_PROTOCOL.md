# User Decision Checkpoint Protocol

## Purpose

BOUNCAMPUS should combine two different execution modes:

- **strategic roles preserve user control at meaningful branches**, and
- **technical execution roles keep moving without unnecessary user-direction pauses**.

This protocol therefore does **not** apply equally to all four KREATE roles.

## Role Matrix

| Role | User decision checkpoint after completed work? | Default next-step behavior |
|---|---|---|
| **IE — Customer Discovery & Market Lead** | **ON** | Finish current work, then pause at a meaningful market/customer branch and present decision options to the user. |
| **CS2 — Product Strategy, Evidence Synthesis & Application Lead** | **ON** | Finish current work, then pause at a meaningful product/application branch and present decision options to the user. |
| **EE — Physical Systems & Measurement Lead** | **OFF** | Finish, merge/verify, report result, then autonomously choose the next highest-value technical/measurement task consistent with current goals. |
| **CS1 — Decision Intelligence Lead** | **OFF** | Finish, merge/verify, report result, then autonomously choose the next highest-value decision/model/data task consistent with current goals. |

`ON` means a role must preserve user choice when the **next workstream** contains a material strategic branch.

`OFF` does **not** mean the role can ignore safety, evidence, product truth, or explicit human-gate rules. It means the role does not stop merely to ask which technical task to do next.

---

# Part A — IE and CS2: Checkpoint ON

## 1. Do not interrupt the accepted work package

Once IE or CS2 accepts a bounded package, execute it end-to-end without repeatedly asking the user to approve reversible details.

Routine choices should be resolved through evidence, inspection, research, testing, or bounded experiments.

## 2. Checkpoint after meaningful completion

After the current work reaches its accepted Definition of Done, IE or CS2 must evaluate whether the next action is:

- a continuation of the same direction, or
- a materially different strategic branch.

If there is a real strategic branch, do **not** silently choose one and continue.

Typical IE checkpoint triggers:

- choose between beachhead markets,
- materially change target customer or buyer,
- choose which PMR segment receives major next effort,
- pivot the operational problem,
- choose between materially different pilot/customer-acquisition paths,
- change the market thesis based on contradictory evidence.

Typical CS2 checkpoint triggers:

- materially change the product thesis,
- choose between major product directions,
- commit substantial time to a new feature family,
- change the core application narrative,
- choose a different differentiation strategy,
- choose a new campus-domain expansion,
- make a strategic tradeoff that displaces another important workstream.

## 3. Required decision package

The checkpoint must give the user enough information to choose without reconstructing the work.

Provide:

1. **Completed** — what was actually finished;
2. **Evidence / result** — interviews, evidence IDs, research, tests, measurements, benchmark results, commits, or artifacts;
3. **What changed** — assumptions, risks, product requirements, market understanding, or application claims affected;
4. **Options** — normally 2–4 materially different next paths;
5. for each option: **expected result, effort/cost, main risk, dependencies, and KREATE impact**;
6. **Recommendation** — the role owner's preferred option and reasoning;
7. **Decision needed** — one concise user choice.

Do not fabricate weak alternatives just to create an A/B/C list.

Do not ask vague questions like “What should I do next?” without first supplying the decision package.

A strong ending is:

> **Recommended:** Option B because it gives the strongest evidence gain before October 8 with lower dependency risk.  
> **Decision needed:** choose A, B, or C for the next strategic workstream.

## 4. Continue without a checkpoint when no material branch exists

IE and CS2 may continue autonomously when the next action is merely:

- required to finish already accepted criteria,
- cleanup or synthesis required by the same package,
- a low-risk follow-up with no real alternative,
- updating evidence/assumptions/decisions based on the completed result,
- a small reversible experiment that informs the same already-selected direction.

---

# Part B — EE and CS1: Checkpoint OFF

## 5. Continuous technical execution

EE and CS1 should **not** stop after each completed task to ask the user which technical direction to take next.

After completing, integrating, and verifying the current work, they should:

1. report the concrete result;
2. record evidence, limitations, failures, and changed assumptions;
3. inspect the current KREATE objective, ready work, dependencies, and latest IE/CS2 decisions;
4. select the next highest-value non-conflicting technical task;
5. continue execution autonomously.

If no ready task exists, EE/CS1 may define a bounded technical experiment or supporting work package that advances the current evidence-backed direction.

They should prefer work that:

- reduces a critical uncertainty,
- tests an important assumption,
- improves technical credibility,
- closes a measurement or decision-evidence gap,
- unblocks IE/CS2,
- improves pilot feasibility,
- strengthens a claim the application may need,
- kills unnecessary complexity.

## 6. EE-specific autonomous scope

EE may autonomously move among, for example:

- measurement architecture comparisons,
- smart-scale or alternative sensor experiments,
- calibration/repeatability work,
- offline/reconnect behavior,
- hardware-free measurement alternatives,
- service identification methods,
- integration feasibility,
- pilot measurement SOPs,
- removal of unnecessary hardware.

EE does not need a user decision merely because multiple technically plausible sensor/component paths exist. Use evidence and bounded experiments to choose.

## 7. CS1-specific autonomous scope

CS1 may autonomously move among, for example:

- realistic baselines,
- signal ablation,
- heuristics versus ML,
- uncertainty representation,
- decision-cost modeling,
- data-quality handling,
- source-health logic,
- evaluation design,
- pilot analytics,
- backend decision contracts,
- simplifying an unjustified model.

CS1 does not need a user decision merely because multiple technically plausible model/data approaches exist. Benchmark them and choose based on evidence.

## 8. What EE/CS1 should report

They should still keep the user informed after meaningful results.

A useful report is:

- **Completed:** what was delivered;
- **Result:** what the evidence/test showed;
- **Implication:** what changed technically;
- **Next:** what the agent selected next and why.

This is a status report, **not** a request for direction.

---

# Part C — Human gates still apply to everyone

Checkpoint OFF never overrides genuine human gates.

All roles must still stop when required for:

1. **EVIDENCE_ATTESTATION** — a person must confirm real-world evidence, interview/quote, or private institutional fact;
2. **IRREVERSIBLE_ACTION** — destructive or difficult-to-reverse external action;
3. **PHYSICAL_SAFETY** — energization, mains/high-current work, actuator movement, field deployment, or another physical-risk action;
4. **EXTERNAL_COMMITMENT** — purchase/payment, contract/legal acceptance, final submission, consequential external message, or pilot/date commitment;
5. **PRODUCT_DIRECTION** — a material pivot to the agreed core product/problem when the repository policy requires user ownership of that pivot.

For EE/CS1, ordinary technical architecture selection is **not** automatically `PRODUCT_DIRECTION`.

If a technical result implies a genuine market/product pivot, EE/CS1 should document the evidence and hand the strategic choice to **IE/CS2**, who then run the user checkpoint.

---

## Core rule

> **IE and CS2 preserve user control over strategic direction. EE and CS1 preserve execution velocity on technical direction.**

No role should ask for permission on routine reversible details, and no role may fabricate evidence to justify autonomy.