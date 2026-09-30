# CS1 Decision Intelligence System — Design Specification

**Status:** architecture direction approved; written specification awaiting final user review before implementation planning.

**Date:** 2026-09-30

**Owner:** CS1 — Decision Intelligence Lead

**Scope:** BOUNCAMPUS institutional dining / food-waste decision support, with reusable decision-intelligence primitives for later campus domains.

## 1. Purpose

BOUNCAMPUS needs a decision system, not a forecast demo. The system must answer: **given only the information actually available at the decision time, what should an operator do, why, with what uncertainty, when should the system abstain, and how can the team later prove whether that decision was better than the current alternative?**

The architecture therefore separates:

1. decision-time source health,
2. forecast / estimate generation,
3. baseline comparison and model eligibility,
4. uncertainty representation,
5. operational decision policy under asymmetric risk,
6. readiness / abstention,
7. operator review and override,
8. measured pilot evaluation,
9. evidence and claim promotion.

No later layer may manufacture evidence that an earlier layer does not provide.

## 2. Current-State Findings

Strong pieces already exist and should be preserved:

- the active Next `/api/v1/food` route separates official baseline data, modeled outputs, unavailable telemetry, scenarios, and forbidden claims;
- `buildProductionBand` already exposes source coverage, readiness, operator approval, no auto-dispatch, and reason codes;
- the pilot score endpoint accepts measured service records rather than fabricating outcomes;
- the CS1 role already requires baseline-first evaluation, uncertainty honesty, abstention, operator usefulness, and measurable pilot design.

The main weaknesses are architectural:

- current TypeScript signal weights and band factors are fixed heuristics without a versioned policy object;
- readiness is driven mainly by source availability while method/data validation state is not a separate dimension;
- the Python `/food` endpoint exposes pre-pilot potential waste/cost savings derived from an assumed buffer;
- the Python demand model trains from `GENERATED_DATA_DIR`, so it cannot be described as validated against real cafeteria demand;
- Python and Next can independently describe food decisions, creating semantic-drift risk;
- no shared baseline-evaluation harness determines whether model complexity beats realistic alternatives;
- uncertainty semantics do not yet distinguish a heuristic planning range from a statistically calibrated predictive interval;
- operator overrides are measured only as pilot fields rather than first-class feedback events;
- reproducibility metadata, drift monitoring, and method eligibility are not yet first-class artifacts.

## 3. Design Goals

### 3.1 Decision integrity

Every recommendation must state:

- service / decision identity,
- information available at decision time,
- method generating the estimate,
- uncertainty representation and semantics,
- policy producing the planning action,
- readiness state and reason codes,
- operator-approval requirement,
- provenance class for material values,
- evaluation / validation state.

### 3.2 Baseline-first evaluation

The learned model is one candidate, not the default winner. Simple operational alternatives must compete on the same time-safe evaluation rows. If a baseline wins, the system uses or recommends the baseline.

### 3.3 Honest uncertainty

A heuristic planning range may exist before statistical calibration, but it must be labeled `POLICY_HEURISTIC` and `calibrated: false`. Terms such as “confidence interval”, “90% interval”, and “calibrated uncertainty” are forbidden without calibration evidence.

### 3.4 Safe abstention

`WITHHOLD` is a valid product outcome. Missing, stale, contradictory, out-of-domain, safety-blocked, or inadequately validated contexts can prevent an operational recommendation.

### 3.5 Human decision support

During the application and pilot stages, BOUNCAMPUS may recommend, explain, and record operator action. It must not automatically dispatch production orders.

### 3.6 Measurable learning loop

Recommendations, source state, model version, operator actions, actual production, served portions, waste, sell-out, and exclusions must be linkable by stable IDs.

### 3.7 Claim firewall

No model output, scenario, generated-data result, or heuristic may be transformed into achieved environmental or financial impact without measured evidence.

## 4. Explicit Non-Goals

Before appropriate real target data exists, the architecture does not require:

- deep learning,
- calibrated predictive intervals,
- causal claims of waste reduction,
- autonomous kitchen control,
- student-level tracking,
- fabricated historical POS data,
- numeric economic loss weights presented as learned facts.

The architecture may later support such capabilities only when evidence supports promotion.

## 5. Research-Informed Principles

The design follows several lessons from forecasting and decision-support literature:

1. **Simple methods are serious competitors.** Restaurant forecasting work shows that simpler methods can remain competitive depending on data and horizon; complexity must earn its place.
2. **Forecast accuracy alone is not enough.** Operational usefulness depends on the downstream decision, asymmetric error costs, and service guardrails.
3. **Human review must be measured.** Human adjustments can help or hurt depending on context, so overrides become evidence rather than assumed improvement.
4. **Abstention and calibration are separate capabilities.** High average accuracy does not guarantee trustworthy uncertainty on the cases that matter.
5. **Probabilistic forecasts should be evaluated for decision utility as well as statistical quality.** Better interval metrics do not automatically mean better operational choices.

### Research references

- A. Schmidt, Md. Wasi Ul Kabir, T. Hoque (2022), *Machine Learning Based Restaurant Sales Forecasting*, Machine Learning and Knowledge Extraction 4, 105–130. https://consensus.app/papers/machine-learning-based-restaurant-sales-forecasting-schmidt-kabir/53da5c3c140d54c19b3afad3c4b64fce/?utm_source=chatgpt
- Sushil Punia, Sonali Shankar (2022), *Predictive analytics for demand forecasting: A deep learning-based decision support system*, Knowledge-Based Systems 258, 109956. https://consensus.app/papers/predictive-analytics-for-demand-forecasting-a-deep-punia-shankar/e1b39ae32a195daf95f265dc2100e0ac/?utm_source=chatgpt
- Naghmeh Khosrowabadi, K. Hoberg, Christina Imdahl (2022), *Evaluating human behaviour in response to AI recommendations for judgemental forecasting*, European Journal of Operational Research 303, 1151–1167. https://consensus.app/papers/evaluating-human-behaviour-in-response-to-ai-khosrowabadi-hoberg/455bc92133375b9f863885da36501731/?utm_source=chatgpt
- Adam Fisch, T. Jaakkola, R. Barzilay (2022), *Calibrated Selective Classification*, Transactions on Machine Learning Research. https://consensus.app/papers/calibrated-selective-classification-fisch-jaakkola/35272f7c8d345a9f89098fe0779029f5/?utm_source=chatgpt
- Elena Revilla, M. Saenz, Matthias Seifert, Ye Ma (2023), *Human–Artificial Intelligence Collaboration in Prediction: A Field Experiment in the Retail Industry*, Journal of Management Information Systems 40, 1071–1098. https://consensus.app/papers/human–artificial-intelligence-collaboration-in-revilla-saenz/ef59fcab5b125edca2b21e758c6dcc4a/?utm_source=chatgpt
- Sheng-Jie Wang, Yanfei Kang, F. Petropoulos (2023), *Combining probabilistic forecasts of intermittent demand*, European Journal of Operational Research 315, 1038–1048. https://consensus.app/papers/combining-probabilistic-forecasts-of-intermittent-wang-kang/c064a03c698956eb838b7e5051b449fb/?utm_source=chatgpt

## 6. Architecture

