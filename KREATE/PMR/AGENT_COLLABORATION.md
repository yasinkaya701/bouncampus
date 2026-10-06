# PMR Agent Collaboration Contract

**Updated:** 2026-10-06  
**Purpose:** let IE, EE/EHB, CS1, CS2 and research agents contribute to one cumulative PMR knowledge base without duplicating work or corrupting the evidence boundary.

---

# 1. Shared rule

Every agent may add research. No agent may silently convert secondary research into PMR evidence.

```text
public source != interview
academic paper != customer validation
vendor claim != independent result
planned contact != completed interview
team belief != persona priority
model output != pilot evidence
```

Only completed real stakeholder conversations can create `E-INT-*` entries.

---

# 2. Canonical shared surfaces

Use these files instead of creating parallel one-off source dumps:

- [README.md](./README.md) — hub entry point / truth boundary
- [SOURCE_REGISTRY.md](./SOURCE_REGISTRY.md) — human-readable cumulative registry
- [source_registry.json](./source_registry.json) — agent-readable cumulative registry
- [ARTIFACT_INDEX.md](./ARTIFACT_INDEX.md) — PDFs/XLSX/images/data
- [SECONDARY_RESEARCH_SYNTHESIS_2026-10-06.md](./SECONDARY_RESEARCH_SYNTHESIS_2026-10-06.md) — current synthesis
- [INTERVIEW_TRACKER.md](./INTERVIEW_TRACKER.md) — real outreach/scheduling/completion
- [INTERVIEW_TEMPLATE.md](./INTERVIEW_TEMPLATE.md) — one file/copy per real interview
- [HYPOTHESIS_FALSIFICATION_MATRIX.md](./HYPOTHESIS_FALSIFICATION_MATRIX.md) — H1–H6

For a promotable claim, route through [../EVIDENCE.md](../EVIDENCE.md). For hypothesis state, use [../ASSUMPTIONS.md](../ASSUMPTIONS.md). For durable product/application decisions, use [../DECISIONS.md](../DECISIONS.md).

---

# 3. Source-ID ownership

Use stable families:

| Prefix | Area | Typical owner |
| --- | --- | --- |
| `SRC-BU-*` | Boğaziçi official sources | IE / CS2 |
| `SRC-PMR-*` | PMR/customer-discovery method | IE |
| `SRC-MEAS-*` | waste measurement/public standards | EE / CS2 |
| `SRC-ACAD-*` | academic mechanism/model evidence | CS1 / CS2 |
| `SRC-TGT-*` | external university/PMR target sources | IE |
| `SRC-COMP-*` | vendor/competitor/incumbent | CS2 / IE |
| `SRC-PROC-*` | procurement/contract mechanics | IE / CS2 |
| `SRC-PRIV-*` | privacy/data governance | CS2 / EE |
| `SRC-HW-*` | sensing/hardware evidence | EE / EHB |
| `SRC-DATA-*` | datasets/data dictionaries | CS1 / IE |

Add new families only when needed.

Never renumber an existing ID because a source is removed. Mark it `SUPERSEDED` or `STALE`.

---

# 4. Required source entry

A new registry entry is not complete until it has:

```yaml
id:
class:
status:
publisher:
title:
date_or_year:
url:
artifact_type:
use:
does_not_prove:
maps_to:
verified_at:
owner_lane:
notes:
```

The most important fields are `use` and `does_not_prove`.

Bad:

> “Interesting paper about AI food waste.”

Good:

> “Shows turnstile + menu + calendar features have been used in an institutional forecasting study; does not prove those features are available or predictive at Boğaziçi.”

---

# 5. Dedupe protocol

Before adding any source:

1. search the exact URL in `SOURCE_REGISTRY.md` and `source_registry.json`;
2. search title/DOI;
3. prefer the primary/official publisher over a news/mirror page;
4. if two links are genuinely useful, keep one as canonical and list the other as an artifact/alternate URL;
5. if an old source is replaced, mark old status rather than deleting history.

Do not create a new research markdown file for every URL. Add a focused synthesis file only when multiple sources resolve a real decision.

---

# 6. Role-specific handoffs

## IE — Customer Discovery & Market

Own:

- interview target selection;
- PMR methodology;
- decision owner / freeze / current workflow;
- buyer/champion/veto;
- procurement/economic incentive discovery;
- cross-site beachhead repeatability;
- updating tracker and interview records.

Pull from other lanes, but do not ask CS1/EE to “validate” customer facts with technical work.

### Next IE asks

- identify Boğaziçi daily production/operations owner;
- identify contractor-side operations/settlement owner;
- secure one second-site operational interview;
- get concrete last-incident narratives.

## CS1 — Decision Intelligence

Own research on:

- current baseline/forecasting methods;
- target/data semantics;
- chronological decision utility;
- model/heuristic comparison;
- uncertainty/abstention;
- decision loss after PMR establishes consequence;
- data dictionary / sample schema.

### PMR handoff back to IE

