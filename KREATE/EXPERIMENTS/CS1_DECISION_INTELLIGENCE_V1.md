# CS1 Decision Intelligence v1 — Pre-Registered Evaluation

This experiment is intentionally written before measured cafeteria-service evidence exists. Repository capability, policy heuristics, model estimates, technical benchmark output, operator feedback, and measured pilot outcomes must remain separate evidence classes.

## QUESTION

Can the BOUNCAMPUS food-decision workflow produce an operator-reviewable next-service production recommendation that is measurably more useful than simple existing alternatives while abstaining when decision context is insufficient?

## HYPOTHESIS

`H-006` — Human-reviewed decision support can fit the existing workflow without unacceptable early-sellout, food-safety, or operational risk.

Technical sub-hypothesis: once measured service-level data is available, the demand model should outperform at least one credible simple baseline on forecast error without requiring hidden future information, and the decision policy should refuse automatic action when required context is missing.

## WHY IT MATTERS

A sophisticated model is not useful if a previous-service estimate, same-cycle lag, rolling average, or operator estimate performs as well or better. KREATE also requires a credible path from prediction to a real operating decision, with uncertainty and limitations visible instead of hidden behind product polish.

This experiment addresses the CS1 portion of `H-006` and provides technical evidence for the decision-support workflow. It does **not** validate the beachhead, persona, causal waste hypothesis, data availability, or operator adoption; those remain dependent on PMR and/or measured pilot evidence.

## OWNER

CS1 — Decision Intelligence Lead.

## TIMEBOX

- Decision-policy and benchmark infrastructure: before October 8 application freeze.
- Offline benchmark: only after a real, provenance-labeled service-level dataset is available.
- Matched CONTROL/INTERVENTION pilot: 14 days when operational access is secured.

## METHOD

### 1. Decision contract

For every next-service estimate, retain:

- model point estimate and model ID;
- source availability for schedule, weather, menu, and academic calendar;
- explicit `POLICY_HEURISTIC` signal weights;
- planning range labeled `PLANNING_RANGE_NOT_CALIBRATED_INTERVAL`;
- readiness state: `PILOT_READY`, `REVIEW_REQUIRED`, or `WITHHOLD`;
- reason codes and limitations;
- mandatory human approval and no automatic kitchen dispatch.

The system must abstain when there is no positive demand estimate or the required schedule backbone is unavailable.

### 2. Leakage-safe offline baseline benchmark

Order observations chronologically. For target service *t*, every baseline may use only information available before *t*.

Candidate baselines:

1. previous comparable service;
2. expanding historical mean;
3. rolling historical mean;
4. same-cycle / seasonal lag when the lag is operationally defensible;
5. operator estimate, if it is captured before the service;
6. food-demand model point estimate.

Primary forecast metrics:

- MAE;
- RMSE;
- WAPE;
- mean error / signed bias.

Run through `scripts/cs1_baseline_benchmark.py` with an explicit `--dataset-label`. Output remains `TECH_TEST` / `OFFLINE_BENCHMARK_ONLY` unless a narrow evidence row is created after review.

### 3. Decision-readiness stress cases

Verify at minimum:

- all configured signals available;
- schedule + partial context;
- required schedule unavailable;
- zero, negative, NaN, or infinite demand estimate;
- fallback/non-live source states;
- model estimate available but operational recommendation withheld.

### 4. Measured pilot, if access is secured

Use the repository food-waste pilot contract. Retain service-level CONTROL and INTERVENTION measurements including produced portions, served portions, waste mass, edible surplus, early sellout, operator override, and the intervention model forecast.

The scorecard may classify a measured pilot as `PROMISING` only if:

- all rows pass measurement validation;
- no duplicate service rows remain;
- every intervention service retains its model forecast;
- at least 5 valid services exist in each arm;
- normalized waste reduction meets the pre-registered 10% target;
- intervention early-sellout incidence does not exceed control;
- food-safety compliance is separately reviewed by a human operator.

`PROMISING` is pilot evidence only, never a generalized climate-impact claim.

## INPUTS

