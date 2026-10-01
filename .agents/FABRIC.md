# BOUNCAMPUS Autonomous Agent Fabric

This document defines the control plane for parallel AI/human work. It extends `AGENTS.md`.

## Operating principle

**Autonomous by default; parallel by role; verified on `master`.**

Implementation and review can happen concurrently. Final product truth remains serialized by the requirement that every `master` integration PR contains the latest `master` and passes exact-head CI.

There are five execution roles but still four human team members. Execution-role count and human/PMR count are separate concepts.

## Control plane

- Durable product truth: `master`
- Role integration branches:
  - `role/ie-customer-discovery`
  - `role/ee-physical-systems`
  - `role/ehb-embedded-integration`
  - `role/cs1-decision-intelligence`
  - `role/cs2-product-strategy`
- Short-lived implementation branches: `agent/<lane>/<task>`
- Coordination metadata branch: `agent-coordination`
- Task store: `.agents/coordination/tasks/`

Task JSON remains the authority for ownership, dependencies, path claims, leases, human gates, and final integration evidence.

## Role boundaries relevant to the fabric

### EE

Owns measurement architecture, measurement-method/sensor choice, calibration, uncertainty, measurement semantics, and field/pilot validity.

### EHB

Owns embedded electronics, PCB, firmware, communications, controller-side power/interface implementation, bring-up, device protocol, buffering/recovery, and HW↔SW integration.

### Shared EE ↔ EHB

System-level hardware verification and the EE↔EHB interface contract are shared. Any task changing voltage/current, pinout, sampling, calibration persistence, protocol, packet schema, quality flags, power budget, fault states, or validation method must identify both roles as impacted and receive dual review.

## Parallel PR model

The repository-wide single-PR lock does not exist.

Two PR classes are expected:

### Feature PR

```text
agent/<lane>/<task> -> role/<role>
```

Feature PRs allow each role to integrate independently. Up to 3 may be open against a role branch at once.

Recommended EHB lanes:

```text
agent/ehb-hardware/<task>
agent/ehb-firmware/<task>
agent/ehb-comms/<task>
agent/ehb-integration/<task>
agent/ehb-verification/<task>
```

### Role integration PR

```text
role/<role> -> master
```

Each role may have at most one open integration PR to `master` at a time. Different roles may have integration PRs open concurrently.

A `master` PR is mergeable only if it contains the current `master` base SHA. After any `master` merge, other open role PRs must sync and revalidate before merging.

Repository-wide policy/bootstrap changes may use `agent/quality-release/<task> -> master`.

## Task lifecycle

`BACKLOG -> READY -> CLAIMED -> ACTIVE -> READY_FOR_INTEGRATION -> INTEGRATING -> MERGED_VERIFYING -> MERGED_VERIFIED`

Side states:

- `BLOCKED`
- `WAITING_HUMAN`
- `CANCELLED`

There is no branch-only `DONE` state.

A feature PR merged into a role branch does not make a task terminal. The task remains non-terminal until its commits reach verified `master`.

## Claim and lease protocol

To claim a task:

1. read the task and current blob SHA from `agent-coordination`;
2. require `READY` or satisfy stale-reclaim rules;
3. require all hard dependencies to be `MERGED_VERIFIED`;
4. verify declared `touched_paths` do not overlap another active task;
5. set owner, feature branch, claim timestamp, heartbeat, and state;
6. update using the current blob SHA precondition;
7. create the feature branch from the correct role branch.

A material commit or meaningful validation checkpoint should refresh the heartbeat.

A stale lease may be reclaimed only when TTL expired, the task is not actively integrating/verifying, no repository evidence shows fresh execution, and the reclaim is recorded.

## File ownership

`touched_paths` is an execution contract.

- Two active tasks may not own overlapping product paths.
- Parent/child paths count as overlap.
- Coordination metadata is not product ownership.
- If a new required path conflicts with another active owner, re-scope or coordinate explicitly.
- Shared/high-conflict files require the broad merge checklist in `AGENTS.md`.

Parallel PRs do not weaken path ownership.

For EE/EHB parallel work, a stable interface contract is the prerequisite for independent path ownership. If the interface is still changing, define it first instead of letting both roles diverge silently.

## Human gates

Allowed human gates:

- `EVIDENCE_ATTESTATION`
- `IRREVERSIBLE_ACTION`
- `PHYSICAL_SAFETY`
- `EXTERNAL_COMMITMENT`
- `PRODUCT_DIRECTION`

Normal engineering decisions, branches, PRs, tests, conflict resolution, reversible changes, firmware design, circuit design, and technical architecture choices are autonomous.

`WAITING_HUMAN` is valid only when a real gate is pending, one concrete question is recorded, and independent work is already complete.

EHB is a technical continuous-execution role: routine post-task checkpoints are OFF, just like EE and CS1. Physical-risk actions still require `PHYSICAL_SAFETY`.

## Integration protocol

### Feature integration into a role branch

The owning workstream agent:

1. updates from the latest role branch;
2. resolves conflicts deliberately;
3. passes targeted and repository-required checks;
4. documents cross-role interface impact where applicable;
5. opens/updates the feature PR;
6. drives exact-head CI green;
7. merges into the role branch.

This is staging, not final completion.

### Role integration into master

The role integration owner:

1. confirms the included workstreams are compatible;
2. synchronizes the role branch from latest `master`;
3. opens/updates the role-to-`master` PR;
4. runs feature-preservation, fabric, KREATE, frontend, Python, and data gates as applicable;
5. drives exact-head CI green;
6. merges with a normal merge commit;
7. verifies the resulting `master`;
8. records the shared PR/head/merge evidence on each included task;
9. moves included tasks to `MERGED_VERIFIED`.

Several tasks may share the same role integration PR number.

## Direct-master-push recovery

Direct push to `master` is a policy violation even though repository administration may not enforce branch protection.

When detected:

1. preserve/revert based on repository evidence;
2. create a P0 recovery task;
3. route the current state through a normal reviewed PR;
4. require exact-head full validation;
5. merge with a normal merge commit;
6. verify `master`;
7. keep the violation auditable.

## Agent-to-agent communication

Prefer repository-visible state:

- task JSON;
- dependency IDs;
- branch/PR references;
- blocker evidence;
- explicit integration notes;
- EE↔EHB interface contracts;
- EHB↔CS1 data-contract notes.

Do not require synchronous human relay.

## Mechanical checks

Run:

```bash
python scripts/agent_fabric_check.py
python scripts/test_agent_fabric_check.py
```

The unit suite includes a repository-level regression check requiring `role/ehb-embedded-integration` and split EE/EHB/shared hardware ownership in `.agents/fabric.json`.

CI additionally enforces approved PR base/head topology, latest-target-base ancestry, per-role feature PR concurrency, feature preservation, exact-head repository validation, merged-PR provenance for `master`, normal merge-commit semantics, and post-merge containment through `agent_exit_gate.py`.
