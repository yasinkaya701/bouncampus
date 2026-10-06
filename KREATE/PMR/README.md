# PMR Knowledge Base

**Owner surface:** IE / Customer Discovery & Market, with CS2 evidence synthesis support  
**Updated:** 2026-10-06  
**Status:** cumulative PMR + VPMR research workspace. Public/secondary research is **not** Primary Market Research evidence.

This directory is the canonical entry point for KREATE Primary Market Research. Concurrent agent work created complementary research views on 2026-10-06; both are preserved here rather than choosing one and losing provenance.

## Read first

### Current cumulative synthesis
1. [PMR_KNOWLEDGE_BASE_2026-10-06.md](PMR_KNOWLEDGE_BASE_2026-10-06.md) — current synthesis, Boğaziçi facts, unresolved questions and interview priorities.
2. [SOURCE_REGISTRY_2026-10-06.json](SOURCE_REGISTRY_2026-10-06.json) — dated machine-readable source/provenance snapshot.
3. [ASSET_AND_MEDIA_INDEX_2026-10-06.md](ASSET_AND_MEDIA_INDEX_2026-10-06.md) — raw data, PDFs, official images and media links.

### Stable source-library view
4. [SOURCE_LIBRARY.md](SOURCE_LIBRARY.md) — human-readable source catalog with stable IDs.
5. [source_catalog.json](source_catalog.json) — machine-readable stable-ID catalog.
6. [CLAIM_SOURCE_MATRIX.md](CLAIM_SOURCE_MATRIX.md) — source-to-hypothesis firewall and exact PMR gaps.
7. [ASSET_MANIFEST.md](ASSET_MANIFEST.md) — asset/license/provenance policy.
8. [AGENT_HANDOFF.md](AGENT_HANDOFF.md) — IE/EE-EHB/CS1/CS2 reuse and append contract.
9. [DATA_SOURCE_INVENTORY.md](DATA_SOURCE_INVENTORY.md) — public/context signals vs source-owned operational truth and dataset promotion gates.

### Real PMR execution
10. [HYPOTHESIS_FALSIFICATION_MATRIX.md](HYPOTHESIS_FALSIFICATION_MATRIX.md) — neutral tests and reject/support criteria.
11. [INTERVIEW_TEMPLATE.md](INTERVIEW_TEMPLATE.md) — one copy per real interview.
12. [INTERVIEW_TRACKER.md](INTERVIEW_TRACKER.md) — interview execution tracker; planned slots are not evidence.

### VPMR research layer
13. [../VPMR/README.md](../VPMR/README.md) — verifiable secondary-research layer.
14. [../VPMR/SOURCE_REGISTRY.md](../VPMR/SOURCE_REGISTRY.md) / [../VPMR/source_registry.json](../VPMR/source_registry.json) — canonical-link registry.
15. [../VPMR/DATASETS.md](../VPMR/DATASETS.md) — public/reference/private-required data map.
16. [../VPMR/PMR_GUIDE.md](../VPMR/PMR_GUIDE.md) — H-001…H-006 interview/falsification conversion.
17. [../VPMR/VISUALS_AND_PDFS.md](../VPMR/VISUALS_AND_PDFS.md) — PDF/visual index.
18. [../VPMR/AGENT_HANDOFF.md](../VPMR/AGENT_HANDOFF.md) — stale-branch recut/dedupe rules.

The two machine-readable registries intentionally have different namespaces (`SRC-*`/stable catalog and `VPMR-SRC-*`/VPMR registry). Do not silently collapse IDs. Future consolidation should preserve aliases/provenance.

## Evidence firewall

| Class | Meaning | Can it close a PMR hypothesis? |
| --- | --- | --- |
| `REAL_PMR` | Real interview/observation/test with a target stakeholder | Yes, when provenance and notes exist |
| `PUBLIC_OFFICIAL` / `PUBLIC_CONTEXT` | University, government, standards or procurement artifact | No; context and public facts only |
| `ACADEMIC` / `ACADEMIC_ANALOGUE` | Peer-reviewed external evidence | No; benchmark/mechanism context |
| `METHOD_REFERENCE` / `STANDARD_METHOD` | Research or measurement methodology | No |
| `REFERENCE_DATASET` | External/sandbox dataset | No |
| `VENDOR_CLAIM` | Competitor/vendor material | No |
| `REPO_SYNTHESIS` | Internal synthesis | No; trace to original sources |

A web page, PDF, spreadsheet, tender, benchmark paper, model run, synthetic dataset or AI summary does **not** become PMR because it is useful.

## Current decision boundary

The active wedge is not “AI predicts cafeteria traffic.” The useful chain is:

```text
real pre-service signals
→ semantic reconciliation
→ reachable quantity/service decision before freeze
→ transparent operator/baseline comparison
→ model complexity only if earned
→ human-reviewed bounded recommendation
→ prospective accepted/service/waste outcome
→ traceable evidence promotion
```

Modify or kill the wedge if real PMR shows that the decision is unreachable, arrives after useful freeze, dominant avoidable waste is unrelated to the decision, the user cannot act, reliable outcome measurement is unavailable, or a simple baseline is already adequate.

## Highest-value unresolved PMR questions

- Who sets or approves service-level production/allocation quantity?
- At what exact time does it become practically fixed?
- What signals are actually known before that cutoff?
- What heuristic/system is used today?
- Which count drives contractor settlement/hakediş?
- Who bears the cost of excess and the consequence of shortage?
- What do BUCampus/BUCard/reservation/turnstile/payment/served fields actually mean?
- Can planned, produced, served, unserved surplus, discard and plate waste be separated?
- What fraction of waste is causally reachable by the quantity decision?
- Who is user, approver, source owner, buyer, beneficiary and veto holder?
- Does the same workflow repeat at a second institutional site?

## Cross-agent rule

**IE:** owns real interviews, workflow/persona/buyer mapping and contradictions.  
**CS1:** consumes only semantically admitted, cutoff-valid fields and establishes transparent baselines first.  
**CS2:** owns claim/evidence consistency, application narrative and kill/modify gates.  
**EE/EHB:** owns physical measurement boundary/calibration only where existing records cannot close the decision-critical gap.

Before adding another source dump, search both current registries. Add research only when it identifies a better PMR target, resolves contract/data/measurement semantics, narrows differentiation, or changes a real decision.

## Current PMR execution target

The tracker targets **16 distinct interviews** with a hard minimum of **12**. This is an execution target, not evidence that interviews occurred.

Priority roles: Food Services/operations; contractor/central-kitchen planning; food engineer/production planner; control/verification; aggregate data/reporting owner; waste measurement owner; procurement/contract/hakediş owner; and at least one comparable external institution.

## Current-master research references

- [../RESEARCH/CS2_CURRENT_MASTER_RECUT_2026-10-06.md](../RESEARCH/CS2_CURRENT_MASTER_RECUT_2026-10-06.md)
- [../RESEARCH/CS2_PILOT_EVIDENCE_GATE_2026-10-06.md](../RESEARCH/CS2_PILOT_EVIDENCE_GATE_2026-10-06.md)
- [../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md](../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md)
- [../RESEARCH/HIGHEST_INFORMATION_VALUE_QUEUE_2026-10-05.md](../RESEARCH/HIGHEST_INFORMATION_VALUE_QUEUE_2026-10-05.md)
- [../RESEARCH/CROSS_UNIVERSITY_WORKFLOW_REPEATABILITY_2026-10-05.md](../RESEARCH/CROSS_UNIVERSITY_WORKFLOW_REPEATABILITY_2026-10-05.md)
- [../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md](../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md)

Every meaningful claim must remain falsifiable and traceable.
