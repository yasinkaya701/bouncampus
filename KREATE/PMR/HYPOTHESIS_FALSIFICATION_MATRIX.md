# PMR Hypothesis Falsification Matrix

**Updated:** 2026-10-05
**Purpose:** Turn the application hypotheses into executable, neutral interviews with explicit support/reject criteria.

This file follows Disciplined Entrepreneurship PMR principles:
- direct interaction with potential customers;
- qualitative before quantitative;
- open-ended incident questions;
- pre-committed criteria to reduce confirmation bias;
- customer is the expert of the problem, not the designer of the solution;
- end every useful interview by asking for another relevant person.

Primary method reference:
https://www.d-eship.com/wp-content/uploads/2019/03/Disciplined_Entrepreneurship_-_Primary_Market_Research.pdf

## PMR-H1 — Reachable production control point

### Hypothesis

> In the target university dining workflow, an identifiable operational role determines or approves meal-production quantities before actual demand is known, and the quantity remains adjustable until a meaningful freeze point.

### Best interview profiles
1. Food Services / Dining Operations manager
2. contractor local project / central-kitchen manager
3. food engineer / kitchen production planner

### Neutral incident prompts
- Walk me through the most recent lunch service from the first quantity estimate until service ended.
- When was the number of meals first set?
- Who set it?
- Who could still change it?
- What was the last point at which a change was practical?
- Tell me about the last time an already-planned quantity was changed. What triggered the change?
- What becomes difficult/costly once that point is passed?

### Supporting evidence
A concrete recent workflow showing:
- named role;
- pre-service quantity decision;
- identifiable timing;
- actual revision rights before a freeze point.

### Contradicting evidence
Repeated findings that:
- quantity is fixed contractually far upstream;
- nobody in reachable workflow can change it;
- quantity is determined only after demand realizes;
- the meaningful decision is a different object (e.g. batch release, allocation, portion size rather than total production).

### Product consequence if rejected
Do not force forecasting onto the wrong control point. Pivot to the real reachable decision (batch release, campus allocation, portioning, menu mix, etc.) or kill the dining production wedge.

---

## PMR-H2 — Material, actionable demand mismatch

### Hypothesis

> Demand uncertainty and the current planning process repeatedly create meaningful mismatches between food prepared and food actually needed, producing avoidable edible surplus and/or shortages that can be affected by changing the production decision.

### Best interview profiles
1. production operator / chef / food engineer
2. Food Services manager
3. contractor operations lead
4. waste-measurement owner for boundary clarification

### Neutral incident prompts
- Tell me about the last service where turnout differed noticeably from what you expected.
- What exactly was different?
- What happened to the food/service afterward?
- What was recorded?
- What did you conclude caused the mismatch?
- What else besides demand forecasting could explain the waste that day?
- Describe the last large food-waste event you remember. Where in the process did that waste arise?

### Supporting evidence
Repeated concrete incidents linking:
- demand estimate error;
- production/allocation decision;
- observable surplus or shortage;
- an action that could plausibly have changed the outcome before the freeze point.

### Contradicting evidence
Waste is dominated by another cause such as:
- preparation loss;
- recipe/taste dissatisfaction;
- plate waste / portion sizing;
- food-safety discard rules;
- procurement constraints;
- unavoidable leftovers;
- service-process failure.

### Product consequence if rejected
Change the problem statement and intervention. Do not keep production forecasting as the core merely because a model exists.

---

## PMR-H3 — Asymmetric shortage risk / safety buffer

### Hypothesis

> Operators intentionally maintain a production safety buffer because running out of food creates a more immediate operational risk than producing surplus, and this buffer is currently determined through experience and fragmented information.

### Best interview profiles
1. kitchen production lead
2. Food Services manager
3. contractor project manager

### Neutral incident prompts
- Which is more disruptive in practice: too much food or running out? Tell me about the last time each happened.
- How do you decide whether to make a little extra?
- Is there a typical buffer? How did that practice emerge?
- What happens if an item runs out early?
- Who hears about it first?
- Are there penalties, emergency cooking, complaints, substitutions or other consequences?
- Tell me about the last time you intentionally produced above the expected number.

### Supporting evidence
Behavioral evidence of deliberate padding / risk-avoidance and a concrete shortage consequence.

