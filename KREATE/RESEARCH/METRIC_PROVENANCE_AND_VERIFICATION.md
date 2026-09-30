# Metric Provenance & Verification — Cross-Domain Product Spec

**Research date:** 2026-10-01  
**Owners:** EE / CS1 / CS2  
**Status:** Product-design proposal derived from public-source research. Not proof of current Boğaziçi internal architecture.

## Why this matters

Public Boğaziçi sources already show measurement programs in food waste, water, energy, carbon and transport. They also reveal that metric semantics can be non-trivial. Example: the 2025 food-waste table says the quantity delivered to İSTAÇ is included in total food waste, yet in August and October the monthly delivered quantity is larger than the published same-month total. This may reflect collection timing/backlog or another definition; public sources do not resolve it.

The product must therefore preserve **what a number means**, not just the number.

---

# 1. Minimum provenance contract

Every operational sustainability observation should be able to carry:

```text
metric_id
metric_name
resource_domain
value
unit
entity_type
entity_id
scope
measurement_stage
observed_at
period_start
period_end
recorded_at
source_system
source_owner
source_artifact
collection_method
calculation_method
transformation_version
quality_state
confidence_or_uncertainty_semantics
review_state
reviewer
supersedes_metric_id
notes
```

## Required semantics

### Event time vs reporting time

Keep separate fields for:

- `observed_at` — when the physical event occurred;
- `recorded_at` — when it entered a system;
- `period_start/end` — accounting/reporting period;
- optional domain-specific timestamps such as `collected_at`, `processed_at`, `served_at`.

Never infer that two monthly columns refer to identical event timing just because they share a month label.

### Scope

Examples:

- whole university;
- campus;
- dining hall;
- building;
- meter;
- shuttle route;
- meal period.

Aggregations must declare their scope explicitly.

### Measurement stage

Food:

- procurement input;
- prepared/produced;
- served;
- edible surplus;
- preparation waste;
- plate/post-consumer waste;
- collected waste;
- transferred/recovered/disposed.

Water:

- utility supply;
- rainwater harvested;
- greywater recovered;
- building consumption;
- irrigation;
- discharge.

Energy:

- grid electricity;
- on-site generation;
- natural gas/fuel;
- building consumption;
- end-use estimate.

This prevents false joins such as treating collected food waste as same-day generated plate waste.

---

# 2. Quality-state contract

Recommended states:

```text
VERIFIED_SOURCE
SOURCE_REPORTED
RECONCILIATION_REQUIRED
DERIVED
MODEL_ESTIMATE
MISSING
WITHHELD
```

Meaning:

- `VERIFIED_SOURCE` — inspected authoritative source with unambiguous definition for the field used.
- `SOURCE_REPORTED` — source reports value, but some semantics may still be incomplete.
- `RECONCILIATION_REQUIRED` — values/definitions conflict or cannot safely be combined.
- `DERIVED` — deterministic calculation from identified inputs.
- `MODEL_ESTIMATE` — model result, never measured reality by default.
- `MISSING` — expected field absent.
- `WITHHELD` — intentionally excluded because quality/evidence is insufficient.

Do not collapse these to a generic `confidence` percentage.

---

# 3. Food pilot data contract

For each service episode, target the following minimum schema:

| Field | Why needed | Evidence status |
| --- | --- | --- |
| `service_id` | stable join key | design requirement |
| `service_date` | matching and trend | design requirement |
| `campus` | multi-campus heterogeneity | public sources show campus differences |
| `dining_hall` | local operational scope | likely needed; availability unknown |
| `meal_period` | breakfast/lunch/dinner differ | public service windows support segmentation |
| `menu_id` / menu items | demand context | public menus exist; historical access unknown |
| `planned_portions` | current decision baseline | PMR/data-access unknown |
| `produced_portions` | overproduction denominator | PMR/data-access unknown |
| `served_portions` | realized demand | PMR/data-access unknown |
| `edible_surplus_kg` | avoidable production surplus | PMR/data-access unknown |
| `prep_waste_kg` | separate production process waste | PMR/data-access unknown |
| `plate_waste_kg` | separate consumer waste | PMR/data-access unknown |
| `waste_measurement_method` | scale/estimate reliability | required for pilot validity |
| `early_sellout` | shortage guardrail | required for decision utility |
| `operator_override` | human-in-loop behavior | required for workflow validation |
| `override_reason` | model failure analysis | recommended |
| `academic_state` | term/exam/holiday | public calendar candidate |
| `weather_context` | optional exogenous signal | incremental value must be tested |
| `special_event_flag` | large campus-demand shock | PMR/data access unknown |

Primary normalized pilot KPI remains repository-defined:

