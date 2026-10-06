# PMR Research Synthesis — 2026-10-06

**Owner:** IE  
**Status:** secondary-research synthesis; not customer validation.  
**Current wedge:** human-reviewed decision support around a reachable pre-service food-production quantity decision in institutional/university dining.

## Executive conclusion

The external evidence supports **mechanism plausibility**, not validation of the Boğaziçi wedge.

Three things are now clearer:

1. Demand forecasting under uncertainty is a real institutional-food-service problem and has been studied with reservation/show-no-show, historical demand, calendar/context, and asymmetric shortage/waste costs.
2. Production mismatch is **not automatically the dominant cause of food waste**. Plate waste, taste/quality, portion size, menu design, preparation loss, and food-safety constraints repeatedly appear as alternative causes.
3. Forecasting and AI waste tracking are already commercialized. BOUNCAMPUS cannot credibly differentiate on “AI predicts cafeteria demand” or “computer vision measures waste” alone.

The next value comes from real PMR on decision ownership, freeze time, waste-stage causality, risk asymmetry, incentive allocation, and data semantics.

---

## H1 — Reachable production control point

### Secondary evidence

- GTÜ publicly describes planned quantities using historical consumption and daily user counts, plus reactive replenishment when unexpected demand depletes items.
- ITU publicly describes planning inputs including academic calendar, course/exam intensity, menu-dependent behavior, weather, and historical consumption.
- Academic catering-demand studies model a pre-service demand decision and compare it with observed demand.

### What this establishes

A recurring pre-service planning mechanism is plausible across institutions.

### What remains UNKNOWN at Boğaziçi

- who sets or approves the quantity;
- exact decision object: total production, campus allocation, batch release, portion mix, or another control;
- when the decision freezes;
- who may revise it after the first plan.

**PMR priority:** highest.

---

## H2 — Material, actionable demand mismatch

### Supporting pressure

Forecasting studies show that better demand estimates can reduce modeled/estimated overproduction while protecting service level.

### Falsification pressure

University-canteen intervention and plate-waste studies repeatedly identify:
- poor taste / food quality;
- large portions;
- menu composition;
- consumer behavior;
- preparation/plate waste;

as meaningful causes.

Therefore:

> `food waste exists` does not imply `overproduction caused by forecast error is the dominant avoidable waste`.

### Required PMR / measurement

Separate at least:
- preparation waste;
- unserved edible production surplus;
- plate/post-consumer waste;
- food-safety discard;
- shortage / substitution / early sellout.

Do not claim causal waste reduction from monthly aggregate totals.

---

## H3 — Asymmetric shortage risk / safety buffer

This is strongly motivated by both operations and literature.

The Faezirad et al. university-dining model explicitly incorporates reservation/show-no-show uncertainty and both waste cost and shortage penalty. Rodrigues et al. compare forecast-driven decisions with baseline estimates while tracking wasted meals and unmet demand.

### Product implication

Optimize a decision loss / service constraint, not prediction error alone.

PMR must recover:
- last surplus incident;
- last shortage incident;
- operational consequence of each;
- intentional safety buffer;
- emergency replenishment/substitution;
- penalty/complaint/escalation path.

---

## H4 — Measurement/data feasibility

### Public Boğaziçi context exists

Official university pages expose:
- aggregate food-waste reporting;
- public menu/calendar context;
- some reservation workflow evidence in a bounded Kilyos period;
- high-level dining scale/context.

### But service truth is not public

Public monthly food-waste totals cannot provide:
- service-level `actual_served`;
- `produced_portions`;
- per-service edible surplus;
- shortage/sellout;
- decision-time operator estimate;
- reservation-to-served reconciliation.

That is why #82 remains a critical CS1 dependency.

### Important source-quality finding

The current official 2025 food-waste table contains months where the “delivered to İSTAÇ” amount exceeds the displayed monthly “total food waste” amount even though the page describes delivered waste as included in the total. Preserve the raw values, but treat them as **unreconciled public reporting** until the source owner explains the semantics.

This is exactly the kind of issue the product's provenance/source-quality boundary is meant to handle.

---

## H5 — Persona / authority

No secondary source can validate the Boğaziçi decision owner.

Public organization pages can identify outreach candidates, but the validated persona requires a real person who can describe:
- the last quantity decision;
- who could overrule it;
- who owns shortages;
- who owns surplus/waste;
- who approves pilots;
- who controls budget/procurement.

Keep persona = `TESTING`.

---

## H6 — Workflow adoption

External studies and vendor cases show that human food-service teams can use waste/forecasting systems, but that does not establish Boğaziçi workflow fit.

The critical adoption question is not:

> “Would you use AI?”

It is:

> “What new information has actually caused you to change an already-planned quantity, who approved that change, how late could it happen, and what would make you refuse a recommendation?”

---

## Competitor / novelty consequence

Existing research in `KREATE/RESEARCH/COMPETITOR_CAPABILITY_RED_TEAM_2026-10-05.md` is reinforced:

- Winnow markets food-waste measurement and production forecasting.
- Leanpath markets university food-waste tracking and operational feedback.
- Turkish campus-sustainability platforms already cover broad reporting/evidence workflows.
- sophisticated universities already use calendar/weather/history-type planning inputs.

### Claims to avoid

- “first AI university food-waste platform”;
- “competitors only measure waste”;
- “nobody forecasts demand”;
- “academic calendar + weather + history is our moat”;
- “computer vision makes the product unique”.

### Better differentiation hypothesis to test

A narrow operations layer that:
- targets a named reachable decision before freeze;
- reconciles campus-specific source semantics;
- makes uncertainty and `WITHHOLD` explicit;
- records operator approval/override;
- links recommendation → action → measured outcome;
- fits Turkish university/contractor governance and procurement.

Still a hypothesis until PMR says it matters.

---

## Highest-information-value interview sequence

1. **Quantity owner + freeze point** — direct operations / production actor.
2. **Waste-stage causality** — production + waste-measurement owner.
3. **Shortage vs surplus asymmetry** — production lead + service manager.
4. **Contract economics** — university/contractor procurement or contract owner.
5. **Existing planning stack** — ask to reconstruct the actual production sheet/system.
6. **Service-level data semantics** — data/report owner; field-by-field.
7. **Real purchasing criteria** — validated decision owner/economic buyer.
8. **Second-site same-product test** — GTÜ/ITU/contractor-led site.

## Cross-role actions

### IE
Run interviews against H1–H6. Promote only real interview claims to `E-INT-*`.

### CS1
Use [source_catalog.json](./source_catalog.json) and the data-quality note to harden source admission. Continue #82; do not infer service rows from aggregate waste.

### CS2
Use sources to constrain product/application claims. Treat academic and vendor outcome numbers as external case results, not BOUNCAMPUS impact.

### EE
Use UNEP / FLW / Türkiye guidance to freeze prospective measurement boundary and direct-ground-truth method before adding sensing.

### EHB
Do not build measurement hardware merely because it is technically possible. Wait for a specific missing decision-critical field and EE validation requirement.

## Decision gate

Keep the dining wedge only while PMR can plausibly establish all of:

```text
material avoidable loss
+ reachable decision owner
+ meaningful pre-freeze control
+ usable pre-decision signal
+ measurable/reconcilable outcome
+ baseline to beat
+ acceptable workflow burden
+ viable incentive/procurement path
```

If repeated evidence breaks any of these, modify or kill the wedge rather than adding model complexity.
