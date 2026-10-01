# Multi-Human Multi-Agent Fabric v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Support four human-owned KREATE parent workstreams, each capable of safely fanning out to 50+ autonomous child agents, while requiring humans only for the five critical gate kinds and preserving exact-head/master merge safety.

**Architecture:** Introduce parent-workstream metadata above the existing task fabric. Child agents remain independently leased task records with non-overlapping path ownership and merge into their parent workstream; only parent workstreams enter the master integration queue. Keep coordination metadata on `agent-coordination`, retain short-lived task branches, and extend the existing validator/CLI rather than reviving the old large agent-bus implementation.

**Tech Stack:** Python 3.11 standard library, JSON coordination records, Git/GitHub branches and pull requests, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-30-multi-human-agent-fabric-v2-design.md`

## Global Constraints

- Exactly four KREATE human parent roles: IE, EE, CS1, CS2; one active parent workstream per human/role.
- No hard-coded child-agent concurrency limit; validator/tests must demonstrate at least 50 simultaneous non-conflicting child tasks.
- Humans block execution only for `EVIDENCE_ATTESTATION`, `IRREVERSIBLE_ACTION`, `PHYSICAL_SAFETY`, `EXTERNAL_COMMITMENT`, or `PRODUCT_DIRECTION`.
- Child agents may not self-attest PMR/interview facts or measured impact.
- Child branches never merge directly to `master`; they integrate into the owning parent workstream first.
- Parent-to-master integration retains latest-master sync, exact-head CI, normal merge commit, post-merge verification, feature preservation, KREATE checks, and `agent_exit_gate.py`.
- Do not revive `scripts/agent_bus.py` or introduce a permanent agent hierarchy/chat system.
- Preserve schema-v1 read compatibility while active records migrate.
- PR #35 (`fabric-task-cli`) is an upstream dependency: consume its CLI implementation after it merges/rebases; do not duplicate it independently.

## Review Focus

- 50 child tasks under one parent with distinct paths must validate without quadratic-policy false positives or arbitrary count rejection.
- Child path collisions across the same or different parents must still be rejected.
- A child must never integrate directly to `master` or escape its parent lifecycle.
- A non-critical `WAITING_HUMAN` transition must be rejected even for IE/CS2.
- Parent/master integration must reject stale master state and missing child completion evidence.

---

### Task 1: Parent/child schema v2 and backward-compatible validator

**Files:**
- Create: `.agents/PARENT_WORKSTREAM_TEMPLATE.json`
- Modify: `.agents/TASK_TEMPLATE.json`
- Modify: `.agents/fabric.json`
- Modify: `scripts/agent_fabric_check.py`
- Modify: `scripts/test_agent_fabric_check.py`

**Interfaces:**
- Consumes: existing schema-v1 task records and `validate_repository(root)` API.
- Produces: v2 parent records keyed by `HUMAN-IE`, `HUMAN-EE`, `HUMAN-CS1`, `HUMAN-CS2`; v2 child fields `parent_id`, `owner_agent`, `produces`, `consumes`, `child_integration`; validators for parent uniqueness, parent existence, role consistency, path ownership, child completion, and 50-child concurrency.

- [ ] **Step 1: Write failing validator tests** for four unique parents, duplicate human parent rejection, missing parent rejection, 50 independent active child tasks passing, and cross-child path collision failing.
- [ ] **Step 2: Run** `python scripts/test_agent_fabric_check.py` and confirm new tests fail on v1.
- [ ] **Step 3: Add minimal schema/config/template fields** without removing v1 read support.
- [ ] **Step 4: Implement parent/child validation** in focused helper functions; do not mix GitHub API logic into the validator.
- [ ] **Step 5: Run** `python scripts/test_agent_fabric_check.py && python scripts/agent_fabric_check.py` and require PASS.
- [ ] **Step 6: Commit** `feat(agents): add parent child fabric schema`.

### Task 2: Child-agent lifecycle and parent integration semantics

**Files:**
- Modify after PR #35 integration: `scripts/agent_task.py`
- Modify: `scripts/test_agent_task.py`

**Interfaces:**
- Consumes: v2 validator APIs from Task 1 and the task mutation CLI merged from PR #35.
- Produces: commands/operations `spawn-child`, `claim-child`, `heartbeat`, `child-ready`, `integrate-child`, `verify-child`, plus parent-aware `next`; all mutations remain single-record atomic and validator-checked.

- [ ] **Step 1: Write failing CLI tests** for spawning multiple children under one parent, agent lease ownership, child dependency checks, parent mismatch rejection, path collision rollback, and child-to-master integration rejection.
- [ ] **Step 2: Run** `python scripts/test_agent_task.py` and confirm failures are specific to missing v2 behavior.
- [ ] **Step 3: Implement parent-aware child creation/claim transitions** while preserving current v1 commands.
- [ ] **Step 4: Implement child integration evidence** requiring validated child head and parent branch target, not `master`.
- [ ] **Step 5: Add deterministic `next` ranking** by parent, priority, dependencies, and conflict-free paths.
- [ ] **Step 6: Run** task CLI tests + fabric tests and require PASS.
- [ ] **Step 7: Commit** `feat(agents): add child agent lifecycle`.

### Task 3: Human owner boundary and critical-only gates

**Files:**
- Modify: `AGENTS.md`
- Modify: `.agents/FABRIC.md`
- Modify: `KREATE/ROLES/USER_DECISION_CHECKPOINT_PROTOCOL.md`
- Modify: `scripts/agent_fabric_check.py`
- Modify: `scripts/test_agent_fabric_check.py`

**Interfaces:**
- Consumes: existing five human-gate kinds.
- Produces: one-human/one-parent accountability contract and mechanical rejection of non-critical `WAITING_HUMAN`; removes IE/CS2 routine post-work checkpoint requirement.

- [ ] **Step 1: Add failing tests** showing IE/CS2 ordinary continuation cannot enter `WAITING_HUMAN`, while each of the five critical gates can.
- [ ] **Step 2: Update policy docs** so all four roles continue autonomously between critical gates.
- [ ] **Step 3: Add validator rule** tying `WAITING_HUMAN` to the five configured gate kinds and a concrete pending question.
- [ ] **Step 4: Run** fabric tests + `python scripts/kreate_check.py` and require PASS.
- [ ] **Step 5: Commit** `policy(agents): limit human intervention to critical gates`.

### Task 4: Parent workstream fan-out/fan-in orchestration

**Files:**
- Modify: `scripts/agent_task.py`
- Modify: `scripts/test_agent_task.py`
- Create: `.agents/PARENT_WORKSTREAMS.md` only if a human-readable view is needed; coordination truth remains JSON.

**Interfaces:**
- Consumes: child lifecycle from Task 2.
- Produces: `parent-status`, `fanout`, `parent-ready`, deterministic child summary, and parent readiness rule: required children verified, no active conflicting child, no unresolved required artifact/dependency.

- [ ] **Step 1: Write failing tests** for a parent with 50 children, partial completion, failed child, optional child, and all-required-children-complete cases.
- [ ] **Step 2: Implement parent readiness aggregation** without a global child-count cap.
- [ ] **Step 3: Implement bounded fan-out** from an explicit child specification list; do not let the CLI invent product direction.
- [ ] **Step 4: Run** task + fabric test suites and require PASS.
- [ ] **Step 5: Commit** `feat(agents): add scalable parent fanout and fanin`.

### Task 5: Parallel parent PRs with a single master integration slot

**Files:**
- Modify: `.agents/fabric.json`
- Modify: `.github/workflows/ci.yml`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `scripts/agent_fabric_check.py`
- Modify: `scripts/test_agent_fabric_check.py`

**Interfaces:**
- Consumes: parent readiness state from Task 4.
- Produces: up to four open parent work PRs, all but at most one draft; only one non-draft parent PR may hold the master integration slot.

- [ ] **Step 1: Add policy tests/fixtures** for 4 open parent PR metadata records, second non-draft rejection, duplicate parent PR rejection, and stale parent/master rejection.
- [ ] **Step 2: Change fabric config** from single-open-PR to `max_parent_pull_requests=4` and `max_integration_ready_pull_requests=1`.
- [ ] **Step 3: Update CI merge-discipline shell** to count non-draft PRs rather than all open PRs and require current master only for the integration-slot PR.
- [ ] **Step 4: Ensure draft PRs still run product/fabric CI** but cannot satisfy merge discipline for master.
- [ ] **Step 5: Run** all fabric tests and inspect workflow syntax.
- [ ] **Step 6: Commit** `feat(ci): allow parallel parent prs with serialized merge`.

### Task 6: Parent integration queue and master exit contract

**Files:**
- Modify: `scripts/agent_task.py`
- Modify: `scripts/test_agent_task.py`
- Modify if needed: `scripts/agent_exit_gate.py`
- Modify: `.agents/FABRIC.md`

**Interfaces:**
- Consumes: parent readiness and PR slot policy.
- Produces: `queue`, `acquire-integration`, `release-integration`, deterministic ordering P0→P1→P2, dependency-unblocking value, ready timestamp, stable ID; parent-only master merge evidence.

- [ ] **Step 1: Write failing queue-order tests** including stable tie-breaking and P0 recovery preemption.
- [ ] **Step 2: Implement integration-slot acquisition** that rejects unready parents, occupied slot, stale master, or incomplete required children.
- [ ] **Step 3: Keep normal merge/post-merge/exit-gate evidence mandatory** for parent `MERGED_VERIFIED`.
- [ ] **Step 4: Run** task tests, fabric tests, compile checks.
- [ ] **Step 5: Commit** `feat(agents): serialize parent master integration`.

### Task 7: Four KREATE parent records and migration tooling

**Files:**
- Create on `agent-coordination`: four parent JSON records for IE/EE/CS1/CS2.
- Modify: `scripts/agent_task.py` only if migration helper is necessary.
- Modify: `KREATE/ROLES/README.md`

**Interfaces:**
- Consumes: v2 schema.
- Produces: exactly four active human-owned parent workstreams; existing v1 active child tasks are associated when unambiguous, while verified history is not rewritten.

- [ ] **Step 1: Add migration dry-run test** proving verified history remains untouched.
- [ ] **Step 2: Create the four parent records** with TODO human GitHub identity placeholders only where identity is not already explicitly known; do not invent identities.
- [ ] **Step 3: Associate active technical tasks only when role mapping is mechanically clear; otherwise leave them legacy-compatible until touched.
- [ ] **Step 4: Run** fabric validation against coordination checkout.
- [ ] **Step 5: Commit coordination metadata** using blob-SHA-safe updates.

### Task 8: Full-system verification and integration

**Files:**
- No new product files expected; only fixes required by verification.

**Interfaces:**
- Consumes: Tasks 1–7.
- Produces: verified Fabric v2 on `master` with 50-agent scalability evidence and no product/KREATE truth regressions.

- [ ] **Step 1: Run local/mechanical gates:**
  - `python scripts/test_agent_fabric_check.py`
  - `python scripts/test_agent_task.py`
  - `python scripts/agent_fabric_check.py`
  - `python scripts/kreate_check.py`
  - `python scripts/verify_feature_preservation.py --base-ref <current-master-sha>`
  - `python -m compileall -q backend/app scripts`
- [ ] **Step 2: Run frontend gates:** `npm ci --no-audit --no-fund && npm run typecheck && npm run lint && npm run build` in `frontend/`.
- [ ] **Step 3: Inspect diff** and confirm no product behavior, PMR claims, evidence, or measured-impact values changed.
- [ ] **Step 4: Demonstrate 50-child fixture** under one parent and concurrent children across all four parents with no overlapping paths.
- [ ] **Step 5: Open/ready the Fabric v2 parent PR only after PR #35 dependency is merged and current-master sync is complete.
- [ ] **Step 6: Require exact-head CI green, normal merge commit, post-merge master CI green, and `python scripts/agent_exit_gate.py --branch-head <validated-head>` PASS.
- [ ] **Step 7: Record parent workstream `MERGED_VERIFIED` evidence and release the integration lease.
