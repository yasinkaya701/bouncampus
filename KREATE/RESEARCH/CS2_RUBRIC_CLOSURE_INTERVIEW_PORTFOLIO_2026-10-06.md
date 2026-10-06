# CS2 KREATE Rubric Closure & Interview Portfolio

**Date:** 2026-10-06  
**Owner:** CS2 — Product Strategy, Evidence Synthesis & Application  
**Base:** current `role/cs2-product-strategy` at branch creation  
**Evidence class:** repository synthesis / execution planning. This file is not interview evidence.

## Current selection-risk diagnosis

The repository is substantially stronger on technical architecture, evidence boundaries and secondary/public research than on primary market research.

At this base:

- `KREATE/EVIDENCE.md` contains no `E-INT-*` interview evidence IDs.
- `KREATE/PMR/INTERVIEW_TRACKER.md` still has all 16 target slots in `TODO`.
- IE's canonical acquisition tracker is now `REQUEST_READY` for #292/#358, but prepared request routes are not completed outreach, interviews, export access, or primary evidence.
- Public waste, procurement, competitor and workflow research cannot substitute for customer/problem/persona evidence.
- Technical prototypes and pilot protocols cannot establish adoption, willingness to pay, buyer identity or workflow fit.
- The KREATE rubric assigns **40%** to PMR, making real interview evidence the highest-leverage remaining application input.

The strategic risk is therefore not "the demo looks too simple." It is:

> The team may have a sophisticated, claim-safe product thesis but insufficient primary evidence showing that the hypothesized decision, user, buyer and pain are real.

## Rubric closure state

| Area | Current defensible state | Main blocker | CS2 consequence |
| --- | --- | --- | --- |
| Team — 20% | Roles and repository execution are visible | application-ready human-verified capability evidence/sign-off | Gather concise proof; do not use generic team superlatives. |
| Problem — 20% | Public Boğaziçi food-waste baseline exists | no primary evidence that demand mismatch / pre-service quantity is a material cause | Keep causal problem wording as hypothesis. |
| Beachhead — 10% | institutional dining is a coherent learning environment | no primary evidence that it is the best first market or repeats across sites | Require a second-site same-workflow test. |
| Persona — 10% | plausible roles are identifiable | no verified operational user + buyer + veto chain | Separate user, decision owner, beneficiary, buyer and approver. |
| PMR — 40% | secondary research and interview tooling are strong | zero registered completed interview evidence at this base | Highest priority: conduct and register real interviews. |

## Do not duplicate IE

IE owns the high-value source-truth and contract acquisition lanes:

- #292 — privacy-minimized service-level export + semantic reconciliation;
- #358 — current contract/specification/hakediş/acceptance mechanics;
- recent-service operational reconstruction.

CS2 interviews should focus on **product adoption, decision authority, buyer logic, switching friction and repeatability**, while consuming IE facts rather than re-asking the same data-access questionnaire.

## CS2 four-interview portfolio

These are target profiles and question contracts for the four CS2 tracker slots. They are not scheduled or completed interviews.

### CS2-01 — Actual decision user / approver

**Target:** the real role that can change or approve a pre-service quantity, allocation or batch decision.

**Primary question:** What would make this person use, edit, ignore or reject a recommendation before the real freeze point?

Capture one recent concrete decision:

- initial quantity / plan;
- information available at that moment;
- later change, if any;
- who could approve the change;
- freeze point;
- consequence of too much vs too little;
- current workaround;
- acceptable recommendation format/range;
- override reasons;
- maximum added workflow burden.

**Decision impact:**
- supports/modifies/kills the human-reviewed decision-support wedge;
- defines product UX requirements;
- constrains recommendation timing and abstention behavior.

**Kill trigger:** the user cannot materially alter the decision, or the recommendation arrives after useful discretion ends.

### CS2-02 — Economic buyer / pilot approver

**Target:** the role with authority to approve a pilot, software spend, operational change or procurement path.

**Primary question:** What evidence and internal process would be required to approve a bounded pilot and later a purchase?

Capture:

