# BOUNCAMPUS Autonomous Agent Fabric v2

This document defines the low-overhead control plane for **four human-owned parent workstreams with arbitrarily many autonomous child agents**. It extends `AGENTS.md` and the KREATE evidence system.

## Operating principle

**One human = one parent workstream. Many agents may execute beneath that parent. Humans intervene only at five critical gates.**

The fabric has no configured child-agent count limit. Effective concurrency is constrained by dependencies, `touched_paths`, repository/runner capacity, and parent integration throughput.

## Control plane

- Durable repository/product truth: `master`
- Parent work branches:
  - `work/ie/<slug>`
  - `work/ee/<slug>`
  - `work/cs1/<slug>`
  - `work/cs2/<slug>`
- Child implementation branches: `agent/<lane>/<task>`
- Coordination branch: `agent-coordination`
- Child task store: `.agents/coordination/tasks/`
- Parent store: `.agents/coordination/parents/`

Exactly one non-cancelled parent is allowed for each KREATE role: IE, EE, CS1, CS2. The parent is the accountability and master-integration boundary. Child tasks are the scalable execution units.

## Parent / child hierarchy

### Parent workstream

A parent record contains:

- human owner (`human:<identity>`);
- role;
- objective and priority;
- parent branch;
- critical human gate, if any;
- parent integration evidence.

The human owner is not required to dispatch ordinary work. Agents may decompose and spawn bounded child tasks autonomously while staying inside the parent objective.

### Child task

A schema-v2 child record contains:

- `parent_id`;
- one leased `owner_agent`;
- dependencies;
- `touched_paths`;
- acceptance criteria and validation commands;
- `produces` / `consumes` artifact contracts;
- `required_for_parent` (default true);
- child-to-parent integration evidence.

Schema-v1 tasks remain readable during migration. Verified history does not need to be rewritten.

## Scale model

The system must support 50+ siblings under one parent when their work is independent.

```text
HUMAN-CS1
├── TASK-CS1-001 -> agent:model-a
├── TASK-CS1-002 -> agent:model-b
├── TASK-CS1-003 -> agent:data-quality
├── ...
└── TASK-CS1-050 -> agent:red-team-50
```

There is intentionally no `max_agents` field. A new child is admitted based on contracts, not count.

## Child claim and lease

To claim a child:

1. parent exists and is not cancelled;
2. child is `READY`;
3. hard dependencies are `MERGED_VERIFIED`;
4. its `touched_paths` do not overlap an active child;
5. no pending/rejected human gate blocks the child;
6. the agent records branch, claim timestamp, heartbeat, and lease owner.

Material commits or validation checkpoints refresh the heartbeat. Stale leases may be reclaimed under the existing evidence rules; a human is not required merely because an agent disappeared.

## File ownership

`touched_paths` is the hard concurrency contract.

- Active children may not overlap paths, even across different parents.
- Parent/child directory ownership counts as overlap.
- READY tasks may coexist until claim; the claim that would create an active collision is rejected and rolled back.
- Read-only consumption does not create path ownership.
- Coordination metadata is not product ownership.

This is the principal safety mechanism that allows dozens of agents without merge chaos.

## Child integration: fan-in to parent only

Child branches never integrate directly to `master`.

Lifecycle:

```text
READY -> CLAIMED -> ACTIVE -> READY_FOR_INTEGRATION
      -> INTEGRATING(parent branch) -> MERGED_VERIFIED(parent-contained)
```

For a v2 child:

- generic legacy `INTEGRATING` / `MERGED_VERIFYING` / `MERGED_VERIFIED` transitions are forbidden;
- `integrate-child` must target the exact owning parent branch;
- `master` is always an invalid child target;
- `verify-child` requires validated child head + parent integrated commit evidence.

A child `MERGED_VERIFIED` means **verified inside the parent branch**, not yet on final `master`.

## Fan-out / fan-in