```text
waste_kg_per_100_served = (waste_kg / served_portions) * 100
```

But waste should be split by stage when feasible.

---

# 4. Decision record contract

A recommendation is not useful evidence unless the team can reconstruct what happened.

Each recommendation should store:

```text
decision_id
created_at
decision_owner_role
input_snapshot_ids
model_version
policy_version
recommended_action
recommended_value
planning_band
uncertainty_semantics
reason_codes
known_missing_inputs
risk_guardrails
operator_action
operator_override
actual_outcome_ids
verification_status
```

This creates an auditable chain:

```text
source observations
    -> derived features
    -> recommendation
    -> human action
    -> measured outcome
```

---

# 5. Verification design

BOUNCAMPUS should distinguish three levels.

## Level A — Descriptive verification

Question: did the source value change after an action?

Useful for operational monitoring, but weak causally.

## Level B — Adjusted comparison

Compare intervention service against matched historical/control services using variables such as:

- campus;
- meal period;
- weekday;
- academic state;
- service volume;
- major event/weather context when relevant.

This aligns with the current repository pilot protocol.

## Level C — Strong causal evidence

Requires a sufficiently designed pilot/experiment and enough repeated observations. A hackathon prototype should not imply Level C proof before it exists.

---

# 6. Water module implications

Boğaziçi's official Water Management Directive establishes a Water Management Commission and requires periodic measurement/analysis and reporting. It states that unit-level water use and recovery data are to be evaluated and submitted periodically, with the commission analyzing data every three months and reporting annually to the rectorate.

Primary sources:

- https://impact.bogazici.edu.tr/sites/impact.bogazici.edu.tr/files/su_yonetimi_yonergesi.pdf
- https://kurumsalveri.bogazici.edu.tr/tr/pages/641-water-reuse-policy/1354

A future water module should therefore augment this governance workflow rather than pretend a new dashboard creates water governance.

Potential decision objects:

- abnormal nighttime usage investigation;
- leak/valve inspection priority;
- irrigation timing;
- rainwater/greywater utilization performance;
- retrofit prioritization.

All remain hypotheses until an owner confirms current workflow and pain.

---

# 7. Energy module implications

Boğaziçi states that its ISO 50001 Energy Management System regularly measures/analyzes consumption and uses indicators such as kWh/m² and CO2 in data-driven decision processes. It also describes an Energy Management Team and campus-wide monitoring/follow-up mechanisms.

Primary source:

https://kurumsalveri.bogazici.edu.tr/tr/pages/724-plan-to-reduce-energy-consumption/1367

Therefore, the future energy value proposition should not be "show energy use." Candidate value must be tested around:

- prioritizing anomalies;
- normalizing by weather/occupancy/use;
- estimating decision impact;
- documenting intervention evidence;
- cross-building capital prioritization.

---

# 8. Reporting/export layer

A long-term platform may reuse verified operational data for external/internal reporting. Potential targets include:

- university sustainability reports;
- internal management reviews;
- ISO 50001 evidence workflows;
- YÖK sustainability monitoring;
- UI GreenMetric evidence preparation;
- THE/SDG evidence packages where definitions align.

**Boundary:** do not claim automated compliance or guaranteed ranking points. Each external framework has its own definitions and evidence rules.

---

# 9. Machine-readable design rules for CS1/backend agents

1. Never merge observations only on `month` and metric name when event semantics differ.
2. Retain raw/source values alongside normalized values.
3. Version every transformation and decision policy.
4. Record missing inputs explicitly; do not silently impute operational truth.
5. Keep `MODEL_ESTIMATE` separate from `MEASURED/SOURCE_REPORTED` at schema level.
6. A UI planning band must expose its semantics; do not call it a confidence interval unless calibrated.
7. Support `WITHHOLD` when evidence quality is inadequate.
8. Preserve operator overrides as signal, not noise.
9. Keep person-level data out of the first pilot unless a decision question genuinely requires it.
10. Any carbon/water/cost conversion derived from food-waste reduction is a second-stage calculation with its own factor source and uncertainty.

---

# 10. Immediate tests enabled by this spec

### EE

Create a one-service measurement sheet and determine whether a kitchen team can record produced, served, surplus and waste quantities without disrupting service.

### CS1

Build the baseline model around the smallest reliable data contract first; evaluate whether each additional feature beats a simple historical/calendar baseline.

### IE

Ask exactly who currently owns each field, where it is stored, how often it is updated, and what decision it changes.

### CS2

Ensure every application claim can distinguish `PUBLIC SOURCE`, `INTERVIEW EVIDENCE`, `MODEL ESTIMATE`, and later `MEASURED PILOT OUTCOME`.
