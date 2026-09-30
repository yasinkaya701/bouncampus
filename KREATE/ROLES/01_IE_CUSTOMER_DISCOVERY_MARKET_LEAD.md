# IE — Customer Discovery & Market Lead

## Mission

Maximize BOUNCAMPUS's probability of reaching the KREATE Top 15 by proving that the team is solving a real, repeated, valuable problem for a sharply defined first market.

The IE role is **not** "the person who does all interviews." Customer discovery is a team responsibility. The IE owns the **method, research quality, market logic, and operational synthesis**.

**Application deadline:** 8 October 2026, 23:59  
**Primary optimization target:** evidence quality, not document volume.

---

## Core question

> What is actually happening in institutional food operations, for whom is it painful, how is the decision made today, and which first market gives BOUNCAMPUS the strongest entry point?

---

## Scope

### P0 — Must be completed before application freeze

1. PMR research protocol and interview quality standard.
2. Problem hypotheses and falsification questions.
3. Market segmentation and beachhead selection.
4. End-user / economic-buyer / champion / influencer map.
5. Current operational workflow and decision map.
6. Status-quo alternatives and switching friction.
7. Persona grounded in actual interviews.
8. PMR evidence synthesis supporting the application.
9. Market and operational inputs for the product requirements.

### P1 — Allowed when supported by evidence

- Adjacent segment discovery: factory cafeterias, hospitals, municipal kitchens, contract catering.
- Procurement and pilot-process research.
- Unit-economics hypotheses.
- Institutional dining process benchmarking.
- TAM/SAM estimation after beachhead definition.
- Pilot recruitment and partner mapping.

### Out of scope unless evidence changes priorities

- Owning frontend implementation.
- Owning forecasting/model development.
- Building hardware.
- Writing generic sustainability market reports with no decision consequence.
- Producing invented personas, synthetic interviews, or unsupported market numbers.

---

## Shared PMR model

Target before the 8 October application: **16 distinct, high-quality interviews**.

Each team member is expected to lead approximately **4 interviews**. A second team member should join as note-taker/observer when practical.

Suggested coverage:

- University dining managers / operators
- Food engineers / kitchen managers
- Catering operators
- Sustainability / SKS / facilities stakeholders
- Procurement / administration stakeholders
- Institutional food-service operators outside universities
- Data / POS / measurement stakeholders

The IE coordinates coverage so the team does not accidentally conduct 16 interviews with the same persona.

### Interview rule

For the first part of an interview, do **not pitch the product**. Investigate the last real occurrence of the problem.

Prefer:

> Tell me about the last lunch service where demand was significantly different from what you expected.

Avoid:

> Would you use an AI system that predicts demand?

---

## Required interview record

Every interview must create a structured PMR record under `KREATE/PMR/` or the repository's current PMR registry.

Minimum fields:

- Interview ID
- Date
- Interviewer(s)
- Role
- Organization type
- Current planning workflow
- Last concrete incident
- Pain / consequence
- Frequency
- Current workaround
- Data currently available
- Decision owner
- Approval / buying structure
- Key operational constraint
- Exact quote(s), where permission and notes allow
- Referral / who else to speak with
- Hypotheses strengthened
- Hypotheses weakened
- New hypothesis
- Product implication

A transcript alone is **not** sufficient.

---

## Workstreams

### 1. Hypothesis map

Maintain explicit hypotheses in `KREATE/ASSUMPTIONS.md`.

At minimum test:

- Demand mismatch is a meaningful contributor to avoidable food waste.
- Production planning contains a recurring pre-service decision that can be improved.
- Current planning uses incomplete or manual information.
- Operators care about both overproduction and early sell-out risk.
- Human-in-the-loop recommendations are operationally more acceptable than autonomous dispatch.
- Service-level food-waste measurement is incomplete, expensive, manual, or fragmented enough that better measurement has value.
- A university dining operation can realistically run a short controlled pilot.
- The end user, economic buyer, and champion may be different people.

Allowed statuses:

- UNKNOWN
- TESTING
- SUPPORTED
- CONFLICTING
- REJECTED

Do not casually use `VALIDATED` for weak qualitative evidence.

### Acceptance gate

A hypothesis may move to `SUPPORTED` only when:

1. Evidence IDs are attached.
2. Evidence comes from more than one source or a single unusually authoritative source.
3. Contradicting evidence is recorded, not hidden.
4. The statement is no stronger than the evidence.

---

### 2. Current-state workflow map

Map the actual institutional food-service process:

`forecast -> production planning -> preparation -> service -> surplus/waste -> measurement -> reporting -> next decision`

