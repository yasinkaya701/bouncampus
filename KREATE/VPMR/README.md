# VPMR — Verifiable PMR Research Base

**Status:** living secondary-research and source-provenance layer for KREATE PMR.

> Working convention in this repository: **VPMR** means the verifiable/validated-source research base that supports Primary Market Research. It does **not** replace interviews, observations, pilots, or source-owner confirmation. Public/academic/market research is context and hypothesis support, never customer validation by itself.

## Why this directory exists

The repository had strong research scattered across stale research and agent branches, while the current KREATE evidence system correctly prevents secondary research from being promoted into PMR. This directory creates one current-master-compatible, cumulative place where agents can:

- find canonical public/academic/standards sources;
- see exactly what each source can and cannot support;
- find PDFs, graphics, datasets and machine-readable endpoints;
- translate desk research into interview questions and acquisition tasks;
- avoid re-researching the same topic;
- preserve provenance when a source changes;
- coordinate with IE, EE/EHB, CS1 and CS2 without wholesale-merging stale branches.

## Truth boundary

Use these categories consistently:

| Class | Meaning | Can close PMR? | Typical use |
| --- | --- | --- | --- |
| `PUBLIC_CONTEXT` | official/public institutional facts | No | scale, process clues, baseline context |
| `STANDARD_METHOD` | methodology/measurement standard | No | pilot and measurement design |
| `ACADEMIC_ANALOGUE` | peer-reviewed external evidence | No | candidate mechanisms/features/interventions |
| `REFERENCE_DATASET` | external data for sandbox/model plumbing | No | pipeline tests, schema design, benchmarking mechanics |
| `ARCHIVED_DECISION_INPUT` | data that can represent what was knowable at decision time | No, but can support technical backtests | leakage-safe feature construction |
| `INTERNAL_REQUIRED` | university/contractor data that must be acquired and semantically verified | Only after real acquisition/attestation | service truth and pilot evidence |
| `INTERVIEW_EVIDENCE` | real documented stakeholder conversation | Yes, narrowly | PMR claim support/contradiction |

Never convert `PUBLIC_CONTEXT`, `STANDARD_METHOD`, `ACADEMIC_ANALOGUE`, or `REFERENCE_DATASET` into `INTERVIEW_EVIDENCE`.

## Start here

1. [SOURCE_REGISTRY.md](./SOURCE_REGISTRY.md) — human-readable canonical source registry.
2. [source_registry.json](./source_registry.json) — machine-readable version for agents/scripts.
3. [DATASETS.md](./DATASETS.md) — data/source inventory with granularity, leakage and intended-use boundaries.
4. [PMR_GUIDE.md](./PMR_GUIDE.md) — research-to-interview conversion mapped to H-001…H-006.
5. [VISUALS_AND_PDFS.md](./VISUALS_AND_PDFS.md) — PDFs, diagrams, graphics and reuse notes.
6. [AGENT_HANDOFF.md](./AGENT_HANDOFF.md) — cross-agent contribution and stale-branch reconciliation rules.

## Current synthesis — what desk research actually says

### High-confidence public context

- Boğaziçi publicly reports a material campus dining operation and a 2025 food-waste baseline.
- Meals are centrally prepared in the North Campus kitchen, while service occurs across multiple dining halls/channels.
- Public menu, calendar, menu-voting, reservation-period and dining-operation pages show that useful pre-service context signals can exist.
- A short Kilyos reservation workflow proves that reservation intent can exist operationally, but it must not be generalized to all campuses or dates.

### What remains unresolved by desk research

- who owns the daily production/allocation quantity decision;
- when that decision freezes and what can still change afterward;
- whether demand mismatch is a material cause of avoidable waste at Boğaziçi;
- what service-level produced/served/surplus/waste records exist and who owns them;
- whether turnstile/payment/reservation events can be exported in privacy-safe aggregate form and what each event semantically means;
- how the university/contractor contract allocates excess-production and shortage risk;
- whether a recommendation would change a real operator action;
- whether a second institutional site has a sufficiently similar workflow to justify a repeatable beachhead.

Those questions require PMR and/or admitted operational artifacts.

## Research priority order

1. **Decision owner + freeze time** — highest information value.
2. **Service-truth schema + source owner** — produced, served, surplus/waste, shortage/sell-out.
3. **Event semantics** — reservation, turnstile entry, card transaction, served meal, settlement are not interchangeable.
4. **Physical measurement boundary** — distinguish preparation, unserved surplus and plate/post-consumer waste when possible.
5. **Economic consequence** — who gains/loses when 100 unnecessary portions are avoided?
6. **Repeatability** — test one second site/contractor workflow before claiming a scalable beachhead.

## Contribution rule

Add new sources to both `SOURCE_REGISTRY.md` and `source_registry.json`. Every entry must include:

- stable source ID;
- title/publisher;
- source class;
- canonical URL;
- publication/update date when known;
- access date;
- narrow factual summary;
- relevance to a named hypothesis/decision;
- explicit `can_support` and `cannot_support` boundaries;
- PDF/visual/data links when available;
- licensing/reuse note;
- verification status.

Prefer canonical publisher URLs. Mirror sites may be useful discovery aids, but material application claims should use an official source or be labeled accordingly.

## Asset policy

Default to **linking** PDFs and graphics rather than vendoring binaries. Add a binary to the repository only when its license/terms permit redistribution, it is stable enough to justify versioning, and the local copy adds reproducibility value. For every copied asset, preserve source URL, license/credit and retrieval date.

## Relationship to KREATE evidence registry

This directory is a research library. It does **not** automatically create `E-PUB-*`, `E-INT-*`, `E-TECH-*`, or `E-MODEL-*` evidence. Promote a source into `KREATE/EVIDENCE.md` only for a narrow application claim that needs it, following the existing evidence rules and human re-verification gate.

Last curated: **2026-10-06**.