- who can approve a pilot;
- who controls budget;
- procurement threshold/process;
- required security/privacy/legal review;
- integration expectations;
- required proof of value;
- acceptable pilot duration/burden;
- whether savings, service reliability, sustainability reporting or another KPI matters;
- who benefits if excess decreases;
- who bears downside if shortages increase.

**Decision impact:**
- separates user from buyer;
- tests whether the value path is commercially plausible;
- determines accelerator/pilot ask.

**Kill trigger:** no plausible sponsor/budget/procurement path even if operational performance improves.

### CS2-03 — Contractor-side operations / adoption counterpart

**Target:** the current or analogous institutional food-service contractor operations role responsible for planning, production, allocation or reconciliation.

**Primary question:** Where would a recommendation enter the contractor workflow, and would it create value or conflict with current incentives/contract obligations?

Capture:

- planning sequence;
- batch/replenishment options;
- revision rights;
- status-quo tools;
- shortage buffer logic;
- overproduction consequence;
- contract constraints;
- data handoffs;
- trust threshold;
- switching friction;
- whether the contractor would prefer university-side, contractor-side or shared ownership of the tool.

**Decision impact:**
- tests whether the product should be university-led, contractor-led or shared;
- reveals integration surface and incentive conflict.

**Kill/modify trigger:** contractor workflow or incentives make the proposed recommendation non-actionable or value-destructive.

### CS2-04 — Second-site same-workflow falsification interview

**Target:** an institutional dining operator / buyer outside the immediate Boğaziçi context.

**Primary question:** Does the same decision object, freeze point, uncertainty and outcome-measurement problem exist elsewhere?

Use the same compact structure:

- what is the decision object?
- who owns it?
- when does it freeze?
- what information exists before freeze?
- how is surplus / shortage measured?
- what is the current workaround?
- what system/vendor already solves part of it?
- what would make a new decision layer worth switching to?
- who approves a pilot?
- what is materially different from Boğaziçi?

**Decision impact:**
- tests beachhead repeatability;
- separates a real market pattern from a single-campus custom workflow;
- identifies product-standard vs site-specific components.

**Kill/modify trigger:** the control point is highly institution-specific or incumbent workflow already solves the problem adequately.

## Interview evidence standard

For every real CS2 interview:

1. update the corresponding `CS2-0X` row only after a real outreach/scheduling/completion event;
2. preserve date, role, organization type and note-taker;
3. record concrete incidents before opinions;
4. separate reported fact from CS2 interpretation;
5. add an `E-INT-*` row only for a narrow promotable claim;
6. preserve contradictory evidence;
7. explicitly write `NONE — no promotable claim` if the conversation produces no admissible application claim;
8. update KEEP / MODIFY / KILL only because evidence changed.

## Cross-role question firewall

Do not ask every stakeholder the same giant questionnaire.

- **IE** asks source truth, current records, real workflow, contract mechanics.
- **CS1** asks technical decision semantics, baseline, input timing and evaluation feasibility.
- **EE/EHB** asks physical outcome truth, measurement method and missing-field feasibility.
- **CS2** asks adoption threshold, buyer/approver chain, decision product fit, switching friction and repeatability.

Overlap is allowed only to triangulate a decision-changing fact.

## Submission rule

Until real `E-INT-*` evidence exists, the application may describe:

- what the team investigated;
- what public/secondary evidence narrowed;
- which hypotheses were killed;
- which primary questions remain open;
- the product architecture and proposed pilot.

It must not describe:

- PMR validation that did not occur;
- a verified persona/buyer;
- willingness to pay;
- operator adoption;
- product-market fit;
- measured local impact.

## Immediate CS2 priority

The next unit of work with the highest expected application value is not another broad source search or model feature.

It is:

```text
4 distinct real CS2-led conversations
→ concrete incidents / buyer mechanics / adoption objections
→ narrow E-INT evidence
→ assumption-state changes
→ product KEEP / MODIFY / KILL
→ application claim promotion or removal
```

If CS2 can complete only one interview first, prioritize **CS2-01 actual decision user / approver** because it can falsify the product control point before further product work.
