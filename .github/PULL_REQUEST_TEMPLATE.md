## PR type

- [ ] Child PR: `agent/<lane>/<task>` -> `work/<role>/<parent>`
- [ ] Parent integration PR: `work/<role>/<parent>` -> `master`
- [ ] Repository-wide governance/bootstrap PR: `agent/quality-release/<task>` -> `master`
- [ ] Legacy role PR during Fabric v2 migration

**Parent workstream:** `HUMAN-IE` / `HUMAN-EE` / `HUMAN-CS1` / `HUMAN-CS2` / N/A governance

**Human owner:** `human:<identity>` / N/A governance

**Agent task ID:** `TASK-...` / N/A parent/governance

**Agent owner:** `agent:<identity>` / N/A parent/governance

**Human gate:** `NONE` / one of the five critical gate kinds + decision evidence

## Parent/child contract

- [ ] Child work belongs to exactly one parent workstream.
- [ ] Child PR targets the owning parent branch, never `master`.
- [ ] Parent PR contains only child work already verified into that parent plus explicit parent-level synthesis.
- [ ] Required children are `MERGED_VERIFIED` into the parent before the parent becomes merge-ready.
- [ ] Optional children are explicitly marked optional in coordination metadata.

## Parallel safety

- [ ] Declared `touched_paths` cover every intentional changed product path.
- [ ] No active child in any parent owns overlapping product paths.
- [ ] Hard dependencies are satisfied.
- [ ] `produces` / `consumes` contracts are recorded when another agent/workstream depends on the output.
- [ ] Cross-parent/shared-file impact is listed below.

**Cross-parent/shared-file impact:** None / describe affected parents and shared surfaces.

## Draft vs integration slot

For parent PRs targeting `master`:

- [ ] This PR remains **draft** while another parent owns the master integration slot.
- [ ] No more than four parent/master PRs are open.
- [ ] At most one parent/master PR is non-draft.
- [ ] When this PR becomes non-draft, it is first in the deterministic integration queue.
- [ ] The non-draft head contains the exact current `master` and receives fresh exact-head CI after that sync.

Draft CI is advisory. Green CI from before another master merge is not merge evidence.

## Base freshness

- [ ] A merge-ready PR contains the exact current target-branch base SHA.
- [ ] Conflicts were resolved by reviewing both sides; no blind whole-file `ours`/`theirs`.
- [ ] Every deletion/rename was reviewed intentionally.

## Feature preservation

- [ ] New durable features were added to `.github/feature-registry.json` when applicable.
- [ ] No registered feature or required path was removed/weakened unintentionally.
- [ ] `python scripts/verify_feature_preservation.py --base-ref <target-base-sha>` passes.

### Feature additions / changes

Describe user-visible features, routes, data sources, assets, and behavior.

### Intentional removals

`None` unless explicitly approved and documented.

## Validation

- [ ] Targeted tests pass.
- [ ] `python scripts/test_agent_fabric_check.py`
- [ ] `python scripts/test_agent_task.py`
- [ ] `python scripts/agent_fabric_check.py`
- [ ] `python scripts/kreate_check.py`
- [ ] `python -m compileall -q backend/app scripts`
- [ ] Critical JSON datasets validate.
- [ ] `cd frontend && npm ci --no-audit --no-fund`
- [ ] `cd frontend && npm run typecheck`
- [ ] `cd frontend && npm run lint`
- [ ] `cd frontend && npm run build`
- [ ] CI is green on the exact merge-ready head SHA.

Mark non-applicable checks explicitly rather than silently skipping them.

## Master integration contract

Required for a non-draft PR targeting `master`:

- [ ] Parent is `READY_FOR_INTEGRATION` and owns the sole integration slot.
- [ ] Head contains current `master`.
- [ ] Required child work is parent-contained and compatible.
- [ ] Full required CI is green on the exact head.
- [ ] Merge uses a normal merge commit.
- [ ] Resulting `master` will be post-merge verified.
- [ ] `agent_exit_gate.py` will verify integrated-head containment.
- [ ] Parent integration is not `MERGED_VERIFIED` until post-merge checks pass.

## KREATE evidence and anti-slop gate

Use this section for application, PMR, evidence, experiment, or claim-bearing changes.

- [ ] Material claims are classified correctly.
- [ ] Every material claim has an evidence ID or remains explicitly `HYPOTHESIS`/`UNKNOWN`.
- [ ] AI did not fabricate interviews, quotes, personas, pilot results, accuracy, climate impact, hardware performance, live data, or savings.
- [ ] Human evidence attestation is recorded when required.
- [ ] Known limitations are disclosed.

**Human reviewer:** N/A unless required

**Evidence IDs / artifacts:** N/A unless applicable

**Known limitations:** TODO / None
