# Fabric v2 Current-Master Recut Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reintroduce the useful Fabric v2 parent/child agent hierarchy on current master without regressing the durable five-role IE/EE/EHB/CS1/CS2 execution model.

**Architecture:** Extend the existing schema-v1 role-branch fabric instead of replacing it wholesale. Schema v2 adds a human-parent layer and child-agent metadata/operations while preserving current role branches, EE/EHB hardware ownership, exact-head merge discipline, leases, and task compatibility. Child work remains path/lease constrained and ultimately fans into a durable role branch or the quality-release governance lane before master.

**Tech Stack:** Python 3.11 standard library, JSON control-plane files, GitHub Actions, Markdown repository policy docs.

**Spec:** GitHub issue #181 `[Fabric v2] Recut multi-human/child agent hierarchy on current master`.

## Global Constraints

- Base all implementation on current verified master; never transplant stale PR #43 wholesale.
- Preserve first-class execution roles `ie`, `ee`, `ehb`, `cs1`, `cs2` and `ehb -> role/ehb-embedded-integration`.
- Preserve EE/EHB/shared hardware ownership and canonical evidence labels.
- Preserve exact-head CI, latest-master/latest-role-base freshness, normal merge commits, merge-before-exit, and post-merge verification.
- Keep task-file compatibility where practical; existing current-master task files must continue validating.
- No product, PMR, model-accuracy, climate, hardware-performance, pilot, or savings claims.

## Review Focus

- EHB must never collapse into EE when schema v2 is enabled.
- A child agent may not claim a path overlapping another active child/role task.
- Parent/child state must not weaken lease or critical-human-gate invariants.
- Parent fan-in must never bypass configured durable role/master topology.
- 50 independent child tasks must validate without an artificial agent-count ceiling.

---

### Task 1: Schema-v2 compatibility and parent topology

**Files:**
- Modify: `.agents/fabric.json`
- Modify: `scripts/agent_fabric_check.py`
- Modify: `scripts/test_agent_fabric_check.py`
- Create: `.agents/PARENT_WORKSTREAM_TEMPLATE.json`

**Interfaces:**
- Consumes: existing role branches, task schema, lease/path validation.
- Produces: schema-v2 config with `parent_workstreams`, `coordination_parent_dir`, parent branch pattern, child-agent unlimited policy, and backward-compatible task validation.

- [ ] Add failing validator tests proving schema v2 preserves all five role branches/EHB ownership, accepts a four-human-parent model, and validates 50 non-overlapping active child tasks.
- [ ] Run repository-data tests on the RED commit and confirm failure is caused by missing schema-v2 support.
- [ ] Implement minimal schema-v2 config/validator compatibility and parent template.
- [ ] Re-run fabric tests and confirm green.
- [ ] Commit.

### Task 2: Parent/child task operations

**Files:**
- Modify: `scripts/agent_task.py`
- Modify: `scripts/test_agent_task.py`

**Interfaces:**
- Consumes: Task 1 parent topology and existing task lifecycle.
- Produces: child spawn/claim/heartbeat/integrate/verify helpers and parent summary/readiness/fanout operations without bypassing path/lease checks.

- [ ] Add failing tests for child spawn under IE/EE/CS1/CS2 parent workstreams, EHB execution-role targeting, invalid parent/role rejection, path collision rejection, and parent readiness based on child states.
- [ ] Run tests and confirm RED.
- [ ] Implement minimal operations using existing `_write_validated`, ownership, lease, and transition primitives.
- [ ] Re-run task + fabric suites and confirm green.
- [ ] Commit.

### Task 3: Integration-slot and regression hardening

**Files:**
- Modify: `scripts/agent_fabric_check.py`
- Modify: `scripts/test_agent_fabric_check.py`
- Modify: `scripts/test_agent_task.py`

**Interfaces:**
- Consumes: Task 1 schema and Task 2 operations.
- Produces: explicit validation that only one master integration-ready lane is active while parallel child/parent draft work remains allowed.

- [ ] Add failing tests for concurrent parent work, single non-draft master integration slot, EHB preservation, and 50-child collision/path cases.
- [ ] Run tests and confirm RED.
- [ ] Implement minimal invariants.
- [ ] Run all current agent-fabric/task tests and compile checks.
- [ ] Commit.

### Task 4: Repository policy/docs and merge gates

**Files:**
- Modify: `AGENTS.md`
- Modify: `.agents/FABRIC.md`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `docs/development-workflow.md`

**Interfaces:**
- Consumes: final Task 1-3 behavior.
- Produces: operator-facing parent/child workflow that explicitly keeps EHB independent and retains current merge gates.

- [ ] Document four human parents versus five execution roles and child fan-in rules.
- [ ] Document collision/lease/integration-slot behavior and critical-only human checkpoints.
- [ ] Verify `python scripts/test_agent_fabric_check.py`, `python scripts/test_agent_task.py`, `python scripts/agent_fabric_check.py`, and `python -m compileall -q backend/app scripts` through exact-head CI.
- [ ] Open one governance PR to master, require standard CI + Hosted Fallback + CS1 Regression Gate, then normal merge commit and post-merge verification.
