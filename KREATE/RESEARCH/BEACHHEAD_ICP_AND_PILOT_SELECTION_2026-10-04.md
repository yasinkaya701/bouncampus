# Beachhead ICP & Pilot Selection Framework — 2026-10-04

**Status:** Market-segmentation hypothesis from secondary research. **Not TAM/SAM/SOM, not willingness-to-pay evidence, not customer validation.**

---

# 1. Market context is large; addressable beachhead is much smaller

YÖK public sources describe Türkiye's higher-education system as roughly:

- **208 universities**;
- more than **7 million students**.

Sources:

- https://www.yok.gov.tr/Sayfalar/Haberler/2024/yuksekogretim-akredite-programlari.aspx
- https://www.yok.gov.tr/documents/documents/68e652769d934.pdf

This is ecosystem context only.

**Forbidden sizing:**

```text
208 universities x assumed software price = TAM
```

That ignores dining structure, outsourcing, decision ownership, measurement maturity, existing systems, procurement and willingness to pay.

---

# 2. Why-now is stronger than simple sustainability awareness

## YÖK direction

YÖK's strategy explicitly includes transformation toward sustainable/climate-friendly campuses and targets increasing Turkish universities' UI GreenMetric presence.

Source:
https://www.yok.gov.tr/documents/documents/6880e6bfa8cdf.pdf

The 2030 roadmap frames sustainability performance as involving:

- policy;
- implementation;
- evaluation supported by data/information and management tools;
- optimization.

Source:
https://www.yok.gov.tr/documents/documents/68e652769d934.pdf

## Actual sustainability investment variation

YÖK reported in 2025 that:

- 62 universities generated renewable electricity;
- 33 used transformed/treated water sources;
- 45 invested in water-saving measures.

Source:
https://www.yok.gov.tr/Sayfalar/Haberler/2025/turkiye-yesil-%C3%BCniversite.aspx

### Implication

Universities differ substantially in sustainability and digital maturity.

A single generic smart-campus product/sales process is unlikely to fit all institutions.

---

# 3. UI GreenMetric 2026 strengthens digital-governance pull

UI GreenMetric 2026 introduces a Governance and Digitalization category and ranks universities on it.

Official ranking:
https://uigreenmetric.com/rankings/university/ranking-by-category-2026/gd

The ranking shows multiple Turkish institutions with high Governance & Digitalization scores, including examples such as:

- İstanbul Technical University;
- Yıldız Technical University;
- Hacettepe University;
- Middle East Technical University;
- Ankara University;
- others.

### Important interpretation

High digital/sustainability maturity can mean **either**:

- attractive early adopter with data/integration capacity;
- difficult customer because mature systems already solve the problem.

Therefore GreenMetric maturity is a **screening variable**, not a direct lead score.

---

# 4. Candidate beachhead definition

The most defensible current beachhead is:

> **Medium-to-large Turkish universities with centrally coordinated or institution-governed dining operations, recurring high-volume meal services, an identifiable and reachable quantity decision, measurable actual consumption, and enough operational/data maturity to run a bounded pilot.**

## Why this is more homogeneous than "universities"

These users share a repeated job:

> choose how much to prepare/release before demand is fully observed while protecting service availability.

They are also more likely to share:

- formal Food Services/SKS-like governance;
- contractor or central-kitchen workflows;
- electronic/administrative consumption records;
- recurrent service periods;
- measurable waste/surplus;
- public procurement constraints.

---

# 5. ICP screening dimensions

Do **not** assign confident numeric scores until PMR supplies evidence. The following are screening dimensions and proposed weights only.

| Dimension | Importance | What must be verified |
| --- | --- | --- |
| repeated meal volume | High | actual service count / frequency |
| central/coordinated production | High | production architecture |
| identifiable quantity owner | Critical | role + authority |
| decision adjustment window | Critical | freeze point / batch flexibility |
| mismatch consequence | Critical | surplus / shortage incident evidence |
| actual-demand measurement | Critical | turnstile/POS/served count semantics |
| waste-stage measurement | High | edible surplus vs prep/plate waste |
| data access path | Critical | owner + approval + retention |
| economic incentive | Critical | who pays/saves/bears risk |
| pilot permission | High | named approver |
| current-tool gap | Critical | existing workflow not already sufficient |
| integration burden | Negative | security/IT/procurement friction |
| procurement cycle | Negative | time/complexity to pilot/buy |
| sustainability/digital maturity | Contextual | early-adopter capacity vs incumbent saturation |
| cross-site repeatability | High | same job at other institutions |

---

