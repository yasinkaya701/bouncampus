# EHB Role Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make EHB a first-class fifth KREATE execution role with independent branch ownership for embedded hardware, communications, firmware, and HW–SW integration while preserving EE ownership of measurement correctness and reducing EE's implementation workload.

**Architecture:** Extend the current role-branch governance model rather than creating an EE sub-lane. Add `role/ehb-embedded-integration`, split hardware ownership in `.agents/fabric.json`, codify the EE↔EHB interface contract, and add a repository-level regression test so a later governance change cannot silently collapse EHB back into EE. Keep the current four-human / 16-interview PMR plan unchanged: five execution roles do not imply five human team members.

**Tech Stack:** Markdown governance documents, JSON fabric configuration, Python 3.11 standard-library validation, GitHub Actions, GitHub branch/PR policy.

**Spec:** `docs/superpowers/specs/2026-10-01-ehb-role-architecture-design.md`

## Global Constraints

- EHB is a peer execution role of IE, EE, CS1, and CS2; it is not an EE lane or assistant role.
- Long-lived EHB branch is exactly `role/ehb-embedded-integration`.
- EE retains final ownership of measurement correctness, calibration, uncertainty, sensor-as-measurement decisions, physical placement, and pilot measurement SOPs.
- EHB owns embedded electronics, schematic/PCB implementation, controller/MCU, firmware, communications, power/interface implementation, bring-up, debug, telemetry, buffering, and HW↔firmware↔backend integration.
- EE↔EHB interface changes require cross-role review; no silent voltage, pinout, schema, sampling, or protocol changes.
- Existing `PHYSICAL_SAFETY`, evidence-maturity, anti-fabrication, exact-head CI, normal-merge, and post-merge verification rules remain unchanged.
- EHB has technical checkpoint **OFF**, matching EE/CS1 behavior.
- Preserve the current four-human team model and the existing 16 PMR interview slots. Do not add EHB interview slots merely because a fifth execution role exists.
- Do not merge or overwrite open Fabric v2 PR #43 in a way that reintroduces a four-role-only assumption. It must be reconciled to preserve EHB before it can become the future governance model.

## Review Focus

1. **Role count vs human count:** five execution roles must not accidentally change the four-person PMR allocation or `IE/EE/CS1/CS2` interview IDs.
2. **EE regression:** splitting embedded work out of EE must not remove measurement, calibration, uncertainty, or field-validation ownership from EE.
3. **EHB branch recognition:** CI must accept `role/ehb-embedded-integration` through the same dynamic `role_branches` configuration used by the existing role branches.
4. **Hardware truth boundary:** removing `hardware.primary_role = ee` must not weaken evidence labels or the physical-safety gate.
5. **Future Fabric v2 conflict:** open PR #43 currently encodes four parent roles; it must be explicitly blocked/reconciled so merging it later cannot delete EHB governance.

---

### Task 1: Lock the five-role contract with a regression test and role documents

**Files:**
- Create: `scripts/test_ehb_role_architecture.py`
- Create: `KREATE/ROLES/05_EHB_EMBEDDED_HARDWARE_COMMUNICATIONS_INTEGRATION_LEAD.md`
- Modify: `KREATE/ROLES/00_ROLE_SYSTEM_SUMMARY.md`
- Modify: `KREATE/ROLES/README.md`
- Modify: `KREATE/ROLES/02_EE_PHYSICAL_SYSTEMS_MEASUREMENT_LEAD.md`
- Modify: `KREATE/ROLES/USER_DECISION_CHECKPOINT_PROTOCOL.md`
- Modify: `docs/superpowers/specs/2026-10-01-ehb-role-architecture-design.md`

**Interfaces:**
- Consumes: approved EHB design spec.
- Produces: authoritative EHB role definition and a Python regression test that later tasks extend to fabric/governance files.

- [ ] **Step 1: Write the failing architecture test**

Create `scripts/test_ehb_role_architecture.py` using `unittest` and repository-relative reads. Add tests named:

```python
def test_ehb_role_document_exists_and_is_peer_role(): ...
def test_ee_and_ehb_ownership_boundary_is_explicit(): ...
def test_checkpoint_matrix_marks_ehb_off(): ...
def test_role_summary_distinguishes_five_roles_from_four_humans(): ...
```

