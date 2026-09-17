# BOUNCAMPUS — KREATE Jury Q&A / Red-Team Sheet

Use this document to keep answers short, credible and consistent with the product truth boundary.

## 1. “What exactly is the problem?”

Boğaziçi University publishes **48,251 kg of food waste for 2025**. The product focuses on the repeated operating decision that happens before waste exists: **how much food should be prepared for the next service under uncertain demand?**

## 2. “What is actually novel here?”

The novelty is not another waste dashboard or a generic demand model. BOUNCAMPUS closes the operational loop:

```text
source-backed context → uncertainty-aware band → human decision → measured service → recalibration
```

It also exposes when the model should **withhold** a recommendation rather than pretending all forecasts are equally reliable.

## 3. “Do you have cafeteria POS data?”

No. We explicitly do not claim it. The current demand band is a `MODEL_ESTIMATE` built from campus context. The 14-day pilot is designed to start with aggregate operational measurements and no student identity. POS time-bucket totals would be a later calibration input if the institution chooses to provide them.

## 4. “Then how can you recommend production?”

We do not claim the recommendation is already production-grade. We expose a conservative band and its signal coverage, and we gate it as:

- `PILOT_READY`
- `REVIEW_REQUIRED`
- `WITHHOLD`

The first deployment is a controlled human-reviewed pilot, not autonomous production control.

## 5. “Why not just use last week’s meal count?”

A static historical rule cannot respond well to changes in class schedules, academic-calendar effects, weather and menu context. BOUNCAMPUS tests whether adding those signals reduces normalized waste compared with the existing planning process. If the controlled pilot does not beat control, the model hypothesis fails.

## 6. “What is your primary KPI?”

**Waste kg per 100 served meals.**

We normalize by served volume because `kg/service` alone can be gamed by comparing a quiet service against a busy one.

## 7. “What does success mean?”

The pre-registered pilot target is:

- at least 5 measured services per arm;
- at least 10% lower normalized waste versus matched control;
- no increase in early-sellout incidence;
- no food-safety process bypass;
- consistent measurement quality.

The 10% value is a **target**, not an achieved result.

## 8. “Couldn’t you reduce waste simply by producing too little?”

That is exactly why the pilot has an early-sellout guardrail and records produced and served portions. A system that reduces waste by degrading meal availability does not pass the gate.

## 9. “Where is the AI?”

The decision model fuses schedule-derived demand context with weather, menu and academic-calendar signals and converts source availability into an uncertainty-aware production band. The important product behavior is not the label “AI”; it is that model uncertainty changes the operational recommendation and can force `WITHHOLD`.

## 10. “Why is this climate tech?”

Food waste embeds the emissions, water, energy and land use of food that was produced but not consumed. BOUNCAMPUS acts **before avoidable surplus is created**. For the pilot, we intentionally measure the direct physical outcome—food waste mass—before converting it into broader climate equivalents.

## 11. “Where are your CO2 and water savings?”

We do not claim them yet. First we measure food-waste reduction. Any later CO2/water conversion must use a documented, context-appropriate lifecycle factor. Separating direct measurements from conversion assumptions is part of the evidence design.

## 12. “Why not compost/recover the waste instead?”

Recovery matters and Boğaziçi already reports recovery activity. BOUNCAMPUS focuses one step earlier in the hierarchy: **prevention at source**. The decision lab still tracks recovery scenarios, but prevention is the primary operating objective.

## 13. “What if a source goes down?”

The production band carries signal coverage. Missing contextual signals widen uncertainty; missing critical context can move the decision to `REVIEW_REQUIRED` or `WITHHOLD`. The official historical baseline remains available even if live/model context degrades.

## 14. “Can the AI send a kitchen command?”

No. `AUTO_DISPATCH=false`. A human operator explicitly approves, edits or holds the recommendation. The hackathon UI demonstrates the same contract and does not fake a connection to an external kitchen system.

## 15. “How do you prevent hallucinated impact claims?”

The API exposes a claim policy separating:

- facts we can claim now;
- model/scenario outputs;
- statements forbidden until measured.

The UI uses the same boundary. Model outputs are labeled `MODEL_ESTIMATE`; scenarios are labeled as scenarios; achieved savings are not shown without measured pilot data.

## 16. “How will you run the first pilot?”

Use matched control and intervention services over 14 days. Record:

- forecast meals;
- produced portions;
- served portions;
- edible surplus kg;
- waste kg;
- early sell-out;
- operator override;
- anomaly notes.

The repository contains a downloadable CSV template and the exact formulas used for the scorecard.

## 17. “Does this require personal data?”

No. The first pilot is service-level and aggregate. It does not require student identity, payment identity, device tracking or individual consumption records.

## 18. “How do you scale beyond Boğaziçi?”

The transferable object is not the campus map. It is the operating loop and evidence contract. The same pattern can be deployed in hospitals, factories, schools, municipal kitchens and large catering operations with organization-specific demand signals.

## 19. “What about your energy, mobility and 3D features?”

They remain implemented expansion modules. We intentionally do not lead with them because a hackathon pitch becomes weaker when three different climate problems compete for attention. Food waste is the wedge; the shared provenance, human-approval and measure-learn architecture is the platform.

## 20. “What would make you stop building this?”

A well-run pilot showing no meaningful normalized waste reduction, persistent service degradation, or unusably high operator override would be evidence that the current intervention is not valuable enough. The system is designed to produce that answer instead of protecting the demo narrative.

## 21. “What do you want from the accelerator?”

The next milestone is not more UI. It is institutional validation:

1. secure one cafeteria pilot partner;
2. establish a repeatable measurement process;
3. calibrate with real production/served data;
4. validate normalized waste reduction;
5. only then add documented climate-equivalent accounting and multi-site deployment.

## 22. 15-second final answer

> BOUNCAMPUS starts from a real 48-ton food-waste baseline, turns campus context into an uncertainty-aware production band, keeps a human in control, and has a pre-registered 14-day pilot that can prove the product wrong. We are building the decision layer before the waste happens, not another dashboard after it does.
