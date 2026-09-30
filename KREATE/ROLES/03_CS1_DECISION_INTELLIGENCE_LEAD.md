# CS1 — Decision Intelligence Lead

## Mission

Own the question: **Can BOUNCAMPUS help a real operator make a measurably better decision than the current alternative, and can we prove it without hiding uncertainty?**

This role is broader than maintaining a forecast model. It owns the logic that turns messy operational signals into useful, explainable, uncertainty-aware decisions and the evidence needed to compare those decisions with realistic baselines.

The CS1 lead is encouraged to challenge the current algorithm, current inputs, and even the assumption that forecasting is the best technical intervention.

## North Star

A strong decision system should improve at least one of:

1. decision quality,
2. uncertainty awareness,
3. operator usefulness,
4. baseline performance,
5. evidence quality,
6. robustness to missing / bad data,
7. pilot measurability,
8. ability to explain why a recommendation exists.

The goal is not maximum model sophistication. The goal is the strongest defensible decision loop.

## Core Ownership

Primary ownership areas include:

- decision problem formulation,
- baseline design,
- forecasting / estimation experiments,
- uncertainty representation,
- source-health and missing-data logic,
- recommendation logic,
- risk tradeoffs,
- model evaluation,
- pilot analytics,
- backend contracts supporting decisions,
- data-quality handling,
- model / heuristic provenance,
- identifying when the system should abstain,
- determining whether additional complexity actually adds value.

## Start From the Decision, Not the Model

Before choosing algorithms, define:

- what decision is being made,
- who makes it,
- when it is made,
- what information is available at that moment,
- what happens if the estimate is too high,
- what happens if it is too low,
- what baseline decision exists today,
- what outcome can later be measured.

For food operations the decision may be production quantity, but PMR may reveal more valuable decisions such as preparation timing, batch sizing, replenishment, surplus handling, or intervention selection.

CS1 has authority to propose a better-defined decision target if evidence supports it.

## Baseline-First Standard

Every complex approach should be compared with realistic alternatives.

Potential baselines include:

- previous comparable service,
- same weekday last week,
- historical mean / median,
- rolling average,
- simple rule-based adjustment,
- operator estimate,
- menu-conditioned baseline,
- schedule-only estimate,
- other status-quo logic discovered during PMR.

Do not manufacture a weak baseline to make BOUNCAMPUS look better.

If a simple baseline wins, that is useful evidence. The product can adopt the simpler method or focus on a different source of value.

## Candidate Context Signals

Current candidates may include:

- course schedule,
- academic calendar,
- weather,
- menu / popularity,
- service type,
- historical attendance or meal counts,
- special events,
- operational constraints,
- measurement feedback.

No signal is sacred. Remove a signal if it adds noise, cannot be obtained in practice, or is not available at decision time. Add new signals if PMR and experiments show they matter.

## Uncertainty and Abstention

Recommendations should represent uncertainty honestly.

Useful concepts may include:

- lower / central / upper demand estimate,
- signal coverage,
- data freshness,
- source health,
- reason codes,
- confidence / uncertainty where statistically justified,
- `PILOT_READY`, `REVIEW_REQUIRED`, `WITHHOLD`, or revised status semantics.

Do not call an arbitrary production band a confidence interval unless it is statistically calibrated as one.

The system should be allowed to say **I do not have enough evidence to recommend**.

## Decision Logic

A recommendation should reflect the asymmetric cost of errors where relevant.

For example, if PMR shows that early sell-out is operationally much more costly than modest surplus, the decision objective should reflect that rather than minimizing forecast MAE alone.

Possible objectives may combine:

- waste reduction,
- stockout / early-sellout risk,
- service quality,
- operator override burden,
- production constraints,
- measurement uncertainty.

The correct objective should be discovered, not assumed.

## Explainability

The decision layer should be able to communicate why the recommendation changed.

Possible explanation elements:

- schedule effect,
- menu effect,
- calendar effect,
- weather effect,
- data missingness,
- historical pattern,
- operational constraint,
- uncertainty source.

Explanations should correspond to actual logic, not post-hoc decorative text.