Assertions must require the exact EHB title `EHB — Embedded Hardware, Communications & Integration Lead`, explicit EE measurement-final-ownership language, explicit EHB embedded/comms ownership language, and EHB `OFF` in the checkpoint matrix. The role summary/README must not claim five humans or increase the 16-interview target.

- [ ] **Step 2: Run the test and verify RED**

Run: `python scripts/test_ehb_role_architecture.py`

Expected: FAIL because `05_EHB_EMBEDDED_HARDWARE_COMMUNICATIONS_INTEGRATION_LEAD.md` does not exist and EHB is absent from the role/checkpoint documents.

- [ ] **Step 3: Add the EHB role document**

Write `KREATE/ROLES/05_EHB_EMBEDDED_HARDWARE_COMMUNICATIONS_INTEGRATION_LEAD.md` with these required sections: Mission, North Star, Core Ownership, EE↔EHB Interface Contract, Decision Rights, Hardware Design Scope, Firmware/Communications Scope, HW–SW Integration, Workload Sharing With EE, Collaboration With IE/EE/CS1/CS2, Evidence/Safety Rules, Strong Outputs, Application-Stage Success Criteria.

- [ ] **Step 4: Narrow EE to measurement-science final ownership without disabling EE prototyping**

Update `02_EE_PHYSICAL_SYSTEMS_MEASUREMENT_LEAD.md`: retain measurement architecture, sensor suitability, calibration, repeatability, uncertainty, physical workflow, and pilot SOPs; route primary PCB/firmware/comms/integration execution to EHB; add an EE↔EHB handoff section. EE may still perform bounded prototypes when they answer a measurement question.

- [ ] **Step 5: Update role navigation and checkpoint policy**

Update `00_ROLE_SYSTEM_SUMMARY.md`, `README.md`, and `USER_DECISION_CHECKPOINT_PROTOCOL.md` to five execution roles, add EHB collaborations, and set EHB checkpoint OFF. Preserve the existing 16 interview slots / four-human PMR language.

- [ ] **Step 6: Mark the approved spec as approved**

Change the spec status from `Proposed / awaiting written-spec approval` to `Approved — 2026-10-01` without altering its accepted architecture.

- [ ] **Step 7: Run the role contract test GREEN**

Run: `python scripts/test_ehb_role_architecture.py`

Expected: PASS.

- [ ] **Step 8: Commit**

Commit message: `feat(roles): add independent EHB execution role`

---

### Task 2: Make EHB first-class in the agent fabric and branch policy

**Files:**
- Modify: `.agents/fabric.json`
- Modify: `.agents/FABRIC.md`
- Modify: `.agents/WORKSTREAMS.md`
- Modify: `AGENTS.md`
- Modify: `scripts/test_ehb_role_architecture.py`

**Interfaces:**
- Consumes: EHB ownership definition from Task 1.
- Produces: machine-readable EHB role branch and explicit EE/EHB hardware ownership model used by CI and agents.

- [ ] **Step 1: Extend the regression test for machine-readable fabric**

Add tests named:

```python
def test_fabric_has_exact_five_execution_role_branches(): ...
def test_hardware_ownership_is_split_between_ee_and_ehb(): ...
def test_shared_hardware_contract_requires_cross_role_review(): ...
def test_governance_docs_list_ehb_branch(): ...
```

Require this branch mapping exactly:

```python
{
    "ie": "role/ie-customer-discovery",
    "ee": "role/ee-physical-systems",
    "ehb": "role/ehb-embedded-integration",
    "cs1": "role/cs1-decision-intelligence",
    "cs2": "role/cs2-product-strategy",
}
```

Require `hardware.primary_role` to be absent. Require `hardware.ownership` keys `ee`, `ehb`, `shared`; require shared `requires_cross_role_review` to be `true`; preserve `physical_safety_gate_required = true` and all seven evidence labels.

- [ ] **Step 2: Run the expanded test and verify RED**

Run: `python scripts/test_ehb_role_architecture.py`

