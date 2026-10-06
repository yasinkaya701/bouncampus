# PMR Knowledge Base

**Status:** Cumulative research and customer-discovery support layer  
**Maintainer:** IE / Customer Discovery & Market  
**Last structural update:** 2026-10-06

This directory is the canonical, cumulative source and Primary Market Research (PMR) workspace for the KREATE dining wedge.

## Evidence firewall

**Secondary research is not PMR evidence.**

Only direct primary evidence can promote a customer/workflow claim:
- completed stakeholder interview;
- direct observation;
- verified operational artifact/data;
- measured pilot/field evidence.

Official pages, academic papers, procurement records, standards, vendor materials and other web sources may:
- identify interview targets;
- falsify novelty claims;
- define measurement methods;
- establish external mechanism plausibility;
- generate questions and hypotheses;
- constrain product/market claims.

They must not be relabeled as customer validation, willingness to pay, Boğaziçi workflow confirmation, or measured impact.

## Canonical files

| File | Purpose |
| --- | --- |
| [HYPOTHESIS_FALSIFICATION_MATRIX.md](HYPOTHESIS_FALSIFICATION_MATRIX.md) | Pre-committed PMR hypotheses, neutral prompts, support/reject criteria |
| [INTERVIEW_TEMPLATE.md](INTERVIEW_TEMPLATE.md) | One record per real interview |
| [INTERVIEW_TRACKER.md](INTERVIEW_TRACKER.md) | Scheduling/completion tracker; a slot is not evidence |
| [SOURCE_LIBRARY.md](SOURCE_LIBRARY.md) | Human-readable cumulative source index |
| [source_catalog.json](source_catalog.json) | Machine-readable source registry with stable IDs |
| [CLAIM_SOURCE_MATRIX.md](CLAIM_SOURCE_MATRIX.md) | What secondary evidence supports, what it cannot establish, and the exact PMR gap |
| [ASSET_MANIFEST.md](ASSET_MANIFEST.md) | PDF/image/data asset links, reuse status, provenance and repo-copy policy |
| [AGENT_HANDOFF.md](AGENT_HANDOFF.md) | Cross-agent ownership, consumption and append rules |

## Stable source IDs

Use these prefixes:
- `S-PMR-*` — PMR method / customer-discovery method
- `S-BU-*` — Boğaziçi official/public sources
- `S-TR-*` — other Türkiye university/sector sources
- `S-MEAS-*` — measurement / standards
- `S-ACAD-*` — academic literature
- `S-COMP-*` — competitor/incumbent sources
- `S-INT-*` — internal repository/agent provenance

Never recycle an ID for a different source. If a URL or source materially changes, append a new version/source row rather than silently overwriting history.

## Minimum source record

Every new source should capture:
- stable ID;
- title;
- source type;
- publisher/author;
- canonical URL;
- direct PDF/data/asset URL when available;
- publication/update date when known;
- access date;
- authority level;
- reuse/license note;
- hypotheses/questions informed;
- supported claim;
- limitation / forbidden inference;
- next primary-research action.

## Authority order

Prefer, in order:
1. primary operational evidence;
2. authoritative first-party official sources / standards;
3. peer-reviewed research and trusted repositories;
4. public procurement/legal records;
5. vendor first-party capability pages;
6. secondary summaries.

Vendor outcome claims stay vendor claims unless independently verified.

## Cumulative update rule

A new agent should:
1. search this catalog before adding a source;
2. reuse the existing source ID if it is exactly the same artifact;
3. add a new row for a materially newer edition or distinct artifact;
4. update the claim-source matrix only when the new source changes a decision;
5. add direct asset links and reuse notes to the asset manifest;
6. preserve contradictions and unknowns;
7. never convert secondary evidence into `E-INT-*` interview evidence.

## Current PMR priority

The highest-value unresolved chain is:

```text
quantity decision owner
→ decision/freeze timestamp
→ signals available before freeze
→ current heuristic/system
→ excess vs shortage consequence
→ settlement/economic beneficiary
→ measurable service-level outcome
```

Until that chain is verified for Boğaziçi/TEMAŞ through primary evidence, model sophistication and impact percentages remain downstream hypotheses.
