# Multi-Human Multi-Agent Fabric v2 Design

## Status

Revised design after user clarification. This specification replaces the earlier multi-contributor-per-task model.

## Goal

Support a KREATE team where each human owns exactly one primary workstream, while that workstream can fan out to an arbitrary number of autonomous agents — 5, 20, 50, or more — without requiring the human to coordinate routine engineering work.

The system must preserve evidence integrity, path ownership, merge safety, KREATE claim discipline, and explicit critical human gates.

## Core model

### One human = one parent workstream

Each human teammate owns exactly one persistent parent workstream:

- IE — Customer Discovery & Market Lead
- EE — Physical Systems & Measurement Lead
- CS1 — Decision Intelligence Lead
- CS2 — Product Strategy, Evidence Synthesis & Application Lead

A human does not own multiple concurrent parent tasks.

The parent workstream is the accountability boundary, not the unit of every implementation action.

### Many agents per parent workstream

Each parent workstream may create any number of child agent subtasks.

Example:

```text
CS1 parent workstream
├── agent:baseline
├── agent:data-quality
├── agent:uncertainty
├── agent:evaluation
├── agent:red-team
└── ... up to 50+ concurrent agents when dependencies and path ownership allow it
```

Agent count is not hard-coded. Effective concurrency is limited only by:

- dependency readiness;
- non-overlapping path ownership;
- CI/runner capacity;
- branch/repository limits;
- parent-workstream integration throughput.

The fabric must not contain an arbitrary "max agents = 4/8/16" policy.

## Human involvement

The human owner is accountable for the parent workstream but is not the routine dispatcher.

Agents may autonomously:

- decompose the parent goal into child subtasks;
- research;
- implement code;
- run experiments;
- write drafts;
- test;
- review other agents;
- resolve reversible technical choices;
- merge child work into the parent workstream branch;
- prepare integration to master;
- continue to the next child subtask.

Humans are required only for the five critical gate kinds:

1. `EVIDENCE_ATTESTATION`
2. `IRREVERSIBLE_ACTION`
3. `PHYSICAL_SAFETY`
4. `EXTERNAL_COMMITMENT`
5. `PRODUCT_DIRECTION`

`WAITING_HUMAN` is invalid for routine technical, research, drafting, prioritization, or coordination decisions.

## Hierarchy

Fabric v2 has only two execution levels beneath `master`.

### Level 1 — Parent human workstream

Each human owns one parent workstream object.

The parent records:

- `human_owner`
- `role`
- `objective`
- `parent_branch`
- current critical human gate, if any
- child subtask IDs
- parent integration state
- parent evidence / output summary

Suggested parent IDs:

- `HUMAN-IE`
- `HUMAN-EE`
- `HUMAN-CS1`
- `HUMAN-CS2`

### Level 2 — Agent child subtasks

Each child subtask is independently leased to one agent.

A child subtask records:

- `id`
- `parent_id`
- `owner_agent`
- `state`
- `depends_on`
- `touched_paths`
- `acceptance_criteria`
- `validation_commands`
- `produces`
- `consumes`
- lease/heartbeat
- child branch
- result/evidence

A child agent may not change `human_owner` or parent product direction.

No deeper recursive hierarchy is required. If an agent needs more parallelism, it asks the parent dispatcher to create more sibling child subtasks rather than spawning unbounded nested agent trees.

## Branch model

### Parent branches

There are at most four active parent workstream branches:

```text
work/ie
work/ee
work/cs1
work/cs2
```

Each is owned by its human workstream and may receive many child-agent merges.

These branches are integration surfaces for the human workstream, not private developer branches.

### Child agent branches

Each child agent works on a short-lived branch:

```text
agent/<role>/<child-task-slug>
```

Examples:

```text
agent/cs1/baseline-model
agent/cs1/uncertainty-eval
agent/ee/load-cell-repeatability
agent/ie/operator-interview-guide
agent/cs2-application/red-team-problem-claim
```

A child branch never merges directly to `master`.

It integrates first into its parent workstream branch.

## Child integration inside a parent workstream

Each parent workstream has one temporary parent integrator lease.

Many child agents may execute in parallel, but updates to the same parent branch are serialized.

Flow:

```text
50 child agents
      ↓
independent child branches
      ↓
child validation
      ↓
READY_FOR_PARENT_INTEGRATION queue
      ↓
one parent integrator lease
      ↓
merge child branch into work/<role>
      ↓
parent validation
```

The parent integrator is normally an autonomous agent, not the human.

