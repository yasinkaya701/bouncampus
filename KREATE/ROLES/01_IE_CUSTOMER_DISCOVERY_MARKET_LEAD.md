# IE — Customer Discovery & Market Lead

## Mission

Own the question: **Is this a real, important, reachable problem for a clearly defined customer, and what must BOUNCAMPUS become to solve it?**

This role is not a narrow interview coordinator. It is the team's market-learning engine. The IE lead may explore adjacent customer segments, operating models, procurement paths, workflow bottlenecks, pricing logic, pilot structures, process redesign opportunities, and new hypotheses whenever the evidence suggests they matter.

The goal is not to defend the current product concept. The goal is to discover the strongest possible KREATE case and help the team change direction when reality disagrees with us.

## North Star

Every major conclusion should improve at least one of these:

1. problem clarity,
2. beachhead clarity,
3. customer access,
4. strength of PMR evidence,
5. product relevance,
6. pilotability,
7. commercial credibility,
8. probability of being selected for the KREATE Top 15.

## Core Ownership

The IE lead owns the quality of the customer-discovery system, but **does not own all interviews**. PMR is distributed across the full four-person team.

Primary ownership areas:

- customer discovery methodology,
- beachhead market reasoning,
- end-user / buyer / champion mapping,
- current workflow and process mapping,
- current alternatives and status quo,
- market-segmentation logic,
- operating and procurement constraints,
- pilot adoption requirements,
- business-model hypotheses,
- synthesis of operational pain,
- identifying contradictions between what we assume and what users actually do.

## Interview Model — Distributed PMR

Target: **16 distinct high-quality interviews before application freeze**, roughly four lead interviews per team member.

Any team member may conduct interviews. The IE lead maintains quality standards, helps improve scripts, reviews evidence quality, and identifies coverage gaps.

Preferred interview configuration when practical:

- one lead interviewer,
- one note-taker / observer,
- rotate roles across interviews.

Do not optimize for raw interview count. One detailed operational interview can be more valuable than five superficial calls.

Useful stakeholder classes include, but are not limited to:

- university dining operations,
- food engineers,
- kitchen managers,
- contracted catering operators,
- SKS / sustainability units,
- procurement and administration,
- facilities or data owners,
- factory / hospital / institutional food-service operators when useful for segment comparison,
- other stakeholders discovered through referrals.

The team is free to pursue an unexpected stakeholder category if it could materially change the product or market thesis.

## Discovery Standard

Prioritize stories and observed behavior over opinions about hypothetical features.

Strong prompts include:

- Tell me about the last time you had too much food left after service.
- How did you decide how much to prepare that day?
- What happened when demand was lower or higher than expected?
- Who makes the final production decision?
- What information do they trust?
- What gets measured today?
- What is not measured?
- What is the cost of being wrong in each direction?
- What happens after food is left over?
- Who would need to approve a pilot?
- What would make a pilot unacceptable?
- What existing process or tool would we be replacing?
- Who else should we speak to?

The script is a starting point, not a cage. Follow important unexpected threads.

## Evidence Quality

A PMR conclusion should preserve the distinction between:

- direct observation,
- participant statement,
- repeated pattern,
- interpretation,
- hypothesis,
- quantitative evidence,
- public / official data.

Important claims should be linked into `KREATE/EVIDENCE.md` and relevant assumptions updated in `KREATE/ASSUMPTIONS.md`.

Do not convert one anecdote into a universal conclusion.

## Market Exploration

The current working beachhead may be university dining, but the IE lead has authority to challenge it.

Compare plausible segments when useful, such as:

- university dining,
- factory cafeterias,
- hospitals,
- institutional catering,
- municipal kitchens,
- schools,
- other high-volume kitchens discovered during PMR.

Useful comparison dimensions:

- severity and frequency of pain,
- customer accessibility,
- decision frequency,
- data availability,
- budget / economic authority,
- ability to pilot quickly,
- procurement friction,
- operational risk,
- measurable climate outcome,
- repeatability across sites,
- competitive intensity,
- expansion potential.

