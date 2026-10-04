# Food-Waste Root Cause & Stage Evidence — 2026-10-04

**Purpose:** red-team the assumption that demand/production mismatch is the correct first intervention point.  
**Status:** academic/public secondary research. **Does not establish the causal composition of Boğaziçi's 48,251 kg 2025 food waste.**

## Executive conclusion

University food waste is clearly **multi-causal**.

The literature does not justify collapsing all waste into a production-forecasting problem. Important competing drivers include:

- portion size;
- taste / palatability;
- perceived food quality;
- menu composition;
- preparation/cooking;
- service design;
- storage;
- satiety;
- overbuying / planning;
- consumer behavior;
- situational factors.

Therefore the first PMR/measurement objective must be:

> **identify the waste stage and controllable cause before choosing the intervention.**

BOUNCAMPUS should retain production quantity as the first **hypothesis**, not as a proven root cause.

---

# 1. Review evidence — causes are broader than forecasting

Deliberador, César & Batalha (2021), `How to fight food waste in university restaurants?`, reviewed literature specifically around university restaurants. The review identified 13 causes including:

- portion size;
- quality;
- price;
- emotion;
- palatability;
- preparation/cooking;
- menu;
- time;
- satiety;
- storage;
- service;
- overbuying;
- security/safety-related factors.

It identified interventions including planning/preordering but also portion, quality, menu, preparation, storage and behavioral approaches.

Consensus record:
https://consensus.app/papers/how-to-fight-food-waste-in-university-restaurants-deliberador-césar/6a9d5120871e59ffa79f67ef898db1b0/

### Product implication

Forecasting/planning is one intervention family, not the universal answer.

---

# 2. Educational-institution systematic review — granular diagnosis required

Kaur et al. (2021) systematically synthesized **88 studies** on food waste in educational institutions. Major themes included:

- drivers;
- quantitative assessment;
- behavioral factors;
- operational reduction strategies;
- behavior-change interventions;
- diversion/disposal;
- implementation barriers.

Consensus record:
https://consensus.app/papers/systematic-literature-review-of-food-waste-in-educational-kaur-dhir/41d44cdd08b7512597ef87b8b9fe942d/

### Product implication

An annual/monthly institution-wide waste total is too coarse to identify an intervention.

---

# 3. 2026 university-restaurant sustainability review — research itself is skewed downstream

Peixoto et al. (2026) scoping review included **58 studies** of sustainability in university restaurants. It reports that **70.69%** of the research focused on the post-distribution phase, especially waste management/food waste, and that menu changes and consumer educational campaigns were common interventions.

Consensus record:
https://consensus.app/papers/sustainability-in-university-restaurants-a-scoping-peixoto-reis/7c69c0fc372e5ee48d2507897e7c76aa/

### Interpretation

Two cautions:

1. university food-waste evidence is heavily represented by downstream/post-distribution studies;
2. that does not prove downstream waste is always the dominant physical share, but it does mean the evidence base is not centered only on production forecasting.

BOUNCAMPUS must measure the local stage rather than infer it from literature frequency.

---

# 4. Türkiye-specific consumer/plate-waste evidence — portion and taste matter

Özokcu & Özdemir (2026), in a Turkish university cafeteria, used a mixed-method design with **479 student questionnaires + 11 in-depth interviews** and found that:

- situational variables;
- perceived portion size;
- taste/palatability

significantly influence students' plate-waste behavior and can outweigh volitional control.

Source:
https://link.springer.com/article/10.1007/s44274-025-00509-y

### Implication

If Boğaziçi waste is predominantly post-consumer plate waste, a total-demand forecast may not address the main mechanism.

Potential alternative interventions:

- portion-size decisions;
- menu acceptance / item mix;
- serving choice;
- food quality / palatability;
- optional portioning;
- plate-level feedback.

---

# 5. Türkiye 2026 menu-algorithm study — algorithmic optimization can worsen the wrong outcome

Ural & Ongan (2026) compared an algorithm-generated menu against traditional menu planning in an İzmir university cafeteria, using weighed leftovers from **960 plates / 240 students over four days**.

Reported abstract results:

- overall plate waste was not significantly lower for the algorithmic menu;
- main-course plate waste was significantly **higher** in the algorithm-generated menu condition.

Source:
https://www.tandfonline.com/doi/full/10.1080/19320248.2026.2705369

### Important lesson

`algorithmic` does not mean `better`.

A model optimized for nutritional/menu constraints can fail on acceptance/waste if consumer preference and operational context are not represented.

