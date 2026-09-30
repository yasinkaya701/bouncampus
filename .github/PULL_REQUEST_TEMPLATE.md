## Contribution summary

**Owner type:** `HUMAN` / `AGENT`

**Owner / role:**

**Branch:**

**Linked issue / task:**

### What changed?

Describe the bounded change in 2–5 bullets.

### Why does it matter?

Explain the product, KREATE, evidence, reliability, or developer-workflow impact.

### Validation performed

List the exact commands/checks you ran and their result.

### Evidence / assumptions / limitations

- Evidence IDs: `N/A` unless this change contains claim-bearing material.
- Assumption labels: `N/A` unless applicable.
- Known limitations: `None` / describe.

### UI evidence

Screenshots/video: `N/A` unless a material UI flow changed.

---

## Integration batch

**Integration Owner:**

**This is the repository's only open integration PR:** `YES` / `NO`

**Human gate:** `NONE` / gate kind + decision evidence

**Additional compatible branches included, if any:**

### Human-owned contribution

Use this subsection when `Owner type = HUMAN`.

- Human role: `IE` / `EE` / `CS1` / `CS2` / other documented maintainer
- Human branch: `human/<role>/<task>`
- [ ] Work started from a recent `master`.
- [ ] The linked issue/task has a bounded outcome and acceptance criteria.
- [ ] I checked for overlapping active agent/human work before editing shared paths.
- [ ] I did not open a second parking-lot PR while another integration PR was active.
- [ ] I will keep driving this integration until merged or document a real external blocker.

### Agent-owned contribution

Use this subsection when `Owner type = AGENT`.

Owning Workstream Agent / temporary Integration Owner:

Agent task ID:

Agent branch:

Coordination task state before PR: `READY_FOR_INTEGRATION`

- [ ] Task/lease metadata exists on `agent-coordination` or this is an explicitly documented fabric-bootstrap PR.
- [ ] Declared `touched_paths` cover every intentional changed product path.
- [ ] No active task owns an overlapping product path.
- [ ] Hard dependencies are `MERGED_VERIFIED`.
- [ ] Human gate is `NONE` unless an explicit critical gate in `AGENTS.md` applies.
- [ ] If a human gate applies, the task records one concrete decision and its evidence; routine engineering judgment was not escalated.
- [ ] `python scripts/agent_fabric_check.py` passes.
- [ ] `python scripts/test_agent_fabric_check.py` passes when agent-fabric code changes.

## Feature preservation

- [ ] This PR starts from / contains the latest required `master` base before final merge validation.
- [ ] Every included branch is listed above.
- [ ] Every deletion/rename was reviewed intentionally.
- [ ] Conflict resolution preserved both sides where both carried valid behavior.
- [ ] New durable features were added to `.github/feature-registry.json` when applicable.
- [ ] No existing feature-registry entry or required path was removed/weakened.

### Feature additions / changes

Describe user-visible features, routes, data sources, assets, behavior, or team workflow added or changed.

### Intentional removals

`None` unless the repository owner explicitly approved a removal. Include the approval context when non-empty.

## Validation

Run the checks that apply to the changed paths. The Integration Owner is responsible for the final merge gate.

- [ ] `python scripts/verify_feature_preservation.py --base-ref <master-sha>` when feature-preservation validation applies.
- [ ] `python scripts/agent_fabric_check.py`
- [ ] `python scripts/kreate_check.py`
- [ ] `cd frontend && npm ci --no-audit --no-fund`
- [ ] `cd frontend && npm run typecheck`
- [ ] `cd frontend && npm run lint`
- [ ] `cd frontend && npm run build`
- [ ] `python -m compileall -q backend/app scripts`
- [ ] Critical JSON datasets validate.
- [ ] CI is green on the exact PR head SHA.

Mark truly non-applicable checks as `N/A` in the validation notes rather than pretending they ran.

## Merge-before-exit contract

Applies to the current Integration Owner, human or agent:

- [ ] This is the repository's only open PR.
- [ ] PR head contains the current required `master` base commit before final validation.
- [ ] No follow-up branch is required to make this batch functionally complete.
- [ ] The Integration Owner will resolve conflicts and CI failures rather than abandon a mergeable batch.
- [ ] The Integration Owner will perform the repository's normal merge into `master`.
- [ ] The merged `master` commit will be verified before the work is reported as integrated.

Agent-owned work additionally requires:

- [ ] `python scripts/agent_exit_gate.py --branch-head <merged-agent-head>` passes before the agent reports completion or exits.
- [ ] Coordination state reaches `MERGED_VERIFIED` with PR/head/merge/post-merge evidence before the lease is released.

**A PR being open, review-ready, or green is not the same as being integrated.**

## KREATE evidence and anti-slop gate

Use this section for PRs that change KREATE application, PMR, evidence, experiment, or claim-bearing material. Real-world evidence cannot be fabricated or self-attested by an AI agent.

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
