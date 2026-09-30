# CS1 Decision Intelligence System — Design Specification

**Status:** design approved in principle; this document is the authoritative architecture for the CS1 implementation plan.

**Date:** 2026-09-30

**Owner:** CS1 — Decision Intelligence Lead

**Scope:** BOUNCAMPUS institutional dining / food-waste decision support, with interfaces designed so the same decision-intelligence primitives can later support other campus operations.

## 1. Purpose

BOUNCAMPUS needs a decision system, not a forecast demo. The system must answer a harder question than “what is tomorrow's demand?”: **given the information available at the actual decision time, what should an operator do, how uncertain is that recommendation, when should the system abstain, and how will we later prove whether the recommendation was better than the current alternative?**

The architecture therefore separates five concerns that are currently partially mixed together:

1. source health and decision-time context,
2. forecast / estimate generation,
3. baseline comparison and model eligibility,
4. operational decision policy under asymmetric risk,
5. measured pilot evaluation and claim promotion.

The system must remain useful before complete cafeteria telemetry exists, but it must never convert missing evidence into fake certainty.

## 2. Current-State Findings

The repository already contains several strong pieces that should be preserved:

- the active Next `/api/v1/food` route distinguishes official historical data, modeled outputs, unavailable telemetry, scenarios, and forbidden claims;
- `buildProductionBand` already exposes source coverage, readiness, operator approval, no auto-dispatch, and reason codes;
- the pilot score endpoint accepts measured records rather than fabricating outcomes;
- the CS1 role explicitly requires baseline-first evaluation, uncertainty honesty, abstention, operator usefulness, and measurable pilot design.

The important weaknesses are architectural rather than cosmetic:

- the current TypeScript production band uses fixed signal weights and fixed multiplicative band factors without an explicit policy/version object;
- readiness is driven mainly by source availability, while model/data validation state is not represented as a separate dimension;
- the Python `/food` endpoint exposes pre-pilot “potential waste saved” and “cost saved” values derived from an assumed buffer, creating a claim-boundary inconsistency;
- the Python demand model trains from `GENERATED_DATA_DIR`, so its outputs cannot be treated as validation against real cafeteria demand;
- Python and Next can independently describe food decisions, which risks semantic drift;
- no shared baseline-evaluation harness currently determines whether additional model complexity beats realistic alternatives;
- uncertainty semantics do not yet distinguish heuristic planning ranges from statistically calibrated predictive intervals;
- operator overrides can be measured in the pilot but are not yet a first-class decision-feedback event.

## 3. Design Goals

The implementation must provide all of the following.

### 3.1 Decision integrity

Every recommendation must state:

- what service / decision it refers to,
- what information was available at decision time,
- which forecast / baseline method generated the estimate,
- what uncertainty representation is being used,
- which policy converted the estimate into a planning action,
- why the recommendation is actionable, review-only, or withheld,
- whether operator approval is required,
- what evidence class supports each material value.

### 3.2 Baseline-first evaluation

The learned model is one candidate, not the default winner. A method is operationally eligible only after comparison against meaningful baselines on time-respecting evaluation data.

### 3.3 Honest uncertainty

The system may expose a heuristic planning range before calibration exists, but that range must be labeled as a policy heuristic. Terms such as “confidence interval”, “90% interval”, or “calibrated uncertainty” are forbidden unless the relevant calibration evaluation exists.

### 3.4 Safe abstention

`WITHHOLD` is a valid product outcome. Missing, stale, contradictory, out-of-domain, or inadequately validated information can prevent a recommendation.

### 3.5 Human decision support, not autonomous kitchen control

The product may recommend, explain, and record operator action. It must not automatically dispatch a production order during the application/pilot stage.

### 3.6 Measurable learning loop

Operator overrides, actual production, actual served portions, waste, early sell-out, source outages, and method identity must be recordable so the next evaluation can learn from real decisions rather than screenshots.

### 3.7 Claim firewall

No endpoint or UI surface may transform model output, a scenario, or a policy heuristic into achieved environmental or financial impact.

## 4. Explicit Non-Goals

This design does **not** require, before real target data exists:

- a deep-learning model,
- a statistically calibrated interval,
- a causal claim that BOUNCAMPUS reduces waste,
- automated kitchen dispatch,
- student-level tracking,
- fabricated historical POS records,
- arbitrary complexity added for presentation value.

The architecture supports these capabilities only when evidence justifies them.

