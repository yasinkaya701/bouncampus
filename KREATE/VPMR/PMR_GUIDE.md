# VPMR -> PMR Conversion Guide

Secondary research should make interviews sharper, not make interviews unnecessary.

## H-001 — Is institutional/university dining a defensible beachhead?

**Desk-research signal:** multi-campus dining, centralized production and formal contractor operations make the segment plausible.

**Must ask in PMR:**

- What was the last concrete quantity-planning problem?
- How often does that workflow repeat?
- Is the workflow standardized across sites or client-specific?
- Could one pilot lead to a second comparable deployment?

**Falsifier:** every institution/site uses materially different ownership, data, freeze times and contract incentives such that one product/sales process does not repeat.

## H-002 — Is the production/allocation decision reachable?

**Desk-research signal:** menu, calendar and some reservation/access workflows exist before service.

**Must ask:**

- Who chose the quantity for the most recent service?
- At what exact time did the number become fixed or expensive to change?
- What could still be changed after that point?
- Which inputs were visible before the freeze?
- What happens operationally when demand exceeds the planned quantity?

**Falsifier:** useful signals arrive after the decision is fixed, or the interviewed operator has no meaningful discretion.

## H-003 — Does demand mismatch materially cause avoidable waste?

**Desk-research signal:** official aggregate waste confirms a problem exists; literature shows multiple possible causes.

**Must ask from the last incident:**

- Was the discarded food preparation waste, unserved surplus or plate waste?
- What caused it: overproduction, menu appeal, portion size, safety rule, event disruption, preparation error or something else?
- How much of that incident could a better pre-service quantity decision have prevented?

**Falsifier:** dominant avoidable waste is consistently unrelated to production/allocation uncertainty.

## H-004 — Can the outcome be measured?

**Desk-research signal:** standards support multiple measurement methods; a service-level outcome is necessary for causal evaluation.

**Ask:**

- Which records already exist for produced, served, unsold/surplus and discarded food?
- What is the smallest reliable unit: service, batch, campus, day?
- Who owns the export and how is each field defined?
- Which fields are reconciled/accepted for operations or payment?
- Can a simple scale protocol be added if records do not capture the target waste stage?

**Falsifier:** no reliable prospective outcome can be captured at the decision boundary at acceptable burden.

## H-005 — Who is the persona and who is the buyer?

**Desk-research signal:** university administration, contractor operations, IT/data, quality and finance can hold different pieces of authority.

**Ask:**

- Who sets tomorrow's production/allocation quantity?
- Who can override it?
- Who bears cost when too much is produced?
- Who bears service risk when too little is produced?
- Who owns the software/data system?
- Who could authorize a pilot?
- Who benefits economically if 100 unnecessary portions are avoided?

**Falsifier:** user, buyer, data owner and beneficiary are split with no workable incentive/approval path.

## H-006 — Can decision support fit safely into workflow?

**Desk-research signal:** standards/literature support measurement and forecasting, but model sophistication is not the product by itself.

**Ask:**

- What recommendation format would be actionable: point estimate, range, campus allocation, alert?
- What confidence/uncertainty would make an operator withhold action?
- Which guardrail matters most: sell-out, safety stock, service-level guarantee, contractor penalty?
- What must remain human-approved?
- What is the current baseline rule and why is it trusted?

**Falsifier:** recommendation cannot arrive in time, violates safety/contract rules, or simple current practice already performs adequately.

## Persona interview order

Recommended sequence to maximize information gain:

1. Boğaziçi Food Services / operations owner.
2. Local contractor/central-kitchen production-planning owner.
3. Data/system owner for aggregate service/entry/reservation records.
4. Finance/procurement/contract owner if incentive semantics remain unresolved.
5. Quality/food-safety owner for surplus/reuse/discard constraints.
6. A second institutional dining site or contractor project to test repeatability.

## What not to ask first

Avoid leading questions such as:

- 'Would you use our AI system?'
- 'Do you think food waste is important?'
- 'Would forecasting help?'

Prefer concrete recent behavior:

- 'Tell me about the last service where the prepared quantity was wrong.'
- 'Who set the number and when?'
- 'What did you know at that moment?'
- 'What happened to the excess / what happened when you ran short?'
- 'What record would prove that afterward?'

## Desk research -> claim discipline

| Desk-research finding | Safe use | Unsafe promotion |
| --- | --- | --- |
| official annual waste total | establish problem scale/context | claim it is all overproduction |
| reservation notice | test reservation semantics/access in interview | claim reservations exist for all campuses/services |
| menu vote | candidate preference feature | call it attendance intent or demand label |
| turnstile/payment metadata clue | ask for privacy-safe aggregate export and semantics | claim the team has data access |
| academic demand paper | justify testing candidate features/methods | reuse external model score as expected local performance |
| measurement standard | design a defensible pilot | claim the pilot already meets the standard |
| contractor public sustainability messaging | prioritize contractor PMR | call it customer pain, intent or endorsement |

## Interview capture

Use the repository's `KREATE/PMR/INTERVIEW_TEMPLATE.md`. A real interview may produce no promotable claim. Contradictions are valuable and must remain visible.