Expected: FAIL on the current four-role fabric and `hardware.primary_role = ee`.

- [ ] **Step 3: Migrate `.agents/fabric.json`**

Add `ehb: role/ehb-embedded-integration` to `role_branches`.

Replace the single hardware primary-role model with:

```json
"ownership": {
  "ee": {
    "owns": [
      "measurement-architecture",
      "sensor-measurement-strategy",
      "calibration-uncertainty",
      "physical-workflow",
      "field-pilot-verification"
    ]
  },
  "ehb": {
    "owns": [
      "embedded-electronics",
      "power-interface-electronics",
      "pcb",
      "firmware",
      "communications",
      "board-bring-up-debug",
      "hw-sw-integration"
    ]
  },
  "shared": {
    "owns": [
      "ee-ehb-interface-contract",
      "system-level-hardware-verification"
    ],
    "requires_cross_role_review": true
  }
}
```

Keep the existing playbook path, evidence labels, safety gate, and a combined `recommended_lanes` list for backward compatibility. Add EHB lanes (`ehb-hardware`, `ehb-firmware`, `ehb-comms`, `ehb-integration`, `ehb-verification`) while retaining useful existing `hw-*` lanes.

- [ ] **Step 4: Update fabric/governance documentation**

Add EHB to `.agents/FABRIC.md`, `.agents/WORKSTREAMS.md`, and `AGENTS.md`. Change four-role literals to five-role execution language. Document EE↔EHB dual review for shared electrical/data interfaces and list `role/ehb-embedded-integration` in branch topology.

- [ ] **Step 5: Preserve existing merge behavior**

Do not change `integration.max_open_feature_pull_requests_per_role`, merge method, exact-head requirement, latest-master requirement, or post-merge verification. EHB inherits the same policy rather than getting a special bypass.

- [ ] **Step 6: Run focused and existing fabric tests**

Run:

```bash
python scripts/test_ehb_role_architecture.py
python scripts/test_agent_fabric_check.py
python scripts/agent_fabric_check.py
```

Expected: all PASS.

- [ ] **Step 7: Commit**

Commit message: `feat(agents): register EHB as fifth role`

---

### Task 3: Wire EHB regression protection into CI and developer workflow

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `docs/development-workflow.md`
- Modify: `README.md` only if it contains a literal four-role topology after current-master inspection.

**Interfaces:**
- Consumes: machine-readable `role_branches` from Task 2.
- Produces: CI that rejects EHB-governance regressions and onboarding that shows the fifth role branch.

- [ ] **Step 1: Verify CI topology remains configuration-driven**

Inspect `.github/workflows/ci.yml` and confirm `role_branches` are loaded from `.agents/fabric.json`. Do not hard-code EHB separately in merge-discipline logic.

Expected: adding EHB to `role_branches` automatically allows feature PRs into `role/ehb-embedded-integration` and role integration PRs from it to `master`.

- [ ] **Step 2: Add the EHB contract test to repository-data CI**

Add a CI step after the existing fabric unit test:

```yaml
- name: Test EHB role architecture
  run: python scripts/test_ehb_role_architecture.py
```

- [ ] **Step 3: Update the development workflow branch map**

Change `docs/development-workflow.md` from four long-lived KREATE role branches to five and add `role/ehb-embedded-integration` to the branch diagram. State explicitly that role count and human headcount are separate concepts.

- [ ] **Step 4: Check root onboarding for stale four-role literals**

If `README.md` describes the role topology as exactly four roles, update only that wording and branch map; do not refactor unrelated onboarding content.

- [ ] **Step 5: Run CI-equivalent governance validation**

Run:

```bash
python scripts/test_ehb_role_architecture.py
python scripts/test_agent_fabric_check.py
python scripts/test_agent_task.py
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
python -m compileall -q backend/app scripts
```

Expected: all PASS. `kreate_check.py` must still expect the original 16 `IE/EE/CS1/CS2` interview slots.

- [ ] **Step 6: Commit**

Commit message: `ci: protect EHB role architecture`

---

### Task 4: Reconcile the open Fabric v2 work so it cannot erase EHB

