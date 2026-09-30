# CS2 — Product Strategy, Evidence Synthesis & Application Lead

## Mission

Own the question: **Given everything we are learning, what should BOUNCAMPUS actually become, how should we prioritize it, and can we defend the resulting startup thesis under skeptical review?**

This role is not a frontend or demo role for the October 8 application stage. It is the synthesis and product-direction role that turns raw PMR, technical evidence, hardware findings, competitor research, and uncertainty into a coherent product strategy.

The CS2 lead is expected to challenge assumptions, change priorities, kill weak features, identify missing evidence, propose stronger product directions, and ensure the application tells the truth without underselling the team's potential.

## North Star

Improve the probability that the team presents a startup thesis that is:

1. evidence-backed,
2. differentiated,
3. technically credible,
4. operationally useful,
5. climate-relevant,
6. pilotable,
7. commercially plausible,
8. coherent across all four team members,
9. strong enough to earn a KREATE Top-15 position.

## Core Ownership

Primary ownership areas include:

- product thesis,
- evidence synthesis,
- assumption management,
- product requirements,
- feature prioritization,
- competitor / status-quo intelligence,
- differentiation,
- product architecture at the decision/workflow level,
- climate-impact logic,
- application narrative and consistency,
- contradiction hunting,
- red-team facilitation,
- identifying missing questions the rest of the team should investigate.

CS2 should not become a documentation secretary. The job is to make high-quality product decisions from incomplete evidence.

## Evidence Synthesis

Raw interview notes are not product strategy.

Synthesize across sources:

`evidence → pattern / contradiction → assumption update → product implication → next test`

Examples:

- Multiple operators report that stockout risk dominates waste concerns → decision objective changes.
- Staff already use a reliable scale but never connect data to planning → focus shifts from building a scale to closing the feedback loop.
- University procurement is too slow for a first pilot while a catering operator can approve quickly → beachhead or buyer strategy may change.
- Weather is frequently mentioned but does not improve retrospective estimates → keep it out of the core model until stronger evidence appears.

Do not force contradictory evidence into a false consensus.

## Assumption Management

Use `KREATE/ASSUMPTIONS.md` as an active decision tool.

Useful states include:

- UNKNOWN,
- TESTING,
- SUPPORTED,
- REJECTED,
- CONFLICTING.

An assumption should move states because of evidence, not because the team wants the story to look complete.

CS2 has authority to surface and prioritize new assumptions that become strategically important.

## Product Requirements

Translate customer evidence into requirements, not feature requests.

Example:

Customer evidence:
> operators need protection from early sell-out and cannot blindly follow an automated quantity.

Possible requirement:
> the system must expose a safe operating range, risk tradeoff, and human decision point rather than a single opaque number.

That requirement may be implemented in many ways. Do not prematurely lock the team into a specific UI or algorithm.

## Feature Portfolio

Features are hypotheses about value.

The team may explore software, hardware, workflow, measurement, market, or operational features beyond the current plan if they could materially strengthen the product.

For each significant feature or experiment, ask:

- Which problem or opportunity does it address?
- What evidence suggests it matters?
- What new capability or learning does it create?
- What is the cheapest way to test it?
- What would make us keep, modify, or kill it?
- Does it distract from stronger work?

A scoring framework can help but should not become bureaucracy. Useful dimensions include:

- evidence strength,
- customer impact,
- differentiation,
- pilotability,
- technical feasibility,
- climate relevance,
- strategic leverage.

CS2 can approve exploration of unconventional ideas when the upside is meaningful and the experiment is bounded.

## Competitor and Status-Quo Intelligence

Competitor research should answer how customers solve the problem today, not merely produce logo slides.

Analyze where relevant:

- workflow,
- customer segment,
- data inputs,
- intervention timing,
- hardware requirements,
- decision support,
- measurement approach,
- buyer,
- deployment model,
- strengths,
- weaknesses,
- likely switching friction.

Important comparison classes may include:

- kitchen-manager experience,
- spreadsheets,
- historical production rules,
- POS / catering software,
- waste-monitoring systems,
- Winnow,
- Leanpath,
- Orbisk,
- adjacent institutional-operations products.

The largest competitor may be the status quo rather than another startup.

## Differentiation

Do not freeze a slogan before evidence supports it.

Current possible direction:

> BOUNCAMPUS helps institutional food operations improve decisions before waste occurs and closes the loop with measured outcomes.

This is a working thesis, not doctrine.

CS2 should continuously ask:

- Why would this customer adopt us?
- Why are current tools insufficient?
- What can we do uniquely well?
- Is that uniqueness actually valuable?
- Is our advantage software, workflow, data, measurement, integration, speed of deployment, or something else?

If competitor research invalidates the current differentiation, change it.

## Product Architecture

Own the user/business-level system logic.

A current candidate loop is:

`KNOW → DECIDE → ACT → MEASURE → LEARN`

For example:

- **KNOW:** operational and contextual signals,
- **DECIDE:** estimate / recommendation / risk,
- **ACT:** operator action,
- **MEASURE:** physical or operational outcome,
- **LEARN:** evaluation / calibration / next decision.

This architecture may evolve if PMR reveals a stronger intervention point.