A child is complete only after its validated head is contained in the parent branch and its result is recorded.

## Path ownership at child scale

`touched_paths` is the hard concurrency contract.

Two active child tasks under the same or different parent workstreams may not own overlapping paths.

Parent/child overlap counts as conflict.

Examples:

```text
agent A owns backend/app/decision/
agent B owns hardware/
→ allowed

agent A owns backend/app/
agent B owns backend/app/decision/model.py
→ rejected
```

With 50 agents, this rule matters more than the raw number of agents.

Read-only consumption does not require path ownership.

If work is conceptually parallel but requires edits to one shared file, split the shared-file edit into one dedicated integration child task instead of allowing many agents to touch it.

## Agent-to-agent communication

Do not build a chat bus.

Agents communicate through repository-visible artifacts:

- child task state;
- `depends_on`;
- `produces`;
- `consumes`;
- evidence IDs;
- commits;
- validation results;
- blocker notes.

Example:

```text
IE child produces:
E-INT-012
H-003-update

CS1 child consumes:
E-INT-012
H-003-update
```

The consuming task remains blocked until required producer artifacts exist.

## Parent dispatcher

Each parent workstream may have an autonomous dispatcher agent.

The dispatcher:

1. reads the parent objective;
2. finds gaps or ready child work;
3. creates bounded child subtasks;
4. calculates dependencies;
5. assigns `touched_paths`;
6. exposes non-conflicting children as READY;
7. allows available agents to claim them;
8. monitors stale leases;
9. queues completed children for parent integration;
10. creates follow-up child tasks when evidence or tests reveal new work.

The dispatcher does not need human permission for routine decomposition.

It must stop only when a new child task would require a critical human gate or materially change parent product direction.

## Scale behavior: 50+ agents

The design must remain valid with 50 or more child agents.

Therefore:

- child state must be stored in separate files, not one shared giant JSON/Markdown ledger;
- heartbeat updates must touch only the child task file;
- child agents must not all edit the parent task file for routine progress;
- parent summary is updated only at meaningful integration checkpoints;
- conflict detection must scan active child `touched_paths` mechanically;
- agent count must not determine merge safety;
- CI should validate changed scopes where practical, while exact parent/master integration still runs full required gates.

Suggested metadata layout:

```text
.agents/coordination/
├── parents/
│   ├── HUMAN-IE.json
│   ├── HUMAN-EE.json
│   ├── HUMAN-CS1.json
│   └── HUMAN-CS2.json
└── subtasks/
    ├── HUMAN-IE/
    │   └── *.json
    ├── HUMAN-EE/
    │   └── *.json
    ├── HUMAN-CS1/
    │   └── *.json
    └── HUMAN-CS2/
        └── *.json
```

This avoids 50 agents contending on one coordination file.

## Parent workstream integration to master

The repository may have up to four parent workstream PRs open concurrently, normally one per human workstream.

Rules:

- parent PRs may stay draft while child agents continue integrating into the parent branch;
- at most one parent PR may be non-draft / hold the master integration slot;
- parent branch must sync current `master` before acquiring the slot;
- fresh exact-head CI is mandatory after sync;
- only the integration-slot parent PR can merge;
- use a normal merge commit;
- post-merge verification and `agent_exit_gate.py` remain mandatory;
- other parent branches then sync the new `master` before their own integration.

This gives four-human parallel work without four simultaneous master merges.

## Integration queue

Parent workstreams ready for master integration are ordered by:

1. P0/P1/P2 priority;
2. dependency-unblocking value;
3. KREATE deadline/rubric impact;
4. oldest ready timestamp;
5. stable parent ID tie-break.

Critical recovery may preempt only with explicit P0 rationale.

## Human workstream lifecycle

A parent workstream is persistent across many child subtasks and may produce multiple master integration batches before October 8.

Therefore parent lifecycle is not identical to a leaf child lifecycle.

Parent states:

```text
ACTIVE
WAITING_HUMAN
READY_FOR_MASTER_INTEGRATION
INTEGRATING_MASTER
BLOCKED
COMPLETE
```

A parent remains `ACTIVE` after one integration batch if its role objective still has outstanding work.

`COMPLETE` is reserved for completion of the human's assigned KREATE workstream objective, not a single merge.

Child states retain the strict implementation lifecycle:

```text
BACKLOG
READY
CLAIMED
ACTIVE
BLOCKED
WAITING_HUMAN
READY_FOR_PARENT_INTEGRATION
INTEGRATING_PARENT
PARENT_VERIFIED
CANCELLED
```

