# Parallel Development & Merge Workflow

BOUNCAMPUS separates **human coordination** from **durable execution ownership**.

## Topology

Four human parent workstreams coordinate work:

```text
IE   EE   CS1   CS2
```

Five execution roles own durable technical integration:

```text
master
├─ role/ie-customer-discovery
├─ role/ee-physical-systems
├─ role/ehb-embedded-integration
├─ role/cs1-decision-intelligence
└─ role/cs2-product-strategy
```

The extra EHB execution role is intentional. It does not imply a fifth human team member.

## Parent and child workflow

For coordinated work, create/use a human parent record under `.agents/coordination/parents/`, then fan out independent child tasks.

```text
HUMAN-EE-HARDWARE
├─ TASK-MEASUREMENT  -> execution_role=ee
├─ TASK-FIRMWARE     -> execution_role=ehb
└─ TASK-CALIBRATION  -> execution_role=ee
```

Children can run in parallel only when paths/dependencies permit it. The parent relationship does not override product ownership.

Useful commands:

```bash
python scripts/agent_task.py parent-status HUMAN-EE-HARDWARE
python scripts/agent_task.py spawn-child ...
python scripts/agent_task.py fanout HUMAN-EE-HARDWARE --spec-file children.json
python scripts/agent_task.py integration-queue
```

## Child branches and role fan-in

Create short-lived task branches from the role that owns the execution result:

```text
agent/<lane>/<task> -> role/<execution-role>
```

Examples:

```text
agent/decision-intelligence/forecast-calibration
    -> role/cs1-decision-intelligence

agent/ehb-firmware/traygate-retry
    -> role/ehb-embedded-integration
```

`integrate-child` enforces this mapping. An EHB child cannot be redirected to EE merely because the EE human parent coordinated it.

## Parallelism

Parallel work is broad; final master integration is narrow.

- Child-agent count has no fixed policy ceiling.
- A role branch may have up to **3 open feature PRs**.
- Multiple human parents may stay ACTIVE concurrently.
- Draft/review work may proceed concurrently.
- Path overlap between active tasks is forbidden.
- Hard dependencies must be satisfied.
- Leases/heartbeats remain required for active ownership.
- **One parent/master integration slot** is available at a time.

The integration queue treats `READY_FOR_INTEGRATION`, `INTEGRATING`, and `MERGED_VERIFYING` as occupying that slot and fails closed if more than one parent holds it.

## Why serialize final integration

The old role-only model allowed multiple master integration PRs to sit ready concurrently. That reduced review serialization but increased stale-head churn and merge races. Fabric v2 keeps implementation parallel while serializing the final master decision point.

This means one master PR merging can never make another simultaneously integration-ready PR silently stale: the next workstream claims the slot only after reconciling current master.

## Master merge gates

Every master-targeting PR must:

1. own the single integration slot;
2. contain current `master`;
3. pass feature-preservation checks when applicable;
4. pass agent-fabric and KREATE validators;
5. pass Python/data/frontend/backend gates required by CI;
6. reconcile shared-file changes;
7. preserve the five-role topology and EE/EHB ownership split;
8. pass CI on the exact head SHA;
9. use a normal merge commit;
10. pass post-merge master verification.

A previously green SHA becomes invalid for merge if either the PR head or current master changes.

## Shared files

`AGENTS.md`, `.agents/**`, `.github/**`, root configuration, dependency lockfiles, shared data/API contracts, and evidence-policy files are high-conflict surfaces. Governance work touching them should use the quality-release lane and broad validation.

## EHB / hardware rule

- EE owns measurement architecture, calibration, uncertainty, and field verification.
- EHB owns embedded electronics, PCB, firmware, communications, buffering/recovery, and HW/SW integration.
- Shared EE↔EHB interfaces require explicit interface-contract review.
- CS1 reviews device/data-contract changes that can alter inference or decision semantics.

Do not replace this split with `hardware.primary_role = ee`.

## Completion

A role-branch merge is staging.

A task is complete only after its validated work is contained in post-merge-verified `master` and the integration evidence is recorded as `MERGED_VERIFIED`.
