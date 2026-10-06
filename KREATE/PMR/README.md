# PMR Research Hub

**Updated:** 2026-10-06  
**Owner:** IE — Customer Discovery & Market Lead  
**Scope:** cumulative, source-traceable preparation layer for KREATE Primary Market Research.

This directory is the shared entry point for PMR preparation. It keeps public/secondary research, real interviews, source provenance, data artifacts and cross-role handoffs connected **without upgrading research into customer evidence**.

## Evidence firewall

Secondary/public research is **not Primary Market Research**.

Use these classes consistently:

- \`PUBLIC_OFFICIAL\` — university, public-body, standards or policy source;
- \`ACADEMIC\` — peer-reviewed/scholarly source;
- \`METHOD_REFERENCE\` — research/PMR methodology;
- \`VENDOR_CLAIM\` — vendor-published capability only;
- \`PUBLIC_PROCUREMENT\` — tender/contract/decision artifact;
- \`REAL_PMR\` — a completed conversation/observation with a target stakeholder;
- \`TECHNICAL_TEST\` — measured technical result;
- \`REPO_ARTIFACT\` — what the repository says/implements;
- \`HYPOTHESIS\` / \`UNKNOWN\` — unresolved proposition/fact.

Only a real completed interview can create \`E-INT-*\` evidence in \`../EVIDENCE.md\`. A paper, official webpage, tender, vendor page, PDF, spreadsheet, model run or AI summary may shape questions and falsifiers; it cannot prove Boğaziçi pain, decision authority, adoption, willingness to pay, product-market fit, service-level causality or live-data access.

## Canonical files

- [SOURCE_REGISTRY.json](./SOURCE_REGISTRY.json) — machine-readable cumulative source registry with stable IDs.
- [SECONDARY_RESEARCH_INDEX.md](./SECONDARY_RESEARCH_INDEX.md) — curated synthesis, falsification pressure, open questions and role handoffs.
- [PDF_VISUAL_REFERENCE_MANIFEST.md](./PDF_VISUAL_REFERENCE_MANIFEST.md) — direct report/PDF/visual/data references and reuse rules.
- [data/bogazici_food_waste_2025_official.csv](./data/bogazici_food_waste_2025_official.csv) — official **aggregate** 2025 monthly snapshot, never service truth.
- [SOURCE_ENTRY_TEMPLATE.md](./SOURCE_ENTRY_TEMPLATE.md) — append/dedupe/provenance contract for future agents.
- [INTERVIEW_TEMPLATE.md](./INTERVIEW_TEMPLATE.md) — one copy per real interview.
- [INTERVIEW_TRACKER.md](./INTERVIEW_TRACKER.md) — scheduling/completion tracker; slots are not evidence.
- [HYPOTHESIS_FALSIFICATION_MATRIX.md](./HYPOTHESIS_FALSIFICATION_MATRIX.md) — executable PMR H1–H6 tests.

Canonical truth stores remain:

- [../EVIDENCE.md](../EVIDENCE.md) — narrow promotable claims;
- [../ASSUMPTIONS.md](../ASSUMPTIONS.md) — hypothesis states;
- [../DECISIONS.md](../DECISIONS.md) — durable KEEP/MODIFY/KILL decisions;
- [../STATUS.md](../STATUS.md) — current state/gaps;
- [../APPLICATION_RUBRIC.md](../APPLICATION_RUBRIC.md) — application evidence gate.

## Current-master research to reuse

Do not duplicate these focused packs:

- [../RESEARCH/HIGHEST_INFORMATION_VALUE_QUEUE_2026-10-05.md](../RESEARCH/HIGHEST_INFORMATION_VALUE_QUEUE_2026-10-05.md)
- [../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md](../RESEARCH/FOOD_WASTE_MEASUREMENT_STANDARD_RESEARCH_2026-10-05.md)
- [../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md](../RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md)
- [../RESEARCH/CROSS_UNIVERSITY_WORKFLOW_REPEATABILITY_2026-10-05.md](../RESEARCH/CROSS_UNIVERSITY_WORKFLOW_REPEATABILITY_2026-10-05.md)
- [../RESEARCH/ECONOMIC_BUYER_AND_INCENTIVE_ARCHETYPES_2026-10-05.md](../RESEARCH/ECONOMIC_BUYER_AND_INCENTIVE_ARCHETYPES_2026-10-05.md)
- [../RESEARCH/TURKIYE_CATERING_SOFTWARE_UPDATE_2026-10-05.md](../RESEARCH/TURKIYE_CATERING_SOFTWARE_UPDATE_2026-10-05.md)
- [../RESEARCH/CS2_CURRENT_MASTER_RECUT_2026-10-06.md](../RESEARCH/CS2_CURRENT_MASTER_RECUT_2026-10-06.md)
- [../RESEARCH/CS2_PILOT_EVIDENCE_GATE_2026-10-06.md](../RESEARCH/CS2_PILOT_EVIDENCE_GATE_2026-10-06.md)

Historical branches such as \`research/kreate-deep-pmr-market-20261004\` and \`agent/campus-data-geo/bogazici-pmr-target-map\` contain useful prior work but are **reference archives** because they diverged substantially from current master. Reverify and recut the smallest useful artifact; never wholesale-merge stale ancestry.

## Highest-information PMR stack

Until real interviews/artifacts close them, keep these \`UNKNOWN\`:

1. Who chose/approved the quantity for the last real service?
2. What exact time/condition is the last meaningful adjustment point?
3. Is production one fixed quantity or a batch/replenishment sequence?
4. What heuristic/software/reservation/report is used today?
5. What happened in the last material mismatch?
6. How much waste is preparation loss vs unserved edible surplus vs plate waste?
7. What happens when food runs out and who bears the consequence?
8. What quantity determines settlement/hakediş and who bears excess-production cost?
9. Which service-level fields exist, who owns them, and at what export granularity?
10. Who can approve a pilot, veto it, use it, and buy/mandate it?
11. Does the same workflow/product repeat at a second institution?
12. Does the proposed differentiation matter to the operator/buyer?

The first operational data dependency is tracked in **#292**. Public evidence that BUCard/dining reports exist is not evidence that the team can export or semantically reconcile service-level rows. CS1 admission remains **#82** via \`scripts/cs1_service_truth_artifact_intake.py\`.

## Cross-role handoff

**IE** owns real interviews, last-incident stories, workflow/persona mapping, referrals, contradictions and institutional access.

**CS1** consumes only semantically admitted fields, defines the cheapest transparent baseline first, and keeps generated/demo data outside measured evidence.

**CS2** owns claim/evidence consistency, economic-buyer logic, application synthesis and product kill/modify gates.

**EE** owns waste/physical measurement boundary, calibration, uncertainty and field-verification semantics.

**EHB** implements measurement/device integration only after the decision-critical measurement gap survives IE/EE gates; public sources do not create bench/field evidence.

## Cumulative contribution flow

\`\`\`text
new source
  ↓
dedupe by canonical URL / DOI / report identity
  ↓
verify publisher + date + source class
  ↓
assign stable SRC-* ID
  ↓
record a narrow "use" and "does not prove" boundary
  ↓
link PDF/data/visual assets instead of copying when rights are unclear
  ↓
map to H1–H6 / buyer / measurement / repeatability questions
  ↓
turn finding into a neutral interview prompt or falsifier
  ↓
only after a real interview: promote narrow E-INT evidence
\`\`\`

Do not silently delete old sources. Mark them stale/superseded/conflicted and point to the newer source. Preserve contradictory evidence.

## Research stop rule

Do more secondary research only when it identifies a high-information target, clarifies authoritative contract/procurement mechanics, kills/narrows a novelty claim, clarifies measurement/privacy constraints, identifies a current incumbent/workflow, or surfaces a reusable dataset/report for a concrete hypothesis.

The bottleneck is now **customer/operational truth**, not link volume.
