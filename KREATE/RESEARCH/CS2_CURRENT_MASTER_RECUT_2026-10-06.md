# CS2 Current-Master Decision Workstream Recut

**Date:** 2026-10-06  
**Owner:** CS2 — Product Strategy, Evidence Synthesis & Application  
**Base:** current `master` at recut start (`799fd2e1402531160ceaef746cd7fff6eb644b9c`)  
**Status:** current-master synthesis. This file is product/evidence guidance, not PMR evidence, pilot evidence, or a measured outcome.

## Why this recut exists

The historical `role/cs2-product-strategy` branch contains useful research, but it has diverged substantially from current `master`. It must not be wholesale merged or treated as current product truth.

This recut keeps the high-value decision logic while adopting the stricter evidence boundaries now present on `master`.

## Current decision thesis

Do **not** frame the product as:

```text
"use AI to predict cafeteria traffic"
```

Frame the current wedge as:

```text
existing institutional intent / service / reporting signals
→ reconcile event semantics
→ identify a decision that is still reachable before freeze
→ compare the cheapest transparent baseline against current practice
→ add residual modeling only if it earns its complexity
→ produce a bounded recommendation
→ require human approval
→ measure accepted operational outcome prospectively
→ promote only traceable evidence
```

The product is therefore a decision-support and verification loop, not a forecasting demo.

## What survives from the legacy CS2 research

The following conclusions remain useful as **hypotheses / research directions** and must be re-verified against current owners before promotion:

1. Reservation and access signals may contain useful intent information, but reservation, entry/passage, served meals, accepted service, user charge, and contractor settlement are different semantic objects.
2. Existing university reporting surfaces should be preferred over building a parallel raw-event pipeline when they can provide the required aggregate operational fields.
3. The first data request should be a schema/data dictionary or owner-generated aggregate export, not raw card/user logs.
4. The useful product boundary is a reachable operational decision with an owner, freeze time, measurable outcome, and review/approval path.
5. Privacy-minimized aggregate data should be the default architecture.
6. Procurement/payment semantics and sustainability reporting obligations are useful only if they change a real decision or verification record; bureaucracy alone is not product value.
7. A pilot must distinguish operator baseline, model recommendation, final approved action, execution, and measured outcome.

## Current-master truth boundary

The following are non-negotiable:

- No claim that BOUNCAMPUS currently has BUCard, POS, BMS, turnstile, shuttle, meter, or other internal university telemetry unless a current admitted source artifact proves it.
- No claim that a public or historical field is equivalent to `actual_served` without source-owner semantic confirmation and reconciliation.
- No generated/synthetic repository dataset may be presented as measured service truth, benchmark evidence, pilot evidence, or customer evidence.
- No model metric is promoted unless it is tied to an admitted dataset with provenance, target semantics, split/evaluation rules, and reproducibility evidence.
- No recommendation is automatic dispatch. Human approval remains the default operational boundary.
- No savings, waste-reduction, climate, cost, or adoption claim is promoted before measured evidence exists.
- Historical policy or service rules are not current policy unless re-verified.

## Minimum decision record

A useful recommendation must be traceable through:

```text
decision_context
source_artifacts
source_semantics
decision_owner_role
execution_owner_role
freeze_time
operator_baseline
model_or_policy_recommendation
uncertainty_or_range
final_human_action
override_reason
execution_record
accepted_service_record
physical_outcome
waste_or_shortage_outcome
evidence_status
```

If these fields cannot be meaningfully populated, the workflow is not ready for a product claim.

## Product wedge gate

Keep university/institutional dining as the active wedge only while the following can plausibly become true:

- a material avoidable loss is connected to a quantity/service decision;
- the decision has a reachable owner;
- the decision occurs before an identifiable freeze point;
- an aggregate signal exists before that freeze point;
- the signal can be semantically reconciled to a measured outcome;
- a simple baseline can be defined;
- a bounded recommendation can fit the operator workflow;
- the result can be measured prospectively.

If any of these fail repeatedly in PMR or artifact acquisition, modify or kill the wedge rather than adding more model complexity.

## Role handoff

### IE

Resolve real user/buyer/influencer workflow:

- last concrete service incident;
- who owned the quantity/service decision;
- what was known at decision time;
- what could still change;
- what pain or consequence followed;
- what workaround exists today.

Generic opinions about AI do not close the gate.

### EE / EHB

Own measurement truth where physical measurement or device-side acquisition is involved:

- measurement boundary;
- units and calibration;
- timing/latency;
- uncertainty;
- failure modes;
- accepted physical truth.

CS2 must not upgrade simulation/datasheet output into bench or field evidence.

### CS1

Own admission, reconciliation, baseline/model evaluation, recommendation semantics, uncertainty, and fail-closed behavior.

CS2 may define the product/evidence gate but must not bypass CS1 source-truth or semantic-mapping guards.

### CS2

Own:

- claim/evidence synthesis;
- decision-rights map;
- acquisition priority;
- pilot/advisory ladder;
- application narrative;
- product kill/modify criteria;
- consistency between PMR, technical evidence, and product claims.

## High-value acquisition order

1. Decision owner + freeze time.
2. Existing report/export schema and source owner.
3. Semantic mapping from available counts to accepted operational truth.
4. Physical surplus/waste measurement boundary.
5. Produced/consumed/discarded reporting schema if it changes verification.
6. Current contract/hakediş basis only when it changes incentives or decision authority.

The machine-readable queue is in `cs2_evidence_acquisition_queue_2026-10-06.json`.

## Product kill / modify conditions

Modify or kill the current wedge when evidence shows any of the following:

- production quantity is effectively fixed before useful signals arrive;
- operators have no meaningful discretion;
- current workflow already solves the uncertainty at adequate quality;
- no trustworthy service-level outcome can be measured;
- the dominant waste source is unrelated to the proposed decision;
- recommendation latency misses the operational window;
- the economic beneficiary and user have no viable incentive path;
- required data would force unjustified person-level tracking;
- a transparent baseline performs as well as the proposed modeling layer;
- control/acceptance records cannot support prospective verification.

## Legacy branch rule

The historical `role/cs2-product-strategy` branch is now a **reference archive**, not an integration source.

Do not:

- merge it wholesale;
- rebase hundreds of stale commits into current master;
- restore old frontend copies already superseded on master;
- reintroduce claims or schemas that weaken current fail-closed CS1 boundaries.

When a legacy artifact is still valuable, recut the smallest current version from `master` and state which assumptions remain unverified.

## Definition of ready for integration

This recut is merge-ready only if:

1. it is based on current master;
2. it touches only low-conflict CS2 research paths;
3. it introduces no new measured/pilot/customer claims;
4. its machine-readable queue parses;
5. repository policy/evidence checks pass;
6. exact-head CI passes on the PR;
7. the branch is resynced if master moves before merge.