# 6. Strong early-pilot profile

A strong pilot candidate would look like:

```text
high-volume repeated service
+ central or coordinated kitchen
+ quantity can change before service/batch
+ validated actual served count
+ recent mismatch incidents
+ identifiable operator
+ bounded data-access path
+ measurable surplus/shortage
+ sponsor who captures operational/sustainability value
```

The product can tolerate imperfect data if the missing fields can be measured cheaply in a pilot.

---

# 7. Weak early-pilot profile

Avoid initially:

- many independent food vendors with no common decision;
- fully outsourced service where no reachable stakeholder can change quantity;
- tiny volume / infrequent service;
- no service-level actual count;
- no way to distinguish waste stages;
- multi-year procurement/integration required before any bounded test;
- mature specialist system already solving the exact decision with low pain;
- institution interested only in annual reporting rather than operational intervention.

---

# 8. Candidate institution archetypes to sample — not sales recommendations

PMR should deliberately sample different mechanisms rather than only the easiest contacts.

## Archetype A — large public, contractor-operated, electronic consumption records

Purpose:

- test daily quantity ownership;
- procurement incentives;
- turnstile measurement;
- public-sector pilot friction.

Research examples showing this mechanism exists include İTÜ, Karabük, Kırıkkale and İzmir Katip Çelebi procurement records.

## Archetype B — foundation university / potentially faster procurement

Purpose:

- compare procurement/pilot cycle;
- determine whether operator economics differ;
- test willingness to integrate existing systems.

Do not assume foundation universities are easier buyers; validate.

## Archetype C — sustainability/digital leader

Purpose:

- test whether mature digital governance creates stronger appetite for a decision layer;
- or whether existing platforms make BOUNCAMPUS redundant.

## Archetype D — lower measurement maturity but high operational pain

Purpose:

- test whether a measurement-first package is needed before decision intelligence;
- estimate hardware/manual-collection burden.

---

# 9. Pilot promotion gate

Do not call university dining a validated beachhead until evidence supports all of:

1. **Repeated pain** — multiple recent mismatch incidents from relevant operators.
2. **Reachable control point** — named person can change quantity/batch/allocation.
3. **Timing** — recommendation can arrive before the action becomes costly/irreversible.
4. **Measurable outcome** — served + surplus/shortage guardrail can be recorded.
5. **Current-tool gap** — status quo does not already solve the decision sufficiently.
6. **Incentive alignment** — a reachable sponsor benefits from improvement.
7. **Pilot feasibility** — data, operations, privacy and procurement permit a bounded test.
8. **Repeatability** — at least two additional institutions show materially similar workflow.

A failure in one critical dimension should trigger narrowing or a different control point.

---

# 10. Buyer / user / beneficiary must be kept separate

Potential structure:

| Role | Candidate |
| --- | --- |
| daily user | contractor production planner / kitchen manager / food engineer |
| operational decision owner | Food Services manager or contractor project lead |
| data owner | IT/BUCard/POS / contractor records / waste owner |
| economic buyer | university/SKS or contractor depending contract |
| sustainability champion | sustainability/Zero Waste office |
| beneficiary | budget owner, contractor margin, students, sustainability program |

### PMR requirement

For every institution ask:

> Who uses it? Who approves it? Who pays for it? Who saves money? Who takes the blame when the meal runs out?

Do not collapse these into one persona.

---

# 11. Market expansion logic if the beachhead works

## Adjacent dining markets

The same operational contract may transfer to:

- hospital foodservice;
- factory/staff cafeterias;
- schools;
- municipal kitchens;
- large catering operators.

The decision/measurement structure may be more portable than the "university" label itself.

## Adjacent campus decisions

Long-term BOUNCAMPUS expansion remains plausible where the same structure exists:

```text
observable state
-> named resource decision
-> human intervention
-> measurable result
```

Candidate domains:

- room/space allocation;
- shuttle frequency/capacity;
- energy anomaly/intervention prioritization;
- water leak/irrigation/retrofit prioritization.

Each requires independent PMR. Success in food does not validate pain in another domain.

---

# 12. Market-size data required later

Before monetary TAM/SAM/SOM, collect:

```text
number_of_institutions_by_dining_workflow
outsourced_vs_inhouse_share
centralized_vs_distributed_share
meal_volume_distribution
actual-consumption measurement penetration
specialist food-tech penetration
budget/procurement owner
pilot-to-contract conversion constraints
credible annual price
implementation/support cost
sales cycle
```

Until these exist, use institution/meal counts as context rather than claiming a monetary opportunity.
