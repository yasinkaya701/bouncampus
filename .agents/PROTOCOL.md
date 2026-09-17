# BOUNCAMPUS Agent Coordination Protocol v1

`AGENTS.md` is the repository policy authority. This document defines the executable coordination and communication protocol used by parallel agents.

## Goals

- Every accepted task has an explicit owner, lane, branch, path scope, state and evidence.
- Parallel agents never silently edit the same path.
- Agent-to-agent requests, decisions, blockers and handoffs are durable and branch-independent.
- Handoffs require acknowledgement; integration ownership cannot be dumped onto another agent.
- There is only one Merge Coordinator lock and at most one integration PR.
- Work is not complete until it exists on verified `master`.

## Architecture

The runtime has two layers.

### 1. Local repository state

`scripts/agent_bus.py` maintains transient machine-readable records under `.agents/`:

- `tasks/<task-id>.json` — task owner, branch, lane, scope, paths, lifecycle and evidence.
- `leases/<task-id>.json` — renewable ownership lease.
- `heartbeats/<agent-id>.json` — liveness record.
- `messages/<message-id>.json` — local cache of structured messages.
- `acks/<message-id>/<agent-id>.json` — acknowledgement record.
- `locks/merge.json` — local Merge Coordinator lock.
- `remote-cache/` — optional cache of remote bus messages.

These directories are ignored by git. They are operational state, not product history.

### 2. Branch-independent remote bus

GitHub Issue **#8** is the durable cross-agent transport. Each message is mirrored as a structured `BOUNCAMPUS_AGENT_BUS_V1` envelope. Agents on separate branches/worktrees can therefore discover dependencies without sharing chat context or mutable branch files.

Remote delivery requires `GITHUB_TOKEN` or `GH_TOKEN`. If remote transport is enabled and no token is available, commands that promise cross-agent delivery fail unless `--offline` is explicitly supplied. Offline mode must never be treated as proof that another agent received a message.

## Required startup

Before editing product code:

```bash
python scripts/agent_bus.py sync --agent <agent-id>
python scripts/agent_bus.py claim \
  --task-id <task-id> \
  --agent <agent-id> \
  --lane <lane> \
  --branch agent/<lane>/<task> \
  --scope "<scope>" \
  --paths <owned-path> [<owned-path> ...]
```

`claim` rejects overlapping active path ownership in the local runtime. Repository agents must also declare the same ownership in `.agents/WORKSTREAMS.md` before the first product edit.

## Lifecycle

The only normal lifecycle is:

`ACTIVE -> READY_FOR_INTEGRATION -> INTEGRATING -> MERGED_VERIFYING -> MERGED_VERIFIED`

`BLOCKED` is allowed only for a real external blocker. It is not completion.

Commands:

```bash
python scripts/agent_bus.py ready --task-id <task> --agent <agent> --evidence "<check>"
python scripts/agent_bus.py lock-acquire --task-id <task> --agent <agent>
python scripts/agent_bus.py merged --task-id <task> --agent <agent> --merge-sha <sha>
python scripts/agent_bus.py verify --task-id <task> --agent <agent> --evidence "<post-merge check>"
```

`verify` is the only normal command that releases the task lease and Merge Coordinator lock.

## Heartbeats and leases

Ownership leases default to 45 minutes. The Merge Coordinator lock defaults to 30 minutes. Agents should heartbeat at least every 15 minutes while actively executing a workstream:

```bash
python scripts/agent_bus.py heartbeat --task-id <task> --agent <agent>
```

An expired lease is evidence of stale ownership, not permission to overwrite it. Reassignment must be explicit.

## Agent-to-agent communication

Allowed message types:

- `INFO` — context another agent may need.
- `REQUEST` — concrete dependency or action request.
- `DECISION` — architectural/interface decision other lanes must consume.
- `BLOCKER` — hard blocker that prevents progress.
- `HANDOFF` — explicit ownership transfer before integration begins.
- `REVIEW` — review request or review finding.
- `ACK` — acknowledgement of a message.

Send a message:

```bash
python scripts/agent_bus.py send \
  --from-agent ux-01 \
  --to-agent geo-02 \
  --type REQUEST \
  --task-id campus-map-polish \
  --subject "Need canonical building ids" \
  --body "Return the exact ids used by campus-directory.ts" \
  --requires-ack
```

Read inbox and acknowledge:

```bash
python scripts/agent_bus.py inbox --agent geo-02 --unread-only
python scripts/agent_bus.py ack --message-id <id> --agent geo-02
```

A message must be independently actionable. Include the task id, exact request/decision, affected path or interface when relevant, and the next action. Never rely on private chain-of-thought or unstated chat context.

## Handoff

Implementation ownership may change only while a task is `ACTIVE` or `BLOCKED`:

```bash
python scripts/agent_bus.py handoff \
  --task-id <task> \
  --from-agent <old> \
  --to-agent <new> \
  --reason "<reason>" \
  --next-action "<next executable action>"
```

The command updates ownership and emits an acknowledgement-required `HANDOFF` message. `READY_FOR_INTEGRATION`, `INTEGRATING` and `MERGED_VERIFYING` work cannot be handed off merely to escape integration responsibility.

## Blocking

```bash
python scripts/agent_bus.py block \
  --task-id <task> \
  --agent <agent> \
  --reason "<hard external blocker>" \
  --next-action "<exact resume action>"
```

The blocker is broadcast through the remote bus and remains owned by the same agent unless explicitly reassigned.

## Retry and acknowledgement semantics

- Messages with `requires_ack=true` remain outstanding until an acknowledgement exists.
- `pending-acks` lists unresolved acknowledgement-required messages.
- `retry` republishes the same logical message with `retry_of=<original-id>`; it does not mutate the original envelope.
- A receiver must not infer delivery merely because a sender created a local message file.
- Remote transport failure is surfaced as an error unless `--offline` is explicitly chosen.

## Merge Coordinator lock

The owning workstream agent becomes the temporary Merge Coordinator for its own batch. The lock is not a separate handoff role.

```bash
python scripts/agent_bus.py lock-acquire --task-id <task> --agent <agent>
python scripts/agent_bus.py lock-renew --task-id <task> --agent <agent>
```

Only the lock holder may own the repository's single integration PR. The same agent resolves conflicts, fixes CI, merges, verifies `master`, then releases ownership through `verify`.

## Validation

CI executes:

```bash
python -m py_compile scripts/agent_bus.py scripts/test_agent_bus.py
python scripts/test_agent_bus.py
python scripts/agent_bus.py validate --offline
python -m json.tool .agents/config.json
```

Validation checks task states, configured lanes, path overlap, message shape, acknowledgement shape and merge-lock consistency.

## Security boundary

Never place secrets, tokens, credentials, personal data, private keys, production cookies or sensitive payloads in `.agents/**` or Issue #8. The bus is coordination metadata only.

## Source of truth hierarchy

1. Merged repository code and tests.
2. `AGENTS.md` policy.
3. `.agents/WORKSTREAMS.md` ownership ledger.
4. Structured agent-bus records and Issue #8 envelopes.
5. Chat messages and informal notes.

If lower layers disagree with higher layers, the higher layer wins.
