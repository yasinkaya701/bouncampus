# PMR Knowledge Base

**Owner surface:** IE / Customer Discovery, with CS2 evidence synthesis support  
**Updated:** 2026-10-06  
**Status:** cumulative research index; public/secondary research is **not** Primary Market Research evidence.

This directory is the canonical entry point for KREATE Primary Market Research work. It keeps the research layer, real interview layer, source provenance, and reusable assets connected without promoting public web research into customer evidence.

## Read first

1. [PMR_KNOWLEDGE_BASE_2026-10-06.md](PMR_KNOWLEDGE_BASE_2026-10-06.md) — current cumulative synthesis, Boğaziçi facts, unresolved questions, and interview priorities.
2. [SOURCE_REGISTRY_2026-10-06.json](SOURCE_REGISTRY_2026-10-06.json) — machine-readable source/provenance registry.
3. [ASSET_AND_MEDIA_INDEX_2026-10-06.md](ASSET_AND_MEDIA_INDEX_2026-10-06.md) — direct PDFs, raw data, official images, and external references.
4. [HYPOTHESIS_FALSIFICATION_MATRIX.md](HYPOTHESIS_FALSIFICATION_MATRIX.md) — neutral hypothesis tests and reject/support criteria.
5. [INTERVIEW_TEMPLATE.md](INTERVIEW_TEMPLATE.md) — one copy per real interview.
6. [INTERVIEW_TRACKER.md](INTERVIEW_TRACKER.md) — interview execution tracker; planned slots are not evidence.

Relevant current-master research:
- [../RESEARCH/CS2_CURRENT_MASTER_RECUT_2026-10-06.md](../RESEARCH/CS2_CURRENT_MASTER_RECUT_2026-10-06.md)
- [../RESEARCH/CS2_PILOT_EVIDENCE_GATE_2026-10-06.md](../RESEARCH/CS2_PILOT_EVIDENCE_GATE_2026-10-06.md)
- [../RESEARCH/DISCIPLINED_ENTREPRENEURSHIP_ALIGNMENT_2026-10-05.md](../RESEARCH/DISCIPLINED_ENTREPRENEURSHIP_ALIGNMENT_2026-10-05.md)
- [../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md](../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md)
- [../RESEARCH/ECONOMIC_BUYER_AND_INCENTIVE_ARCHETYPES_2026-10-05.md](../RESEARCH/ECONOMIC_BUYER_AND_INCENTIVE_ARCHETYPES_2026-10-05.md)
- [../RESEARCH/HIGHEST_INFORMATION_VALUE_QUEUE_2026-10-05.md](../RESEARCH/HIGHEST_INFORMATION_VALUE_QUEUE_2026-10-05.md)
- [../RESEARCH/CROSS_UNIVERSITY_WORKFLOW_REPEATABILITY_2026-10-05.md](../RESEARCH/CROSS_UNIVERSITY_WORKFLOW_REPEATABILITY_2026-10-05.md)
- [../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md](../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md)

## Evidence firewall

Use these classes consistently:

| Class | Meaning | Can it close a PMR hypothesis? |
| --- | --- | --- |
| `REAL_PMR` | Real interview/observation/test with a target stakeholder | Yes, when provenance and notes exist |
| `PUBLIC_OFFICIAL` | University, government, standards body, procurement or official public artifact | No; it informs questions and verifies public facts |
| `ACADEMIC` | Peer-reviewed or scholarly external evidence | No; benchmark/context only |
| `METHOD_REFERENCE` | PMR/research methodology source | No |
| `VENDOR_CLAIM` | Competitor/vendor material | No; capability claim only |
| `REPO_SYNTHESIS` | Internal synthesis of admitted sources | No; trace to original sources |

A web page, PDF, spreadsheet, tender, benchmark paper, model run, synthetic dataset, or AI summary does **not** become PMR because it is useful. Real customer discovery remains separately evidenced in interview records and `KREATE/EVIDENCE.md`.