For each step identify:

- Owner
- Inputs
- Decision
- Tool / workaround
- Failure mode
- Data generated
- Pain
- Constraint

### Acceptance gate

The workflow is FAIL if it is based mainly on assumptions from the team rather than interview evidence.

---

### 3. Beachhead market selection

Compare at least:

- University dining
- Factory cafeterias
- Hospital kitchens
- Municipal / public kitchens
- Contract catering

Score using consistent criteria:

- Pain strength
- Pain frequency
- Access to users
- Ability to pilot
- Data availability
- Budget / willingness to allocate resources
- Decision speed
- Need for the whole product
- Competitive intensity
- Expansion potential
- Team access / unfair advantage

### Acceptance gate

The selected beachhead must have:

- A specific end user.
- A repeated decision.
- A measurable outcome.
- A plausible pilot path.
- Evidence explaining why this segment wins over alternatives.

"Universities because we are students" is not sufficient.

---

### 4. Persona and buying structure

Do not invent demographic fiction.

Build an interview-derived persona containing:

- Job-to-be-done
- Operational KPI
- Daily workflow
- Repeated pain
- Worst failure
- Risk tolerance
- Current workaround
- Decision authority
- Buying influence
- Objections
- Trigger to try a pilot
- Required trust/evidence

Separately map:

- End user
- Economic buyer
- Champion
- Influencer
- Blocker

### Acceptance gate

Every material persona statement must trace back to PMR evidence.

---

### 5. Status quo and switching logic

The most important competitor may not be a startup.

Research:

- Manager experience
- Last-week / same-weekday heuristic
- Excel / manual sheets
- POS reports
- Catering software
- Existing waste-measurement processes
- Winnow
- Leanpath
- Orbisk
- Other relevant systems discovered during PMR

Questions to answer:

- Why is the current method still used?
- What does it do well?
- Where does it fail?
- What would make switching too risky?
- What data or integration would be required?
- Who pays for the failure today?

---

## Daily operating expectations

Each day produce concrete artifacts, not activity descriptions.

Daily update format:

```text
DONE:
EVIDENCE CREATED:
ASSUMPTION CHANGED:
BLOCKER:
NEXT:
```

"Did market research" is not a valid DONE statement.

---

## Cross-team handoffs

### To EE

Provide:

- What is actually measured today.
- Who performs measurement.
- Required accuracy / workflow constraints learned from operators.
- Whether smart-scale hardware solves a real pain or only looks impressive.

### To CS1

Provide:

- Decision timing.
- Inputs operators actually use.
- Cost of forecast errors.
- Asymmetric risks: overproduction vs early sell-out.
- Baselines used today.

### To CS2

Provide:

- Raw PMR records.
- Market comparison.
- Buyer/user structure.
- Contradictions and rejected assumptions.
- Operational requirements.

CS2 owns cross-interview product synthesis and application narrative; IE owns the quality of market/customer research feeding it.

---

## Anti-AI-slop rules

Automatic FAIL if any of the following appears without evidence:

- Invented interview or customer quote.
- Invented market size.
- Invented willingness to pay.
- Generic persona demographics presented as research.
- "AI-powered", "revolutionary", "seamless", "transformative", "cutting-edge" used instead of a precise claim.
- A survey/interview count that cannot be traced to individual records.
- Unsupported statement that demand mismatch explains all or most measured food waste.
- PMR summary that hides contradicting interviews.

AI may assist with organization, coding, comparison, or drafting. It may not create facts.

---

## Definition of Done — 8 October

The IE role is DONE only if:

- [ ] The shared PMR target has meaningful coverage across relevant stakeholder types.
- [ ] IE personally led roughly 4 high-quality interviews, unless team coverage required a justified redistribution.
- [ ] All interviews have structured evidence records.
- [ ] Major assumptions have explicit statuses and evidence links.
- [ ] At least one important team assumption was challenged or changed by PMR, or the evidence explains why none changed.
- [ ] Current operational workflow is evidence-backed.
- [ ] One beachhead market is selected and alternatives are explicitly rejected with reasons.
- [ ] End user, buyer, champion, influencer and blocker are distinguished.
- [ ] Persona is interview-derived.
- [ ] Status quo is understood, not caricatured.
- [ ] CS2 has everything needed to write a strong Problem, Beachhead, Persona and PMR application narrative.
- [ ] No important claim depends on fabricated or unattributed evidence.

---

## Success standard

The goal is not to prove the team's initial idea correct.

The goal is to make the strongest possible evidence-backed decision about **which problem, customer, and intervention BOUNCAMPUS should pursue** before the KREATE application freezes.
