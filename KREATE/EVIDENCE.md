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
| E-PUB-001 | PUBLIC_SOURCE | `PUBLIC SOURCE` — Boğaziçi University has a public campus food-waste tracking source referenced by the existing repository. | https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310 | 2026-10-04 re-check | IE | HIGH | Re-opened official source. Current page reports 2025 total food waste of 48,251 kg, but this does not establish the causal share attributable to overproduction. |
| E-PUB-002 | PUBLIC_SOURCE | `PUBLIC SOURCE` — Boğaziçi reports 48,251 kg total food waste for 2025, alongside a six-dining-hall service footprint. | https://kurumsalveri.bogazici.edu.tr/tr/pages/221-campus-food-waste-tracking/1310 | 2026-10-04 inspection | IE | HIGH | Official university source. Supports problem scale/context only; not evidence that demand mismatch or production planning caused the waste. |
| E-PUB-003 | PUBLIC_SOURCE | `PUBLIC SOURCE` — Boğaziçi SKS reports six dining halls and 6,000 daily meals in its 2025 activity report. | https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096 | 2026-10-04 inspection | IE | HIGH | Official SKS source. Treat `daily meals` as a published operational scale indicator, not a model-ready daily observation series. |
| E-PUB-004 | PUBLIC_SOURCE | `PUBLIC SOURCE` — Boğaziçi states that dining-hall meals are produced in the North Campus kitchen and distributed to its dining operation; contractor nutrition/portion information is provided to the administration. | https://kurumsalveri.bogazici.edu.tr/tr/pages/234-healthy-and-affordable-food-choices/1314 | 2026-10-04 inspection | IE | HIGH | Official university source. Supports centralized-production context, not ownership of the daily production-quantity decision. |
| E-PUB-005 | PUBLIC_SOURCE | `PUBLIC SOURCE` — the current 2026–2027 Boğaziçi food-service procurement publicly lists 3.13 million meal units across six campuses and TEMAŞ as contractor. | https://www.ihaledetay.com/2025-1727143 and https://ekapveri.com/ihale/ekap-2025-1727143/ | 2026-10-04 inspection | IE | MEDIUM | Public mirrors reproducing EKAP procurement/result information. Supports contract scale and contractor identity; does not establish daily settlement quantity or who bears overproduction cost. |
| E-PUB-006 | PUBLIC_SOURCE | `PUBLIC SOURCE` — a 2026 Kırıkkale University food-service procurement required the contractor to determine daily meal quantities using previous meal counts, paid based on meals actually eaten, and placed excess-food risk on the contractor. | https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=0b6db2bdc4dcba60ddf7cb70334f72bf03b482e26ad51295bd12345ea082c52b | 2026-10-04 inspection | IE | HIGH | Official Public Procurement Board decision `2026/UH.I-2269`. Supports existence of this mechanism in another Turkish university only; do not transfer contract semantics to Boğaziçi. |
| E-PUB-007 | PUBLIC_SOURCE | `PUBLIC SOURCE` — an İzmir Katip Çelebi University food-service specification described daily production as reservations plus expected guests/walk-ins, with electronic-card/turnstile counts used for payment and excess-production risk not borne by the administration. | https://herpoz.com/kamu-ihale-kararlari/2025UH.II-2367-kamu-ihale-karari-kik | 2026-10-04 inspection | IE | MEDIUM | Public mirror of Public Procurement Board decision `2025/UH.II-2367`. Supports market-mechanism plausibility/segmentation, not Boğaziçi workflow. |
| E-PUB-008 | PUBLIC_SOURCE | `PUBLIC SOURCE` — a 2026 Gebze Technical University procurement dispute explicitly concerned a clause requiring the contractor to forecast daily meal counts without sufficient reference information; the Board found the uncertainty material to healthy bid preparation. | https://herpoz.com/kamu-ihale-kararlari/2026UH.II-962-kamu-ihale-karari-kik | 2026-10-04 inspection | IE | MEDIUM | Public mirror of decision `2026/UH.II-962`. Shows demand/reference-data uncertainty can be contractually material; not customer validation for BOUNCAMPUS. |
| E-PUB-009 | PUBLIC_SOURCE | `PUBLIC SOURCE` — UI GreenMetric 2026 adds Governance and Digitalization indicators covering ICT for sustainability planning/monitoring/evaluation and advanced digital technologies such as AI/IoT for decision-making, operational efficiency and service delivery. | https://uigreenmetric.com/resources/university/guidelines/2026/english and https://uigreenmetric.com/wp-content/uploads/2026/06/2026_Guideline_UI-GreenMetric-SUR-eng-v2.pdf | 2026-10-04 inspection | CS2 | HIGH | Official UI GreenMetric source. Useful as why-now/institutional context; not evidence of willingness to buy or guaranteed ranking gains. |
| E-PUB-010 | PUBLIC_SOURCE | `PUBLIC SOURCE` — YÖK's 2030 roadmap states Türkiye had 208 universities in 2025 and calls for scaling sustainable/climate-friendly campus practices. | https://s3-ankara.yok.gov.tr/yokmedia/537cb59e-4949-4c0e-8a59-e3e5cc317a03.pdf | 2026-10-04 inspection | CS2 | HIGH | Official YÖK source. `208 universities` is ecosystem context, not TAM or addressable-customer count. |
| E-PUB-011 | PUBLIC_SOURCE | `PUBLIC SOURCE` — Boğaziçi SKS publicly lists Aygül Demir Yolasığmazoğlu as Yemek Hizmetleri Şube Müdürü. | https://sks.bogazici.edu.tr/tr/pages/kadromuz/2212 | 2026-10-04 inspection | IE | HIGH | Establishes a concrete governance contact/role, not that this person owns the daily quantity decision. |
| E-REP-001 | REPO_ARTIFACT | `FACT` — the current BOUNCAMPUS repository frames the KREATE product around institutional food-waste decision support and explicitly separates public facts, model estimates, unavailable telemetry, and forbidden pre-pilot impact claims. | [`../README.md`](../README.md) and [`../docs/assumptions.md`](../docs/assumptions.md) | 2026-09-30 inspection | CS2 | HIGH | Directly inspected repository artifacts. This supports repo-state claims only, not market validation. |
| E-REP-002 | REPO_ARTIFACT | `FACT` — the repository contains a falsifiable food-waste pilot protocol with CONTROL/INTERVENTION measurement fields, normalized waste KPI, guardrails, and a claim firewall. | [`../docs/food-waste-pilot-protocol.md`](../docs/food-waste-pilot-protocol.md) | 2026-09-30 inspection | EE | HIGH | Directly inspected repository artifact. The protocol is a proposed method, not evidence that a pilot occurred. |
| E-REP-003 | REPO_ARTIFACT | `FACT` — the current KREATE application draft targets university dining operations and describes the production decision as the present product wedge. | [`../docs/kreate-application-pack.md`](../docs/kreate-application-pack.md) | 2026-09-30 inspection | CS2 | HIGH | Directly inspected repository artifact. Current positioning is not PMR evidence that the beachhead/persona is validated. |
| E-REP-004 | REPO_ARTIFACT | `FACT` — the repository implements a versioned human-reviewed food decision policy with source-health readiness, abstention, explicit policy-heuristic planning ranges, leakage-safe naive baselines, offline forecast metrics, and pilot evidence-quality gates. | [`../backend/app/decision/food_policy.py`](../backend/app/decision/food_policy.py), [`../backend/app/decision/baselines.py`](../backend/app/decision/baselines.py), [`../frontend/src/lib/food-waste.ts`](../frontend/src/lib/food-waste.ts), and [`../scripts/cs1_baseline_benchmark.py`](../scripts/cs1_baseline_benchmark.py) | 2026-09-30 inspection | CS1 | HIGH | Supports technical repo-state claims only. It does not prove operator adoption, forecast accuracy on measured cafeteria data, workflow fit, waste reduction, or climate impact. |

## Adding interview evidence

Use IDs such as `E-INT-001`, `E-INT-002`, ... only after a real interview is completed. Link the corresponding interview artifact and state the **narrow** claim it supports or contradicts.

A completed interview is allowed to produce **no promotable evidence**. In that case, keep the interview record and write `NONE — no promotable claim` in the tracker rather than manufacturing an `E-INT-*` row.

## Adding technical/model evidence

- Technical tests: `E-TECH-001`, `E-TECH-002`, ...
- Model results: `E-MODEL-001`, `E-MODEL-002`, ...

Always record method/artifact, date, owner, limitations, and why the confidence level is appropriate.
