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
| E-PUB-009 | PUBLIC_SOURCE | `PUBLIC SOURCE` — UI GreenMetric 2026 adds Governance and Digitalization indicators covering ICT for sustainability planning/monitoring/evaluation and advanced digital technologies such as AI/IoT for decision-making, operational efficiency and service delivery. | https://uigreenmetric.com/resources/university/guidelines/2026/english | 2026-10-04 inspection | CS2 | HIGH | Official UI GreenMetric source. Useful as why-now/institutional context; not evidence of willingness to buy or guaranteed ranking gains. |
| E-PUB-010 | PUBLIC_SOURCE | `PUBLIC SOURCE` — YÖK's higher-education roadmap/strategy describes a 208-university ecosystem and explicitly calls for scaling sustainable/climate-friendly campus practices and UI GreenMetric performance. | https://www.yok.gov.tr/documents/documents/68e652769d934.pdf and https://www.yok.gov.tr/documents/documents/6880e6bfa8cdf.pdf | 2026-10-04 inspection | CS2 | HIGH | Official YÖK sources. `208 universities` is ecosystem context, not TAM or addressable-customer count. |
| E-PUB-011 | PUBLIC_SOURCE | `PUBLIC SOURCE` — Boğaziçi publicly lists Aygül Demir Yolasığmazoğlu as Yemek Hizmetleri Şube Müdürü. | https://yemekhane.bogazici.edu.tr/people and https://sks.bogazici.edu.tr/tr/pages/kadromuz/2212 | 2026-10-04 inspection | IE | HIGH | Establishes a concrete governance contact/role, not that this person owns the daily quantity decision. |
| E-PUB-012 | PUBLIC_SOURCE | `PUBLIC SOURCE` — an İTÜ 2026 dining procurement uses electronic turnstile/cafeteria-automation records for contractor payment and requires additional food to be prepared when service is at risk of running out. | https://herpoz.com/kamu-ihale-kararlari/2026UH.II-740-kamu-ihale-karari-kik | 2026-10-04 inspection | IE | MEDIUM | Public mirror of Public Procurement Board decision `2026/UH.II-740`. Supports existence of electronic realized-demand measurement and replenishment logic in another university; not Boğaziçi evidence. |
| E-PUB-013 | PUBLIC_SOURCE | `PUBLIC SOURCE` — a 2025 Karabük University dining procurement required contractor quantity planning using previous meal counts, recognized calendar/weather/menu demand variation, used turnstile/actual consumption for payment, and provided multi-year historical consumption context. | https://herpoz.com/kamu-ihale-kararlari/2025UH.I-1089-kamu-ihale-karari-kik | 2026-10-04 inspection | IE | MEDIUM | Public mirror of Public Procurement Board decision `2025/UH.I-1089`. Supports mechanism/feature plausibility, not a novel BOUNCAMPUS feature or Boğaziçi workflow. |
| E-PUB-014 | PUBLIC_SOURCE | `PUBLIC SOURCE` — Boğaziçi BİD publicly identifies BUCard as a university service and Dining/BUCard public pages indicate time/campus/turnstile-context operations and QR-based dining entry. | https://bilgiislem.bogazici.edu.tr/tr/pages/hizmet-envanteri/3513 and https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0 | 2026-10-04 inspection | IE | HIGH | Supports existence of the operational systems/context only; does not prove historical retention, export rights, clean semantics or team access. |
| E-PUB-015 | PUBLIC_SOURCE | `PUBLIC SOURCE` — KVKK's official guidance requires personal-data processing to be purpose-linked, limited and proportionate, supporting a data-minimizing pilot architecture. | https://kvkk.gov.tr/SharedFolderServer/CMSFiles/0517c528-a43d-49f5-b1eb-33dc666cb938.pdf | 2026-10-04 inspection | EE | HIGH | Official KVKK guidance. Product-design/legal boundary only; not legal approval of any specific BOUNCAMPUS deployment. |
| E-PUB-016 | PUBLIC_SOURCE | `PUBLIC SOURCE` — GTÜ's current 10 Sep 2026 food-services page states that production quantities use historical consumption and daily user counts with food-waste prevention in planning; unexpected demand can cause early depletion and prompt rapid replenishment. | https://www.gtu.edu.tr/kategori/5904/0/display.aspx | 2026-10-04 inspection | IE | HIGH | Official current university source. Strong evidence that the production-quantity / demand / shortage mechanism exists in another target institution; not evidence that GTÜ needs or would adopt BOUNCAMPUS and not Boğaziçi validation. |
| E-PUB-017 | PUBLIC_SOURCE | `PUBLIC SOURCE` — Bilkent currently has a dedicated Cafeterias Management director plus dietitians and administrative staff, showing a comparable operational persona family under a foundation-university structure. | https://www.bilkent.edu.tr/phonedir/dep/ktym.htm and https://w3.bilkent.edu.tr/bilkent/cafeterias-management/personnel/ | 2026-10-04 inspection | IE | HIGH | Establishes organizational-role recurrence only. It does not establish the daily production-quantity owner, pain or willingness to adopt. |
| E-PUB-018 | PUBLIC_SOURCE | `PUBLIC SOURCE` — the active Boğaziçi procurement `2025/1727143` requires bidders to document at least 5,000 meals/day production capacity, explicitly defined as one half of the administration's daily meal need; this implies a tender capacity-reference need of 10,000 meals/day. | https://ekapveri.com/ihale/ekap-2025-1727143/ | 2026-10-04 inspection | IE | MEDIUM | EKAP-derived public mirror. This is a qualification/planning-capacity reference only; it is not actual daily served demand, average attendance, daily production instruction, BUCard count or hakediş/payment quantity. It must not be silently reconciled with the separate SKS `6,000 daily meals` indicator. |
| E-PUB-019 | PUBLIC_SOURCE | `PUBLIC SOURCE` — TEMAŞ currently publicly frames correct need determination and production planning according to demand as food-loss/waste prevention practices, using a multi-kitchen excess-quantity example to illustrate cumulative resource loss. | https://tr.linkedin.com/posts/temasgida_tema%C5%9Fg%C4%B1da-g%C4%B1dakayb%C4%B1veisraf%C4%B1-s%C3%BCrd%C3%BCr%C3%BClebilirlik-activity-7510697620009353216-qq72 | 2026-10-04 inspection | IE | MEDIUM | Current company communication / problem-awareness evidence only. The example is hypothetical and does not prove TEMAŞ has forecast errors, wants BOUNCAMPUS, lacks an incumbent system, or would pay for external software. |
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
