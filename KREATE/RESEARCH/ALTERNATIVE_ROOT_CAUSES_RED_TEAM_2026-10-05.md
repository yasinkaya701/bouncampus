# Alternative Root Causes Red-Team — University Food Waste

**Research date:** 2026-10-05
**Status:** Secondary/public research. Purpose is to challenge the preferred production-demand-mismatch hypothesis.

## Core warning

A university can have both:
- uncertain meal demand / production mismatch; and
- substantial food waste caused by quality, taste, portioning, preparation, service or consumer behavior.

Therefore:

> `food waste exists` does **not** imply `better demand forecasting is the right intervention`.

## 1. Boğaziçi already treats food quality/preference as an operational variable

### Daily tasting program
Official Boğaziçi dining announcement:
https://yemekhane.bogazici.edu.tr/yemek-tadim-etkinligi

The university introduced daily pre-service tasting for lunch/dinner with volunteer students and evaluation forms to improve meal quality.

### Large satisfaction survey / feedback ecosystem
2025 SKS activity report:
https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096

The report states, among other food-service activities:
- satisfaction survey with **2,386 participants**;
- feedback sharing;
- tasting activity;
- instant request/complaint area;
- BUCampus menu-selection process;
- planned daily meal rating through BUCampus in 2026–2027 goals.

### Implication

Boğaziçi has explicit institutional mechanisms around:
- meal quality;
- menu preference;
- service experience;
- user feedback.

This means menu acceptance / taste / perceived quality are credible alternative causes of food left uneaten and should be actively tested rather than treated as noise.

## 2. GTÜ changed menu variety and measured satisfaction in 2026

Official GTÜ sources:
- new meal-service/menu-diversity model: https://www.gtu.edu.tr/icerik/1229/30837/display.aspx
- July 2026 satisfaction results: https://www.gtu.edu.tr/icerik/1229/31238/display.aspx

GTÜ introduced multiple main/side/salad choices and explicitly measured stakeholder satisfaction afterward.

### Implication

University dining operators may respond to food-service problems through **menu architecture and quality interventions**, not only quantity forecasting.

A strong product must distinguish:

```text
people did not come
vs
people came but did not select the item
vs
people selected it but left it uneaten
```

These require different interventions.

## 3. Academic evidence: waste causes can be behavioral/service-driven

### Fatemi et al. (2024), Agriculture & Food Security
`Food waste reduction and its environmental consequences: a quasi-experimental study in a campus canteen`

Consensus record:
https://consensus.app/papers/food-waste-reduction-and-its-environmental-consequences-a-fatemi-eini-zinab/0667ce80210d5c80a993b05012cfb8eb/?utm_source=chatgpt

The study's student interviews identified causes including:
- low-quality meals;
- unpleasant taste;
- large portion size;
- limited menu.

The intervention combined staff/student actions and portion/quality-related changes.

### Dyrbye-Wright et al. (2025), scoping review
`Strategies to Curb Food Waste on University Campuses`

Consensus record:
https://consensus.app/papers/strategies-to-curb-food-waste-on-university-campuses-a-dyrbye-wright-stull/4c51cb380c0b5694a7ced9d030870590/?utm_source=chatgpt

The review found heterogeneous intervention results and emphasized inconsistent waste-measurement methods and short intervention periods.

### Visschers et al. (2020), Waste Management
`Smaller servings vs. information provision`

The study found that portion-size intervention could materially affect plate waste whereas information alone did not produce the same result in the studied canteens.

### Implication

The literature supports **multi-causality** and warns against assuming forecasting is dominant.

## 4. Causal-stage decomposition required

For each service, distinguish where possible:

### A. Attendance/demand mismatch
Question:
> Did fewer/more people arrive than expected?

Evidence:
- planned attendance;
- served/validated entry count;
- timing of turnout.

Potential intervention:
- demand forecasting / allocation / batch release.

### B. Item selection mismatch
Question:
> People came, but selected different items than expected?

Evidence:
- offered portions by item;
- item take-rate;
- menu-choice data.

Potential intervention:
- item-level production/menu-mix prediction.

### C. Portion/plate waste
Question:
> People selected food but did not eat it?

Evidence:
- plate/tray leftovers;
- portion size;
- taste/quality feedback.

Potential intervention:
- portion adjustment;
- recipe/menu quality;
- choice architecture.

### D. Preparation/process loss
Question:
> Waste occurred before serving?

Evidence:
- preparation waste;
- batch/process records.

Potential intervention:
- kitchen process / yield / procurement.

### E. Food-safety / service-rule discard
Question:
> Food was safe/unsafe to reuse after time/temperature/service exposure?

Potential intervention:
- batch timing;
- cold/hot holding;
- operational rules, not simply forecast.

## 5. Strong PMR prompts

Ask:
1. Tell me about the last large amount of food that had to be discarded. Where exactly did it come from?
2. How do you know whether the cause was low attendance versus an unpopular menu?
3. Which foods most often remain on trays?
4. Which foods most often remain unserved in the kitchen?
5. Have you changed portion sizes because of leftovers? What happened?
6. Have menu/taste complaints ever changed production quantities?
7. Which waste type worries you most operationally?
8. If attendance forecasting were perfect tomorrow, what food waste would still remain?

That final question is a high-value falsifier.

## 6. Product decision tree

```text
if attendance mismatch dominates:
    demand / production decision support
elif item-mix mismatch dominates:
    menu-conditioned item planning
elif plate waste dominates:
    portion + preference + TrayGate/measurement intervention
elif preparation loss dominates:
    kitchen process/yield intervention
else:
    do not force the existing solution thesis
```

## 7. Solution-copy consequence

Before PMR, avoid:
> `The main cause of university food waste is inaccurate demand forecasting.`

Prefer:
> `One potentially preventable source is a mismatch between uncertain demand and production decisions. Our PMR is testing how material that mechanism is relative to other causes such as menu acceptance, portioning and preparation waste.`

## 8. Strategic benefit of falsification

If production mismatch is not dominant, the broader BOUNCAMPUS decision-and-verification architecture may still survive while the first decision changes.

For example:
- portion decision;
- menu mix;
- batch release;
- campus allocation;
- surplus redistribution timing.

This is stronger than defending the current forecast product regardless of evidence.

## 9. Bottom line

The strongest current problem statement should describe **uncertain operational decisions and avoidable mismatch**, while explicitly leaving causal magnitude for PMR.

Boğaziçi's existing feedback programs and university food-waste literature make alternative causes credible enough that any application claiming demand forecasting as the proven root cause would overstate the evidence.