| Input | Evidence class before experiment | Required provenance |
| --- | --- | --- |
| Official historical food-waste figures | `PUBLIC SOURCE` | E-PUB source must be re-opened before numeric submission claims. |
| Repository decision policy and evaluator | `REPO_ARTIFACT` | E-REP-004. |
| Food-demand point forecasts | `MODEL ESTIMATE` | Model ID + training-data provenance + target service retained. |
| Signal weights / readiness thresholds / planning factors | `POLICY HEURISTIC` | Versioned policy constant; never described as learned probability or confidence. |
| Offline forecast metrics | `TECHNICAL TEST` | Dataset label, chronological ordering, candidate definitions, command/output artifact. |
| Operator estimate | `INTERVIEW EVIDENCE` or measured operational input | Must be captured before the target service; never reconstructed after seeing outcome. |
| CONTROL/INTERVENTION outcomes | measured pilot evidence | Real service-level records only; no synthetic rows. |
| Workflow-fit claim | `HYPOTHESIS` until PMR | Requires operator interviews/objections and later operational evidence. |

## SUCCESS CONDITION

Technical infrastructure succeeds when all of the following are true:

1. backend and frontend expose the same versioned policy semantics;
2. missing required context can produce `WITHHOLD` with no production target;
3. the repository exposes no achieved food-waste/cost/carbon/water savings from unmeasured decisions;
4. baseline evaluation is past-only and produces MAE/RMSE/WAPE/bias;
5. measured pilot rows cannot be promoted through the scorecard when data-quality/sample/guardrail gates fail.

A future **model-performance** success claim additionally requires measured data and a pre-declared baseline comparison. A future **workflow/impact** success claim additionally requires operator evidence and measured pilot outcomes.

## FAILURE CONDITION

Modify or kill the current decision-intelligence approach if any of the following is observed with credible evidence:

- a simple/operator baseline matches or beats the model consistently enough that model complexity adds no operational value;
- required inputs are unavailable at the real decision time;
- operators cannot interpret or safely act on the proposed range/readiness output;
- override or early-sellout risk is unacceptable;
- the workflow requires a different decision than production quantity;
- measured pilot data fail the registered outcome/guardrail gates;
- implementation begins presenting heuristic ranges as calibrated uncertainty or scenarios as achieved impact.

## RAW EVIDENCE LOCATION

Current repo artifacts:

- `backend/app/decision/food_policy.py`
- `backend/app/decision/baselines.py`
- `backend/app/models/food_demand.py`
- `backend/app/routers/food.py`
- `frontend/src/lib/food-waste.ts`
- `frontend/src/app/api/v1/food/route.ts`
- `frontend/src/app/api/v1/food/pilot-score/route.ts`
- `scripts/cs1_baseline_benchmark.py`
- `scripts/test_food_decision_policy.py`
- `scripts/test_cs1_decision_intelligence.py`

Future raw benchmark/pilot outputs must be stored as separate artifacts with dataset provenance. Do not overwrite this pre-registration with results.

## RESULT

**NOT RUN on measured cafeteria outcome data.**

Repository capability has been implemented, but there is currently no promotable result showing model superiority, operator workflow fit, achieved waste reduction, cost savings, or climate impact. Any later result must be recorded as a new technical/model/interview evidence item with source artifact and limitations.

## DECISION: KEEP / MODIFY / KILL

**KEEP for evidence collection and testing; no impact or workflow-fit claim promotion.**

Reason: the decision contract, abstention path, baseline harness, and pilot gate are useful prerequisites for falsifying `H-006`, but they are not evidence that `H-006` is supported.

## LIMITATIONS

- No verified cafeteria POS / served-meal dataset is currently registered as evidence.
- No calibrated forecast interval is currently available.
- Policy signal weights and planning factors are heuristics, not learned probabilities.
- Repository-generated training data provenance is not equivalent to measured target-operations data.
- Food-safety compliance cannot be inferred from numeric service-level fields.
- Public waste totals do not establish that demand mismatch caused the waste.
- PMR remains the dominant application evidence gap.

## NEXT STEP

1. Use CS1 PMR slots to capture the last concrete production decision, current baseline, decision timing, available data, under/overproduction loss, override behavior, and safety constraints.
2. If a real historical service dataset is obtained, run the leakage-safe baseline benchmark and register narrow `E-TECH-*` / `E-MODEL-*` evidence only after reviewing provenance.
3. If pilot access is obtained, use the v1.1 measurement contract and scorecard without changing the success threshold after seeing outcomes.
4. Revisit `H-006` only when PMR or measured technical/pilot evidence exists.

## Human review

- **Reviewer:** Pending real evidence promotion.
- **Review date:** Pending.
- **Evidence IDs created:** E-REP-004 for repository capability only; no `E-TECH-*`, `E-MODEL-*`, or `E-INT-*` result created by this pre-registration.