## Cumulative update protocol

When any agent finds a useful source:

1. Add a stable `SRC-...` record to `SOURCE_REGISTRY_2026-10-06.json`.
2. Preserve publisher, canonical URL, retrieval date, source class, PMR status, key usable facts, caveats, and direct asset links.
3. Add the source to `ASSET_AND_MEDIA_INDEX_2026-10-06.md` if it exposes a PDF, raw data file, image, worksheet, standard, or reusable visual.
4. Update the knowledge base only with claims traceable to one or more source IDs.
5. Never silently delete a source. Mark it `superseded`, `stale`, or `conflicted` and point to the newer source.
6. Preserve contradictions. A contradiction is a research result, not a cleanup problem.
7. For any downloaded binary later added to the repository, record origin URL, retrieval date, license/permission, and checksum. Prefer links when redistribution rights are unclear.

## Current decision boundary

The active dining wedge is not “AI predicts cafeteria traffic.” The useful chain is:

```text
real pre-service signals
→ semantically reconcile them
→ identify a reachable quantity/service decision before freeze
→ compare against the cheapest transparent baseline
→ add model complexity only if it earns its place
→ human-reviewed bounded recommendation
→ prospective physical/service outcome measurement
→ traceable evidence promotion
```

The product direction must be modified or killed if PMR shows that the quantity decision is unreachable, arrives after the useful freeze point, the dominant waste cause is unrelated to the decision, or reliable outcome measurement is unavailable.

## Highest-value unresolved PMR questions

These remain **UNKNOWN until real interviews/artifacts close them**:

- Who sets or approves the service-level production quantity?
- At what exact time does that quantity become practically fixed?
- Which quantity/count is used for contractor settlement or hakediş?
- Who bears the economic consequence of excess and of shortage?
- What heuristic/baseline is actually used today?
- Which pre-service aggregate signals are available before freeze?
- What does each BUCampus/BUCard/entry/reporting field semantically mean?
- Can planned, produced, served, surplus, discard and plate-waste stages be separated?
- What fraction of current waste is actually causally reachable by changing production quantity?
- What evidence would operators trust enough to change a quantity?
- Who is the user, approver, data owner, economic buyer, and veto holder?

## Cross-agent handoff

**IE:** own real interviews, incident stories, workflow/persona mapping, referrals, contradictions, and evidence IDs. Do not ask only whether stakeholders “like the idea.”

**CS1:** consume only semantically admitted fields; define operator baseline before a model; keep synthetic/demo data out of measured evidence; use asymmetric loss only when shortage/surplus consequences are supported.

**CS2:** maintain claim/evidence consistency, buyer/incentive logic, pilot ladder, application narrative, and kill/modify criteria. Public research cannot be rewritten as customer validation.

**EE / EHB:** enter only where a decision-critical physical field is missing or unreliable. Own measurement boundary, calibration, uncertainty, timing, failure modes, and device integration. Do not build sensing for fields that reliable existing reports already provide.

## PMR execution target

The current tracker targets **16 distinct interviews** with a hard minimum of **12**, distributed across the four human-owned workstreams. This is an execution target, not evidence that any interview happened.

The first high-information roles should cover:
- university Food Services / dining operations;
- contractor project or central-kitchen operations;
- food engineer / production planner;
- dining control / verification;
- aggregate data/reporting system owner;
- waste/sustainability measurement owner;
- procurement/contract/hakediş owner;
- at least one comparable external institution to test repeatability.

## Source quality rule

Prefer, in order:
1. current official artifact directly describing the operating fact;
2. current legal/procurement/standards artifact;
3. source-owner generated export/schema;
4. peer-reviewed evidence for external mechanisms/benchmarks;
5. vendor pages only for vendor capability claims;
6. general articles only as navigation clues.

Every meaningful claim should remain falsifiable and traceable.
