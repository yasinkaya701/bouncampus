# KREATE Evidence-Gated Feature Backlog

Feature work is subordinate to the October 8 application evidence gate. Do not invent scores to make an existing feature look prioritized.

**Scoring scale:** `TODO — team must agree the component scoring scale before any weighted score is calculated.` Missing component evidence stays `TODO`; do not treat missing values as zero or as an implied score.

| Feature | Problem/decision improved | Evidence IDs | PMR evidence 30 | Problem impact 25 | Differentiation 15 | Pilotability 15 | Feasibility 10 | Climate relevance 5 | Weighted score | Decision | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Next-service production planning band | Helps the accountable dining operator choose how much to prepare for a service under uncertain demand/context. | E-REP-001, E-REP-002 | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO — PMR required | CS1 |
| Human approve / edit / hold gate | Helps the accountable operator decide whether and how to use a recommendation instead of auto-dispatching an unvalidated command. | E-REP-001, E-REP-002 | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO — PMR required | CS1 |
| Pilot measurement and scorecard workflow | Helps the team/operator decide whether an intervention reduced normalized waste without worsening service or bypassing safety. | E-REP-002 | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO — PMR required | CS2 / IE |

## Rules

- A feature description must name the user decision or measurable workflow it improves.
- `PMR evidence 30` cannot be scored from team opinion, product copy, or public waste totals alone.
- `MODEL_RESULT` and demo behavior do not substitute for interview evidence.
- A `KEEP`, `MODIFY`, or `KILL` feature decision must be logged in [DECISIONS.md](./DECISIONS.md) with rationale and evidence.
- New product work is P2 unless it directly closes a rubric/evidence gap.