Whenever CS1 needs a field, convert it into a stakeholder question:

> “Who owns this field, when is it available relative to freeze, and what decision uses it today?”

Do not infer data availability from public pages.

## EE / EHB — Measurement / physical systems

Own research on:

- waste-stage measurement;
- scale/camera/sensor feasibility;
- calibration;
- uncertainty;
- physical workflow;
- privacy-by-geometry;
- hardware only where a decision-critical measurement gap exists.

### PMR handoff back to IE

Ask operators:

- what is already measured;
- where a sensor can physically fit;
- what extra step staff will tolerate;
- what must be washable/food-safe/non-disruptive;
- whether sensing solves a real missing field.

Do not build hardware to compensate for an unvalidated decision.

## CS2 — Product strategy / evidence / application

Own:

- claim firewall;
- evidence synthesis;
- competitor/incumbent monitoring;
- public/procurement research;
- application mapping;
- value proposition hypothesis;
- pilot evidence gate.

### PMR handoff back to IE

Turn every application claim into:

```text
claim
current evidence class
missing primary fact
best stakeholder
falsifying answer
```

Do not smooth contradictions for pitch coherence.

---

# 7. Legacy/unmerged research branches

Known useful PMR-related branches include:

- `research/kreate-deep-pmr-market-20261004`
- `agent/campus-data-geo/bogazici-pmr-target-map`

They contain useful research surfaces, but they must **not** be merged wholesale merely to recover documentation.

Protocol:

1. mine a specific useful source/finding;
2. reverify it against the current official/primary source;
3. add it to this registry with a new stable source ID;
4. link the old branch only as provenance/context if useful;
5. do not import stale code, old assumptions or conflicting root files.

This keeps master merge-safe.

---

# 8. Interview collaboration

A completed interview should ideally have:

- one lead interviewer;
- one note-taker;
- one post-interview reviewer from a different lane when high-impact.

Within the same day:

1. create/fill the interview record;
2. preserve exact quotes separately from interpretation;
3. tag hypotheses supported/contradicted;
4. update tracker;
5. create `E-INT-*` only for narrow promotable claims;
6. preserve contradictions;
7. add referrals;
8. state what changed in product/application, if anything.

No AI agent should invent a missing quote, name, date or incident to make the record look complete.

---

# 9. Cross-role PMR question queue

Any agent who encounters an unresolved dependency should append it to the relevant hypothesis rather than silently assume it.

Examples:

| Lane | Technical/research uncertainty | Convert to PMR question |
| --- | --- | --- |
| CS1 | reservation signal usefulness | “At the freeze point, what reservation/count signal exists and how is it used today?” |
| CS1 | asymmetric loss | “What actually happens operationally when 100 portions are extra vs 100 portions short?” |
| EE | need for TrayGate | “Which waste stage cannot be measured reliably with current records/scales?” |
| EHB | camera placement | “Where can a capture point exist without slowing tray return or capturing unnecessary people?” |
| CS2 | buyer | “Who signs/approves a pilot or software purchase and who can veto it?” |
| CS2 | differentiation | “What present tool/workflow already solves this; what remains painful?” |
| IE | beachhead repeatability | “Would the same role/process/data/approval path exist at your second site?” |

---

# 10. Research quality gate

Before merging a research contribution, check:

- [ ] primary/official source preferred where possible;
- [ ] URL works and title/publisher match;
- [ ] date/version captured when material;
- [ ] source class is correct;
- [ ] vendor claims labeled as vendor claims;
- [ ] academic effect sizes are not projected onto BOUNCAMPUS;
- [ ] public source is not called PMR;
- [ ] “does not prove” boundary is explicit;
- [ ] duplicate source IDs/URLs avoided;
- [ ] source maps to a live hypothesis/question;
- [ ] PDF/XLSX/image added to artifact index if useful;
- [ ] no invented interview/contact fact;
- [ ] contradictions preserved.

---

# 11. Merge / conflict policy

The PMR registry is shared infrastructure and can become a conflict hotspot.

Prefer:

- one bounded research branch;
- append-only new source IDs;
- small logical commits;
- update both markdown and JSON registry in the same PR when adding sources;
- avoid unrelated changes to root config, lockfiles or product code.

If multiple agents are researching simultaneously:

1. claim a source family or hypothesis area in the coordination issue/PR;
2. do not edit the same table block unless necessary;
3. use new source IDs;
4. rebase/sync before final merge;
5. resolve by preserving both non-duplicate sources rather than choosing based on author.

---

# 12. Definition of done for this hub

This hub is healthy when another agent can answer, without re-browsing:

- What are the strongest current sources?
- Which are official vs academic vs vendor?
- Where are the PDFs/XLSX/images?
- What does each source legitimately support?
- What must we **not** infer?
- Which PMR question does it create?
- Which stakeholder should answer it?
- What remains UNKNOWN?
- Where does a completed interview get promoted?

The hub should grow cumulatively, but its value is **decision quality**, not link count.