Do not preserve university dining merely because it was our first idea. Preserve it only if it remains the strongest evidence-backed wedge.

## Customer System Map

The IE lead should establish who actually plays each role:

- end user,
- decision maker,
- economic buyer,
- champion,
- blocker,
- data owner,
- operational owner,
- pilot approver.

These may be different people.

Map the actual workflow from planning through service and waste handling. A useful map may include:

`forecast / expectation → production decision → preparation → service → leftover handling → waste measurement → reporting → next planning cycle`

Add owners, information used, failure modes, delays, workarounds, and decision rights.

## Product Influence

The IE role is expected to change the product.

Examples:

- If operators care more about stockout risk than waste, that changes recommendation logic.
- If production decisions happen one day earlier than expected, the data pipeline must change.
- If waste data exists but is too delayed to influence decisions, measurement architecture changes.
- If the buyer is a catering contractor rather than the university, market and pilot strategy changes.
- If a non-food use case unexpectedly scores much higher and fits the KREATE climate brief, raise it to the team rather than suppressing it.

When PMR changes product direction, record the change in `KREATE/DECISIONS.md`.

## Business and Pilot Reasoning

Explore, where relevant:

- current operational cost of the problem,
- what is already paid for,
- switching costs,
- procurement path,
- who controls budget,
- willingness to run a pilot,
- acceptable pilot duration,
- operational guardrails,
- success metrics,
- failure conditions,
- adoption friction,
- potential pricing basis.

These can remain hypotheses until evidence exists. Do not fabricate numbers merely to complete a business model.

## Freedom to Explore

This role may initiate new work when it uncovers a high-leverage question.

Examples:

- investigate a newly discovered buyer class,
- compare an adjacent beachhead,
- run a short observation study,
- inspect public waste or procurement datasets,
- test a workflow with a service blueprint,
- propose a different pilot design,
- challenge whether hardware is necessary,
- challenge whether forecasting is the right intervention,
- identify an entirely different decision point within food operations.

New work should have a clear question, expected decision impact, and evidence target. It does **not** require prior permission for routine reversible exploration.

## Collaboration

### With EE

Share operational measurement needs, physical constraints, staff burden, installation realities, and data-quality gaps.

### With CS1

Translate observed decision workflows into model requirements and identify which input signals users actually have access to.

### With CS2

Provide structured evidence, contradictions, customer language, beachhead reasoning, and changes in assumptions so the product/application story reflects reality.

## Anti-AI-Slop Standard

AI may accelerate research, transcription, synthesis, analysis, and writing. It may not replace evidence.

Reject outputs that:

- invent interview findings,
- infer customer needs without evidence and present them as facts,
- contain unsourced market numbers,
- create fictional personas and pass them off as research,
- flatten contradictory interviews into a fake consensus,
- use generic startup language in place of operational detail,
- claim climate or financial impact that has not been measured or defensibly estimated.

Generic phrasing should be rewritten into specific operational language whenever possible.

## Evidence-Based Completion Standard

Work is considered useful when it changes or strengthens a decision, not merely when a document exists.

Strong outputs may include:

- interview records with specific evidence,
- a validated or rejected assumption,
- a new stakeholder map,
- a changed beachhead ranking,
- a quantified process constraint,
- a clearer pilot path,
- a discovered blocker,
- a customer-language insight that changes product design,
- evidence that an earlier product feature should be killed.

The IE lead is encouraged to challenge the team's current thesis aggressively. A rejected assumption is valuable progress.

## Application-Stage Success Criteria

By the October 8 application freeze, the market/customer side should ideally support:

- a sharply stated climate-relevant operational problem,
- a justified initial beachhead,
- evidence from a diverse set of relevant stakeholders,
- an interview-derived end-user / persona description,
- buyer and decision-path understanding,
- an explicit record of what the team originally believed and what changed,
- a credible pilot path,
- a clear statement of what is still unknown.

The goal is not certainty. The goal is a disciplined, evidence-rich startup thesis that the team can defend under questioning.