## 5. Research-Informed Principles

The implementation follows several findings from forecasting and decision-support literature:

1. **Simple methods remain serious competitors.** Restaurant forecasting studies show that simpler linear/statistical approaches can be competitive depending on the horizon and data, so the system must benchmark rather than assume complex ML wins.
2. **Prediction accuracy alone is insufficient.** Operational decisions should be evaluated against the cost and utility of the downstream decision, not only one generic forecasting metric.
3. **Human review must be measured, not romanticized.** Human adjustments can help or hurt depending on context. Overrides therefore become logged evidence rather than assumed improvement.
4. **Abstention and calibration are separate capabilities.** A model can be accurate on average yet badly calibrated on important cases. The system must evaluate calibration and selective risk before using probabilistic confidence operationally.
5. **Probabilistic forecasts should be judged by decision value as well as statistical quality.** If a probabilistic method improves coverage but produces worse operational choices, it should not win the decision layer.

### Research references

- A. Schmidt, Md. Wasi Ul Kabir, T. Hoque (2022), *Machine Learning Based Restaurant Sales Forecasting*, Machine Learning and Knowledge Extraction 4, 105–130. https://consensus.app/papers/machine-learning-based-restaurant-sales-forecasting-schmidt-kabir/53da5c3c140d54c19b3afad3c4b64fce/?utm_source=chatgpt
- Sushil Punia, Sonali Shankar (2022), *Predictive analytics for demand forecasting: A deep learning-based decision support system*, Knowledge-Based Systems 258, 109956. https://consensus.app/papers/predictive-analytics-for-demand-forecasting-a-deep-punia-shankar/e1b39ae32a195daf95f265dc2100e0ac/?utm_source=chatgpt
- Naghmeh Khosrowabadi, K. Hoberg, Christina Imdahl (2022), *Evaluating human behaviour in response to AI recommendations for judgemental forecasting*, European Journal of Operational Research 303, 1151–1167. https://consensus.app/papers/evaluating-human-behaviour-in-response-to-ai-khosrowabadi-hoberg/455bc92133375b9f863885da36501731/?utm_source=chatgpt
- Adam Fisch, T. Jaakkola, R. Barzilay (2022), *Calibrated Selective Classification*, Transactions on Machine Learning Research. https://consensus.app/papers/calibrated-selective-classification-fisch-jaakkola/35272f7c8d345a9f89098fe0779029f5/?utm_source=chatgpt
- Elena Revilla, M. Saenz, Matthias Seifert, Ye Ma (2023), *Human–Artificial Intelligence Collaboration in Prediction: A Field Experiment in the Retail Industry*, Journal of Management Information Systems 40, 1071–1098. https://consensus.app/papers/human–artificial-intelligence-collaboration-in-revilla-saenz/ef59fcab5b125edca2b21e758c6dcc4a/?utm_source=chatgpt
- Sheng-Jie Wang, Yanfei Kang, F. Petropoulos (2023), *Combining probabilistic forecasts of intermittent demand*, European Journal of Operational Research 315, 1038–1048. https://consensus.app/papers/combining-probabilistic-forecasts-of-intermittent-wang-kang/c064a03c698956eb838b7e5051b449fb/?utm_source=chatgpt

## 6. System Architecture

The decision system is organized as a pipeline with explicit boundaries:

```text
Source Adapters
    ↓
Decision-Time Signal Snapshot
    ↓
Forecast Candidate Layer ──→ Baseline Candidate Layer
    ↓                           ↓
Forecast Evaluation / Eligibility Registry
    ↓
Uncertainty Representation
    ↓
Decision Policy + Risk Objective
    ↓
Readiness / Abstention Gate
    ↓
Operator Recommendation + Explanation
    ↓
Operator Action / Override Event
    ↓
Pilot Measurement + Evaluation
    ↓
Evidence / Claim Promotion
```

No later layer may silently invent evidence that an earlier layer does not provide.

## 7. Truth and Provenance Model

Every material value must carry or inherit one of these classes:

- `OFFICIAL_PUBLIC`: value copied from an official public source;
- `MEASURED_OPERATIONAL`: value measured in an authorized pilot or operational system;
- `MODEL_ESTIMATE`: output produced by a predictive model;
- `BASELINE_ESTIMATE`: output produced by an explicit baseline method;
- `POLICY_HEURISTIC`: value created by a transparent decision rule that has not been statistically learned or calibrated;
- `SCENARIO`: user-selected what-if calculation;
- `GENERATED_SANDBOX`: synthetic/generated data or an output dependent on such data;
- `UNAVAILABLE`: value not currently observed.

