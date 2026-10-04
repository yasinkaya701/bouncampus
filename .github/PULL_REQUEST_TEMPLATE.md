## PR type

- [ ] Child/feature PR: `agent/<lane>/<task>` -> configured `role/<execution-role>`
- [ ] Role integration PR: `role/<execution-role>` -> `master`
- [ ] Repository-wide governance/bootstrap PR -> `master`

Human parent workstream: `ie` / `ee` / `cs1` / `cs2` / N/A

Execution role: `ie` / `ee` / `ehb` / `cs1` / `cs2` / governance

Agent task ID(s):

Parent ID (when applicable):

Human gate: `NONE` / gate kind + decision evidence

## Parent / child contract

- [ ] Child metadata names a valid parent workstream and execution role when schema-v2 child orchestration is used.
- [ ] Child fan-in targets the branch configured for its execution role.
- [ ] EHB work remains on `role/ehb-embedded-integration`; it is not collapsed into EE.
- [ ] Required parent children are reconciled before parent/master integration.
- [ ] This PR does not create a second parent-level master integration slot.

## Parallel safety

- [ ] Declared `touched_paths` cover every intentional changed product path.
- [ ] No active incompatible task owns overlapping paths.
- [ ] Hard dependencies are `MERGED_VERIFIED`.
- [ ] Feature PR is within the configured per-role concurrency limit.
- [ ] Cross-role/shared-file impact is described below.

**Cross-role/shared-file impact:** None / describe affected roles and shared surfaces.

## Base freshness

- [ ] PR head contains the exact current target-branch base SHA.
- [ ] Conflicts were resolved by reviewing both sides; no blind whole-file `ours`/`theirs`.
- [ ] Every deletion/rename was reviewed intentionally.

A green but stale PR is not mergeable. If `master` changes first, resync and rerun exact-head checks.

## Feature preservation

- [ ] New durable features were registered when applicable.
- [ ] No registered feature, required path, ownership split, evidence vocabulary, or safety gate was removed/weakened unintentionally.
- [ ] `python scripts/verify_feature_preservation.py --base-ref <target-base-sha>` passes when applicable.

### Feature additions / changes

Describe user-visible/product/control-plane behavior.

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
- [ ] CI is green on the exact PR head SHA.

Mark non-applicable checks explicitly rather than silently skipping them.

## Master integration contract

Required for any PR targeting `master`:

- [ ] The work owns the single parent/master integration slot.
- [ ] Head contains current `master`.
- [ ] Included workstreams are compatible.
- [ ] Cross-role/shared changes have been reconciled.
- [ ] Full required CI is green on the exact head.
- [ ] Merge uses a normal merge commit.
- [ ] Resulting `master` will be post-merge verified.
- [ ] Included tasks are not marked `MERGED_VERIFIED` until verified master containment is proven.

A child/feature PR merged only into a role branch is staging, not final completion.

## Hardware / EHB preservation

When hardware or device contracts are touched:

- [ ] EE retains measurement/calibration/uncertainty/field-verification ownership.
- [ ] EHB retains embedded electronics/PCB/firmware/comms/device-integration ownership.
- [ ] EE↔EHB interface changes use the canonical interface contract.
- [ ] CS1 consumer review is included when device/schema/timing/calibration/quality semantics can alter inference or decisions.
- [ ] Evidence labels remain `ASSUMPTION / DATASHEET / CALCULATION / SIMULATION / BENCH_TEST / FIELD_TEST / PRODUCTION_EVIDENCE`.

## KREATE evidence and anti-slop gate

Use this section for application, PMR, evidence, experiment, or claim-bearing changes.

- [ ] Material claims are classified correctly.
- [ ] Every material claim has an evidence ID or remains explicitly `HYPOTHESIS`/`UNKNOWN`.
- [ ] AI did not fabricate interviews, quotes, personas, pilot results, accuracy, climate impact, hardware performance, live data, or savings.
- [ ] No AI-generated interview, quote, persona, pilot result, metric, or field observation is represented as human or measured evidence.
- [ ] No fabricated evidence, measurement, source, result, or operational claim is included.
- [ ] Human evidence attestation is recorded when required.
- [ ] Known limitations are disclosed.

**Human reviewer:** N/A unless required

**Evidence IDs / artifacts:** N/A unless applicable

**Known limitations:** TODO / None
