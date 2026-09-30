# KREATE Evidence Registry

Every material application claim must point to one or more evidence IDs below or remain explicitly `HYPOTHESIS`/`UNKNOWN`.

Allowed evidence types: `PUBLIC_SOURCE`, `INTERVIEW`, `TECH_TEST`, `REPO_ARTIFACT`, `MODEL_RESULT`.

Confidence values: `LOW`, `MEDIUM`, `HIGH`. When confidence is not self-evident, the Notes field must state why.

## Claim discipline

Evidence type is not the same as claim label. In application prose, use the explicit labels defined in [README.md](./README.md): `FACT`, `PUBLIC SOURCE`, `INTERVIEW EVIDENCE`, `TECHNICAL TEST`, `MODEL ESTIMATE`, `POLICY HEURISTIC`, `HYPOTHESIS`, `UNKNOWN`.

Rules:

1. Evidence IDs are immutable; add a new row rather than silently changing what an ID means.
2. A source only supports the claim written in its row. Do not stretch one interview or source into adjacent claims it did not establish.
3. Interview evidence requires a real interview record and exact source artifact; never create an `INTERVIEW` row for a planned conversation.
4. Model output is `MODEL_RESULT`/`MODEL ESTIMATE`, not measured impact.
5. Repository copy is evidence of what the product/repo currently says or implements, not evidence that a market claim is true.
6. Public-source values must be rechecked before final submission if date/currentness matters.
7. Raw notes/test logs/model outputs become promotable only after a human creates a narrow evidence row with provenance and limitations.
8. Evidence that contradicts a preferred hypothesis is registered with the same standard as supporting evidence.
9. `SUPPORTED`, `REJECTED`, and `CONFLICTING` assumption states require traceable evidence IDs.
10. A `READY` application claim must satisfy the evidence-admissibility rules in [APPLICATION_RUBRIC.md](./APPLICATION_RUBRIC.md).

## ID/type contract

Use prefixes consistently so mechanical validation can catch accidental relabeling:

| Prefix | Required type |
| --- | --- |
| `E-PUB-*` | `PUBLIC_SOURCE` |
| `E-INT-*` | `INTERVIEW` |
| `E-TECH-*` | `TECH_TEST` |
| `E-REP-*` | `REPO_ARTIFACT` |
| `E-MODEL-*` | `MODEL_RESULT` |

Do not recycle an old ID for a different source, interview, run, result, or claim.

| Evidence ID | Type | Claim supported | Source/artifact | Date | Owner | Confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E-PUB-001 | PUBLIC_SOURCE | `PUBLIC SOURCE` — Boğaziçi University has a public campus food-waste tracking source referenced by the existing repository. | https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310 | TODO — verify source page date/current values before submission | IE | MEDIUM | Existing repo cites an official university URL. Human must re-open and verify any numeric value used in the application. |
| E-REP-001 | REPO_ARTIFACT | `FACT` — the current BOUNCAMPUS repository frames the KREATE product around institutional food-waste decision support and explicitly separates public facts, model estimates, unavailable telemetry, and forbidden pre-pilot impact claims. | [`../README.md`](../README.md) and [`../docs/assumptions.md`](../docs/assumptions.md) | 2026-09-30 inspection | CS2 | HIGH | Directly inspected repository artifacts. This supports repo-state claims only, not market validation. |
| E-REP-002 | REPO_ARTIFACT | `FACT` — the repository contains a falsifiable food-waste pilot protocol with CONTROL/INTERVENTION measurement fields, normalized waste KPI, guardrails, and a claim firewall. | [`../docs/food-waste-pilot-protocol.md`](../docs/food-waste-pilot-protocol.md) | 2026-09-30 inspection | EE | HIGH | Directly inspected repository artifact. The protocol is a proposed method, not evidence that a pilot occurred. |
| E-REP-003 | REPO_ARTIFACT | `FACT` — the current KREATE application draft targets university dining operations and describes the production decision as the present product wedge. | [`../docs/kreate-application-pack.md`](../docs/kreate-application-pack.md) | 2026-09-30 inspection | CS2 | HIGH | Directly inspected repository artifact. Current positioning is not PMR evidence that the beachhead/persona is validated. |

## Adding interview evidence

Use IDs such as `E-INT-001`, `E-INT-002`, ... only after a real interview is completed. Link the corresponding interview artifact and state the **narrow** claim it supports or contradicts.

A completed interview is allowed to produce **no promotable evidence**. In that case, keep the interview record and write `NONE — no promotable claim` in the tracker rather than manufacturing an `E-INT-*` row.

## Adding technical/model evidence

- Technical tests: `E-TECH-001`, `E-TECH-002`, ...
- Model results: `E-MODEL-001`, `E-MODEL-002`, ...

Always record method/artifact, date, owner, limitations, and why the confidence level is appropriate.