`GENERATED_SANDBOX` may demonstrate software behavior and experiment plumbing. It may not be promoted into measured performance or an achieved impact claim.

## 8. Decision-Time Signal Snapshot

A source being present is not enough. Each signal snapshot must capture:

```ts
type DecisionSignal = {
  id: string;
  available: boolean;
  valuePresent: boolean;
  provenance: ProvenanceClass;
  sourceId: string;
  observedAt: string | null;
  effectiveFor: string | null;
  freshnessSeconds: number | null;
  maxFreshnessSeconds: number | null;
  quality: 'OK' | 'STALE' | 'DEGRADED' | 'MISSING' | 'CONTRADICTORY';
  requiredForPolicy: boolean;
  reasonCodes: string[];
};
```

Initial food-decision candidates include:

- course schedule,
- academic calendar,
- menu,
- weather,
- event context,
- historical service counts when later available,
- operator-supplied context when explicitly recorded.

Signal importance is **not** hard-coded as scientific truth. A policy may currently assign heuristic weights, but those weights must be versioned and labeled `POLICY_HEURISTIC` until experiments justify them.

## 9. Forecast Candidate Layer

Forecasting becomes a registry of candidate methods. Each method exposes a common interface:

```ts
type ForecastCandidateResult = {
  methodId: string;
  methodVersion: string;
  target: 'MEALS_SERVED';
  horizon: string;
  pointEstimate: number | null;
  interval: PredictiveInterval | null;
  provenance: ProvenanceClass;
  trainingDataClass: 'GENERATED' | 'MEASURED' | 'MIXED' | 'NONE';
  featureIds: string[];
  eligibleForDecision: boolean;
  eligibilityReasons: string[];
};
```

Candidate methods should include, as data allows:

1. same comparable service / same weekday,
2. recent median,
3. rolling mean,
4. schedule-only estimate,
5. menu-conditioned simple baseline,
6. operator estimate captured during PMR/pilot,
7. current XGBoost model,
8. later quantile / probabilistic candidates only when real target data supports them.

The current XGBoost path depends on generated cafeteria data and must therefore be classified as `GENERATED_SANDBOX` until trained/evaluated on an acceptable measured target dataset.

## 10. Time-Safe Baseline Evaluation

Offline evaluation must prevent leakage. Random train/test shuffling is not the default for service forecasting.

The evaluator uses chronological or rolling-origin splits when timestamps exist. Each candidate is evaluated on exactly the same eligible service rows.

Core metrics:

- MAE,
- WAPE,
- sMAPE where denominator behavior is acceptable,
- signed mean error / bias,
- median absolute error,
- large-underforecast incidence,
- large-overforecast incidence,
- error by cafeteria / meal type / weekday where sample size permits.

Decision metrics become available only when the corresponding measured outcomes exist:

- waste kg / 100 served,
- overproduction rate,
- early-sellout incidence,
- operator override rate,
- service-level decision loss.

A model is not promoted because it has a lower training loss. The evaluation registry records whether it beats a meaningful baseline and on what dataset.

### Eligibility states

- `SANDBOX_ONLY`: software/demo use only;
- `EVALUATED_OFFLINE`: evaluated on acceptable real targets but not yet operator-piloted;
- `PILOT_ELIGIBLE`: meets predefined offline gates and can be used in a human-reviewed pilot;
- `PILOT_EVALUATED`: has measured pilot outcome evidence;
- `RETIRED`: kept for reproducibility but not selectable.

## 11. Uncertainty Model

The design separates two different objects.

### 11.1 Planning range

A planning range may be generated from policy heuristics before calibrated uncertainty exists.

Required metadata:

```ts
type PlanningRange = {
  lower: number;
  target: number;
  upper: number;
  semantics: 'POLICY_PLANNING_RANGE';
  provenance: 'POLICY_HEURISTIC';
  policyVersion: string;
  calibrated: false;
};
```

It must never be called a confidence interval.

### 11.2 Predictive interval

A predictive interval is allowed only when produced by an evaluated probabilistic method.

```ts
type PredictiveInterval = {
  lower: number;
  upper: number;
  nominalCoveragePct: number;
  method: string;
  calibrated: boolean;
  calibrationDatasetId: string;
  empiricalCoveragePct: number | null;
};
```

