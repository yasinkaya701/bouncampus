# KREATE Roles — Autonomous Operating Model

## Purpose

These role files define **ownership, not confinement**.

Each execution role owns a critical question for the KREATE application and product thesis, but no role is restricted to a fixed task list. Team members and agents should cross boundaries whenever doing so materially improves evidence, product quality, technical credibility, or Top-15 selection probability.

The five core execution questions are:

1. **IE — Customer Discovery & Market Lead:** What is actually happening in the market and operation?
2. **EE — Physical Systems & Measurement Lead:** What should we measure, and can we trust the physical measurement?
3. **EHB — Embedded Hardware, Communications & Integration Lead:** Can we implement the electronics/firmware/communications path reliably and connect it correctly to software?
4. **CS1 — Decision Intelligence Lead:** Can we help the operator make a better decision and prove it?
5. **CS2 — Product Strategy, Evidence Synthesis & Application Lead:** Given the evidence, what should we build and how do we defend the thesis?

These questions overlap by design.

## Execution Roles vs Human Team

There are five execution roles but still four human team members. Roles may be staffed by the most appropriate human plus autonomous agents and do not imply one human per role.

The PMR operating target remains **16 distinct high-quality interviews**, approximately four lead interviews per human team member. Adding EHB does not create a fictitious fifth person or a 20-interview requirement.

## Autonomy Principle

Agents and humans may:

- propose new tasks;
- open bounded experiments;
- investigate adjacent markets;
- challenge the current beachhead;
- test or remove product features;
- compare hardware and hardware-free approaches;
- change model strategy;
- investigate competitors;
- request work from another role;
- contribute directly outside their nominal role;
- stop low-value work;
- surface contradictions;
- recommend a pivot when evidence justifies it.

Routine, reversible exploration does not require prior permission. The role owner remains responsible for keeping the relevant question coherent and evidence-backed.

## What Roles Are Not

Roles are not silos, permission boundaries, fixed sprint backlogs, exhaustive task lists, reasons to ignore a problem outside one's file, or reasons to continue weak work because it was assigned earlier.

If the best next action falls between roles, whoever identifies it should move it forward and coordinate ownership.

## Evidence Over Compliance

The team should optimize for learning and decision quality, not documentation volume.

A task is valuable when it produces new evidence, a better decision, a stronger requirement, a rejected assumption, a clearer customer/buyer, a tested technical path, a stronger pilot, a useful failure, a changed feature priority, or a more defensible claim.

Creating a document without changing understanding is not automatically progress.

## Exploration Contract

For significant new work, be able to answer:

1. **Question:** What are we trying to learn or improve?
2. **Why now:** Why could this matter for KREATE or the product?
3. **Evidence target:** What result would inform a decision?
4. **Bound:** What is the cheapest useful experiment or investigation?
5. **Decision:** What will we keep, modify, kill, or investigate next based on the result?

This is a thinking tool, not an approval process.

## Cross-Role Collaboration

### IE ↔ EE

Operational reality should shape measurement design; measurement feasibility should shape PMR questions.

### IE ↔ EHB

Installation, connectivity, provisioning, maintenance, and operator constraints from PMR should shape embedded design. EHB should return feasibility constraints that sharpen PMR.

### IE ↔ CS1

Customer workflow and error costs should define decision objectives; model limitations should generate new PMR questions.

### IE ↔ CS2

Raw evidence should change product strategy; product contradictions should generate new customer-discovery work.

### EE ↔ EHB

EE owns measurement correctness; EHB owns embedded implementation. Their boundary is governed by an explicit interface contract covering the relevant voltage/current, pinout, sampling, calibration persistence, protocol, packet schema, quality flags, power budget, fault states, and verification method. Cross-boundary changes require dual review.

### EE ↔ CS1

Physical data quality should inform model confidence; model evaluation should define which measurements actually matter.

### EE ↔ CS2

Measurement hardware should exist only where it creates product value; product strategy should reflect real deployment constraints.

### EHB ↔ CS1

EHB owns reliable transport/device semantics; CS1 owns decision/model semantics. They align on timestamps, ordering, invalid/missing readings, quality flags, metadata, duplicates, replay, and API expectations.

### EHB ↔ CS2

EHB supplies implementation evidence; CS2 controls product/application framing. Prototype behavior must not be promoted to production-readiness claims.

### CS1 ↔ CS2

Technical evidence should constrain product claims; product priorities should determine which technical experiments are worth running.

## PMR Is Shared

PMR is a team responsibility, not an IE-only activity.

Working target: **16 distinct high-quality interviews**, approximately four lead interviews per human team member, adjusted as needed by access and relevance.

Any team member may conduct interviews. IE owns research quality and coverage, not all execution.

## Scope Freedom

The current focus is university/institutional food operations because it is a promising KREATE wedge, not because the team is forbidden from exploring anything else.

The team may explore adjacent institutional food segments, alternative operational decisions, different measurement paths, new contextual signals, hardware-free approaches, additional hardware where justified, workflow interventions, stronger campus-climate expansion paths, or other ideas that could materially strengthen the thesis.

Exploration should not become random feature accumulation. Ask:

> Does this work create evidence or strategic leverage that could change an important decision?

If yes, explore it. If not, defer it.

## Application Stage vs Hackathon Stage

### Until October 8

Optimize for PMR evidence, problem clarity, beachhead quality, persona/buyer understanding, credible solution logic, measurement feasibility, defensible decision intelligence, differentiation, and coherent application narrative.

A polished live demo is not a mandatory application deliverable.

### If Selected for Top 15

The team can shift aggressively toward integrated product implementation, jury demo, hardware polish, UI/UX, live data flow, pitch choreography, and reliability testing.

Role emphasis may change after selection.

## Anti-AI-Slop Principle

AI is encouraged as a force multiplier. It should increase speed, coverage, experimentation, and rigor—not create fake certainty.

AI-generated work is unacceptable when it fabricates evidence, results, user needs, market facts, hardware performance, or production readiness.

Before an important claim becomes part of the application, ask what evidence supports it, whether the source can be shown quickly, whether it is fact/interpretation/estimate/hypothesis, and whether a skeptical judge would understand the limitation.

## Team Behavior

Preferred behavior:

- move without unnecessary approval;
- communicate important changes early;
- challenge assumptions directly;
- share evidence across roles;
- keep experiments bounded;
- prefer real learning over cosmetic progress;
- simplify when complexity adds no value;
- escalate only genuinely ambiguous, strategic, unsafe, or irreversible decisions.

The objective is not to keep five role queues busy. It is to make the **best possible startup and application decisions before the deadline**.

## Human Decision Checkpoints

Checkpoint behavior is role-specific, not universal.

- **IE: ON**
- **CS2: ON**
- **EE: OFF**
- **EHB: OFF**
- **CS1: OFF**

IE/CS2 preserve user choice at genuine strategic branches. EE/EHB/CS1 continue autonomously through aligned technical work unless an explicit human gate applies.

Full protocol: [`USER_DECISION_CHECKPOINT_PROTOCOL.md`](./USER_DECISION_CHECKPOINT_PROTOCOL.md).