```text
Source Adapters
    ↓
Decision-Time Signal Snapshot
    ↓
Forecast Candidates ↔ Baseline Candidates
    ↓
Time-Safe Evaluation + Method Eligibility Registry
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

Each boundary has a versioned contract. The active Next runtime orchestrates product decisions; Python is responsible for model/offline analytics and must not independently create stronger claims.

## 7. Provenance Model

Every material value must carry or inherit one of:

- `OFFICIAL_PUBLIC`
- `MEASURED_OPERATIONAL`
- `MODEL_ESTIMATE`
- `BASELINE_ESTIMATE`
- `POLICY_HEURISTIC`
- `SCENARIO`
- `GENERATED_SANDBOX`
- `UNAVAILABLE`

`GENERATED_SANDBOX` can prove software plumbing works. It cannot prove real forecasting performance, pilot readiness, or achieved impact.

## 8. Decision-Time Signal Snapshot

Source presence is insufficient. Each signal must represent data quality at the decision timestamp.

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

Food-decision candidates include schedule, academic calendar, menu, weather, events, historical meal/service counts when available, and explicitly recorded operator context.

A feature may be used only if it would have been available at the real decision time. This rule prevents temporal leakage from future-known information.

Signal weights, when used before evidence exists, are versioned policy heuristics rather than learned importance.

## 9. Forecast Candidate Registry

All estimators implement a common result contract.

```ts
type ForecastCandidateResult = {
  methodId: string;
  methodVersion: string;
  target: 'MEALS_SERVED';
  horizon: string;
  pointEstimate: number | null;
  predictiveInterval: PredictiveInterval | null;
  provenance: ProvenanceClass;
  trainingDataClass: 'GENERATED' | 'MEASURED' | 'MIXED' | 'NONE';
  featureIds: string[];
  eligibilityState: MethodEligibility;
  eligibilityReasons: string[];
};
```

Candidate methods, as data permits:

1. same comparable service / same weekday,
2. recent median,
3. rolling mean,
4. schedule-only estimate,
5. menu-conditioned simple baseline,
6. operator estimate captured during PMR/pilot,
7. current XGBoost model,
8. later quantile / probabilistic methods.

The current XGBoost path is trained from generated cafeteria data and is therefore `GENERATED_SANDBOX` / `SANDBOX_ONLY` until trained and evaluated on acceptable measured targets.

## 10. Method Eligibility and Reproducibility

Method eligibility states:

- `SANDBOX_ONLY`
- `EVALUATED_OFFLINE`
- `PILOT_ELIGIBLE`
- `PILOT_EVALUATED`
- `RETIRED`

Every evaluation artifact must include:

- method ID and version,
- git commit SHA,
- dataset ID / provenance class,
- dataset checksum or immutable artifact identifier when possible,
- target definition,
- feature list,
- decision-time cutoff rule,
- split definition,
- evaluation window,
- metrics,
- baseline IDs,
- exclusions / missingness,
- generated-vs-measured label,
- eligibility conclusion.

A method cannot become `PILOT_ELIGIBLE` from generated data alone.

## 11. Time-Safe Baseline Evaluation

Random shuffling is not the default for service forecasting. Evaluation uses chronological or rolling-origin splits when timestamped data exists.

Every candidate is scored on the same eligible rows.

Core forecast metrics:

- MAE,
- WAPE,
- sMAPE where denominator behavior is acceptable,
- signed mean error / bias,
- median absolute error,
- large-underforecast incidence,
- large-overforecast incidence,
- segmented errors by cafeteria / meal type / weekday where sample size supports interpretation.

Decision metrics are computed only when corresponding measured outcomes exist:

- waste kg / 100 served,
- overproduction rate,
- early-sellout incidence,
- operator override rate,
- service-level decision loss.

A complex model is not promoted because of training loss or one cherry-picked metric.

## 12. Uncertainty Model

### 12.1 Heuristic planning range

Before calibration, operational policy may define a planning range:

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

A heuristic planning range **does not by itself force `REVIEW_REQUIRED`**. It may be used in an operator-reviewed pilot if the forecast method is `PILOT_ELIGIBLE`, the heuristic is explicitly versioned/pre-registered, sensitivity is acceptable, required sources are healthy, and all pilot guardrails pass. The system must still label the range as uncalibrated.

### 12.2 Predictive interval

A statistical predictive interval is allowed only after evaluated probabilistic forecasting.

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

Potential future methods include quantile regression and conformal intervals. Promotion requires held-out chronological empirical coverage checks.

### 12.3 Selective risk

When a meaningful uncertainty score exists, evaluation should include a risk–coverage curve showing the tradeoff between abstention rate and error on accepted decisions. A raw confidence threshold without calibration/selective-risk evidence must not be described as safe.

## 13. Decision Policy and Asymmetric Risk

The decision layer must not equate “forecast × fixed buffer” with optimization.

Inputs:

- selected forecast/baseline,
- source snapshot,
- operational constraints,
- policy version,
- method validation state,
- PMR-informed risk assumptions when available.

Conceptual objective:

```text
expected decision loss
= overproduction_cost × overproduction
+ underproduction_cost × underproduction
+ early_sellout_penalty
+ operator_burden_penalty
+ safety_violation_penalty
```

Until PMR supplies credible cost ratios, numeric weights are `POLICY_HEURISTIC`. They may support scenarios and sensitivity analysis, not learned-economic claims.

Policy sensitivity is first-class. If small changes in plausible weights cause large target changes, readiness is downgraded and the instability is visible.

## 14. Readiness and Abstention

Readiness combines source readiness, method eligibility, uncertainty/policy state, disagreement, and operational constraints.

States:

- `PILOT_READY`
- `REVIEW_REQUIRED`
- `WITHHOLD`

### WITHHOLD

Examples:

- critical source missing/stale,
- no eligible method,
- out-of-domain request,
- invalid input,
- unresolved source contradiction,
- safety constraint cannot be checked,
- only sandbox-generated estimates exist for a real operational recommendation.

Diagnostic estimates may be returned, but `actionable=false` and no target may be presented as an operational instruction.

### REVIEW_REQUIRED

Examples:

- non-critical source degraded,
- model/baseline disagreement exceeds the policy threshold,
- policy sensitivity is high,
- method is in shadow/offline-evaluated state rather than pilot-eligible,
- heuristic policy is unregistered, changed, or outside its pre-registered range.

### PILOT_READY

Requires:

- required signals pass health rules,
- selected method is `PILOT_ELIGIBLE` or better,
- contract/provenance are complete,
- any heuristic planning policy is explicit and versioned,
- policy sensitivity stays within the pilot gate,
- no safety blocker exists,
- operator approval is mandatory,
- auto-dispatch is false.

`PILOT_READY` means suitable for an operator-reviewed experiment, not validated waste reduction.

## 15. Method Selection and Disagreement

The system returns selected method, selection rule, compared alternatives, baseline status, and disagreement diagnostics.

Initial selection logic:

1. consider only methods eligible for the requested stage;
2. prefer a method that beats the designated operational baseline under the registered primary offline metric and does not violate guardrails;
3. if no complex method beats the baseline, select the baseline;
4. if no acceptable evaluation exists, remain review-only or withhold;
5. if eligible methods disagree beyond a versioned threshold, expose disagreement and require review.

“Simple baseline wins” is a valid and desirable result.

## 16. Explanation Contract

Explanations must derive from actual computation and state.

Possible explanation components:

- method selected and why,
- baseline comparison,
- source used/missing/stale,
- actual policy rule applied,
- constraint that changed the target,
- uncertainty/planning-range semantics,
- readiness downgrade reason,
- operator-review requirement.

Reason codes are stable machine-readable identifiers; display copy can evolve separately.

## 17. Canonical Decision Contract

A language-neutral versioned JSON schema is the contract source of truth.

Representative response:

```json
{
  "schemaVersion": "food-decision-v1",
  "decisionId": "2026-10-01:B-SOUTH-GY:lunch:food-policy-v1",
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

Values are illustrative contract examples, not performance claims.

## 18. Runtime Responsibility Split

### Next / TypeScript — authoritative product decision runtime

The active Next product owns:

- source snapshots,
- contract assembly,
- readiness / abstention,
- versioned policy application,
- explanation / claim boundary,
- pilot score API.

Decision logic should move from a growing `food-waste.ts` into focused modules under `frontend/src/lib/decision-intelligence/`.

Recommended modules:

- `contracts.ts`
- `provenance.ts`
- `signals.ts`
- `readiness.ts`
- `policy.ts`
- `baselines.ts`
- `uncertainty.ts`
- `pilot.ts`
- `claims.ts`
- `index.ts`

### Python — model, benchmark, calibration, and offline policy evaluation

Python owns:

- model training/inference,
- baseline benchmarking,
- chronological evaluation,
- calibration experiments,
- signal ablations,
- policy-sensitivity experiments,
- model metadata / eligibility artifacts.

Python may reproduce policy calculations for offline evaluation, but it is not a second authoritative product-policy implementation. If the legacy FastAPI `/food` route remains, it must behave as a compatibility adapter under the shared schema/claim firewall rather than inventing independent semantics.

### Shared schema

`contracts/food-decision-v1.schema.json` defines the language-neutral contract. TypeScript and Python-facing fixtures are validated against it in CI.

## 19. Operator Feedback Loop

Original recommendations are immutable events. Operator actions are separate linked events.

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

This enables later analysis of whether overrides improve outcomes, which conditions trigger them, and which operator-visible context is missing from the system.

## 20. Pilot Measurement System

The current matched control/intervention design is retained and strengthened.

A measured service record includes:

- service/date/arm,
- decision ID,
- method ID/version,
- forecast point estimate,
- planning range shown,
- recommended target,
- operator final target,
- operator action and override reason,
- produced portions,
- served portions,
- edible surplus kg,
- waste kg,
- early sell-out,
- source snapshot ID,
- notes / exclusion reason.

### Primary KPI

`waste_kg_per_100_served = waste_kg / served_portions × 100`

### Guardrails

- early-sellout incidence must not worsen materially versus matched control;
- food-safety processes cannot be bypassed;
- missing measurements remain visible;
- overrides stay in the dataset;
- exclusions require documented reasons;
- arm assignment / comparability is not retrospectively changed to improve results.

### Interpretation states

- `INSUFFICIENT_EVIDENCE`
- `PROMISING`
- `FAILED`

A stronger `SUPPORTED`/`VALIDATED` state is intentionally absent from the small application-stage pilot.

### Statistical reporting

For small pilots, report sample counts, raw distributions, means/medians, effect size, missingness, and uncertainty without implying population-level proof. Bootstrap or permutation sensitivity may be added when the design supports it, but does not erase small-sample limitations.

## 21. Experiment Suite

### EXP-CS1-01 — Data lineage audit

Classify every decision variable as official, measured, generated, modeled, heuristic, scenario, or unavailable.

### EXP-CS1-02 — Baseline benchmark

Compare candidate models with realistic simple baselines using time-safe evaluation.

### EXP-CS1-03 — Signal ablation

Measure which signals improve held-out performance/decision utility; remove signals that add no defensible value.

### EXP-CS1-04 — Source outage and degradation

Verify safe behavior under missing, stale, and contradictory schedule/menu/weather/calendar data.

### EXP-CS1-05 — Uncertainty calibration

If predictive intervals are introduced, test empirical coverage, width, and risk–coverage behavior.

### EXP-CS1-06 — Policy sensitivity

Map target changes under plausible under/overproduction cost ratios and buffer assumptions; flag unstable decisions.

### EXP-CS1-07 — H-006 operator workflow fit

Use PMR to learn decision timing, current baseline, available data, failure costs, override behavior, and safety constraints.

### EXP-CS1-08 — Measured pilot

Test whether operator-reviewed decision support improves the registered waste KPI without violating sell-out/safety guardrails.

## 22. Drift and Runtime Observability

Once measured targets exist, the system records:

- source uptime/freshness,
- feature missingness,
- forecast residual distribution,
- signed bias over rolling windows,
- baseline-vs-selected-method performance,
- method-selection frequency,
- abstention rate,
- operator override rate and reasons,
- readiness-state distribution.

Drift alerts are evidence for review, not automatic retraining permission. Retraining requires a new versioned evaluation artifact.

Before real targets exist, observability is limited to source health, contract integrity, and sandbox diagnostics.

## 23. Claim Firewall

### Allowed before measured pilot evidence

- sourced historical food-waste totals,
- source-health state,
- labeled model/baseline estimates,
- labeled heuristic planning ranges,
- labeled scenarios,
- pre-registered pilot targets/formulas,
- offline benchmark results with dataset provenance disclosed.

### Forbidden before measured evidence

- “BOUNCAMPUS saved X kg of food”;
- “BOUNCAMPUS saved X TL”;
- avoided CO2/water attributed to operation;
- “actual production optimized” without measured production integration;
- “actual student demand observed” without served/POS telemetry;
- confidence/calibration language for arbitrary heuristic bands;
- “validated model” when evaluation depends only on generated data.

CI scans critical active product surfaces and fixtures for known forbidden fields/semantics and verifies required provenance fields remain present.

## 24. Error Handling and Degraded Modes

- official source unavailable → stale snapshot only if staleness is explicit and policy permits it;
- weather unavailable → mark missing; never synthesize “live” weather for a real decision contract;
- menu fallback → classify separately from official live menu;
- model artifact unavailable → use eligible baseline if available, otherwise withhold;
- generated data only → sandbox rendering allowed, real operational recommendation withheld;
- invalid pilot measurement → reject with field-level errors;
- ambiguous service identity → reject rather than attach evidence to the wrong service;
- shared schema mismatch → fail CI and reject incompatible runtime payloads where validation is active.

## 25. Testing Strategy

### Unit tests

Cover provenance, freshness, readiness, abstention, heuristic boundaries, asymmetric-cost behavior, method selection, disagreement, claim firewall, operator events, pilot validation, and pilot scoring.

### Contract tests

Verify:

- Next/Python-facing fixtures match the shared schema;
- `WITHHOLD` cannot be actionable;
- auto-dispatch remains false;
- planning ranges cannot claim calibration;
- generated-data models cannot be promoted to pilot-eligible/validated status;
- achieved-savings fields cannot reappear before measured evidence.

### Evaluation tests

Synthetic/generated fixtures may test benchmark mechanics only. Output must explicitly identify them as non-empirical evidence.

### Failure matrix

At minimum test schedule missing, menu missing, weather missing, calendar missing, multiple missing, stale source, contradictory source, model unavailable, model-vs-baseline disagreement, invalid/negative demand, and schema-version mismatch.

## 26. Work Packages and Migration

The architecture is broad; execution is intentionally split into reviewable, merge-safe work packages under this single spec.

### WP1 — Contract, provenance, and claim integrity

- shared schema,
- unsupported Python savings removal,
- provenance classes,
- readiness/abstention semantics,
- contract/claim regression tests.

**Independent value:** eliminates the most dangerous truth-boundary failures even if later packages are delayed.

### WP2 — Modular runtime, baselines, and evaluation

- modular TS decision runtime,
- baseline registry,
- Python chronological evaluator,
- reproducibility artifact,
- generated-data eligibility gate,
- method selection/disagreement.

**Independent value:** converts the system from “one model” to baseline-first decision intelligence.

### WP3 — Operator loop, policy sensitivity, and pilot evidence

- operator events,
- policy sensitivity,
- enhanced pilot records/scorecard,
- H-006 workflow-fit experiment contract,
- source-outage matrix.

**Independent value:** makes real operator learning and pilot evaluation auditable.

### WP4 — Calibrated uncertainty and drift, evidence-gated

- probabilistic candidate(s),
- calibration evaluation,
- risk–coverage analysis,
- residual drift monitoring.

**Gate:** WP4 must not fabricate calibration using generated data. If suitable measured targets are unavailable, WP4 ships only the evaluation interfaces/tests and remains unpromoted.

## 27. Expected Repository Shape

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
  policy_eval.py
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

Exact file count may change during planning if existing repository patterns provide a cleaner boundary, but responsibilities and contract semantics may not be silently weakened.

## 28. Application-Stage Acceptance Criteria

The implementation is application-stage complete when:

1. one versioned decision contract captures source state, estimate, uncertainty semantics, readiness, human gate, reason codes, provenance, and claim boundary;
2. Python no longer exposes unsupported pre-pilot waste/cost savings;
3. generated-data-dependent models remain visibly sandbox-only;
4. realistic baseline methods are implemented where target data allows, and the benchmark tool explicitly reports when target data is insufficient;
5. evaluation is chronological/time-safe for timestamped data;
6. model selection can choose a simple baseline when it wins;
7. heuristic ranges are labeled `POLICY_HEURISTIC`, `POLICY_PLANNING_RANGE`, and `calibrated: false`;
8. calibrated interval terminology is impossible without calibration metadata;
9. `WITHHOLD` is exercised under critical failure states;
10. operator approval is mandatory and auto-dispatch disabled;
11. operator override events are separate from original recommendations;
12. pilot scoring validates measured inputs, KPI, sell-out guardrail, overrides, missingness, and evidence sufficiency;
13. claim-firewall tests prevent unmeasured savings / validated-language leaks;
14. method evaluation artifacts are reproducible and versioned;
15. TypeScript and Python CI gates remain green;
16. application-facing claims can be traced to official source, model result, baseline result, policy heuristic, scenario, or measured pilot evidence without category mixing.

## 29. Deferred Promotion Gates

Architecturally supported but not promotable without evidence:

- calibrated predictive intervals,
- learned asymmetric cost coefficients,
- validated feature importance,
- real operator-vs-model performance comparison,
- measured food-waste reduction,
- financial savings,
- environmental impact attribution,
- autonomous production control.

Not having these yet is acceptable. Pretending to have them is not.

## 30. Final Design Decision

BOUNCAMPUS CS1 will be an **evidence-aware decision intelligence system**, not a single forecasting model. Forecasts, baselines, policy heuristics, uncertainty, operator judgment, source health, measurements, and impact claims remain separate but connected layers. More sophisticated methods may be added, but every promotion in sophistication requires stronger evidence rather than stronger wording.