Candidate approaches later include quantile regression, conformal intervals, or other justified methods. Promotion requires empirical coverage checks on held-out chronological data.

### 11.3 Selective risk

Once calibrated uncertainty exists, the evaluator should report a risk–coverage curve: how error changes as the system abstains on increasingly uncertain cases. A single confidence threshold without such evaluation must not be described as “safe”.

## 12. Decision Policy and Asymmetric Risk

The decision layer must not simply return forecast × 1.05 and call it optimization.

It receives:

- forecast candidate result,
- source snapshot,
- operational constraints,
- current policy version,
- known model validation state,
- PMR-informed risk assumptions when available.

The abstract objective is:

```text
expected decision loss
= overproduction_cost × overproduction
+ underproduction_cost × underproduction
+ early_sellout_penalty
+ operator_burden_penalty
+ safety_violation_penalty
```

Before PMR establishes credible cost ratios, numeric weights are policy hypotheses and must be labeled `POLICY_HEURISTIC`. They may be used for scenario/sensitivity analysis, not presented as learned economics.

The policy must support sensitivity analysis over plausible risk ratios. If the recommendation changes drastically under small weight changes, readiness should degrade and the reason should be visible.

## 13. Readiness and Abstention

Readiness combines **source readiness**, **method eligibility**, **uncertainty state**, and **operational constraints**. It is not a synonym for source coverage.

Primary states remain:

- `PILOT_READY`
- `REVIEW_REQUIRED`
- `WITHHOLD`

### 13.1 WITHHOLD

Examples:

- a policy-critical source is missing or stale;
- no eligible forecast/baseline exists for the requested service;
- the selected method is outside its supported domain;
- input values fail integrity checks;
- contradictory sources create unresolved decision ambiguity;
- a safety constraint cannot be checked;
- the only available estimate is sandbox-generated and the request is for a real operational recommendation.

When `WITHHOLD`, the API may return estimates for diagnostic visibility, but `recommendation.actionable` is false and no production target is presented as an operator action.

### 13.2 REVIEW_REQUIRED

Examples:

- useful context exists but one non-critical source is degraded;
- only a heuristic planning range exists;
- the model/baseline disagreement exceeds a policy threshold;
- policy sensitivity is high;
- an offline-evaluated model is being shadow-tested rather than piloted.

### 13.3 PILOT_READY

Requires all of the following:

- required decision-time signals satisfy policy health rules;
- the selected method is `PILOT_ELIGIBLE` or better;
- decision contract and provenance are complete;
- no safety blocker exists;
- operator approval is required;
- auto-dispatch is false.

`PILOT_READY` means suitable for an operator-reviewed experiment. It does **not** mean waste reduction is proven.

## 14. Method Selection and Disagreement

The system should not silently switch methods. It returns:

- selected method,
- selection rule,
- evaluated alternatives,
- baseline comparison state,
- disagreement diagnostics.

An initial selection policy may be:

1. prefer the highest-eligible method that beats the designated operational baseline on the registered primary offline metric;
2. if no complex method beats the baseline, use the baseline;
3. if no acceptable evaluation exists, remain review-only or withhold depending on context;
4. if methods disagree beyond a configured threshold, expose the disagreement and require review.

This makes “simple baseline wins” a valid system outcome.

## 15. Explanation Contract

Explanations must be generated from actual inputs and policy decisions, not decorative copy.

A recommendation explanation may include:

- selected method and why it was selected,
- sources used / missing / stale,
- forecast-vs-baseline difference,
- active policy heuristic,
- decision constraint that changed the target,
- uncertainty / planning-range semantics,
- readiness downgrade reasons,
- operator-review requirement.

Reason codes are machine-readable and stable; display text may evolve independently.

## 16. Canonical Decision Contract

A versioned language-neutral schema becomes the contract source of truth. TypeScript and Python models conform to it.

Representative response:

