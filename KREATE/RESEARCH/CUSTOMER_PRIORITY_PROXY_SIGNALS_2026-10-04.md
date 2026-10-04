# Customer-Priority Proxy Signals — 2026-10-04

**Purpose:** identify recurring operational/service priorities in university dining so PMR can test tradeoffs intelligently.  
**Status:** institutional proxy evidence only. **These are NOT the validated prioritized purchasing criteria of the BOUNCAMPUS Persona.**

## Executive conclusion

Current official university dining sources repeatedly emphasize a multi-objective service problem, not a waste-only objective.

Recurring institutional dimensions include:

```text
food safety / hygiene
meal quality / taste
portion adequacy
variety / menu fit
service continuity and speed
user satisfaction
cost / affordability / subsidy
contract compliance
operational control
waste / sustainability
```

This supports a strong product guardrail:

> BOUNCAMPUS should never optimize waste by silently degrading meal availability, food safety, portion standards or service quality.

However, public mission statements and user satisfaction surveys do **not** establish which criterion the actual production-decision Persona ranks #1 when tradeoffs occur.

That ranking still requires PMR.

---

# 1. İTÜ — official mission puts quality/safety and demand satisfaction first

İstanbul Technical University's current Food Services page states that the mission of its Food Operations Branch is to provide students and staff with food that is:

- healthy;
- balanced;
- tasty;
- high quality;
- served in environments where food safety is ensured.

Its vision includes continuously improving service quality according to guest requests and increasing demand/satisfaction.

Official source:
https://www.sks.itu.edu.tr/hizmetlerimiz/beslenme-hizmetleri

The same page states:

- 9 lunch dining halls;
- 4 dinner dining halls;
- roughly 14,000 daily diners in the academic term;
- electronic identity-card dining automation;
- regular accredited laboratory microbiological testing.

### Product implication

An operator decision cannot be evaluated only on:

```text
surplus reduction
```

It sits inside a broader utility function including:

```text
availability
quality
safety
satisfaction
```

---

# 2. İzmir Katip Çelebi — 2026 survey explicitly measures multiple service dimensions

İKÇÜ's official measurement/evaluation center published a **16 July 2026** Dining Service Quality Satisfaction Survey report description.

The survey covered:

- taste;
- variety;
- portion adequacy;
- hygiene;
- service process;
- personnel behavior;
- dining environment;
- overall service quality.

It contained 20 questions and 488 participants.

Official source:
https://ismer.ikcu.edu.tr/Etkinlik/9076/ikcu-yemekhane-hizmet-kalitesi-memnuniyet-anketi-raporu

### Implication

The customer organization treats user value as multi-dimensional.

`less food remaining` is not sufficient evidence of a better service.

---

# 3. Giresun University — current survey exposes specific improvement areas

Giresun University's current quality page reports 2026 dining-hall satisfaction results and identifies improvement areas including:

- portion quantity adequacy;
- main-dish taste;
- soup taste.

It identifies strengths such as:

- fast service;
- staff cleanliness standards;
- staff behavior.

Official source:
https://kalite.giresun.edu.tr/tr/page/anket-degerlendirme/8032

### Important boundary

These are user satisfaction dimensions, not direct food-waste causes and not operator purchasing criteria.

### PMR implication

When an operator refuses to reduce production or portions, do not assume irrationality. They may be protecting a service-quality dimension the model does not see.

---

# 4. GTÜ — menu diversity changes are explicitly measured with satisfaction

Gebze Technical University's current July 2026 food-service survey announcement states that a new meal-service application was introduced from June 2026 to improve:

- quality;
- diversity;
- user satisfaction;
- access to balanced and varied nutrition.

It reports 81 in-person survey responses and 177 online responses, with differing general satisfaction levels by collection mode.

Official source:
https://www.gtu.edu.tr/icerik/1229/31238/display.aspx

### Implication

Dining operations actively change service design and measure user reaction.

Any BOUNCAMPUS recommendation affecting:

- menu mix;
- portion;
- availability;
- service format

must be evaluated against user-service outcomes as well as waste.

---

# 5. İstanbul University — quality, safety, satisfaction and oversight are explicit institutional objectives

İstanbul University's current dining-services page describes a quality- and satisfaction-oriented service model and states that:

- technological innovations are followed to improve service;
- a university control/acceptance structure supervises contractor service;
- periodic surveys are used;
- improvements are made from survey results and requests;
- occupational/food-service safety requirements are treated as mandatory.

Official source:
https://sks.istanbul.edu.tr/yemekhane-tanitim

### Implication

A new product must fit an established continuous-improvement/governance process rather than merely produce a dashboard score.

---

# 6. Recurring institutional priority families

Across the sources, five priority families recur.

## P1 — safety / compliance

Examples:
- food hygiene;
- laboratory controls;
- portion/recipe/spec compliance;
- safe service.

Likely behavior:
- hard constraint rather than optimizable tradeoff.

## P2 — service continuity / availability

Examples:
- avoiding shortages;
- service speed;
- consistent access.

Likely behavior:
- can create a safety buffer in production planning.

This remains an H-C PMR hypothesis until real operators describe it.

## P3 — food experience / acceptance

Examples:
- taste;
- variety;
- menu fit;
- temperature;
- portion adequacy.

Likely behavior:
- can change demand and plate waste independently of attendance forecasting.

## P4 — operational/economic efficiency

Examples to test:
- avoid unnecessary production;
- reduce emergency substitutions;
- lower manual planning effort;
- reduce contractor/administrative reconciliation friction.

Public mission statements rarely quantify this priority sufficiently; PMR is required.

## P5 — sustainability / evidence

Examples:
- waste prevention;
- zero-waste reporting;
- institutional sustainability objectives.

Likely value:
- important champion/reporting dimension, but may not be the daily operator's top criterion.

---

# 7. Proposed multi-objective decision model — hypothesis only

Do not optimize:

```text
minimize waste
```

as a standalone objective.

A more realistic decision formulation to validate is:

```text
minimize
    surplus_cost
  + shortage_penalty
  + emergency_substitution_cost
  + operator_friction

subject to
    food_safety = satisfied
    contract_rules = satisfied
    portion/recipe standards = satisfied
    minimum service availability = satisfied
```

Possible additional monitored outcomes:

```text
user satisfaction
menu/item acceptance
plate waste
```

Coefficients and constraints must be obtained from policy/PMR rather than team intuition.

---

# 8. Tradeoff questions for Persona PMR

Do not ask the Persona simply to rank nine abstract criteria.

Use concrete tradeoffs:

- If reducing tomorrow's production by 5% had a small chance of one main dish selling out 15 minutes early, would you do it? Why?
- Which is worse: 100 unserved portions or one early sellout incident?
- What happens internally after an early sellout?
- What happens after a high-surplus service?
- Would you accept lower surplus if it required more staff work every morning?
- Which recommendation would you reject even if the forecast looked statistically better?
- If a recommendation conflicts with tasting/quality feedback, what wins?
- What performance measure would make you say after one month: `this improved my operation`?

Use the answers to derive prioritized criteria rather than asking for polite importance scores.

---

# 9. Persona purchasing-criteria hypothesis revised

Current proxy-informed order to **test**, not assert:

1. hard food-safety / contract compliance;
2. service continuity / no unacceptable shortage;
3. actionable timing before freeze point;
4. operational simplicity / low staff burden;
5. food-quality/menu/portion compatibility;
6. reliability, uncertainty handling and human control;
7. measurable physical/economic improvement;
8. system/integration/privacy/procurement fit;
9. sustainability/reporting value.

The actual Persona may rank economic value, service continuity or another dimension differently.

---

# 10. Application consequence

Safe before PMR:

> University dining is a multi-objective operation in which food safety, service quality, user satisfaction and continuity matter alongside waste and efficiency. Our solution therefore treats shortage/service quality as guardrails rather than optimizing waste alone.

Unsafe before PMR:

> The Food Services manager's #1 priority is waste reduction.

Unsafe:

> Operators would trade X% shortage risk for Y% waste reduction.

Both require direct operator evidence.

---

## Current conclusion

Secondary research can tell us **what tradeoffs to ask about**.

It cannot tell us the real Persona's prioritized purchasing criteria.

The PMR goal is therefore not to confirm that all these dimensions matter; it is to discover:

```text
which one dominates when they conflict
who feels that consequence
what measurable threshold changes behavior
```