A parent may fan out from an explicit list of bounded child specifications. Agents may generate those child specifications when the decomposition is mechanically inside the accepted parent objective; they may not use fan-out to invent a product pivot.

Parent readiness is computed from coordination state:

- at least one child exists;
- every `required_for_parent=true` child is `MERGED_VERIFIED` into the parent;
- optional children do not block parent readiness;
- unresolved hard dependencies or critical human gates still block their own required children.

No parent is declared ready merely because many child branches exist.

## Artifact contracts

`produces` and `consumes` are repository-visible handoff contracts. Use them instead of synchronous human relay when one child/parent creates evidence or an artifact another worker needs.

Examples:

- IE child produces `E-INT-012`;
- CS1 child consumes `E-INT-012`;
- EE child produces `TECH_TEST-scale-repeatability-v1`;
- CS2 child consumes that test artifact for a defensible draft.

External human-attested evidence can be consumed without being produced by an agent task; authenticity remains governed by the KREATE evidence system.

## Human gates

The only valid human gates are:

- `EVIDENCE_ATTESTATION`
- `IRREVERSIBLE_ACTION`
- `PHYSICAL_SAFETY`
- `EXTERNAL_COMMITMENT`
- `PRODUCT_DIRECTION`

`WAITING_HUMAN` requires one of those five kinds, `PENDING` status, and one concrete question. Routine review, architecture, prioritization, model choice, drafting, branch operations, merge conflict resolution, or uncertainty are not human gates.

All four roles continue autonomously outside these gates.

## Parent integration queue

Only parent workstreams enter the `master` integration queue.

Queue order is deterministic:

1. priority: P0, then P1, then P2;
2. greater dependency-unblocking value;
3. oldest `ready_for_integration_at`;
4. parent ID tie-break.

A P0 recovery can therefore preempt lower-priority normal work without an ad-hoc human dispatcher.

## Parallel parent PRs, serialized master merge

Up to four parent PRs may be open concurrently, normally one per human parent.

- At most one parent PR may be non-draft / hold the master integration slot.
- Other parent PRs remain draft and may run advisory CI/review.
- The integration-slot PR must include current `master` and rerun fresh exact-head CI.
- CI from before another `master` merge is not merge evidence.
- Only the integration-slot parent may merge.
- Merge method remains a normal merge commit.
- Post-merge verification and `agent_exit_gate.py` remain mandatory.

This separates **review parallelism** from **merge serialization**.

## Parent master integration

Before acquiring the slot:

1. parent is `READY_FOR_INTEGRATION`;
2. required children are verified into the parent;
3. the parent is first in the deterministic queue;
4. no other parent is `INTEGRATING` or `MERGED_VERIFYING`;
5. current master SHA is recorded;
6. exact parent head to validate is recorded.

After merge:

1. record PR, validated head, merge SHA, and post-merge verification time;
2. verify merged-PR provenance and normal merge semantics;
3. verify parent head containment in `master`;
4. run repository/KREATE/feature/frontend/data checks;
5. run `agent_exit_gate.py`;
6. only then mark parent integration `MERGED_VERIFIED`.

## Agent-to-agent communication

Prefer durable repository-visible state:

- parent/child JSON;
- dependency IDs;
- `produces` / `consumes`;
- branch/PR references;
- blocker evidence;
- integration notes.

Do not create a chat bus or require a human to relay messages among agents.

## Direct-master-push recovery

Direct pushes remain policy violations. Preserve the existing incident procedure: create a P0 recovery work package, route current state through a normal integration PR, validate exact head, merge normally, verify `master`, and retain an audit trail.

## Mechanical commands

```bash
python scripts/test_agent_fabric_check.py
python scripts/test_agent_task.py
python scripts/agent_fabric_check.py
python scripts/agent_task.py summary
python scripts/agent_task.py queue
```

The test suite must include a fixture with at least **50 simultaneous non-conflicting child agents** and must still reject active path collisions.