### Contradicting evidence
- no intentional buffer;
- surplus considered much more costly than shortages;
- rapid batch/replenishment means shortage risk is negligible;
- contract fixes quantity independently of operator risk preference.

### Model consequence
If supported, prediction accuracy alone is insufficient. Recommendation must use asymmetric decision loss and service-continuity guardrails.

---

## PMR-H4 — Measurement/data feasibility

### Hypothesis

> The operation can capture enough service-level planned/produced/served/surplus/waste information at acceptable effort to evaluate the intervention.

### Best interview profiles
1. operational data / office staff identified by Food Services
2. food engineer / kitchen records owner
3. IT / card/turnstile system owner
4. sustainability / waste measurement owner

### Questions
- What numbers are recorded for one meal service today?
- Where are they stored?
- Who owns each field?
- Which are entered before vs after service?
- Can records be exported at date × campus × meal level without personal identifiers?
- How are duplicates/refunds/second meals handled in access-card data?
- Is waste separated into preparation, unserved edible surplus and plate waste?
- What is weighed versus estimated?

### Supporting evidence
At least a viable minimum dataset with clear source owner/semantics.

### Contradicting evidence
Outcome cannot be measured or reconstructed without excessive staff burden, privacy risk or incompatible semantics.

### Product consequence
Use minimum measurement hardware only for the missing decision-critical field. Do not add sensing where reliable existing data already exists.

---

## PMR-H5 — Persona / authority

### Hypothesis

> A specific operational persona owns or strongly influences the production decision and can act on a recommendation.

### Questions to ask every interviewee
- Who made the last quantity decision?
- Who could overrule them?
- Who approves a change?
- Who receives complaints if the meal runs out?
- Who reviews surplus/waste afterward?
- Who would have to approve a pilot?
- Who controls the budget?

### Supporting evidence
Independent accounts converge on a real role/person and authority chain.

### Contradicting evidence
Authority is so fragmented that no persona can use the proposed product without multi-party coordination every service.

---

## PMR-H6 — Workflow adoption

### Hypothesis

> Human-reviewed decision support can fit the production workflow without unacceptable food-safety, service, contractual or operational risk.

### Ask about current behavior, not product opinion
- Tell me about a recent time new information changed production.
- What information would you trust enough to change a planned quantity?
- What would stop you from acting even if a forecast looked convincing?
- What approvals/checks cannot be skipped?
- How much extra work can a planning step realistically add?
- When is a recommendation too late to be useful?

### Strong evidence
Existing behavior shows operators already revise decisions based on new signals and can articulate trust/guardrail requirements.

### Weak/non-evidence
- `Sounds useful.`
- `AI could help.`
- `We support sustainability.`

---

# Economic buyer / contract module

Ask only relevant decision/procurement actors:
- What quantity is used for payment/hakediş?
- Who absorbs excess-production ingredient/labor cost?
- Who bears shortage/recovery/penalty cost?
- If unnecessary production decreases, whose economics improve?
- Who can purchase software / require contractor usage?
- When contracts renew, who writes the technical requirement?

Do not assume end user = economic buyer.

---

# Interview evidence standard

A useful interview record should capture:

```text
role
last_real_incident
current_workflow
input_signals
decision_owner
freeze_point
revision_rights
current_baseline/heuristic
surplus_consequence
shortage_consequence
measurement/data
contract/economic_incentive
objections
unexpected_finding
hypothesis_effect
referral
```

## Evidence promotion

Do not count `yes/no` confirmations as equal evidence to a concrete incident.

Prefer:
1. recent specific event;
2. direct participant in workflow;
3. observable record/artifact if available;
4. independent corroboration from another role;
5. explicit contradiction preserved.

---

# Sample strategy

Avoid selection bias from interviewing only friendly Boğaziçi contacts.

Minimum high-information pattern:
- university-side governance/operations;
- daily technical/production operator;
- contractor-side operation if outsourced;
- second institution with similar proposed beachhead workflow;
- one institution with a different procurement/governance archetype to test segmentation.

The form minimum of three interviews is not a research maximum.

---

# Final question

Every interview should end with:

> Who else do you know who deals with this same production-planning problem from a different angle, and would you be willing to introduce us?

This tests the DE `word-of-mouth / community` condition while expanding the sample.
