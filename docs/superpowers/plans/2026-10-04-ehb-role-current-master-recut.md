# EHB Role Current-Master Recut Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make EHB a first-class fifth execution role on the current repository control plane without replaying the stale #71 snapshot or overwriting newer CS1/EE work.

**Architecture:** Re-cut only the durable role/control-plane contract onto current master. The repository config is authoritative for role branches and hardware ownership; focused regression tests pin that contract. Role/interface documentation defines EE↔EHB↔CS1 boundaries, while existing product runtime and evidence semantics remain untouched.

**Tech Stack:** JSON repository policy, Python `unittest`, Markdown role/interface contracts, GitHub Actions repository validation.

**Spec:** superseding current-master interpretation of draft PR #71 (`feat(agents): add independent EHB execution role`).

## Global Constraints

- Five execution roles do not imply five human team members; human/PMR accounting remains four-person.
- EE owns measurement architecture, sensor/measurement choice, calibration, uncertainty, and field validity.
- EHB owns embedded electronics, PCB, firmware, communications, device-side power/interfaces, bring-up, buffering/recovery, and HW↔SW integration.
- EE↔EHB cross-boundary interface/schema/calibration/power/fault changes require explicit coordination.
- CS1 owns downstream decision/model/data interpretation and reviews device/data-contract changes that affect inference semantics.
- No fabricated BENCH_TEST/FIELD_TEST/PRODUCTION_EVIDENCE or production-readiness claim.
- Preserve all current master product/runtime changes; do not replay stale documentation rewrites wholesale.

## Review Focus

- Existing IE/EE/CS1/CS2 branches must remain unchanged while EHB is added.
- Hardware ownership must remove the single `primary_role` ambiguity and expose EE/EHB/shared responsibilities explicitly.
- Physical-safety gating must remain enabled.
- EHB role docs must not steal EE calibration/measurement-truth ownership or CS1 model/decision ownership.
- The old four-role Fabric v2 draft must not be merged in a way that removes EHB after this recut.

---

### Task 1: Pin first-class EHB control-plane behavior

**Files:**
- Modify: `scripts/test_agent_fabric_check.py`

**Interfaces:**
- Consumes: `.agents/fabric.json`
- Produces: repository-level assertions for the fifth role and split hardware ownership.

- [ ] Add failing tests asserting `role_branches.ehb == role/ehb-embedded-integration`, exact five-role keys, EE/EHB/shared ownership, no `hardware.primary_role`, and representative ownership terms.
- [ ] Run `python scripts/test_agent_fabric_check.py` and verify RED against current master config.

### Task 2: Implement minimum authoritative fabric contract

**Files:**
- Modify: `.agents/fabric.json`

**Interfaces:**
- Produces: first-class EHB branch plus explicit `hardware.ownership.ee`, `.ehb`, and `.shared` lists.

- [ ] Add EHB to `role_branches` without changing existing branch names.
- [ ] Replace `hardware.primary_role` with split ownership while preserving playbook, lanes, evidence labels, and physical-safety gate.
- [ ] Run `python scripts/test_agent_fabric_check.py` and `python scripts/agent_fabric_check.py`; require green.

### Task 3: Add role and cross-role interface contracts

**Files:**
- Create: `KREATE/ROLES/05_EHB_EMBEDDED_HARDWARE_COMMUNICATIONS_INTEGRATION_LEAD.md`
- Create: `KREATE/HARDWARE/EE_EHB_INTERFACE_CONTRACT_TEMPLATE.md`
- Modify: `KREATE/ROLES/00_ROLE_SYSTEM_SUMMARY.md`
- Modify: `KREATE/ROLES/README.md`
- Modify: `.agents/FABRIC.md`
- Modify: `.agents/WORKSTREAMS.md`

**Interfaces:**
- Produces: durable EHB ownership language and explicit EE↔EHB↔CS1 handoff/change-control rules.

- [ ] Add the EHB role document with ownership/non-ownership, evidence, safety, and coordination boundaries.
- [ ] Add the EE↔EHB interface template covering power, pinout, sampling, calibration persistence, protocol/schema, quality/fault states, and verification ownership.
- [ ] Update only authoritative role/fabric indexes to list EHB and distinguish execution-role count from human count.
- [ ] Preserve current product/runtime content and avoid broad README/onboarding rewrites.

### Task 4: Verify and converge stale governance PRs

**Files:** none beyond Tasks 1–3.

- [ ] Run repository-required compile/data/fabric checks plus exact-head Standard CI, Hosted Fallback, and relevant regression gates.
- [ ] Open a current-master governance PR and mark #71 superseded only after the recut exists.
- [ ] Add a guard to stale #43: it must not remove/collapse first-class EHB if ever refreshed.
- [ ] Merge normally only with current-master ancestry, then verify post-merge master and role/control-plane consistency.
