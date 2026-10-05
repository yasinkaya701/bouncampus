# Cross-University Workflow Repeatability — Türkiye

**Research date:** 2026-10-05
**Status:** Public-source secondary research. This establishes mechanism plausibility/repetition, not customer validation and not willingness-to-pay.

## Research question

Is BOUNCAMPUS's dining problem merely a Boğaziçi-specific hypothesis, or do similar production-planning mechanisms recur in other Turkish university food-service operations?

## 1. Gebze Technical University — direct current evidence

Official GTÜ dining page, last updated **10 September 2026**:
https://www.gtu.edu.tr/kategori/5904/0/display.aspx

The university publicly states that:
- production quantities are determined using historical consumption data;
- daily user counts are part of planning;
- food-waste prevention is part of the planning objective;
- high-demand items can still run out later in the service period because of unexpected demand increases;
- fast replenishment/substitution is used to maintain service.

### Mechanism represented

```text
historical demand + expected users
→ planned quantity
→ unexpected demand shock
→ early depletion risk
→ reactive replenishment
```

### Implication

This strongly supports **market-mechanism plausibility** for:
- demand uncertainty;
- overproduction/shortage trade-off;
- recurring pre-service planning;
- service-continuity guardrails.

It does **not** prove:
- Boğaziçi has the same workflow;
- GTÜ would buy BOUNCAMPUS;
- existing GTÜ planning is inadequate enough to justify new software.

## 2. Istanbul Technical University — mature manual/data-informed planning

Official ITU food-waste / sustainability page:
https://sustainability.itu.edu.tr/tr/itu-kafeteryalari-ve-yemek-hizmetleri-gida-israfini-onlemeye-yonelik-ozel-programlar-saglamaktadir

ITU publicly describes production forecasting inputs including:
- academic calendar;
- course-program intensity;
- examination schedule;
- menu-dependent choice patterns;
- weather;
- meals consumed in prior weeks/months/years.

It also describes contingency behavior:
- when demand exceeds production, an alternative fast menu is prepared;
- when production exceeds demand, surplus is handled under food-safety constraints.

Official electronic dining-entry source:
https://kim.itu.edu.tr/itukart/yemekhane-uygulamasi

This establishes electronic turnstile/card meal entry in the operation.

### Critical strategic implication

Several feature classes proposed by BOUNCAMPUS are **already recognized operational inputs at a sophisticated Turkish university**.

Therefore novelty cannot be:
> `we use academic calendar + weather + menu + history.`

The product must prove value in one or more of:
- better combination/calibration than current heuristics;
- uncertainty and asymmetric-risk treatment;
- timing relative to the actual freeze point;
- data/provenance reconciliation;
- human-review workflow;
- outcome verification;
- lower operational friction.

## 3. ITU food-service organizational pattern

Current ITU food-services page:
https://sks.itu.edu.tr/hizmetlerimiz/beslenme-hizmetleri

Public role pattern includes:
- Dining/Food Operations Branch management;
- food engineer;
- food technician;
- head chef;
- SKS governance.

This independently supports the previously observed role cluster across Turkish university dining:

```text
operations/governance owner
+ food-domain technical professional
+ kitchen execution
```

The exact production-quantity decision owner remains institution-specific and requires PMR.

## 4. Bilkent ecosystem — different governance archetype

Bilkent's BCC Catering public page describes a large professional catering organization with:
- central kitchen at Bilkent University;
- production management;
- food engineers;
- dietitians;
- head chefs and quality controls;
- production/distribution services at scale.

Source:
https://obi.bilkent.edu.tr/index.php/bcc-catering/

This represents a different archetype from a public-university SKS-managed operation and is useful as a heterogeneity test.

### Implication

If BOUNCAMPUS requires materially different product language, sales process, integrations and buyer mapping for:
- public SKS-governed dining;
- contractor-risk public dining;
- vertically integrated professional catering;

then these should not be treated as one beachhead.

## 5. Public procurement cases previously identified

The repository evidence registry already records:
- Kırıkkale — contractor quantity estimation + actual-consumption settlement + contractor excess risk;
- İzmir Katip Çelebi — reservation + expected walk-in planning, electronic consumption settlement;
- Gebze Technical — procurement dispute over quantity forecasting without sufficient reference data;
- ITU — electronic turnstile/cafeteria-automation settlement and replenishment requirements;
- Karabük — history/calendar/weather/menu variation recognized in planning.

These establish that **quantity planning is contractually material across multiple institutions**, but also that contractual allocation of risk differs substantially.

## 6. Repeatable problem kernel

Across the strongest public cases, the repeated kernel is not `food waste` alone.

It is:

```text
future service demand is uncertain
→ an operational quantity must be selected before demand fully realizes
→ historical/context signals inform the decision
→ surplus and shortage have different consequences
→ realized consumption is measured in some systems
→ contingency/replenishment may exist
```

This is the best current secondary-evidence foundation for the food wedge.

## 7. What is already commoditized / known practice

Secondary research now shows that operators may already use:
- history;
- calendar;
- weather;
- menu;
- daily user estimates;
- electronic card/turnstile counts;
- reservation data;
- reactive replenishment.

Therefore BOUNCAMPUS must not present these ingredients individually as innovation.

## 8. Stronger PMR questions after repeatability research

Do not ask:
> `Would academic calendar/weather improve planning?`

Some institutions already use them.

Ask:
1. Which signals are actually used at your decision cutoff?
2. How are they combined today?
3. Which signal most often surprises you?
4. How large is the safety buffer and why?
5. When does the planned quantity become expensive/impossible to revise?
6. Does the current forecast have an uncertainty range or only a point estimate?
7. When did you last ignore a production sheet/forecast and why?
8. How do you distinguish bad forecasting from menu/taste/portion problems after service?
9. What would another decision-support product have to do materially better than today's process?

## 9. Beachhead consequence

A better candidate beachhead is increasingly:

> **Turkish university dining operations with centralized/coordinated high-volume production, a repeated pre-service quantity decision, electronically or operationally measurable realized demand, and a decision owner who can modify production before a real freeze point.**

Further segmentation by `institution-led` vs `contractor-led` quantity ownership may still be required after PMR.

## 10. Bottom line

Secondary evidence now supports that the **problem mechanism repeats across Turkish university dining**, including explicit current examples of forecast inputs, unexpected demand and shortage/replenishment behavior.

What remains completely unvalidated is the commercial claim:

> `BOUNCAMPUS adds enough value beyond those existing processes to change operator behavior and justify adoption.`

That is the next PMR target.
