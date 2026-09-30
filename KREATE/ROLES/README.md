# KREATE Roles — Autonomous Operating Model

## Purpose

These role files define **ownership, not confinement**.

Each role owns a critical question for the KREATE application and product thesis, but no role is restricted to a fixed task list. Team members and agents are expected to cross boundaries whenever doing so can materially improve evidence, product quality, technical credibility, or Top-15 selection probability.

The four core questions are:

1. **IE — Customer Discovery & Market Lead:** What is actually happening in the market and operation?
2. **EE — Physical Systems & Measurement Lead:** What can we reliably measure and deploy in the physical world?
3. **CS1 — Decision Intelligence Lead:** Can we help the operator make a better decision and prove it?
4. **CS2 — Product Strategy, Evidence Synthesis & Application Lead:** Given the evidence, what should we build and how do we defend the thesis?

These questions overlap by design.

## Autonomy Principle

Agents and humans may:

- propose new tasks,
- open bounded experiments,
- investigate adjacent markets,
- challenge the current beachhead,
- test new product features,
- remove existing features,
- compare alternative hardware approaches,
- change model strategy,
- investigate competitors,
- request work from another role,
- contribute directly outside their nominal role,
- stop low-value work,
- surface contradictions,
- recommend a pivot when evidence justifies it.

Routine, reversible exploration does not require prior permission.

The role owner remains responsible for keeping the relevant question coherent and evidence-backed.

## What Roles Are Not

Roles are not:

- silos,
- permission boundaries,
- fixed sprint backlogs,
- exhaustive task lists,
- reasons to ignore a problem outside one's file,
- reasons to continue weak work because it was assigned earlier.

If the best next action falls between roles, whoever identifies it should move it forward and coordinate ownership.

## Evidence Over Compliance

The team should optimize for learning and decision quality, not compliance with documentation.

A task is valuable if it produces one or more of:

- new evidence,
- a better decision,
- a stronger product requirement,
- a rejected assumption,
- a clearer customer or buyer,
- a tested technical path,
- a stronger pilot design,
- a useful failure,
- a changed feature priority,
- a more defensible application claim.

Creating a document without changing understanding is not automatically progress.

## Exploration Contract

For significant new work, be able to answer:

1. **Question:** What are we trying to learn or improve?
2. **Why now:** Why could this matter for KREATE or the product?
3. **Evidence target:** What result would inform a decision?
4. **Bound:** What is the cheapest useful experiment or investigation?
5. **Decision:** What will we keep, modify, kill, or investigate next based on the result?

This should remain lightweight. It is a thinking tool, not an approval process.

## Cross-Role Collaboration

### IE ↔ EE

Operational reality should shape measurement design; measurement feasibility should shape PMR questions.

### IE ↔ CS1

Customer workflow and error costs should define decision objectives; model limitations should generate new PMR questions.

### IE ↔ CS2

Raw evidence should change product strategy; product contradictions should generate new customer-discovery work.

### EE ↔ CS1

Physical data quality should inform model confidence; model evaluation should define which measurements actually matter.

### EE ↔ CS2

Hardware should exist only where it creates product value; product strategy should reflect real deployment constraints.

### CS1 ↔ CS2

Technical evidence should constrain product claims; product priorities should determine which technical experiments are worth running.

## PMR Is Shared

PMR is a team responsibility, not an IE-only activity.

Working target: **16 distinct high-quality interviews**, approximately four lead interviews per person, adjusted as needed by access and relevance.

Any role may conduct interviews. The best interviewer for a specific stakeholder is the person most capable of understanding the domain and following useful technical or operational threads.

IE owns research quality and coverage, not all execution.

## Scope Freedom

The current focus is university/institutional food operations because it is a promising KREATE wedge, not because the team is forbidden from exploring anything else.

The team may explore:

- adjacent institutional food segments,
- alternative operational decisions,
- different measurement paths,
- new contextual signals,
- hardware-free approaches,
- additional hardware where justified,
- workflow interventions,
- stronger campus-climate expansion paths,
- other ideas that could materially strengthen the thesis.

However, exploration should not become random feature accumulation. The test is simple:

> Does this work create evidence or strategic leverage that could change an important decision?

If yes, explore it. If not, defer it.

## Application Stage vs Hackathon Stage

### Until October 8

Optimize for:

- PMR evidence,
- problem clarity,
- beachhead quality,
- persona / buyer understanding,
- credible solution logic,
- measurement feasibility,
- defensible decision intelligence,
- differentiation,
- coherent application narrative.

A polished live demo is not a mandatory application deliverable.

### If Selected for Top 15

The team can shift aggressively toward:

- integrated product implementation,
- jury demo,
- hardware polish,
- UI/UX,
- live data flow,
- pitch choreography,
- reliability testing.

Role emphasis may change after selection.

## Anti-AI-Slop Principle

AI is encouraged as a force multiplier. It should increase speed, coverage, experimentation, and rigor—not create fake certainty.

AI-generated work is acceptable when it helps produce or analyze real evidence. It is unacceptable when it fabricates evidence, results, user needs, market facts, or technical performance.

Before an important claim becomes part of the application, ask:

- What type of evidence supports this?
- Can we show the source quickly?
- Is this a fact, interpretation, estimate, or hypothesis?
- Would a skeptical judge understand the limitation?

If the answer is unclear, improve or downgrade the claim rather than hiding uncertainty.

## Team Behavior

Preferred behavior:

- move without waiting for unnecessary approval,
- communicate important changes early,
- challenge assumptions directly,
- share evidence across roles,
- keep experiments bounded,
- prefer real learning over cosmetic progress,
- simplify when complexity adds no value,
- escalate only genuinely ambiguous or irreversible decisions.

The operating objective is not to keep four agents busy. It is to make the **best possible startup and application decisions before the deadline**.

## Human Decision Checkpoints

Role autonomy does **not** mean agents should blindly continue into a new strategic workstream after finishing the current one.

The required pattern is:

> **Finish the accepted work package → verify the result → explain what changed → present the real next options → recommend one → ask the user to choose the next meaningful direction.**

Agents should not interrupt the user for routine, reversible details inside an accepted task. But when a completed task creates multiple materially different next directions, the agent must pause before committing substantial time to one of them.

A checkpoint should include:

1. **Completed** — exactly what was delivered;
2. **Evidence / result** — tests, interview findings, benchmark results, calibration data, files, commits, or evidence IDs;
3. **What changed** — which assumption, product requirement, risk, or application claim changed;
4. **Options** — normally 2–4 real alternatives, each with expected value, effort, risk, dependencies, and KREATE impact;
5. **Recommendation** — the agent's preferred option and why;
6. **Decision needed** — one concise choice for the user.

Do not invent artificial choices. If there is only one obvious, reversible next step required to finish the same accepted work package, continue autonomously.

Do not ask vague questions such as “What should I do now?” before doing the analysis. Give the user enough information to decide intelligently.

Full protocol: [`USER_DECISION_CHECKPOINT_PROTOCOL.md`](./USER_DECISION_CHECKPOINT_PROTOCOL.md).
