# BOUNCAMPUS Autonomous Agent Fabric

This document defines the low-overhead control plane for parallel AI work in BOUNCAMPUS. It extends `AGENTS.md`; it does not replace the repository's single-PR integration discipline or merge-before-exit contract.

## Operating principle

**Autonomous by default; human-gated by exception.**

Agents do not ask a human for routine implementation choices, branch operations, decomposition, testing, reversible refactors, documentation updates, ordinary conflict resolution, or merge execution when repository evidence is sufficient.

A human is required only for one of the explicit gate kinds below. Uncertainty alone is not a human gate: the agent must investigate, test, choose the safest reversible option, or mark the task `BLOCKED` with evidence.

## Control plane

- Durable product/repository truth lives on `master`.
- Work executes on short-lived `agent/<lane>/<task>` branches.
- Shared coordination metadata lives on the long-lived `agent-coordination` branch under `.agents/coordination/tasks/`.
- Each task is one JSON file. Updating an existing task requires the current blob SHA, so competing claims on the same task are serialized by GitHub rather than by a human dispatcher.
- The repository still permits at most one open integration PR. That PR is the integration lock.
- `.agents/WORKSTREAMS.md` remains a human-readable compatibility/history view. New autonomous coordination must not rely on editing that single file for every heartbeat or task claim.

## Task lifecycle

`BACKLOG -> READY -> CLAIMED -> ACTIVE -> READY_FOR_INTEGRATION -> INTEGRATING -> MERGED_VERIFYING -> MERGED_VERIFIED`

Side states:

- `BLOCKED`: hard dependency/infrastructure blocker with exact evidence and next executable action.
- `WAITING_HUMAN`: only when one of the explicit human gate kinds applies.
- `CANCELLED`: intentionally abandoned task with rationale; never equivalent to success.

There is no branch-only `DONE` state.

## Autonomous dispatcher behavior

An orchestrating agent may, without human approval:

1. inspect issues, repository state, CI, and current task files;
2. decompose a goal into independently reviewable tasks;
3. mark tasks `READY` when hard dependencies are satisfied;
4. choose a lane and priority;
5. identify non-overlapping `touched_paths`;
6. claim a `READY` task atomically;
7. create its work branch;
8. execute, test, self-review, and update task state;
9. reclaim a stale lease when the lease TTL has expired, no task PR is open, and repository evidence does not show fresh work;
10. acquire the integration slot when no other PR is open;
11. update from `master`, resolve conflicts, drive CI green, merge, and verify `master`;
12. release the lease only after `MERGED_VERIFIED`.

Agents should prefer multiple narrow, non-overlapping tasks over one broad task that serializes unrelated work.

## Claim and lease protocol

Task files follow `.agents/TASK_TEMPLATE.json` and live on `agent-coordination`.

To claim a task:

1. read the current task file and blob SHA from `agent-coordination`;
2. require state `READY` (or a reclaimable stale state);
3. verify every `depends_on` task is `MERGED_VERIFIED`;
4. verify `touched_paths` do not overlap an active task;
5. set `owner_agent`, `branch`, state `CLAIMED`, `lease.claimed_at`, and `lease.heartbeat_at`;
6. update the task file using the blob SHA precondition;
7. if the update loses a race, do not retry blindly; choose another `READY` task or reread the task.

A material commit or meaningful validation checkpoint should refresh `lease.heartbeat_at`. The default TTL is defined in `.agents/fabric.json`.

A stale lease can be reclaimed autonomously only when all are true:

- TTL expired;
- state is not `INTEGRATING` or `MERGED_VERIFYING`;
- no open PR exists for that task branch;
- no newer branch commit or other repository evidence shows active execution;
- the reclaim is recorded in the task notes.

## File ownership and conflict prevention

`touched_paths` is an execution contract, not a rough guess.

- Two active tasks may not own overlapping product paths.
- Parent/child path ownership counts as overlap (`frontend/src` conflicts with `frontend/src/app/page.tsx`).
- Coordination metadata paths are not product ownership.
- If a newly discovered necessary path overlaps another active task, the agent must either wait/re-scope or combine the tasks through explicit coordination; it must not silently edit the overlapping path.
- Integration remains serialized even when implementation is parallel.

