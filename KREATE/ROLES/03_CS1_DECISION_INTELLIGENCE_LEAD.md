# CS1 — Decision Intelligence Lead

## Mission

Prove that BOUNCAMPUS can support a better pre-service production decision than simple status-quo baselines, while exposing uncertainty and refusing to overclaim.

The CS1 role is not "build the fanciest model." The role is to make the decision logic measurable, comparable, explainable, and operationally defensible.

**Application deadline:** 8 October 2026, 23:59  
**Primary optimization target:** decision quality and falsifiability.

---

## Core question

> Given the data realistically available to an institutional dining operation, can we produce a decision that is meaningfully more useful than current heuristics without hiding uncertainty?

---

## Scope

### P0 — Must be completed before application freeze

1. Audit the current decision logic in the repository.
2. Define status-quo baselines.
3. Define prediction / recommendation contracts.
4. Define uncertainty and readiness behavior.
5. Define failure / withholding logic.
6. Define pilot KPIs and analysis plan.
7. Integrate or specify physical measurement inputs from EE.
8. Translate PMR-derived decision costs into technical requirements.

### P1 — Allowed experiments

- Historical mean / rolling mean baselines.
- Same-weekday or same-service baselines.
- Context-aware heuristics.
- Probabilistic forecasts.
- Calibration experiments.
- Weather/menu/calendar/course-schedule signal ablations.
- Scenario analysis.
- Simple ML only when a baseline and evaluation design exist.
- Robust missing-data handling.

### Out of scope unless evidence changes priorities

- Deep learning for its own sake.
- Model complexity without a credible dataset.
- Accuracy claims from synthetic or cherry-picked examples.
- Autonomous kitchen dispatch.
- Confidence scores with no statistical/operational meaning.

---

## Shared PMR responsibility

CS1 is expected to lead approximately **4 interviews** as part of the team's target of 16 distinct interviews.

Priority interview targets:

- Dining operations managers
- Planners deciding production quantity
- Data/POS owners
- Catering operations leads
- Stakeholders who experience forecast error consequences

Questions should identify the decision contract:

- When is the production quantity decided?
- What information is available at that time?
- What is the current default/baseline method?
- What happens if you prepare too much?
- What happens if you prepare too little?
- Is one error direction worse?
- What level of recommendation would be trusted?
- What explanation would an operator need?
- When should a system say "I do not know"?

PMR findings must change model requirements when appropriate.

---

## Workstreams

### 1. Current model audit

Document every active signal and transformation relevant to food-demand / production recommendation.

For each signal:

- Source
- Availability
- Provenance
- Current weight / logic
- Missing-data behavior
- Operational rationale
- Evidence status

Likely signals include:

- Course schedule
- Academic calendar
- Menu
- Weather
- Historical demand/measurement when available

### Acceptance gate

The audit must distinguish:

- Official/public data
- Operator-provided data
- Model estimate
- Policy assumption
- Hard-coded demo value
- Missing signal

Unknown provenance is FAIL until resolved or explicitly labeled.

---

### 2. Baseline-first evaluation

Before introducing advanced models, implement or formally specify credible baselines.

Minimum baseline candidates:

1. Historical mean.
2. Previous same weekday.
3. Previous comparable service.
4. Rolling average.
5. Existing operator heuristic if PMR reveals one.
6. Current BOUNCAMPUS context-aware method.

The evaluation question is not "is our model smart?"

It is:

> Does the additional complexity beat a realistic alternative enough to matter operationally?

### Acceptance gate

No advanced method may be promoted as better unless:

- Baselines are defined.
- Evaluation data is identified.
- Metric is defined.
- Comparison is reproducible.
- Limitations are stated.

If real outcome data does not yet exist, say so and frame the method as a hypothesis for pilot validation.

---

### 3. Decision contract

The product should return a decision object rather than a naked number.

Example:

```json
{
  "service_id": "2026-10-03-lunch",
  "predicted_meals": 810,
  "lower": 740,
  "upper": 875,
  "signal_coverage": 0.82,
  "readiness": "PILOT_READY",
  "reason_codes": ["SCHEDULE_AVAILABLE", "MENU_AVAILABLE"],
  "operator_approval_required": true
}
```

The exact values are illustrative. Never copy example values into production evidence.

### Acceptance gate

The contract must expose:

- Estimate.
- Operating range/band when appropriate.
- Signal/source coverage.
- Readiness.
- Missing-data reasons.
- Provenance.
- Human approval requirement.

---

### 4. Uncertainty and readiness

Current repository behavior such as `PILOT_READY`, `REVIEW_REQUIRED`, and `WITHHOLD` should be treated as explicit product policy, not hidden logic.

Define:

- What evidence is sufficient to recommend.
- When human review is mandatory.
- When the system must withhold.
- Which missing signals matter.
- How the range widens or confidence degrades.

### Acceptance gate

A system that always returns a confident answer is FAIL.

---

### 5. Explainability

Every recommendation must be explainable in operational terms.

Example structure:

- Schedule suggests higher midday flow.
- Menu signal increases expected turnout.
- Weather signal is unavailable.
- Academic calendar is normal.
- Range widened because source coverage is incomplete.

Avoid fake precision such as assigning causal percentages without evidence.

### Acceptance gate

A technically literate teammate must be able to explain the recommendation without saying "the AI decided."

---

### 6. Physical measurement integration

Work with EE on a canonical outcome schema.

Potential fields:

- Produced quantity
- Served quantity
- Edible surplus
- Waste mass
- Measurement category
- Measurement quality
- Station/service ID
- Timestamp
- Operator override

The backend must preserve measurement quality and provenance.

### Acceptance gate

Simulated data and physical telemetry must be distinguishable at the schema/storage level or clearly labeled in the consuming analysis.

---

### 7. Pilot analytics

Define metrics before outcome collection.

Potential metrics:

- Waste kg / 100 served
- Forecast MAE
- Absolute percentage error where appropriate
- Overproduction ratio
- Early sell-out rate
- Operator override rate
- Measurement completeness
- Data-quality failure rate

Primary intervention logic should compare matched CONTROL vs INTERVENTION services where feasible.

### Acceptance gate

Success criteria must exist before pilot results. Do not redefine success after seeing results.

---

## Experiment standard

Every non-trivial model or signal experiment must state:

- Question
- Hypothesis
- Dataset/source
- Baseline
- Metric
- Success condition
- Failure condition
- Result
- KEEP / MODIFY / KILL

Example:

> Does weather add enough predictive information beyond schedule and historical service data to justify operational dependence on a weather API?

This is stronger than "add weather AI."

---

## Cross-team handoffs

### From IE

Need:

- Current decision timing.
- Current heuristics.
- Asymmetric cost of errors.
- Trust/explanation requirements.
- Signals operators believe matter.

### From EE

Need:

- Outcome measurement schema.
- Calibration/error information.
- Quality flags.
- Connectivity/failure behavior.

### To CS2

Provide:

- What the decision engine can actually do.
- What is still hypothesis.
- Baseline comparison design.
- Evidence behind feature choices.
- Clear technical differentiation without buzzwords.

---

## Anti-AI-slop rules

Automatic FAIL if:

- A model is called AI because it uses weighted rules.
- A hard-coded example is described as a prediction result.
- Confidence is displayed without defined meaning.
- A model is compared only against a weak strawman.
- A metric is reported without dataset/sample context.
- A result is selected because it looks favorable while contradicting the defined metric.
- Missing signals are silently imputed with fabricated certainty.
- "Personalized", "intelligent", "adaptive", or similar terms replace an actual algorithmic description.

---

## Definition of Done — 8 October

The CS1 role is DONE only if:

- [ ] CS1 led roughly 4 relevant PMR interviews, unless team coverage justified redistribution.
- [ ] Current decision logic and data provenance are audited.
- [ ] Realistic baselines are specified or implemented.
- [ ] Decision contract is documented.
- [ ] Uncertainty/readiness/withhold behavior is explicit.
- [ ] Explainability behavior is defined.
- [ ] EE measurement contract is compatible with backend/pilot analytics.
- [ ] Pilot metrics and success logic are pre-defined.
- [ ] Model/feature claims are separated into proven vs unproven.
- [ ] At least one weak or unnecessary signal/model assumption can be killed if evidence does not support it.
- [ ] CS2 has concise, defensible technical inputs for the application.

---

## Success standard

The strongest CS1 output is not the most sophisticated model.

It is a decision system where a reviewer can see:

> what went in, what came out, what baseline it must beat, how uncertainty is handled, and exactly what must be tested in a real pilot.