```json
{
  "schemaVersion": "food-decision-v1",
  "service": {
    "serviceId": "2026-10-01:B-SOUTH-GY:lunch",
    "date": "2026-10-01",
    "cafeteriaId": "B-SOUTH-GY",
    "mealType": "lunch"
  },
  "context": {
    "signals": [],
    "sourceCoveragePct": 75,
    "criticalSourcesHealthy": true
  },
  "forecast": {
    "selectedMethodId": "schedule-baseline-v1",
    "pointEstimate": 810,
    "provenance": "BASELINE_ESTIMATE",
    "eligibilityState": "PILOT_ELIGIBLE",
    "predictiveInterval": null
  },
  "decision": {
    "planningRange": {
      "lower": 770,
      "target": 825,
      "upper": 875,
      "semantics": "POLICY_PLANNING_RANGE",
      "provenance": "POLICY_HEURISTIC",
      "policyVersion": "food-policy-v1",
      "calibrated": false
    },
    "readiness": "PILOT_READY",
    "actionable": true,
    "operatorApprovalRequired": true,
    "automaticDispatchAllowed": false,
    "reasonCodes": ["HEURISTIC_BAND_NOT_CALIBRATED"]
  },
  "evaluation": {
    "baselineComparisonAvailable": true,
    "pilotOutcomeValidated": false
  },
  "claimBoundary": {
    "achievedSavingsAvailable": false
  }
}
```

Exact numeric example values are illustrative contract examples, not performance claims.

## 17. Runtime Responsibility Split

### 17.1 Next / TypeScript — product decision runtime

The active Next API is the authoritative product orchestration layer for:

- source snapshots,
- decision contract assembly,
- readiness / abstention,
- policy heuristics,
- explanation and claim boundary,
- pilot score API.

New code should live in focused modules under `frontend/src/lib/decision-intelligence/` rather than allowing `food-waste.ts` to become a monolith.

Recommended module boundaries:

- `contracts.ts`
- `provenance.ts`
- `signals.ts`
- `readiness.ts`
- `policy.ts`
- `baselines.ts`
- `uncertainty.ts`
- `evaluation.ts`
- `pilot.ts`
- `claims.ts`
- `index.ts`

### 17.2 Python — model and offline evaluation layer

Python owns:

- model training / inference,
- baseline benchmark tooling,
- chronological evaluation,
- calibration experiments,
- offline ablations,
- model metadata / eligibility artifacts.

Python must not invent achieved impact. The legacy `/food` response must be brought behind the same contract / claim rules or reduced to a compatibility adapter.

### 17.3 Shared contract

A versioned JSON schema under `contracts/` defines the language-neutral response contract. Contract fixtures are validated in CI from both TypeScript-facing and Python-facing tests where practical.

## 18. Pilot Measurement System

The current matched control/intervention protocol is retained and strengthened.

Required service record fields include:

- date / service ID,
- arm,
- method ID / version,
- forecast point estimate,
- planning range,
- selected target shown to operator,
- operator final target,
- operator action (`ACCEPT`, `OVERRIDE`, `REJECT`),
- override reason code,
- produced portions,
- served portions,
- edible surplus kg,
- waste kg,
- early sell-out,
- source-health snapshot ID,
- notes.

### 18.1 Primary KPI

`waste_kg_per_100_served = waste_kg / served_portions × 100`

This remains the pre-registered primary outcome because it normalizes waste by service volume.

### 18.2 Guardrails

At minimum:

- early-sellout incidence must not worsen materially versus matched control;
- no food-safety process may be bypassed;
- missing measurements are reported, not silently imputed into favorable outcomes;
- operator overrides remain in the dataset;
- service exclusions require a pre-specified or documented reason.

### 18.3 Pilot interpretation states

Retain conservative language:

- `INSUFFICIENT_EVIDENCE`
- `PROMISING`
- `FAILED`

A future `SUPPORTED` or `VALIDATED` state requires a stronger evidence rule and is intentionally absent from the initial application-stage scorecard.

### 18.4 Statistical reporting

For small pilots, report raw service counts, arm means/medians, effect size, and uncertainty without pretending a tiny sample proves a population-level effect. Bootstrap or randomization/permutation intervals may be added as descriptive sensitivity analysis when sample structure permits; they do not override design limitations.

## 19. Operator Feedback Loop

Every recommendation event should be addressable by ID. Operator action is stored as a separate event so the original recommendation cannot be rewritten after the fact.

Operator event:

```ts
type OperatorDecisionEvent = {
  decisionId: string;
  action: 'ACCEPT' | 'OVERRIDE' | 'REJECT';
  finalTarget: number | null;
  reasonCode: string | null;
  note: string | null;
  recordedAt: string;
};
```

This enables later analysis of:

- whether overrides improve accuracy/outcomes,
- which conditions trigger overrides,
- whether explanations reduce unnecessary overrides,
- whether the model misses operator-visible context.

## 20. Experiment Suite