## Human gates

Allowed human gate kinds are intentionally narrow.

### `EVIDENCE_ATTESTATION`

Use only when a human must attest that real-world evidence is genuine or correctly represented, for example:

- interview notes/quotes;
- private institutional facts supplied by a person;
- application claims that require human factual sign-off.

Agents may summarize evidence but may not self-attest that an interview happened or that a quote is genuine.

### `IRREVERSIBLE_ACTION`

Use for destructive or difficult-to-reverse external actions, including deleting production data, rotating/revoking credentials, changing repository/account administration, or equivalent irreversible changes.

Normal git commits, branches, PRs, merges, and reversible code changes are **not** irreversible actions.

### `PHYSICAL_SAFETY`

Use before real-world hardware energization, actuator movement, mains/high-current work, field deployment, or another action where a software decision can create physical risk. Simulation, CAD, firmware development, and non-energized review remain autonomous.

### `EXTERNAL_COMMITMENT`

Use before actions that bind the team externally: final application submission, purchase/payment, contract/legal acceptance, sending a consequential external message, or committing to a pilot/date on behalf of the team.

Drafting and preparing these artifacts remains autonomous.

### `PRODUCT_DIRECTION`

Use only for a material strategic pivot that changes the agreed beachhead, primary problem, or core product direction when available evidence supports multiple materially different choices. Routine feature prioritization, architecture, implementation details, and reversible experiments remain autonomous.

## `WAITING_HUMAN` standard

A task may enter `WAITING_HUMAN` only if:

- `human_gate.kind` is not `NONE`;
- `human_gate.status` is `PENDING`;
- `human_gate.question` asks for one concrete decision;
- the agent has already completed all work that does not depend on that decision;
- the task notes include the recommended option and evidence.

Never use `WAITING_HUMAN` as a substitute for investigation or engineering judgment.

## Blockers

`BLOCKED` is reserved for blockers the agent cannot resolve with available repository/tool access. The `blocker` field must state:

- exact failed dependency/action;
- evidence (error, missing permission, unavailable service, etc.);
- work already attempted;
- next executable action and who/what can perform it.

If an alternate safe route exists, the task is not blocked.

## Integration

Implementation can be parallel; integration is serialized.

- At most one integration PR may be open.
- The task that owns the integration PR is `INTEGRATING`.
- Other agents continue non-overlapping work while the slot is occupied.
- The integration owner updates from latest `master`, runs feature preservation and required validators, and drives exact-head CI green.
- Use a normal merge commit.
- After merge, move to `MERGED_VERIFYING`, verify the resulting `master`, then move to `MERGED_VERIFIED`.
- A task may not release its lease before `MERGED_VERIFIED`.

## Agent-to-agent communication

Prefer repository-visible state over chat messages.

Agents communicate through:

- task JSON state and notes on `agent-coordination`;
- dependency IDs;
- branch commits;
- issue/PR discussion when relevant;
- explicit blocker evidence.

Do not require synchronous human relay between agents.

## Minimal agent roles

The fabric needs only four logical roles; one model/session may perform more than one when paths do not conflict:

- **Dispatcher**: decomposes goals, maintains dependencies, exposes `READY` work.
- **Workstream Agent**: claims and executes one task end-to-end.
- **Verifier / Red Team**: independently checks high-risk diffs, tests, evidence boundaries, or acceptance criteria when useful.
- **Integration Owner**: the workstream agent currently holding the single PR slot and responsible for merge/post-merge verification.

No permanent hierarchy or large agent framework is required.

## Mechanical checks

Run:

```bash
python scripts/agent_fabric_check.py
python scripts/test_agent_fabric_check.py
```

The validator checks the fabric configuration, task schema, dependency graph, active path ownership, lease fields, human gates, and terminal integration evidence. The normal CI pipeline must run it before integration.
