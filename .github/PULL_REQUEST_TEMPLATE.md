## Integration batch

Owning Workstream Agent / temporary Merge Coordinator:

Agent branch:

Additional compatible branches included, if any:

## Feature preservation

- [ ] This PR starts from the latest `master`.
- [ ] Every included agent branch is listed above.
- [ ] Every deletion/rename was reviewed intentionally.
- [ ] Conflict resolution preserved both sides where both carried valid behavior.
- [ ] New durable features were added to `.github/feature-registry.json`.
- [ ] No existing feature-registry entry or required path was removed/weakened.

### Feature additions / changes

Describe user-visible features, routes, data sources, assets, and behavior added or changed.

### Intentional removals

`None` unless the repository owner explicitly approved a removal. Include the approval context when non-empty.

## Validation

- [ ] `python scripts/verify_feature_preservation.py --base-ref <master-sha>`
- [ ] `cd frontend && npm ci --no-audit --no-fund`
- [ ] `cd frontend && npm run typecheck`
- [ ] `cd frontend && npm run lint`
- [ ] `cd frontend && npm run build`
- [ ] `python -m compileall -q backend/app`
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

**A PR being open, review-ready, or green is not completion. The owning agent must merge and verify `master` before releasing the workstream.**
