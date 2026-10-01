# KREATE Assumption Register

Allowed status values are exactly: `UNKNOWN`, `TESTING`, `SUPPORTED`, `REJECTED`, `CONFLICTING`.

Rules:

- `SUPPORTED` requires evidence IDs that directly support the hypothesis; it does not mean universally proven.
- `REJECTED` requires evidence that contradicts the hypothesis or a decision to abandon it based on evidence.
- `CONFLICTING` means credible evidence points in materially different directions.
- Do not promote a hypothesis because it appears in product copy or because the team prefers it.

| ID | Hypothesis | Why it matters | Evidence needed | Evidence IDs | Status | Owner | Last updated | Revisit condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H-001 | University/institutional dining is a defensible beachhead for the application. | Beachhead and PMR scope determine who we interview and what claims we can make. | Repeated evidence from relevant operators/decision stakeholders showing a concentrated, reachable problem and a coherent decision workflow. | E-REP-003 only documents current repo focus; it is not market validation. | TESTING | IE | 2026-09-30 | Reassess after at least 8 relevant interviews or earlier if strong contradictory evidence appears. |
| H-002 | The food-production quantity decision happens early enough and with enough discretion for decision support to change an outcome. | If the decision is fixed elsewhere or too late to influence, the proposed intervention point is wrong. | Concrete last-incident stories: timing, actors, approvals, constraints, and what can actually change. | — | UNKNOWN | IE | 2026-09-30 | Reassess after 4 decision-workflow interviews. |
| H-003 | Demand mismatch materially contributes to avoidable food waste in the target dining workflow. | This is the core causal problem hypothesis; public waste totals alone do not prove it. | Incident-level evidence separating demand error from menu quality, procurement, serving policy, safety rules, leftovers, events, and other causes. | — | UNKNOWN | IE | 2026-09-30 | Reassess after 6 relevant incidents across multiple stakeholders. |
| H-004 | Produced portions, served portions, waste mass, menu/context, or equivalent operational data can be captured with acceptable effort for a pilot. | Without usable measurement, the team cannot validate the intervention or make defensible impact claims. | Stakeholder confirmation of current data, access rules, measurement process, missing fields, and effort; technical test only after access exists. | E-REP-002 specifies desired fields but does not prove availability. | TESTING | EE | 2026-09-30 | Reassess after 4 data/measurement conversations or a real measurement test. |
| H-005 | A specific operational persona owns or strongly influences the production-quantity decision and can act on a recommendation. | Persona quality depends on real decision authority, not a generic sustainability stakeholder. | Interviews identifying decision owner, influencers, approval path, success metric, failure risk, and escalation path. | — | UNKNOWN | IE | 2026-09-30 | Reassess when at least 3 independent accounts agree or conflict clearly. |
| H-006 | Human-reviewed decision support can fit the existing workflow without unacceptable early-sellout, food-safety, or operational risk. | A useful prediction is insufficient if operators cannot safely use it. | Workflow interviews, objections, baseline comparison, risk constraints, and later a measured pilot if access is secured. | E-REP-001, E-REP-002, E-REP-004 show the proposed human gate, abstention/readiness policy, evaluation framework, and pilot design; PMR/workflow support is still missing. | TESTING | CS1 | 2026-09-30 | Reassess after operator interviews and any measured technical/pilot evidence. |