For BOUNCAMPUS:

- forecast/model accuracy is not sufficient;
- outcome measurement and guardrails are mandatory;
- item/menu features should be validated, not assumed useful.

---

# 6. Turkish university cafeteria satisfaction/leftover evidence

A 2025 Süleyman Demirel University journal study used both subjective assessment and objective weighing over five days in a university cafeteria. The abstract reports meaningful leftover levels associated with dissatisfaction and differences in leftovers across foods/groups.

Source:
https://dergipark.org.tr/en/pub/sdusbed/article/1588744

### Implication

Quality/satisfaction can be an important confounder of waste outcomes.

A high-waste service cannot automatically be labelled `overproduction` without stage/cause evidence.

---

# 7. Large plate-waste example from Türkiye

A Çukurova University cafeteria study reported plate-leftover measurements across **54,987 diners**, with the highest reported average in student dining at approximately **81.7 g/person/day** in the study context.

Publicly indexed record:
https://www.researchgate.net/publication/308413957_TABAKTA_KALAN_YEMEKLER_UNIVERSITE_YEMEKHANESINDEN_ORNEK-LEFTOVER_DISHES_on_PLATE_A_CASE_STUDY_FROM_THE_UNIVERSITY_CAFETERIA

### Boundary

This is historical/site-specific evidence and should not be used as a current Boğaziçi baseline.

It simply demonstrates that plate waste can be materially large in Turkish university dining.

---

# 8. Decision tree for the food wedge

Before committing to total-production forecasting, determine the dominant controllable waste stream.

```text
TOTAL FOOD WASTE
        |
        +-- preparation/cooking waste
        |       -> process / recipe / training / storage intervention
        |
        +-- cooked but unserved edible surplus
        |       -> demand forecast / production / batch / allocation intervention
        |
        +-- plate waste
        |       -> portion / menu / quality / choice / behavior intervention
        |
        +-- spoilage/storage
        |       -> inventory / cold-chain / procurement intervention
        |
        +-- reporting/collection timing artifacts
                -> data reconciliation, not operational waste claim
```

The BOUNCAMPUS production wedge is strongest only if **cooked-but-unserved edible surplus** is meaningful and controllable.

---

# 9. PMR questions required to distinguish stages

Ask operators about the **last real waste episode**, not the annual total.

- What exactly was discarded?
- Was it prepared but never served, returned from plates, prep scraps, expired stock or another stream?
- Was it edible at the point it became surplus?
- Was the quantity measured or estimated?
- Could a smaller production quantity have prevented it?
- Would changing quantity have increased shortage risk?
- Was the issue tied to menu acceptance/taste/portion?
- What happened to safe unserved food?
- Are waste streams physically separated?
- Which stream is largest in a typical week?

### Strongest evidence

Service-level direct measurement separated into:

```text
produced
served
unserved edible surplus
preparation waste
plate waste
```

with consistent measurement methods.

---

# 10. Product pivot map

## If unserved surplus dominates

Keep:

- demand forecast;
- production band;
- batch/release/allocation optimization.

## If plate waste dominates

Shift emphasis toward:

- TrayGate / plate-waste diagnosis;
- portion sizing;
- menu-conditioned waste patterns;
- item-level acceptance;
- serving choice/portion policy.

Demand forecasting may remain useful for total attendance but is not the primary waste intervention.

## If prep/storage loss dominates

Potential wedge:

- process monitoring;
- inventory/cold-chain;
- preparation planning;
- batch recipe optimization.

## If causes vary by service

The strongest product may become **diagnose the waste stage first, then recommend the correct intervention** rather than one fixed forecasting intervention.

This is strategically more robust but increases whole-product scope; do not expand until PMR requires it.

---

# 11. Application language consequence

Unsafe before PMR:

> `Boğaziçi's food waste is caused by inaccurate demand forecasting.`

Safe:

> **University dining operations face multiple sources of food waste. We are testing whether pre-service production mismatch is a material and controllable source in our target workflow.**

Stronger if a real interview later supports it:

> `Operators identified repeated cooked-but-unserved surplus linked to demand error, making production planning a measurable intervention point.`

Only use the latter after interview/measurement evidence exists.

---

# 12. Strategic conclusion

The strongest research posture is not to defend forecasting at all costs.

It is:

```text
measure stage
-> identify controllable cause
-> choose decision
-> intervene
-> verify outcome
```

That principle remains compatible with the broader BOUNCAMPUS decision-and-verification architecture even if PMR forces the first food decision to change.