## Experiment Freedom

CS1 may investigate any technical approach that could materially strengthen the decision system.

Examples include:

- transparent heuristics,
- linear / tree-based models,
- probabilistic forecasting,
- quantile models,
- Bayesian approaches,
- time-series baselines,
- contextual models,
- anomaly detection,
- uncertainty calibration,
- optimization under asymmetric cost,
- scenario analysis,
- causal / quasi-experimental pilot analysis,
- signal ablation,
- lightweight simulation,
- a conclusion that no ML is currently justified.

Experiments should answer a question and lead to a decision. Avoid complexity for its own sake.

## Evaluation

Metrics should align with the decision.

Potential metrics include:

- MAE / RMSE where useful,
- absolute / percentage production error,
- waste kg per 100 served,
- overproduction rate,
- early-sellout frequency,
- interval coverage,
- calibration error,
- override rate,
- data completeness,
- performance versus operator or historical baseline.

Avoid presenting metrics that cannot be supported by real or clearly labeled experimental data.

## Pilot Analytics

Work with EE and IE to ensure the pilot can distinguish outcome from storytelling.

Potential structure:

- comparable services,
- control vs intervention where feasible,
- predefined primary KPI,
- guardrails,
- data-quality rules,
- explicit exclusion / missing-data policy,
- operator overrides preserved,
- no retrospective relabeling to make results favorable.

CS1 should challenge any pilot design that cannot support a meaningful conclusion.

## Backend / Data Contracts

Where implementation is useful, keep contracts explicit and auditable.

Example decision response:

```json
{
  "serviceId": "...",
  "estimate": 810,
  "lower": 740,
  "upper": 875,
  "signalCoverage": 0.82,
  "readiness": "PILOT_READY",
  "reasons": [],
  "provenance": "MODEL_ESTIMATE"
}
```

The exact contract may evolve as the product thesis improves.

Physical measurements and model estimates must remain distinguishable.

## Freedom to Challenge the Product

CS1 may conclude that:

- a weather input is useless,
- a schedule signal is insufficient,
- hardware feedback matters more than prediction accuracy,
- a rule is better than an ML model,
- the primary value is uncertainty communication rather than point forecasting,
- production planning is the wrong decision point,
- a new operational intervention should be tested.

These are not failures. Record evidence and surface implications to the team.

## Collaboration

### With IE

Use PMR to define real decisions, error costs, available signals, and current baselines.

### With EE

Define measurement needs, quality flags, feedback variables, and what is necessary to evaluate interventions.

### With CS2

Provide defensible technical conclusions, experiment results, limitations, and product implications. Help ensure application claims are technically accurate.

## Anti-AI-Slop Standard

AI may help with code, experiment design, analysis, documentation, and literature exploration. It may not create scientific legitimacy by wording alone.

Reject:

- fake evaluation data,
- invented performance improvements,
- arbitrary model weights described as learned,
- decorative explainability disconnected from actual computation,
- unsupported confidence scores,
- benchmarks on cherry-picked examples,
- complex ML used solely to make the project sound advanced,
- hard-coded outputs presented as model results,
- claims that a model reduces waste before intervention evidence exists.

## Strong Outputs

Useful outputs may include:

- a baseline benchmark,
- signal-ablation results,
- a better decision formulation,
- uncertainty calibration analysis,
- a clear decision contract,
- source-health handling,
- a model or heuristic that beats a meaningful baseline,
- evidence that a proposed model does not help,
- pilot analytics code,
- documented failure cases,
- a recommendation to simplify the system.

## Application-Stage Success Criteria

By October 8, the decision-intelligence side should ideally support:

- a clearly formulated operational decision,
- realistic baselines,
- transparent current methodology,
- explicit uncertainty and limitations,
- evidence for which signals appear useful and which remain hypotheses,
- a credible plan for evaluating impact,
- technical claims that can survive skeptical questioning,
- no implication that sophistication equals value.

The strongest outcome is a decision system whose logic the team understands, whose limitations it can state clearly, and whose value can eventually be tested against a real alternative.