The implementation must support the following evidence-producing experiments rather than a single model demo.

### EXP-CS1-01 — Data lineage audit

Question: which current variables are official, measured, generated, inferred, or unavailable?

Output: machine-readable source/provenance registry and claim implications.

### EXP-CS1-02 — Baseline benchmark

Question: does the candidate model beat realistic simple alternatives on acceptable target data?

Output: chronological benchmark report with metrics and dataset provenance.

### EXP-CS1-03 — Signal ablation

Question: which context signals materially improve held-out performance or decision utility?

Output: per-signal delta; remove signals that add complexity without value.

### EXP-CS1-04 — Source outage / degradation

Question: does the system fail safely when schedule, menu, weather, or calendar data is missing/stale?

Output: readiness state and reason-code matrix.

### EXP-CS1-05 — Uncertainty calibration

Question: if intervals are introduced, do empirical coverage and interval width support their stated semantics?

Output: calibration table and risk–coverage analysis.

### EXP-CS1-06 — Policy sensitivity

Question: how sensitive is the recommendation to plausible under/overproduction cost ratios and planning-buffer assumptions?

Output: target-vs-policy surface and instability flags.

### EXP-CS1-07 — Operator workflow fit / H-006

Question: can an operator understand, review, override, and use the recommendation within the real workflow without unacceptable service/safety risk?

Output: PMR evidence, objections, decision timing, baseline workflow, override reasons, changed requirements.

### EXP-CS1-08 — Measured pilot

Question: does operator-reviewed decision support improve the pre-registered waste KPI without violating sell-out/safety guardrails?

Output: measured pilot scorecard and evidence registry entries.

## 21. Claim Firewall

The product and CI must enforce four categories.

### Allowed before measured pilot evidence

- official historical food-waste totals with source,
- current source-health state,
- model/baseline estimates clearly labeled,
- heuristic planning ranges clearly labeled,
- what-if scenarios clearly labeled,
- experiment design and pre-registered target,
- offline benchmark results when dataset provenance is disclosed.

### Forbidden before measured evidence

- “BOUNCAMPUS saved X kg of food”;
- “BOUNCAMPUS saved X TL”;
- avoided CO2/water attributed to BOUNCAMPUS operation;
- “actual production optimized” without measured production integration;
- “actual student demand observed” without real served/POS telemetry;
- “90% confidence interval” for an arbitrary heuristic band;
- “validated model” when evaluation used generated data only.

CI should scan critical active product surfaces and contract fixtures for known forbidden fields / wording and require provenance semantics to remain present.

## 22. Error Handling and Degraded Modes

The system must degrade explicitly rather than silently substitute facts.

Examples:

- official source unavailable → keep last official snapshot only if staleness is visible and policy permits it;
- weather source unavailable → mark signal unavailable; never synthesize “live” weather for the decision contract;
- menu source fallback → classify fallback separately from official live menu;
- model artifact missing → use an eligible baseline if available, otherwise withhold;
- generated dataset only → sandbox output may render but cannot become real operator action;
- invalid pilot measurement → reject the record with field-level errors;
- ambiguous service ID → reject rather than join measurements to the wrong service.

## 23. Testing Strategy

Testing is layered.

### 23.1 Unit tests

Cover:

- provenance classification,
- signal freshness / availability,
- readiness rules,
- abstention rules,
- policy heuristic boundaries,
- asymmetric-cost behavior,
- model/baseline selection,
- disagreement handling,
- claim firewall,
- pilot validation / scoring.

### 23.2 Contract tests

Fixtures must verify that:

- Next and Python-facing contracts preserve required fields;
- `WITHHOLD` cannot accidentally be actionable;
- `automaticDispatchAllowed` remains false for pilot stage;
- planning ranges cannot claim calibration;
- generated-data models cannot be promoted to validated operational status;
- achieved-savings fields do not reappear before measured evidence.

### 23.3 Evaluation tests

Synthetic/generated fixtures are allowed to test evaluator mechanics, but output must state that the fixture is not empirical performance evidence.

### 23.4 Failure-mode tests

Explicit source-outage matrix:

- schedule missing,
- menu missing,
- weather missing,
- calendar missing,
- multiple sources missing,
- stale source,
- contradictory source,
- model unavailable,
- model-vs-baseline large disagreement,
- negative / zero / malformed demand.

## 24. Migration Strategy

Implementation should be incremental and merge-safe.

### Phase A — Contract and truth boundary

