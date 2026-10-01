# Multi-Human / Multi-Agent Development Workflow

BOUNCAMPUS uses four persistent human-owned parent workstreams and scalable short-lived child-agent branches.

## Topology

```text
master
  ↑ one serialized integration slot
  ├─ work/ie/<parent>
  ├─ work/ee/<parent>
  ├─ work/cs1/<parent>
  └─ work/cs2/<parent>
       ↑ verified child fan-in
       ├─ agent/<lane>/<task-a>
       ├─ agent/<lane>/<task-b>
       └─ ... 50+ children when safe
```

The parent branch is the human accountability/integration boundary. Child branches are the scalable execution units.

## One human, one parent

The KREATE team has exactly one persistent parent per role:

- `HUMAN-IE`
- `HUMAN-EE`
- `HUMAN-CS1`
- `HUMAN-CS2`

A parent persists across multiple master integration batches. It does not end when one batch merges.

## Child-agent branches

Child agents use:

```text
agent/<lane>/<task>
```

A child:

- belongs to exactly one parent;
- declares `touched_paths`;
- declares hard dependencies;
- may declare `produces` / `consumes` artifacts;
- owns one lease/heartbeat;
- integrates into its parent branch only.

Example:

```text
agent/api-product/forecast-calibration
  -> work/cs1/kreate
```

A child never targets `master` directly.

## Concurrency

There is no configured child-agent count limit.

Concurrency is admitted by:

- dependency readiness;
- active path non-overlap;
- artifact availability;
- runner/repository capacity;
- parent fan-in throughput.

Fifty non-conflicting child agents under one parent are valid. Two children editing overlapping paths are not.

## Parent readiness

A parent integration batch is ready only when:

1. at least one new child has been verified into the parent;
2. every pending required child is verified;
3. optional incomplete children are explicitly optional;
4. parent branch represents the validated combined batch.

Previously promoted children recorded in parent `integration_history` are excluded from later batch readiness.

## Parent pull requests

Up to four PRs targeting `master` may be open concurrently, normally one per parent.

- At most one may be non-draft.
- The single non-draft PR owns the `master` integration slot.
- Other parent PRs stay draft and may receive advisory CI/review.
- Draft CI becomes stale when `master` changes.
- The parent that acquires the slot must sync current `master` and rerun fresh exact-head CI.

## Deterministic master queue

Ready parents are ordered by:

1. P0, P1, P2;
2. dependency-unblocking value;
3. oldest ready timestamp;
4. parent ID.

Agents do not ask a human which ready PR should merge next when the queue can decide mechanically.

## Merge gates

A merge-ready parent PR must:

1. contain current `master`;
2. contain verified child fan-in;
3. pass `verify_feature_preservation.py`;
4. pass Fabric validator/tests;
5. pass KREATE validation;
6. pass repository Python/data validation;
7. pass frontend typecheck/lint/build while those checks remain part of CI;
8. disclose shared-file impact;
9. use a normal merge commit;
10. pass post-merge `master` audit and `agent_exit_gate.py`.

When another parent merges first, any waiting integration PR must resync and rerun exact-head CI.

## After master merge

The parent does not terminate.

Record an immutable integration-history entry containing:

- PR number;
- base master SHA;
- validated parent head;
- merge SHA;
- post-merge verification time;
- included child IDs.

Then clear current integration metadata and return the parent to `ACTIVE` for the next child wave.

## Shared/high-conflict files

Treat these as shared surfaces:

- `AGENTS.md`
- `.agents/**`
- `.github/**`
- root build/deployment configuration
- lockfiles
- shared API/data contracts
- KREATE evidence/claim policy

Child agents should avoid these unless the task explicitly owns the shared change. Shared changes require broad validation and cross-parent review.

## Human involvement

Humans are not routine merge coordinators or agent dispatchers.

Only five human gates exist:

- `EVIDENCE_ATTESTATION`
- `IRREVERSIBLE_ACTION`
- `PHYSICAL_SAFETY`
- `EXTERNAL_COMMITMENT`
- `PRODUCT_DIRECTION`

Everything else should proceed through repository evidence, tests, reversible choices, and the deterministic queue.

## Mechanical commands

```bash
python scripts/agent_fabric_check.py
python scripts/agent_task.py summary
python scripts/agent_task.py ready --parent HUMAN-CS1
python scripts/agent_task.py next --parent HUMAN-CS1
python scripts/agent_task.py parent-status HUMAN-CS1
python scripts/agent_task.py queue
```

See `.agents/FABRIC.md` for the full contract.
