# CS2 — Product Strategy, Evidence Synthesis & Application Lead

## Mission

Convert raw customer evidence, technical findings, hardware feasibility, and market research into the strongest possible KREATE application and product strategy.

CS2 is the team's **synthesis and contradiction owner**. The role is not primarily frontend work and not the team-platform maintainer. The repository operating system can be automated; CS2's human time should be spent deciding **what BOUNCAMPUS should become and what can honestly be claimed**.

**Application deadline:** 8 October 2026, 23:59  
**Primary optimization target:** maximize Top-15 selection probability through evidence-backed product clarity.

---

## Core question

> Given everything we learned, what should we build, for whom, why is it better than the status quo, and can we prove every important statement in the application?

---

## Scope

### P0 — Must be completed before application freeze

1. Cross-interview PMR synthesis.
2. Assumption-status discipline.
3. Product requirements derived from evidence.
4. Feature prioritization and scope control.
5. Competitor + status-quo intelligence.
6. Differentiation and positioning.
7. Product-level architecture and causal logic.
8. Climate-impact claim discipline.
9. KREATE rubric coverage.
10. Single-voice final application.
11. Red-team / contradiction review.

### P1 — Allowed experiments

- Alternative product positioning.
- Feature-scoring refinements.
- New segment comparison if PMR reveals stronger evidence.
- Product requirement experiments.
- Lightweight prototypes that answer a strategic question.
- Application narrative A/B versions for internal review.
- Competitive research extensions.

### Out of scope unless evidence changes priorities

- Pixel-perfect frontend redesign before selection.
- Jury-demo polishing before the 8 October application.
- Owning repository automation as a full-time task.
- Creating generic startup decks or strategy documents with no rubric consequence.
- Adding features because they sound innovative.

---

## Shared PMR responsibility

CS2 is expected to lead approximately **4 interviews** as part of the team's target of 16 distinct interviews.

Priority interview targets:

- Decision-makers and champions
- Sustainability / operations stakeholders
- Potential buyers
- Operators who can articulate product trust and adoption constraints
- Stakeholders useful for competitor/status-quo comparison

CS2 should deliberately seek **contradictory evidence**, not only friendly confirmation.

Example probes:

- What would make you refuse to use this system?
- What do existing tools already solve well?
- Why would you not run a pilot?
- Who would block this internally?
- Which part of this problem is actually not important?
- When is overproduction acceptable?
- What would make a recommendation untrustworthy?

---

## Workstreams

### 1. Evidence synthesis

IE owns customer-discovery method and market research quality. CS2 owns cross-source synthesis into product decisions.

For every major pattern, produce:

`raw evidence -> repeated pattern -> assumption impact -> product implication -> application implication`

Example:

```text
Evidence:
Several operators prioritize avoiding early sell-out over minimizing small surplus.

Pattern:
Forecast error has asymmetric operational cost.

Product implication:
Do not return a single aggressive minimum-production number.
Expose a recommendation band and risk trade-off.

Application implication:
Human approval and risk-aware planning are product requirements, not demo decoration.
```

### Acceptance gate

A synthesis statement must reference evidence IDs or clearly state that it remains a hypothesis.

---

### 2. Assumption discipline

Use `KREATE/ASSUMPTIONS.md` as the canonical assumption ledger.

Statuses:

- UNKNOWN
- TESTING
- SUPPORTED
- CONFLICTING
- REJECTED

CS2 is responsible for asking:

- What would falsify this?
- Is the wording stronger than the evidence?
- Are we confusing preference with behavior?
- Are we generalizing one interview to a market?
- Are we ignoring contradicting evidence?

### Acceptance gate

No critical application claim may depend on an assumption still marked UNKNOWN without being explicitly framed as a hypothesis.

---

### 3. Product requirement synthesis

Translate PMR and technical evidence into requirements.

Every important requirement should include:

- Requirement ID
- User/operational problem
- Evidence ID(s)
- Required behavior
- Success condition
- Owner
- Open risk

Example:

