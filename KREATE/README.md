# KREATE Team Operating System

This directory is the single operating entry point for the BOUNCAMPUS KREATE application effort. It does not replace product documentation under `docs/`; it controls how the team creates, reviews, traces, and uses evidence for the October 8 application gate.

## Current objective

Submit the strongest evidence-backed KREATE application by **2026-10-08 23:59** without presenting hypotheses, model outputs, demo data, or AI-generated text as validated market evidence.

- **HYPOTHESIS:** the current beachhead is university/institutional dining food-waste prevention around the production decision.
- **HYPOTHESIS:** demand mismatch may contribute materially to avoidable food waste. PMR must test this rather than assume it.
- **FACT:** the current repository already contains a food-waste decision-support product direction and a strict claim boundary; this operating system does not redesign it. See `E-REP-001` through `E-REP-003` in [EVIDENCE.md](./EVIDENCE.md).

## Deadline and rubric

- Application deadline: **October 8, 2026, 23:59**.
- Top-15 announcement: **October 9, 2026**.
- This phase is an **application gate, not a demo contest**.

| Rubric area | Weight |
| --- | ---: |
| Team | 20% |
| Problem | 20% |
| Beachhead Market | 10% |
| Persona | 10% |
| Primary Market Research | 40% |

## Scope

### P0 — required before submission

- Complete and document genuine PMR.
- Trace every material application claim to an evidence ID or label it `HYPOTHESIS`/`UNKNOWN`.
- Resolve the highest-risk beachhead, persona, workflow, decision-owner, and problem-causality assumptions.
- Close rubric gaps in [APPLICATION_RUBRIC.md](./APPLICATION_RUBRIC.md).
- Keep application-relevant prose under second-human review.

### P1 — do when it improves P0 evidence quality

- Synthesize interviews into assumptions and KEEP / MODIFY / KILL decisions.
- Run tightly scoped experiments that answer a named question.
- Prioritize features only after evidence exists.
- Verify public sources and repository artifacts used in the application.

### P2 — defer unless it directly closes a rubric gap

- UI polish.
- New demo choreography.
- New product features without PMR support.
- Extra modeling, climate conversion, or hardware work that does not create evidence needed for the application.

## Human PMR ownership

The human team still has **four people**. PMR/interview ownership remains person-based:

| Human PMR lead role | KREATE responsibility |
| --- | --- |
| IE — Customer Discovery & Market Lead | Beachhead, persona, workflow, decision owner, PMR quality; leads 4 target interviews. |
| EE — Physical Systems & Measurement Lead | Measurement feasibility, operational data availability, technical measurement risks; leads 4 target interviews. |
| CS1 — Decision Intelligence Lead | Decision logic, model/technical assumptions, feasibility and failure conditions; leads 4 target interviews. |
| CS2 — Product Strategy, Evidence Synthesis & Application Lead | Rubric coverage, evidence synthesis, application draft and claim traceability; leads 4 target interviews. |

**CS2 owns final synthesis. Domain owners must sign off factual claims in their area before submission.**

## Execution-role architecture

Repository execution uses **five roles**:

1. IE — Customer Discovery & Market Lead
2. EE — Physical Systems & Measurement Lead
3. **EHB — Embedded Hardware, Communications & Integration Lead**
4. CS1 — Decision Intelligence Lead
5. CS2 — Product Strategy, Evidence Synthesis & Application Lead

EHB is an independent execution/ownership role, not a fifth human and not an EE sub-role. It may be staffed by the appropriate human plus autonomous agents.

EE owns measurement correctness: measurand, measurement architecture, calibration, uncertainty, physical workflow and field validity. EHB owns implementation-heavy embedded work: electronics, controller/PCB, firmware, communications, buffering/recovery, bring-up and HW↔SW integration. Cross-boundary changes use the EE↔EHB interface contract and dual review. See [ROLES/05_EHB_EMBEDDED_HARDWARE_COMMUNICATIONS_INTEGRATION_LEAD.md](./ROLES/05_EHB_EMBEDDED_HARDWARE_COMMUNICATIONS_INTEGRATION_LEAD.md) and [HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md](./HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md).

## PMR target

- Target: **16 distinct interviews**.
- Hard minimum: **12 distinct interviews**.
- Each human teammate leads **4** target interviews.
- Adding EHB does **not** add `EHB-01..04` slots or change the target to 20 interviews.
- A conversation counts toward the tracker only when a real stakeholder conversation occurred and the repo contains notes sufficient to create at least one traceable evidence item or an explicit finding of no promotable evidence.
- Never invent names, quotes, organizations, incidents, or outcomes to fill the tracker.

See [PMR/INTERVIEW_TRACKER.md](./PMR/INTERVIEW_TRACKER.md) and [PMR/INTERVIEW_TEMPLATE.md](./PMR/INTERVIEW_TEMPLATE.md).

## Claim labels

Use these exact labels where relevant:

- `FACT` — directly verifiable internal fact, such as an artifact existing in the repository.
- `PUBLIC SOURCE` — claim supported by a cited external public source.
- `INTERVIEW EVIDENCE` — claim supported by a documented real interview.
- `TECHNICAL TEST` — result produced by a reproducible technical test.
- `MODEL ESTIMATE` — model output or scenario, never measured reality by default.
- `POLICY HEURISTIC` — team-selected operating rule or threshold, not a learned/validated truth.
- `HYPOTHESIS` — claim actively being tested.
- `UNKNOWN` — material question with no adequate evidence yet.

