# BOUNCAMPUS Autonomous Agent Fabric

This document defines the executable coordination model layered on top of `AGENTS.md`.

## Operating principle

**Autonomous by default; parallel by child/role; serialized at final master integration; verified on `master`.**

BOUNCAMPUS has four human parent workstreams (`ie`, `ee`, `cs1`, `cs2`) and five durable execution roles (`ie`, `ee`, `ehb`, `cs1`, `cs2`). Human-team count and execution-role count are intentionally different.

## Control-plane surfaces

- Durable product truth: `master`
- Role branches:
  - `role/ie-customer-discovery`
  - `role/ee-physical-systems`
  - `role/ehb-embedded-integration`
  - `role/cs1-decision-intelligence`
  - `role/cs2-product-strategy`
- Human parent branch pattern: `work/<ie|ee|cs1|cs2>/<workstream>`
- Short-lived child/task branches: `agent/<lane>/<task>`
- Coordination metadata branch: `agent-coordination`
- Task store: `.agents/coordination/tasks/`
- Parent store: `.agents/coordination/parents/`
- Task template: `.agents/TASK_TEMPLATE.json`
- Parent template: `.agents/PARENT_WORKSTREAM_TEMPLATE.json`

## Parent versus execution role

A parent is a human-owned coordination unit. An execution role is a durable technical ownership/integration unit.

Examples:

- A CS1 parent normally spawns children targeting `cs1`.
- The EE parent may spawn an EE calibration child and an EHB firmware child in parallel.
- The EHB firmware child still targets `role/ehb-embedded-integration`; it never becomes EE-owned merely because the human parent is EE.

The configured `role_branches` map is authoritative. `hardware.primary_role` is forbidden.

## Hardware boundary

- **EE:** measurement architecture, measurement/sensor selection, calibration, uncertainty, field verification.
- **EHB:** embedded electronics, PCB, firmware, communications, device-side power/interface implementation, bring-up, recovery/buffering and HW/SW integration.
- **Shared:** EE↔EHB interface contract and system verification.
- **CS1:** downstream inference/decision semantics; consumer review is required when device/data-contract changes can alter those semantics.

Evidence labels are locked to `.agents/fabric.json` and `KREATE/HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md`.

## Task lifecycle

`BACKLOG -> READY -> CLAIMED -> ACTIVE -> READY_FOR_INTEGRATION -> INTEGRATING -> MERGED_VERIFYING -> MERGED_VERIFIED`

Side states: `BLOCKED`, `WAITING_HUMAN`, `CANCELLED`.

There is no branch-only `DONE` state.

## Parent lifecycle

Parent workstreams may use:

- `ACTIVE`
- `BLOCKED`
- `WAITING_HUMAN`
- `READY_FOR_INTEGRATION`
- `INTEGRATING`
- `MERGED_VERIFYING`
- `COMPLETE`

Multiple parents may be ACTIVE in parallel. Only one parent-level workstream may occupy the final master integration slot at a time.

## Child spawning and fanout

A child task must declare:

- `agent_kind = CHILD`
- `parent_id`
- `parent_workstream`
- `execution_role`
- `required_for_parent`
- `touched_paths`
- `child_integration.target_role_branch`

There is no fixed child-agent count cap. Parallelism is bounded by contracts instead:

- path ownership;
- dependencies;
- leases;
- execution-role target;
- human gates;
- final integration slot.

`spawn-child` rejects active path overlap before mutating parent state. `fanout` is batch-rollback-safe: any failed specification removes children created by that batch and restores the original parent metadata.

Examples:

```bash
python scripts/agent_task.py spawn-child HUMAN-EE-HARDWARE TASK-EHB-NETWORK \
  --title "Implement retry transport" \
  --execution-role ehb \
  --lane ehb-comms \
  --path KREATE/HARDWARE/runtime

python scripts/agent_task.py fanout HUMAN-EE-HARDWARE --spec-file /tmp/children.json
python scripts/agent_task.py parent-status HUMAN-EE-HARDWARE
```

## Claim, lease and path ownership

To claim a task:

1. task is `READY`;
2. hard dependencies are `MERGED_VERIFIED`;
3. no unresolved human gate blocks execution;
4. declared paths do not overlap another active owner;
5. owner, branch, claim time and heartbeat are recorded.

A material commit or meaningful validation checkpoint should refresh heartbeat.

Parent-child relationships never waive path ownership. Parent and child coordination is metadata; product paths remain exclusive while active.

## Child fan-in

A child integrates only to the branch configured for its `execution_role`.

```bash
python scripts/agent_task.py integrate-child TASK-EHB-NETWORK \
  --owner agent-ehb-network \
  --pr 123 \
  --validated-head-sha <sha> \
  --target-role-branch role/ehb-embedded-integration
```

`integrate-child` fails closed if the requested branch differs from the configured execution-role branch.

A role-branch merge is staging. Final `MERGED_VERIFIED` requires verified master containment.

## Parent readiness

`parent-status` reports child state counts and `required_remaining`.

A parent is ready only when all children marked `required_for_parent` are `MERGED_VERIFIED`. Optional children do not block readiness.

## Single master integration slot

Parallel implementation/review remains allowed, but final master integration is serialized.

```bash
python scripts/agent_task.py integration-queue
```

Parent states occupying the slot:

- `READY_FOR_INTEGRATION`
- `INTEGRATING`
- `MERGED_VERIFYING`

`.agents/fabric.json` sets `max_integration_ready_pull_requests = 1`. If more than one parent occupies these states, the queue fails closed.

This slot does not cap active children, active parents, or draft review work. It prevents competing final integrations from racing stale master state.

## PR topology

### Child/feature PR

```text
agent/<lane>/<task> -> configured role branch
```

### Role integration PR

```text
role/<execution-role> -> master
```

### Governance PR

```text
agent/quality-release/<task> -> master
```

A master-targeting PR must contain current `master`, own the integration slot, pass exact-head gates, use a normal merge commit, and receive post-merge verification.

## Human gates

Only these gate kinds may interrupt autonomous work:

- `EVIDENCE_ATTESTATION`
- `IRREVERSIBLE_ACTION`
- `PHYSICAL_SAFETY`
- `EXTERNAL_COMMITMENT`
- `PRODUCT_DIRECTION`

Routine child fanout, branch/PR creation, reversible refactoring, tests, conflict resolution, merge execution, and plugin discovery are autonomous.

## Agent-to-agent communication

Prefer repository-visible state:

- parent/task JSON;
- dependency IDs;
- path claims;
- leases/heartbeats;
- branch/PR references;
- blocker evidence;
- integration notes.

Do not require synchronous human relay for ordinary coordination.

## Mechanical checks

Run:

```bash
python scripts/test_agent_fabric_check.py
python scripts/test_agent_task.py
python scripts/agent_fabric_check.py
python -m compileall -q backend/app scripts
```

CI additionally enforces current-base ancestry, approved topology, feature preservation, KREATE/data/frontend/backend gates, normal master merge provenance, and post-merge containment.
