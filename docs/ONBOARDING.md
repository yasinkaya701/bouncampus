# BOUNCAMPUS Team Onboarding

This guide gets a teammate from zero context to a useful contribution without turning humans into merge coordinators or agent dispatchers.

## 1. Run the product

```bash
git clone https://github.com/yasinkaya701/bouncampus.git
cd bouncampus/frontend
npm ci
npm run dev
```

Open `http://localhost:3000`.

Requirements:

- Git
- Node.js 24.x
- Python 3.11+ for repository/backend tooling

A separate FastAPI process is not required for normal frontend work because the active Next.js application has co-located `/api/v1` routes.

## 2. Understand the current KREATE truth boundary

Start with:

1. `/demo`
2. `/food-waste`
3. `/food-waste/pilot`
4. `/data`
5. `/decisions`
6. [`../KREATE/README.md`](../KREATE/README.md)

The active beachhead/problem story remains evidence-gated. Do not invent private university telemetry, PMR, pilot outcomes, model metrics, hardware performance, or climate savings.

## 3. Know your one parent workstream

Each human owns exactly one persistent parent:

| Parent | Human role | Parent branch |
| --- | --- | --- |
| `HUMAN-IE` | Customer Discovery & Market Lead | `work/ie/kreate` |
| `HUMAN-EE` | Physical Systems & Measurement Lead | `work/ee/kreate` |
| `HUMAN-CS1` | Decision Intelligence Lead | `work/cs1/kreate` |
| `HUMAN-CS2` | Product Strategy, Evidence Synthesis & Application Lead | `work/cs2/kreate` |

The parent is an accountability/integration boundary, not a single small coding task. It persists across multiple master integration batches.

Detailed role guidance lives in [`../KREATE/ROLES/`](../KREATE/ROLES/).

## 4. Child agents do most routine execution

A parent may fan out any number of bounded child tasks:

```text
HUMAN-CS1 / work/cs1/kreate
├── agent/api-product/baseline
├── agent/api-product/data-quality
├── agent/api-product/uncertainty
├── agent/quality-release/red-team
└── ... 50+ children when contracts allow
```

There is no arbitrary agent-count ceiling.

A child must have:

- one `parent_id`;
- one leased `owner_agent`;
- explicit `touched_paths`;
- dependencies;
- acceptance criteria;
- validation commands;
- optional `produces` / `consumes` artifact IDs;
- an explicit required/optional relationship to the parent batch.

Concurrency is limited by conflicts and dependencies, not by the number of agents.

## 5. Branch correctly

### Human parent branch

```bash
git fetch origin --prune
git switch work/cs1/kreate
```

### Child branch

```bash
git switch -c agent/api-product/forecast-calibration
```

Child PR:

```text
agent/<lane>/<task>
        ↓
work/<role>/kreate
```

A child never targets `master` directly.

Parent PR:

```text
work/<role>/kreate
        ↓
master
```

Up to four parent/master PRs may exist concurrently. At most one may be non-draft and own the master integration slot.

## 6. Claim work mechanically

From an `agent-coordination` checkout/worktree, agents can use:

```bash
python scripts/agent_task.py summary
python scripts/agent_task.py ready --parent HUMAN-CS1
python scripts/agent_task.py next --parent HUMAN-CS1
```

The fabric rejects unsafe claims when:

- hard dependencies are unresolved;
- an in-fabric consumed artifact is unavailable;
- active `touched_paths` overlap another task;
- a critical human gate blocks the task.

## 7. Humans are exception handlers, not routine dispatchers

Do not stop for permission on normal research, architecture, model selection, hardware comparison, drafting, coding, tests, docs, branch operations, conflict resolution, or merge work.

Humans are required only for:

1. `EVIDENCE_ATTESTATION`
2. `IRREVERSIBLE_ACTION`
3. `PHYSICAL_SAFETY`
4. `EXTERNAL_COMMITMENT`
5. `PRODUCT_DIRECTION`

If none applies, keep working.

## 8. Evidence still belongs to reality

Agents may prepare interview guides, research sources, summarize notes, inspect evidence gaps, code, test, simulate, and red-team claims.

Agents may not self-attest:

- that an interview happened;
- that a quote is real;
- that a pilot result occurred;
- that measured savings exist;
- that a hardware bench result exists;
- that a model metric was achieved.

Use the KREATE evidence ledger and human attestation when required.

## 9. Hardware workflow

EE/hardware work begins at [`../KREATE/HARDWARE/README.md`](../KREATE/HARDWARE/README.md).

Typical child lanes:

- `hw-measurement`
- `hw-sensors`
- `hw-power`
- `hw-firmware`
- `hw-pcb`
- `hw-mechanical`
- `hw-calibration`
- `hw-verification`

Hardware claims keep their real maturity: ASSUMPTION, DATASHEET, CALCULATION, SIMULATION, BENCH_TEST, FIELD_TEST, or PRODUCTION_EVIDENCE.

## 10. Validation

During development, run targeted checks. Before parent integration, run the full relevant gates.

Repository:

```bash
python -m compileall -q backend/app scripts
python scripts/test_agent_fabric_check.py
python scripts/test_agent_task.py
python scripts/agent_fabric_check.py
python scripts/kreate_check.py
```

Frontend:

```bash
cd frontend
npm ci --no-audit --no-fund
npm run typecheck
npm run lint
npm run build
```

Feature preservation:

```bash
python scripts/verify_feature_preservation.py --base-ref <current-master-sha>
```

## 11. Parent integration

A parent batch is ready only when at least one new child is verified into the parent and every pending required child is verified.

Ready parents enter a deterministic queue:

1. priority;
2. dependency-unblocking value;
3. oldest ready time;
4. parent ID.

The selected parent:

1. acquires the sole non-draft master slot;
2. syncs current `master`;
3. reruns exact-head CI;
4. merges via normal merge commit;
5. verifies resulting `master`;
6. records the batch in parent `integration_history`;
7. returns the parent to `ACTIVE`.

## 12. Repository map

- `frontend/` — active Next.js product
- `backend/` — supporting Python service/research backend
- `KREATE/` — PMR/evidence/application/hardware operating system
- `docs/` — maintained technical/product documentation
- `scripts/` — validators and agent-fabric tooling
- `.agents/` — machine-readable coordination/policy
- `legacy/` — historical experiments; not active architecture by default

## 13. Good first child tasks

Good:

```text
validate one decision edge case
red-team one application claim against evidence IDs
compare two measurement architectures
prepare one interview guide for one stakeholder type
add one missing failure-mode test
check one BOM/sensor assumption against a source
```

Bad:

```text
improve everything
redo the whole architecture
make the pitch amazing
add AI everywhere
make hardware impressive
```

Bound the work so an agent can own it, test it, and fan it into the parent without creating hidden conflicts.

## Primary references

- [`development-workflow.md`](development-workflow.md)
- [`../AGENTS.md`](../AGENTS.md)
- [`../.agents/FABRIC.md`](../.agents/FABRIC.md)
- [`../KREATE/ROLES/README.md`](../KREATE/ROLES/README.md)
- [`../KREATE/ROLES/USER_DECISION_CHECKPOINT_PROTOCOL.md`](../KREATE/ROLES/USER_DECISION_CHECKPOINT_PROTOCOL.md)