Every material claim must cite an ID from [EVIDENCE.md](./EVIDENCE.md) or remain explicitly `HYPOTHESIS`/`UNKNOWN`.

## Evidence promotion pipeline

No AI or human summary may skip these layers:

```text
RAW ARTIFACT
(interview notes / source / test output / model output)
        ↓
EVIDENCE REGISTRY
(narrow claim + evidence ID + type + source + owner + confidence)
        ↓
ASSUMPTION / DECISION UPDATE
(what changed, what did not, contradiction preserved)
        ↓
SUBMISSION CLAIM LEDGER
(label + evidence IDs + domain owner + human reviewer)
        ↓
APPLICATION COPY
```

Rules:

1. Raw notes are not automatically evidence.
2. An evidence item supports only the narrow claim written in its registry row.
3. Repository artifacts prove repository state, not customer demand or market validation.
4. Interview count is not validation by itself; concrete incidents and changed decisions matter.
5. Contradictory evidence is preserved and can move an assumption to `CONFLICTING` or `REJECTED`.
6. A claim is not submission-ready until it reaches `READY` in the claim ledger and a second human has reviewed it.

## Operating files

- [STATUS.md](./STATUS.md) — current state only.
- [ASSUMPTIONS.md](./ASSUMPTIONS.md) — hypothesis register.
- [EVIDENCE.md](./EVIDENCE.md) — evidence registry.
- [PMR/INTERVIEW_TEMPLATE.md](./PMR/INTERVIEW_TEMPLATE.md) — one interview record format.
- [PMR/INTERVIEW_TRACKER.md](./PMR/INTERVIEW_TRACKER.md) — 16-slot PMR tracker.
- [DECISIONS.md](./DECISIONS.md) — KEEP / MODIFY / KILL decision log.
- [EXPERIMENTS/EXPERIMENT_TEMPLATE.md](./EXPERIMENTS/EXPERIMENT_TEMPLATE.md) — bounded experiment record.
- [FEATURES.md](./FEATURES.md) — evidence-gated feature backlog.
- [APPLICATION_RUBRIC.md](./APPLICATION_RUBRIC.md) — rubric closure board + final claim ledger.
- [HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md](./HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md) — shared measurement/embedded interface contract.
- [`../docs/assumptions.md`](../docs/assumptions.md) — existing product truth boundary and methodology.
- [`../docs/food-waste-pilot-protocol.md`](../docs/food-waste-pilot-protocol.md) — existing falsifiable pilot protocol.

## Validation commands

Daily/PR mechanical gate:

```bash
python scripts/kreate_check.py
```

This validates structure, evidence ID/type consistency, interview tracker states, assumption/decision references, claim-ledger mechanics, local links, and GitHub review gates. It is intentionally compatible with unfinished PMR.

Final application gate:

```bash
python scripts/kreate_check.py --submission
```

The submission mode additionally requires:

- at least **12** tracker rows marked `COMPLETED` with real metadata;
- every completed interview to link `E-INT-*` evidence or explicitly state `NONE — no promotable claim`;
- `E-PUB-001` to have a human re-verification/date instead of a TODO;
- no `DRAFT` material claims in the submission claim ledger;
- at least one `READY` claim;
- matching evidence type for `PUBLIC SOURCE`, `INTERVIEW EVIDENCE`, `TECHNICAL TEST`, and `MODEL ESTIMATE` claims;
- named domain owner and human reviewer on every `READY` claim.

**Passing the script is necessary, not sufficient.** Humans still verify interview notes, public sources, context, claim wording, and final application copy.

## Daily workflow

### Morning async — each person

- **TODAY:** the highest-priority question or task.
- **OUTPUT:** the artifact/evidence expected by end of day.
- **DEPENDENCY:** person/data/access needed.
- **BLOCKER:** only a real blocker, not uncertainty that can be tested.

### Evening async — each person

- **DONE:** artifact that meets the definition below.
- **EVIDENCE CREATED:** evidence IDs added or `NONE`.
- **ASSUMPTION CHANGED:** assumption IDs moved or `NONE`.
- **BLOCKER:** exact blocker and next executable action.
- **NEXT:** first next action.

### Every 48 hours — 30-minute red-team

Required output: at least one evidence-backed `KEEP`, `MODIFY`, or `KILL` decision in [DECISIONS.md](./DECISIONS.md), **or** one specific evidence gap added to [STATUS.md](./STATUS.md) with owner and deadline.

## Anti-AI-slop gate

Reject or flag application content that includes any of the following without evidence:

- `revolutionary`, `groundbreaking`, `transformative`, `seamless`, `cutting-edge`, `unique`, `real-time`, or `AI-powered`;
- percentages without denominator and source;
- invented PMR quotes/personas;
- fake pilot outcomes;
- hard-coded demo data described as live;
- model confidence described statistically without calibration;
- carbon/water savings without measured reduction plus documented conversion;
- feature descriptions that do not identify the user decision being improved;
- generic climate-startup prose that could be pasted into an unrelated application unchanged.

AI-generated prose, code, or research is never `DONE` until a human reviewer verifies it.

## Definition of DONE

A task is `DONE` only if all are true:

1. the artifact exists in the repository/evidence store;
2. acceptance criteria passed;
3. evidence is attached or linked;
4. known limitations are written;
5. a second human reviewed application-relevant claims;
6. the work closes a rubric gap, reduces a major risk, creates evidence, or changes a real decision.

If any condition is missing, the task remains `IN PROGRESS` or `BLOCKED`.