A child may not report success before `PARENT_VERIFIED`.

## Ownership rules

### Human owner

Each parent has exactly one `human_owner`.

A human cannot simultaneously own two KREATE parent workstreams under this model.

Changing the human owner is an explicit administrative transfer, not normal agent behavior.

### Agent owner

Each active child has exactly one `owner_agent` lease at a time.

There may be arbitrarily many active child owners across the four parents when paths and dependencies permit.

### Reviewer agents

Independent verifier/red-team agents may review another child without becoming its owner.

Reviewer agents do not obtain write ownership of the reviewed paths unless a new fix child task is created.

## Evidence boundary

Multi-agent scale does not weaken KREATE evidence rules.

Agents may:

- research public sources;
- draft interview questions;
- summarize provided interview notes;
- classify hypotheses;
- prepare application prose;
- run technical tests.

Agents may not self-attest:

- that an interview happened;
- exact quotes from a person;
- private institutional facts;
- measured pilot outcomes;
- physical hardware performance not actually tested;
- final application claim sign-off where human review is required.

Those remain `EVIDENCE_ATTESTATION` gates.

## CI and validator requirements

Mechanical validation must test at least:

1. exactly one parent workstream per human owner;
2. four KREATE role parents maximum;
3. arbitrary number of child agent subtasks;
4. every child references one valid parent;
5. every active child has one lease owner;
6. no active path overlaps across all parents;
7. dependencies form no cycles;
8. required `consumes` artifacts exist before dependent execution/integration;
9. child branch matches parent role/task metadata;
10. a child cannot merge directly to `master`;
11. child completion requires parent containment evidence;
12. max four open parent PRs;
13. max one non-draft parent integration PR;
14. parent integration requires latest master and fresh exact-head CI;
15. `WAITING_HUMAN` requires one of the five critical gate kinds;
16. PMR/evidence gates cannot be agent-self-approved;
17. post-merge master provenance remains enforced.

## CLI requirements

The existing agent task CLI should evolve toward parent/child operations such as:

```text
parent list
parent status
subtask next --parent HUMAN-CS1
subtask create --parent HUMAN-CS1
subtask claim
subtask heartbeat
subtask ready
subtask integrate-parent
subtask verify-parent
queue parent
queue master
human-gate request
human-gate resolve
```

The CLI should update only the smallest relevant coordination file and use blob-SHA preconditions for race safety.

## Migration

1. Let the currently open task-CLI PR finish under current fabric policy.
2. Add parent-workstream schema and separate child subtask storage.
3. Create the four parent KREATE workstream objects.
4. Add high-concurrency child validation and tests, including a fixture with at least 50 concurrent non-overlapping agents.
5. Add parent branch integration semantics.
6. Replace single-open-PR policy with up to four parent PRs and one master integration slot.
7. Remove routine IE/CS2 post-work user checkpoint behavior; keep only five critical human gates.
8. Extend CLI for parent/child dispatch and integration.
9. Update CI, issue/PR templates, and docs.
10. Run exact-head CI, normal merge, and post-merge verification.

## Acceptance criteria

Fabric v2 is complete when mechanically demonstrated that:

1. four humans can each hold exactly one parent workstream;
2. one parent can manage at least 50 simultaneous child agent tasks in test fixtures;
3. 50 non-overlapping child tasks are accepted by the validator;
4. one overlapping child path among those 50 is rejected;
5. child agents can finish without routine human interaction;
6. child results integrate into the correct parent branch before master;
7. parent branch updates are serialized while child execution remains parallel;
8. up to four parent PRs may exist concurrently as drafts;
9. a second non-draft master-integration PR is rejected;
10. master sync invalidates stale merge readiness and requires fresh exact-head CI;
11. the human is interrupted only for the five critical gate kinds;
12. real PMR/evidence cannot be self-attested by agents;
13. application claim-review rules remain intact;
14. existing product behavior is unchanged by the fabric itself;
15. normal merge commit, post-merge audit, and exit verification remain mandatory.

## Design decision summary

Use a hierarchical fan-out model:

```text
4 human-owned parent workstreams
        ↓
unbounded child-agent pool (50+ supported)
        ↓
serialized child integration into each parent branch
        ↓
up to 4 parent PRs
        ↓
one serialized master integration slot
        ↓
master
```

The number of agents is deliberately not the control boundary. The control boundaries are task dependencies, path leases, parent integration, evidence gates, and exact-head CI.
