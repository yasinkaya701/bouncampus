## Integration batch

Merge Coordinator:

Agent branches/workstreams included:

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

## Merge contract

- [ ] This is the repository's only open PR.
- [ ] PR head contains the current `master` base commit.
- [ ] No follow-up branch is required to make this batch functionally complete.
- [ ] After merge, the merged `master` commit will be used for deployment/release verification.
