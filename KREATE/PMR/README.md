# PMR Research Hub

**Updated:** 2026-10-06  
**Owner:** IE — Customer Discovery & Market Lead  
**Scope:** cumulative source, artifact and research index supporting KREATE primary market research.

This directory is the shared entry point for PMR preparation. It exists so every human/agent can reuse the same verified sources, see what each source actually proves, avoid duplicate research, and route findings into interviews, assumptions, decisions and the application without silently upgrading secondary research into customer evidence.

## Evidence firewall

**Secondary/public research is not Primary Market Research.**

Use these classes consistently:

```text
PUBLIC SOURCE        official institutional/public-body source
ACADEMIC SOURCE      peer-reviewed or scholarly source
VENDOR SOURCE        vendor-published capability/claim
PUBLIC PROCUREMENT   tender / procurement / decision material
INTERVIEW EVIDENCE   real completed stakeholder conversation
TECHNICAL TEST       measured repo/lab result
REPO ARTIFACT        repository evidence or implementation artifact
HYPOTHESIS           unvalidated proposition
UNKNOWN              unresolved fact
```

Only a real completed interview can produce `E-INT-*` evidence. A strong paper, official webpage, tender or competitor page can shape questions and falsifiers; it cannot prove Boğaziçi pain, authority, adoption, willingness to pay, or product-market fit.

Canonical truth stores:

- [../EVIDENCE.md](../EVIDENCE.md) — narrow promotable claims;
- [../ASSUMPTIONS.md](../ASSUMPTIONS.md) — supported/rejected/unknown hypotheses;
- [../DECISIONS.md](../DECISIONS.md) — durable KEEP/MODIFY/KILL decisions;
- [../STATUS.md](../STATUS.md) — live execution state and gaps;
- [../APPLICATION_RUBRIC.md](../APPLICATION_RUBRIC.md) — application claim/evidence gate;
- [INTERVIEW_TEMPLATE.md](./INTERVIEW_TEMPLATE.md) — one copy per real interview;
- [INTERVIEW_TRACKER.md](./INTERVIEW_TRACKER.md) — real interview scheduling/completion only;
- [HYPOTHESIS_FALSIFICATION_MATRIX.md](./HYPOTHESIS_FALSIFICATION_MATRIX.md) — PMR hypotheses and pre-committed falsifiers.

## Hub files

- [SOURCE_REGISTRY.md](./SOURCE_REGISTRY.md) — human-readable cumulative registry with source IDs, URLs, uses, limitations and mapped hypotheses.
- [source_registry.json](./source_registry.json) — machine-readable version for agents/scripts.
- [ARTIFACT_INDEX.md](./ARTIFACT_INDEX.md) — direct PDF/XLSX/image/report/data links and copy/licensing rules.
- [SECONDARY_RESEARCH_SYNTHESIS_2026-10-06.md](./SECONDARY_RESEARCH_SYNTHESIS_2026-10-06.md) — current synthesis: what public evidence changes in PMR, what remains unknown and which interviews have the highest information value.
- [AGENT_COLLABORATION.md](./AGENT_COLLABORATION.md) — append/dedupe/provenance protocol and role handoffs.

## Existing research that should be reused, not duplicated

Current master already contains strong focused research:

- [../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md](../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md)
- [../RESEARCH/CROSS_UNIVERSITY_WORKFLOW_REPEATABILITY_2026-10-05.md](../RESEARCH/CROSS_UNIVERSITY_WORKFLOW_REPEATABILITY_2026-10-05.md)
- [../RESEARCH/DISCIPLINED_ENTREPRENEURSHIP_ALIGNMENT_2026-10-05.md](../RESEARCH/DISCIPLINED_ENTREPRENEURSHIP_ALIGNMENT_2026-10-05.md)
- [../RESEARCH/ECONOMIC_BUYER_AND_INCENTIVE_ARCHETYPES_2026-10-05.md](../RESEARCH/ECONOMIC_BUYER_AND_INCENTIVE_ARCHETYPES_2026-10-05.md)
- [../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md](../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md)
- [../RESEARCH/HIGHEST_INFORMATION_VALUE_QUEUE_2026-10-05.md](../RESEARCH/HIGHEST_INFORMATION_VALUE_QUEUE_2026-10-05.md)
- [../RESEARCH/TURKIYE_CATERING_SOFTWARE_UPDATE_2026-10-05.md](../RESEARCH/TURKIYE_CATERING_SOFTWARE_UPDATE_2026-10-05.md)
- [../RESEARCH/CS2_CURRENT_MASTER_RECUT_2026-10-06.md](../RESEARCH/CS2_CURRENT_MASTER_RECUT_2026-10-06.md)
- [../RESEARCH/CS2_PILOT_EVIDENCE_GATE_2026-10-06.md](../RESEARCH/CS2_PILOT_EVIDENCE_GATE_2026-10-06.md)

The registry points to these files where detailed analysis already exists.

## Current PMR question stack

The highest-value unresolved facts remain:

1. Who chose the quantity for the last real meal service?
2. What exact time/condition is the last meaningful adjustment point?
3. Is production one fixed quantity or a sequence of batches/replenishment decisions?
4. What current heuristic/software/reservation signal is used?
5. What was the last material mismatch and what physically happened?
6. How much waste is preparation loss vs unserved edible surplus vs plate waste?
7. What happens when food runs out; who absorbs the consequence?
8. What quantity determines settlement/payment and who absorbs excess-production cost?
9. Which service-level fields exist, who owns them, and at what granularity can they be exported?
10. Who can approve a pilot, who can veto it, and who could buy/mandate the tool?
11. Does the same product/workflow repeat at a second institution?
12. Does the proposed differentiation matter to the operator/buyer, or is it engineering preference?

Until interviews answer these, keep them `UNKNOWN`.

## Research stop rule

Do more secondary research only when it does at least one of the following:

- identifies a high-information interview target;
- clarifies an authoritative contract/procurement mechanism;
- kills or narrows a novelty claim;
- clarifies measurement/privacy/legal constraints;
- identifies a directly relevant incumbent/current workflow;
- surfaces a reusable dataset/report/artifact for a concrete hypothesis.

Do not browse for volume. The application needs customer truth more than another pile of links.

## Minimal contribution flow

```text
new source
  ↓
dedupe against SOURCE_REGISTRY / source_registry.json
  ↓
verify publisher + date + URL + source class
  ↓
write one narrow “supports / does not prove” statement
  ↓
map to H1–H6 or commercial/measurement/privacy question
  ↓
add artifact link if PDF/XLSX/image/data exists
  ↓
turn it into a neutral interview question/falsifier
  ↓
only after a real interview: create/promote E-INT evidence
```

See [AGENT_COLLABORATION.md](./AGENT_COLLABORATION.md) for the exact shared-work contract.