- add shared decision schema,
- remove unsupported Python savings claims,
- add explicit provenance/readiness semantics,
- preserve current UI/API fields where compatibility is required.

### Phase B — Modular decision runtime

- split `food-waste.ts` decision logic into focused modules,
- make policy version and heuristic semantics explicit,
- add source freshness / health,
- prevent generated-data model from being silently treated as validated.

### Phase C — Baselines and offline evaluation

- implement baseline registry,
- add chronological evaluator,
- write machine-readable model eligibility artifact,
- support signal ablation and policy sensitivity.

### Phase D — Operator and pilot evidence loop

- extend pilot records with method/recommendation/operator events,
- strengthen scorecard completeness/guardrails,
- preserve raw override behavior.

### Phase E — Calibrated uncertainty when evidence permits

- add probabilistic candidate(s),
- evaluate empirical interval coverage,
- add risk–coverage analysis,
- promote interval semantics only if calibration passes.

No phase is allowed to claim outcomes from a later phase.

## 25. Expected Repository Shape

Likely implementation paths:

```text
contracts/
  food-decision-v1.schema.json

frontend/src/lib/decision-intelligence/
  contracts.ts
  provenance.ts
  signals.ts
  readiness.ts
  policy.ts
  baselines.ts
  uncertainty.ts
  evaluation.ts
  pilot.ts
  claims.ts
  index.ts

frontend/src/app/api/v1/food/
  route.ts
  pilot-score/route.ts
  pilot-template/route.ts

backend/app/decision/
  contract.py
  provenance.py
  baselines.py
  evaluation.py
  policy.py
  uncertainty.py

backend/app/models/
  food_demand.py

backend/app/routers/
  food.py

scripts/
  benchmark_food_demand.py
  test_food_decision_policy.py
  kreate_check.py

KREATE/EXPERIMENTS/
  CS1_DATA_LINEAGE.md
  CS1_BASELINE_BENCHMARK.md
  CS1_SIGNAL_ABLATION.md
  CS1_POLICY_SENSITIVITY.md
  CS1_H006_WORKFLOW_FIT.md
```

The implementation plan may combine or omit files when an existing repository pattern is clearly better, but it must preserve the responsibilities above.

## 26. Acceptance Criteria

The CS1 subsystem is implementation-complete for the application-stage architecture when all of the following hold:

1. a single versioned decision contract describes source state, estimate, planning range/interval semantics, readiness, human gate, reason codes, and claim boundary;
2. Python no longer exposes unsupported pre-pilot waste/cost savings as achieved or potential product impact;
3. generated-data-dependent models are visibly sandbox-only until evaluated on acceptable targets;
4. at least four realistic baseline methods are implemented or the absence of required real target data is explicitly surfaced by the benchmark tool;
5. evaluation is chronological/time-safe when timestamped data exists;
6. model selection can choose a simple baseline when it wins;
7. arbitrary planning ranges are labeled `POLICY_HEURISTIC` and `calibrated: false`;
8. calibrated interval terminology is impossible without calibration metadata;
9. `WITHHOLD` is tested for critical missing/degraded contexts;
10. operator approval is mandatory and automatic dispatch remains disabled;
11. operator override events can be represented without rewriting the original recommendation;
12. pilot scoring validates measured inputs, primary KPI, sell-out guardrail, override rate, and evidence sufficiency;
13. claim-firewall tests prevent reintroduction of unmeasured savings fields / validated-language leaks;
14. TypeScript typecheck/lint/build and repository Python validation remain green;
15. application-facing claims can be traced to official source, model result, policy heuristic, or measured pilot evidence without category mixing.

## 27. Deferred Promotion Gates

These capabilities remain architecturally supported but cannot be promoted until evidence exists:

- calibrated predictive intervals,
- learned asymmetric cost coefficients,
- validated signal importance,
- real operator-vs-model performance comparison,
- measured food-waste reduction,
- financial savings,
- environmental impact attribution,
- autonomous production control.

Their absence is not a product failure. Pretending they already exist would be.

## 28. Final Design Decision

BOUNCAMPUS CS1 will be implemented as an **evidence-aware decision intelligence system** rather than a single forecasting model. Forecasts, baselines, policy heuristics, operator judgment, uncertainty, source health, pilot measurements, and impact claims remain separate but connected layers. The architecture is intentionally capable of becoming more sophisticated, yet every promotion in sophistication requires stronger evidence rather than stronger wording.