```text
PR-07
Problem: operator cannot trust a recommendation when source coverage is incomplete.
Evidence: E-014, E-021, technical failure analysis.
Requirement: recommendation must expose source health and may WITHHOLD when critical signals are missing.
Success: missing-source scenario produces visible degraded state rather than a normal recommendation.
```

### Acceptance gate

No evidence/problem link -> requirement is P1 experiment, not P0 product requirement.

---

### 4. Feature prioritization

Score candidate features using a consistent framework.

Recommended dimensions:

| Criterion | Weight |
|---|---:|
| PMR evidence | 30% |
| Problem impact | 25% |
| Differentiation | 15% |
| Pilotability | 15% |
| Technical feasibility | 10% |
| Climate relevance | 5% |

Possible decisions:

- BUILD NOW
- TEST FIRST
- DEFER
- KILL FOR KREATE

### Acceptance gate

Every BUILD NOW feature must identify:

- Evidence.
- Owner.
- User/decision affected.
- Success condition.
- Kill condition.

"It would look impressive" scores zero.

---

### 5. Competitor and status-quo intelligence

Analyze both commercial products and non-product alternatives.

Minimum comparison set should include, when relevant:

- Winnow
- Leanpath
- Orbisk
- Manager experience
- Excel/manual planning
- Last-week/same-day heuristic
- POS/reporting systems
- Existing kitchen scales/waste processes

For each competitor/status quo capture:

- Target customer
- Job solved
- Inputs
- Intervention timing
- Hardware dependency
- Outputs
- Decision supported
- Strengths
- Limitations
- Adoption friction
- Why a customer stays with it
- Potential coexistence/integration path

### Acceptance gate

Do not manufacture weaknesses to make BOUNCAMPUS look better.

The required question is:

> Why BOUNCAMPUS instead of doing nothing, continuing the current workflow, or buying an established solution?

---

### 6. Differentiation and positioning

A candidate positioning hypothesis is:

> BOUNCAMPUS helps institutional food operations make a better production decision before food becomes waste, keeps the operator in control, and closes the loop with measured outcomes.

This is a hypothesis until PMR and competitor evidence support it.

### Acceptance gate

Differentiation must be:

- Relevant to the selected beachhead.
- Meaningful in an actual workflow.
- Supported by evidence.
- Difficult to confuse with a generic "AI sustainability platform."

---

### 7. Product architecture

CS1 owns technical decision architecture. EE owns physical measurement architecture. CS2 owns the product-level narrative:

```text
KNOW
context + operational signals

-> DECIDE
risk-aware production recommendation

-> ACT
human operator decision

-> MEASURE
real service outcome / waste measurement

-> LEARN
pilot evidence + calibration

-> IMPROVE
next service decision
```

### Acceptance gate

Every block must correspond to a real user/operational need or a clearly defined experiment.

---

### 8. Climate-impact causal chain

Maintain claim discipline:

```text
better production decision
-> less avoidable overproduction, if hypothesis holds
-> less food discarded, if measured
-> measured waste reduction
-> only then climate-impact estimation using documented conversion methodology
```

### Automatic FAIL

Any unsupported claim such as:

> BOUNCAMPUS reduces carbon emissions by 30%.

without measured evidence and a documented conversion method.

---

## KREATE application ownership

CS2 is the **single owner of the final application narrative**.

Other roles provide evidence and technical sign-off, but the final form must read as one coherent argument rather than four pasted sections.

### Rubric targets

#### Team — 20%

Explain why 1 IE + 1 EE + 2 CS is structurally suited to this problem:

- Customer/operations evidence
- Physical measurement
- Decision intelligence
- Product/evidence synthesis

Do not rely on generic "multidisciplinary team" language.

#### Problem — 20%

Must be:

- Narrow
- Quantified where evidence exists
- Causally careful
- Operationally specific

Official food-waste baseline is problem evidence; do not claim the full waste amount is caused by demand mismatch.

#### Beachhead Market — 10%

Show:

- Alternatives considered
- Selection criteria
- Evidence
- Why the segment is pilotable