CS1 owns algorithmic logic; EE owns physical measurement; CS2 ensures the pieces form a product rather than disconnected technologies.

## Climate Logic

Climate claims must follow a causal chain.

Example:

`better operational decision → less avoidable overproduction → less discarded food → measured reduction → defensible climate-impact estimate`

Do not jump directly from a prediction model or sensor to carbon claims.

CS2 should identify what evidence would eventually be required to make stronger climate-impact statements.

## Application Ownership

CS2 is the single narrative owner for the final October 8 submission.

That does **not** mean writing everything alone.

- IE provides PMR, customer, beachhead, market and operational evidence.
- EE provides physical feasibility, measurement strategy, limitations and pilot instrumentation.
- CS1 provides decision logic, baselines, evaluation and technical limitations.
- CS2 integrates these into one coherent voice.

The application should make it obvious:

- what we believed initially,
- what we actually investigated,
- what surprised us,
- what changed because of PMR,
- why the chosen customer / problem / solution now makes sense,
- what remains uncertain,
- why this four-person team is suited to continue.

## Rubric Strategy

The application rubric should inform priorities without turning the product into a checkbox exercise.

PMR has exceptionally high weight, so evidence quality should influence product strategy heavily.

Use `KREATE/APPLICATION_RUBRIC.md` to identify weak sections and missing evidence. The goal is not to stuff every possible claim into the form; it is to make every included claim earn its place.

## Contradiction Hunter

CS2 should actively attack team assumptions.

Questions to ask repeatedly:

- How do we know this?
- Is this interview evidence, measured evidence, public data, or our interpretation?
- What would falsify this?
- Are we overgeneralizing?
- Does the customer actually care?
- Is the customer also the buyer?
- Why hardware?
- Why software?
- Why AI?
- Why this segment?
- Why now?
- Is a competitor already doing this better?
- Could a spreadsheet solve 80% of the problem?
- Which part of our current product should disappear?

These questions are not blockers. They are tools for discovering a stronger thesis.

## Red-Team Leadership

Run short red-team reviews when they can change decisions.

Attack examples:

- demand mismatch may not be the dominant cause of food waste,
- the proposed signals may not outperform operator judgment,
- a new smart scale may add no value,
- the beachhead may have no fast purchasing path,
- competitors may already offer pre-production forecasting,
- the climate effect may be too hard to measure,
- the proposed workflow may add staff burden.

A useful red-team session ends with a decision or next test, not just criticism.

## Freedom to Explore

CS2 has broad authority to open bounded research or product experiments that could materially improve the thesis.

Examples:

- investigate a different product wedge,
- compare an alternative beachhead,
- propose a new decision point,
- test a different value proposition,
- explore a procurement strategy,
- research competitors more deeply,
- prototype a requirement quickly,
- ask CS1 for a technical experiment,
- ask EE to compare a hardware-free measurement path,
- ask IE to test a newly discovered buyer hypothesis,
- identify a stronger cross-campus expansion story.

Do not wait for a formal role boundary when an unanswered question is strategically important. Coordinate ownership and move.

## Collaboration

### With IE

Receive structured PMR evidence, market contradictions, customer language, stakeholder maps and new hypotheses.

### With EE

Understand what can actually be measured, what physical deployment costs, and whether hardware creates strategic advantage.

### With CS1

Understand what decision logic is technically justified, how uncertainty is represented, what benchmarks show, and which claims are premature.

### Across the Team

Keep the product thesis synchronized. If one workstream changes a core assumption, ensure the other workstreams know the implication.

## Anti-AI-Slop Standard

AI may accelerate synthesis, research, drafting, comparison, ideation, and red-teaming. It must not manufacture evidence or certainty.

Reject:

- invented interview quotes or findings,
- generic startup language that could describe any sustainability project,
- fictional personas presented as PMR,
- unsourced market sizing,
- false competitor claims,
- fabricated pilot results,
- carbon / cost savings without defensible evidence,
- copy that says `AI-powered`, `revolutionary`, `seamless`, `transformative`, etc. instead of explaining the actual mechanism,
- application prose that hides rejected assumptions or technical limitations.

Strong writing is specific, falsifiable, and grounded.

## Strong Outputs

Useful outputs may include:

- an updated product thesis,
- a changed feature priority,
- a killed feature with evidence,
- a new product requirement,
- an assumption-state change,
- competitor insight that changes positioning,
- a revised beachhead recommendation,
- a coherent application section,
- a red-team attack that exposes a real weakness,
- a cross-team question that triggers a valuable experiment,
- an explicit statement of what remains unknown.

## Application-Stage Success Criteria

By October 8, CS2 should be able to defend a coherent answer to:

- What problem are we solving?
- For whom?
- Why this beachhead?
- What evidence did we gather?
- What did we learn that changed our thinking?
- What is the current product thesis?
- Why is it better than the status quo?
- Why are we different from relevant alternatives?
- What can the technology credibly do today?
- What remains unvalidated?
- How would a pilot test the critical assumptions?
- Why is this team unusually suited to execute?

The goal is not a perfectly polished story. The goal is a startup thesis strong enough that every important sentence can survive the question: **What evidence supports that?**
