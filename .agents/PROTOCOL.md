# BOUNCAMPUS Agent Coordination Protocol v1

This protocol is the machine-readable coordination layer for parallel repository agents. `AGENTS.md` remains the authority for repository policy; this file defines how agents claim work, communicate, transfer ownership, and serialize integration.

## Design goals

- No hidden ownership: every accepted task has an explicit owner, lane, branch, scope, and touched paths.
- No shared mutable mega-file: tasks, leases, heartbeats, messages, acknowledgements, and locks use separate files to reduce merge conflicts.
- No silent handoffs: ownership transfer creates a durable message and requires acknowledgement when requested.
- No merge parking lot: the owning workstream agent keeps responsibility through merge and post-merge verification.
- No lost features: the existing feature-preservation and exact-head CI gates remain mandatory.

## Runtime layout

The runtime is repository-native and lives under `.agents/`:

- `config.json` — lanes, TTLs, and protocol constants.
- `tasks/<task-id>.json` — task state, owner, branch, paths, history, and evidence.
- `leases/<task-id>.json` — renewable ownership lease for the task.
- `heartbeats/<agent>.json` — latest liveness record for an agent.
- `messages/<message-id>.json` — immutable inter-agent message.
- `acks/<message-id>/<agent>.json` — acknowledgement record.
- `locks/merge.json` — the single repository Merge Coordinator lock.

The runtime directories are created by `python scripts/agent_bus.py init` or automatically by commands that need them. Runtime records should only be committed when they are intentionally part of a coordination handoff or audit trail; transient local records do not need to be pushed.

## Required lifecycle

`ACTIVE -> READY_FOR_INTEGRATION -> INTEGRATING -> MERGED_VERIFYING -> MERGED_VERIFIED`

`BLOCKED` is allowed only for a hard blocker and is not completion. Ownership remains active while blocked.

An implementation handoff is permitted only while the task is `ACTIVE` or `BLOCKED`. `READY_FOR_INTEGRATION`, `INTEGRATING`, and `MERGED_VERIFYING` work must not be handed to another agent merely to finish the merge.

## Claiming work

Before the first product edit, claim the task and exact path scope:

```bash
python scripts/agent_bus.py claim \
  --task-id campus-map-polish \
  --agent ux-01 \
  --lane frontend-ux \
  --branch agent/frontend-ux/campus-map-polish \
  --scope "Polish map controls and responsive layout" \
  --paths frontend/src/components/Dashboard frontend/src/app
```

The command rejects overlapping active ownership. Parent/child path overlaps count as conflicts.

## Heartbeats and stale work

An active agent renews its lease periodically:

```bash
python scripts/agent_bus.py heartbeat --task-id campus-map-polish --agent ux-01
```

Default task lease TTL is 45 minutes. Merge-lock TTL is 30 minutes. Expired leases are evidence of stale ownership, not automatic permission to overwrite another task. A coordinator must explicitly reassign or resolve the stale owner before conflicting edits begin.

## Agent-to-agent messages

Send durable structured messages instead of relying on chat context:

```bash
python scripts/agent_bus.py send \
  --from-agent ux-01 \
  --to-agent geo-02 \
  --type REQUEST \
  --task-id campus-map-polish \
  --subject "Need canonical South Campus building ids" \
  --body "Please return the exact ids used by campus-directory.ts" \
  --requires-ack
```

Read and acknowledge:

```bash
python scripts/agent_bus.py inbox --agent geo-02 --unread-only
python scripts/agent_bus.py ack --message-id <id> --agent geo-02
```

Allowed message types: `INFO`, `REQUEST`, `DECISION`, `BLOCKER`, `HANDOFF`, `REVIEW`, `ACK`.

A message must contain enough context for another agent to act without reconstructing the sender's private reasoning: task id, concrete request/decision, affected paths or interface when relevant, and the next action.

## Handoff

Use handoff only when the implementation owner genuinely changes before integration:

```bash
python scripts/agent_bus.py handoff \
  --task-id campus-map-polish \
  --from-agent ux-01 \
  --to-agent ux-02 \
  --reason "Original agent unavailable" \
  --next-action "Continue responsive pass; no integration has started"
```

The command changes ownership, renews the task lease, writes the new heartbeat, and creates an acknowledgement-required `HANDOFF` message.

## Blocking

For a real external blocker:

```bash
python scripts/agent_bus.py block \
  --task-id campus-map-polish \
  --agent ux-01 \
  --reason "Required external credential unavailable" \
  --next-action "Resume after repository owner provisions credential"
```

This broadcasts an acknowledgement-required blocker message. `BLOCKED` never means done.

## Integration lock

When branch validation is complete:

```bash
python scripts/agent_bus.py ready --task-id campus-map-polish --agent ux-01 --evidence "npm run build"
python scripts/agent_bus.py lock-acquire --task-id campus-map-polish --agent ux-01
```

Only one merge lock may exist. The lock holder is the temporary Merge Coordinator for its own batch and must keep driving the single integration PR.

After the normal merge commit lands:

```bash
python scripts/agent_bus.py merged --task-id campus-map-polish --agent ux-01 --merge-sha <sha>
python scripts/agent_bus.py verify --task-id campus-map-polish --agent ux-01 --evidence "post-merge CI green"
```

`verify` is the only command that releases the task lease and merge lock and moves the task to `MERGED_VERIFIED`.

## Validation

Every PR and `master` CI run executes:

```bash
python -m py_compile scripts/agent_bus.py
python scripts/agent_bus.py validate
```

Validation checks task states, configured lanes, path ownership overlap, message shape, and consistency between the merge lock and the integrating task.

## Communication rules

1. Prefer `REQUEST` for a dependency and `DECISION` for an interface or architectural choice that other lanes must consume.
2. Use `BLOCKER` only when work genuinely cannot continue; otherwise send a request and switch to an independent task segment.
3. Cross-lane changes require a message before editing another lane's owned path.
4. Acknowledgement-required messages are not complete until the receiver writes an ack record.
5. Never encode secrets, tokens, private credentials, or production personal data in `.agents/messages/**`.
6. The repository is the durable shared memory. Chat is advisory; committed code, tests, protocol records, and CI evidence are authoritative.
