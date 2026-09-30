## Integration batch

Owning Workstream Agent / temporary Integration Owner:

Agent task ID:

Agent branch:

Coordination task state before PR: `READY_FOR_INTEGRATION`

Human gate: `NONE` / gate kind + decision evidence

Additional compatible branches included, if any:

## Agent fabric

- [ ] Task/lease metadata exists on `agent-coordination` or this is an explicitly documented fabric-bootstrap PR.
- [ ] Declared `touched_paths` cover every intentional changed product path.
- [ ] No active task owns an overlapping product path.
- [ ] Hard dependencies are `MERGED_VERIFIED`.
- [ ] Human gate is `NONE` unless an explicit critical gate in `AGENTS.md` applies.
- [ ] If a human gate applies, the task records one concrete decision and its evidence; routine engineering judgment was not escalated.
- [ ] `python scripts/agent_fabric_check.py` passes.
- [ ] `python scripts/test_agent_fabric_check.py` passes when agent-fabric code changes.

## Feature preservation

- [ ] This PR starts from the latest `master`.
- [ ] Every included agent branch is listed above.
- [ ] Every deletion/rename was reviewed intentionally.
- [ ] Conflict resolution preserved both sides where both carried valid behavior.
- [ ] New durable features were added to `.github/feature-registry.json` when applicable.
- [ ] No existing feature-registry entry or required path was removed/weakened.

### Feature additions / changes

Describe user-visible features, routes, data sources, assets, and behavior added or changed.

### Intentional removals

`None` unless the repository owner explicitly approved a removal. Include the approval context when non-empty.

## Validation

- [ ] `python scripts/verify_feature_preservation.py --base-ref <master-sha>`
- [ ] `python scripts/agent_fabric_check.py`
- [ ] `python scripts/kreate_check.py`
- [ ] `cd frontend && npm ci --no-audit --no-fund`
- [ ] `cd frontend && npm run typecheck`
- [ ] `cd frontend && npm run lint`
- [ ] `cd frontend && npm run build`
- [ ] `python -m compileall -q backend/app scripts`
- [ ] Critical JSON datasets validate.
- [ ] CI is green on the exact PR head SHA.

## Mandatory merge-before-exit contract

- [ ] The agent that accepted this work is the agent driving this PR.
- [ ] This is the repository's only open PR.
- [ ] PR head contains the current `master` base commit.
- [ ] No follow-up branch is required to make this batch functionally complete.
- [ ] The owning agent will resolve conflicts and CI failures rather than hand the merge to another agent.
- [ ] The owning agent will perform the merge using a normal merge commit.
- [ ] The owning agent will verify the resulting `master` commit after merge.
- [ ] `python scripts/agent_exit_gate.py --branch-head <merged-agent-head>` will pass before the agent reports completion or exits.
- [ ] Coordination state will reach `MERGED_VERIFIED` with PR/head/merge/post-merge evidence before the lease is released.

**A PR being open, review-ready, or green is not completion. The owning agent must merge and verify `master` before releasing the task.**

## KREATE evidence and anti-slop gate

Use this section only for PRs that change KREATE application, PMR, evidence, experiment, or claim-bearing material. This is stricter than the normal autonomous engineering path because real-world evidence cannot be self-attested by an AI agent.

- [ ] Linked issue is present.
- [ ] Acceptance criteria passed.
- [ ] Test and/or evidence artifact is attached or linked.
- [ ] No unrelated changes are included.
- [ ] Material claims are classified correctly (`FACT`, `PUBLIC SOURCE`, `INTERVIEW EVIDENCE`, `TECHNICAL TEST`, `MODEL ESTIMATE`, `POLICY HEURISTIC`, `HYPOTHESIS`, `UNKNOWN`).
- [ ] Every material claim has an evidence ID or remains explicitly `HYPOTHESIS`/`UNKNOWN`.
- [ ] AI-generated application prose/research that asserts real-world facts was verified under the applicable evidence-attestation gate.
- [ ] Known limitations are disclosed.
- [ ] No fabricated interview, quote, persona, pilot result, model accuracy, climate impact, hardware performance, live data, or savings claim is present.
- [ ] Human reviewer is named below when this section applies.

**Human reviewer:** N/A unless KREATE claim/evidence material changed

**Evidence IDs / artifacts:** N/A unless applicable

**Known limitations:** TODO / None