#### Persona — 10%

Persona must be interview-derived and operational, not fictional storytelling.

#### PMR — 40%

This is the dominant section.

The strongest PMR narrative has the form:

> We initially believed X. We spoke with Y. We observed Z. Evidence contradicted/strengthened our assumption. Therefore we changed A in the product/market strategy.

Interview count without learning is weak PMR.

---

## Contradiction Hunter duty

At least daily during the final application period, challenge the team with questions such as:

- How do we know this?
- Is this source primary or secondary?
- Is this a fact, estimate, assumption, target, or demo value?
- Did a customer actually say/do this?
- Does a competitor already solve it?
- Why does hardware need to exist?
- Why does AI/ML need to exist?
- Why university dining first?
- What is the strongest reason not to adopt?
- What result would make us kill the feature?

If the team cannot answer, downgrade/remove the claim or create a test.

---

## Red-team ownership

Every ~48 hours during the sprint, run a short red-team review.

Required outputs:

- At least one attacked assumption.
- Evidence for/against it.
- A KEEP / CHANGE / KILL decision, or a clearly defined experiment needed to decide.

Example attacks:

> A kitchen manager using last week's count may perform just as well as BOUNCAMPUS.

> A custom smart scale may add no value over an existing commercial scale.

> Demand mismatch may not be a major cause of avoidable food waste in the selected environment.

> Universities may be easy to access but a poor economic beachhead.

The team gets stronger when these attacks survive honest testing.

---

## Cross-team handoffs

### From IE

Need:

- Structured PMR records.
- Beachhead comparison.
- Workflow map.
- Buyer/user/champion structure.
- Contradictions.

### From EE

Need:

- Measurement feasibility.
- Hardware evidence.
- Deployment constraints.
- What hardware does and does not prove.

### From CS1

Need:

- Baselines.
- Decision contract.
- Uncertainty logic.
- Technical limitations.
- Pilot metric design.

### Back to all roles

CS2 returns:

- Product requirements.
- Feature priorities.
- Claims requiring sign-off.
- Rejected claims.
- Missing evidence requests.
- Final application draft.

---

## Anti-AI-slop rules

Automatic FAIL if:

- Application prose contains facts without evidence ownership.
- The team uses adjectives in place of differentiation.
- PMR findings read like generic LLM-generated customer pain statements.
- A persona contains invented age, biography, habits, or motivations not supported by interviews.
- Competitor weaknesses are guessed.
- Product features are listed without showing which customer problem they solve.
- Technical prototypes are described as deployed systems.
- Climate outcomes are claimed before measurement.
- Four role outputs are pasted together without a consistent thesis.

Words such as `revolutionary`, `groundbreaking`, `seamless`, `transformative`, `cutting-edge`, and `AI-powered` should be treated as warning signs. Replace them with precise mechanisms and evidence.

---

## Definition of Done — 8 October

The CS2 role is DONE only if:

- [ ] CS2 led roughly 4 relevant PMR interviews, unless team coverage justified redistribution.
- [ ] Cross-interview PMR synthesis exists.
- [ ] Major assumptions have evidence-aware statuses.
- [ ] Important contradictions are visible.
- [ ] Product requirements trace to evidence or explicit experiments.
- [ ] Features are prioritized with BUILD/TEST/DEFER/KILL decisions.
- [ ] Status quo and relevant competitors are honestly compared.
- [ ] Differentiation is specific and defensible.
- [ ] Product architecture is coherent across IE, EE and CS1 outputs.
- [ ] Climate causal chain does not overclaim.
- [ ] Every KREATE rubric section has evidence coverage.
- [ ] Final application has one voice and one thesis.
- [ ] Factual/technical claims have role-owner sign-off.
- [ ] A final red-team pass has removed unsupported claims.

---

## Success standard

CS2 succeeds when the application makes a reviewer think:

> This team did not fall in love with a feature. They investigated a real operational problem, changed their assumptions when evidence demanded it, built a coherent intervention around that evidence, and know exactly what still needs to be proven.
