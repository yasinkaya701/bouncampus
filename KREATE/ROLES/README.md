# KREATE Role Operating Model

BOUNCAMPUS uses **four persistent human-owned parent workstreams** with many autonomous child agents beneath each parent.

## Four humans, four parent workstreams

| Parent | Human role | Core accountability |
| --- | --- | --- |
| `HUMAN-IE` | Customer Discovery & Market Lead | problem/customer evidence, PMR, beachhead/persona testing |
| `HUMAN-EE` | Physical Systems & Measurement Lead | measurement strategy, hardware feasibility, calibration, physical evidence |
| `HUMAN-CS1` | Decision Intelligence Lead | decision logic, data/model baselines, uncertainty, evaluation |
| `HUMAN-CS2` | Product Strategy, Evidence Synthesis & Application Lead | product synthesis, application claims, rubric closure, red-team |

Each human owns exactly one parent workstream. The parent persists across multiple integration batches; it is not recreated after every task.

Detailed role briefs:

- [`01_IE_CUSTOMER_DISCOVERY_MARKET_LEAD.md`](01_IE_CUSTOMER_DISCOVERY_MARKET_LEAD.md)
- [`02_EE_PHYSICAL_SYSTEMS_MEASUREMENT_LEAD.md`](02_EE_PHYSICAL_SYSTEMS_MEASUREMENT_LEAD.md)
- [`03_CS1_DECISION_INTELLIGENCE_LEAD.md`](03_CS1_DECISION_INTELLIGENCE_LEAD.md)
- [`04_CS2_PRODUCT_STRATEGY_EVIDENCE_APPLICATION_LEAD.md`](04_CS2_PRODUCT_STRATEGY_EVIDENCE_APPLICATION_LEAD.md)

## Many agents per human parent

A parent may create as many bounded child-agent tasks as useful. There is no fixed 4/8/16-agent ceiling.

Example:

```text
HUMAN-CS1
├── baseline agent
├── data-quality agent
├── uncertainty agent
├── heuristic-vs-ML agent
├── evaluation agent
├── red-team agent
└── ... 50+ children when dependencies and path ownership allow it
```

Child agents are admitted by contracts, not by count:

- hard dependencies must be ready;
- active `touched_paths` may not overlap;
- in-fabric produced artifacts must exist before consumers claim work;
- each child has one lease owner;
- every child has acceptance criteria and validation commands;
- child work integrates into the owning parent branch, never directly into `master`.

## Branch topology

```text
agent/<lane>/<child-task>
        ↓ verified fan-in
work/<role>/<parent>
        ↓ exact-head integration
master
```

Parent branch families:

- IE: `work/ie/<slug>`
- EE: `work/ee/<slug>`
- CS1: `work/cs1/<slug>`
- CS2: `work/cs2/<slug>`

Up to four parent/master PRs may exist concurrently, normally as drafts. At most one may be non-draft and hold the master integration slot.

## Humans are not routine dispatchers

All four roles continue autonomously through routine research, decomposition, coding, testing, analysis, drafting, prioritization, conflict resolution, and merge work.

There is no longer an IE/CS2 post-task permission checkpoint.

Human involvement is required only for:

1. `EVIDENCE_ATTESTATION`
2. `IRREVERSIBLE_ACTION`
3. `PHYSICAL_SAFETY`
4. `EXTERNAL_COMMITMENT`
5. `PRODUCT_DIRECTION`

See [`USER_DECISION_CHECKPOINT_PROTOCOL.md`](USER_DECISION_CHECKPOINT_PROTOCOL.md).

## Shared PMR ownership

The interview target remains a team responsibility. Human teammates conduct or attest real-world interviews; agents may help prepare interview guides, synthesize notes, classify evidence, identify contradictions, and update assumption/claim ledgers.

Agents must never self-attest that an interview occurred or invent a quote/customer.

Use:

- [`../PMR/INTERVIEW_TEMPLATE.md`](../PMR/INTERVIEW_TEMPLATE.md)
- [`../PMR/INTERVIEW_TRACKER.md`](../PMR/INTERVIEW_TRACKER.md)
- [`../EVIDENCE.md`](../EVIDENCE.md)
- [`../ASSUMPTIONS.md`](../ASSUMPTIONS.md)
- [`../DECISIONS.md`](../DECISIONS.md)

## Artifact handoffs instead of chat relay

Cross-role collaboration should be repository-visible.

A child may declare:

- `produces`: evidence/artifact IDs it creates;
- `consumes`: evidence/artifact IDs it requires.

Examples:

```text
IE child       produces E-INT-012
CS1 child      consumes E-INT-012
EE child       produces TECH_TEST-scale-repeatability-v1
CS2 child      consumes both when drafting a claim
```

If an artifact has an in-fabric producer, consumers wait for verified production. External human evidence remains governed by the KREATE evidence system rather than being fabricated as an agent output.

## Parent integration batches

Parent workstreams are long-lived. A verified batch:

1. contains one or more new verified child outputs;
2. syncs current `master`;
3. passes exact-head CI;
4. merges normally to `master`;
5. passes post-merge verification;
6. records PR/base/head/merge/child IDs in `integration_history`;
7. returns the parent to `ACTIVE` for the next wave.

Previously integrated children cannot be promoted again as a new empty batch.

## Evidence boundary

Role autonomy does not weaken KREATE evidence rules.

Application-relevant factual claims require traceable evidence. Real-world interviews, quotes, pilot measurements, achieved savings, model accuracy, and hardware performance may not be invented or upgraded beyond their real evidence class.

## Daily human experience

Humans should receive concise status rather than constant permission requests:

- **Completed**
- **Evidence / result**
- **What changed**
- **Next autonomous action**

Only add **Decision needed** when one of the five critical gates is actually pending.

## Primary references

- Repository fabric: [`../../.agents/FABRIC.md`](../../.agents/FABRIC.md)
- Repository working policy: [`../../AGENTS.md`](../../AGENTS.md)
- Human-gate protocol: [`USER_DECISION_CHECKPOINT_PROTOCOL.md`](USER_DECISION_CHECKPOINT_PROTOCOL.md)
- Hardware execution: [`../HARDWARE/HARDWARE_AGENT_PLAYBOOK.md`](../HARDWARE/HARDWARE_AGENT_PLAYBOOK.md)
- Application rubric: [`../APPLICATION_RUBRIC.md`](../APPLICATION_RUBRIC.md)
