# User Decision Checkpoint Protocol

## Purpose

All four KREATE workstreams operate **autonomously by default**. A human owns each parent workstream for accountability, evidence attestation, safety, external commitments, and true product-direction pivots; the human is not a routine dispatcher for the agents beneath that workstream.

## Parent workstreams

Exactly one human-owned parent workstream exists for each role:

- IE — Customer Discovery & Market Lead
- EE — Physical Systems & Measurement Lead
- CS1 — Decision Intelligence Lead
- CS2 — Product Strategy, Evidence Synthesis & Application Lead

Each parent may fan out to any number of child agents when dependencies and `touched_paths` permit it. There is no artificial child-agent count limit.

## Default behavior for every role

IE, EE, CS1, and CS2 all follow the same default lifecycle:

1. execute the accepted parent objective;
2. decompose it into bounded child-agent tasks as useful;
3. let agents resolve routine reversible choices through research, tests, experiments, and repository evidence;
4. integrate verified child outputs into the parent workstream;
5. continue to the next highest-value aligned work without asking the human for routine direction.

Routine PMR planning, stakeholder prioritization, model choice, hardware alternative comparison, drafting, code architecture, testing, documentation, branch operations, conflict resolution, PR creation, and merge execution are not human checkpoints.

## The only human gates

`WAITING_HUMAN` is valid only for one of these five gate kinds:

1. **EVIDENCE_ATTESTATION** — confirm that a real interview, exact quote, private institutional fact, measured result, or other real-world evidence is genuine and represented correctly.
2. **IRREVERSIBLE_ACTION** — approve destructive or difficult-to-reverse external operations such as data deletion, credential revocation/rotation, or repository/account administration.
3. **PHYSICAL_SAFETY** — approve real hardware energization, actuator movement, mains/high-current work, or field deployment where physical risk exists.
4. **EXTERNAL_COMMITMENT** — approve final application submission, purchase/payment, contract/legal acceptance, consequential external communication, or a binding pilot/date commitment.
5. **PRODUCT_DIRECTION** — decide a material pivot to the agreed beachhead, primary problem, or core product thesis when evidence supports materially different credible directions.

A pending gate must contain exactly one concrete question. Agents must finish all independent work before entering `WAITING_HUMAN`.

## What is not PRODUCT_DIRECTION

The following remain autonomous unless they independently trigger another gate:

- choosing a forecasting/model baseline;
- selecting a reversible software architecture;
- choosing between sensor/component candidates for analysis or non-energized prototyping;
- prioritizing interviews inside the already-agreed market hypothesis;
- refining application wording without changing factual claims;
- choosing tests, metrics, experiments, or implementation order;
- killing an unsupported feature while preserving the agreed core problem;
- resolving merge conflicts or CI failures.

## Evidence boundary

Agents may collect, structure, summarize, challenge, and synthesize PMR/evidence, but they may not self-attest that an interview occurred, invent a quote, invent a customer, or convert model/simulation output into a measured result.

Application-relevant factual claims continue to require the human-review rules in the KREATE evidence system.

## Human-owner reports

Agents should keep the human owner informed with concise status, not permission requests:

- **Completed** — what changed;
- **Evidence/result** — tests, evidence IDs, measurements, commits, or artifacts;
- **Implication** — what assumption/risk changed;
- **Next** — the next autonomous action.

Only append **Decision needed** when one of the five critical gates is actually pending.

## Core rule

> **Humans own accountability and critical real-world decisions. Agents own routine execution, decomposition, experimentation, integration, and continuation.**