**Files / External surfaces:**
- PR #43: `feat(agents): scale fabric to human parents and 50+ child agents`
- PR #71: current EHB governance PR
- No product files.

**Interfaces:**
- Consumes: EHB five-role contract and the existing 50+ child-agent Fabric v2 proposal.
- Produces: repository-visible coordination preventing a later four-role governance overwrite.

- [ ] **Step 1: Compare PR #43 against the EHB contract**

Verify the known conflict remains: PR #43 currently states exactly four parent roles and only `work/ie`, `work/ee`, `work/cs1`, `work/cs2` branches.

- [ ] **Step 2: Record the reconciliation requirement on PR #43**

Add a top-level PR comment stating that EHB is now an approved fifth execution role and #43 must not be readied/merged until its parent/child model represents EHB without inventing a fifth human.

The required future rule is: **five execution roles may be owned by four humans; one human may own more than one persistent role parent.**

- [ ] **Step 3: Do not merge or force-update #43 as part of this EHB migration**

Keep #43 draft unless its own branch is deliberately rebased/reworked after EHB reaches verified `master`. This plan establishes the compatibility guard; it does not silently rewrite a parallel agent's large governance branch.

- [ ] **Step 4: Update PR #71 body**

Document the five-role migration, EE/EHB ownership split, validation commands, and the #43 compatibility constraint.

- [ ] **Step 5: Commit any repository-side reconciliation note only if needed**

If no repository file is required, do not create ceremonial documentation. PR comments/body are sufficient coordination evidence.

---

### Task 5: Exact-head validation, merge, and creation of the durable EHB role branch

**Files / Git refs:**
- Governance branch: `agent/quality-release/ehb-role-architecture`
- Target: `master`
- Create after verified merge: `role/ehb-embedded-integration`

**Interfaces:**
- Consumes: Tasks 1–4 complete and current `master`.
- Produces: EHB governance on durable product truth plus a long-lived EHB integration branch based on the verified merge.

- [ ] **Step 1: Synchronize the governance branch with current `master`**

Before final validation, require the PR head to contain the exact current `master` base SHA. Resolve shared-file conflicts by preserving valid concurrent changes; never use blind whole-file `ours`/`theirs`.

- [ ] **Step 2: Run the complete validation suite on the exact head**

Run:

```bash
python scripts/test_ehb_role_architecture.py
python scripts/test_agent_fabric_check.py
python scripts/test_agent_task.py
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
python scripts/verify_feature_preservation.py --base-ref <current-master-sha>
python -m compileall -q backend/app scripts
```

Also require the normal frontend CI (`npm ci`, typecheck, lint, build) on the exact PR head because the changed governance surfaces are high-conflict repository policy.

Expected: every required repository check GREEN on the exact head SHA.

- [ ] **Step 3: Mark PR #71 ready only after exact-head validation**

PR #71 must remain a governance/bootstrap PR `agent/quality-release/* -> master` and use a normal merge commit.

- [ ] **Step 4: Merge PR #71 with expected-head protection**

Merge only if GitHub still reports the validated head SHA. If another PR lands first, re-sync current `master`, rerun exact-head CI, and retry.

- [ ] **Step 5: Verify merged `master`**

Require post-merge master CI/provenance success and verify the integrated governance head is contained in `master` using the existing merge-before-exit gate.

- [ ] **Step 6: Create the durable EHB role branch from verified `master`**

Create:

```text
role/ehb-embedded-integration
```

Base it on the verified post-merge `master` commit, not the pre-merge governance branch head.

- [ ] **Step 7: Verify branch and fabric agreement**

Confirm `.agents/fabric.json` on `master` maps `ehb` to the exact branch name and that GitHub reports the branch exists at the verified master commit.

- [ ] **Step 8: Final cross-role smoke check**

Confirm IE, EE, CS1, and CS2 branch mappings remain unchanged; EHB is additive; EHB feature PRs can target its role branch under dynamic CI topology; and the 16-slot PMR tracker remains unchanged.

- [ ] **Step 9: Record completion evidence**

Update PR/coordination evidence with validated head, merge SHA, post-merge verification, and EHB branch SHA. Only then call the role installation complete.
