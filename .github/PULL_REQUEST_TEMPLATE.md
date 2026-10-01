## PR type

- [ ] Feature PR: `agent/<lane>/<task>` -> `role/<role>`
- [ ] Role integration PR: `role/<role>` -> `master`
- [ ] Repository-wide governance/bootstrap PR -> `master`

Owning role / governance owner:

Agent task ID(s):

Feature branch(es):

Human gate: `NONE` / gate kind + decision evidence

## Parallel-safety

- [ ] Declared `touched_paths` cover every intentional changed product path.
- [ ] No active incompatible task owns overlapping product paths.
- [ ] Hard dependencies are `MERGED_VERIFIED`.
- [ ] This PR is within the per-role concurrency limit.
- [ ] Cross-role/shared-file impact is listed below.

**Cross-role/shared-file impact:** None / describe affected roles and shared surfaces.

## Base freshness

- [ ] PR head contains the exact current target-branch base SHA.
- [ ] Conflicts were resolved by reviewing both sides; no blind whole-file `ours`/`theirs`.
- [ ] Every deletion/rename was reviewed intentionally.

A green but stale PR is not mergeable. If another `master` PR lands first, resync and rerun CI.

## Feature preservation

- [ ] New durable features were added to `.github/feature-registry.json` when applicable.
- [ ] No existing registered feature or required path was removed/weakened unintentionally.
- [ ] `python scripts/verify_feature_preservation.py --base-ref <target-base-sha>` passes.

### Feature additions / changes

Describe user-visible features, routes, data sources, assets, and behavior.

### Intentional removals

`None` unless explicitly approved and documented.

## Validation

- [ ] Targeted tests pass.
- [ ] `python scripts/agent_fabric_check.py`
- [ ] `python scripts/kreate_check.py`
- [ ] `python -m compileall -q backend/app scripts`
- [ ] Critical JSON datasets validate.
- [ ] `cd frontend && npm ci --no-audit --no-fund`
- [ ] `cd frontend && npm run typecheck`
- [ ] `cd frontend && npm run lint`
- [ ] `cd frontend && npm run build`
- [ ] CI is green on the exact PR head SHA.

Mark non-applicable checks explicitly in the PR description rather than silently skipping them.

## Master integration contract

Required for any PR targeting `master`:

- [ ] Head contains current `master`.
- [ ] Included workstreams are compatible.
- [ ] Cross-role/shared changes have been reconciled.
- [ ] Full required CI is green on the exact head.
- [ ] Merge will use a normal merge commit.
- [ ] Resulting `master` will be post-merge verified.
- [ ] Included tasks will not be marked `MERGED_VERIFIED` until their commits are proven present on verified `master`.

A feature PR merged only into a role branch is staging, not final completion.

## KREATE evidence and anti-slop gate

Use this section for application, PMR, evidence, experiment, or claim-bearing changes.

<!-- Automation compatibility: AI-generated material must contain no fabricated evidence or results. -->

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
