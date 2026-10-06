# VPMR Data & Source Inventory

This file answers a different question from the source registry: **what data can actually enter a model, analysis or pilot, at what granularity, and with what leakage/provenance risk?**

## 1. Public context sources

| Data/source | Availability | Granularity | Intended use | Leakage / semantic risk |
| --- | --- | --- | --- | --- |
| Boğaziçi 2025 food-waste page | Public | monthly/aggregate | problem baseline, sanity context | cannot label individual services or causes |
| SKS 2025 activity report | Public | annual aggregate | scale/context | cannot fabricate campus×meal rows from averages |
| Official dining menu | Public | day/menu item | pre-service feature/context | archive/snapshot must prove availability before cutoff |
| Academic calendar | Public | dated calendar events | regime/term/holiday feature | bind to version valid at decision date |
| Menu survey | Public workflow | preference signal | candidate menu-appeal feature | preference != attendance/demand |
| Kilyos reservation workflow | Public notice | specific campus/date period | proves reservation can exist | do not generalize to all services |

## 2. Archived exogenous feature sources

### Weather

Use `VPMR-SRC-027` Open-Meteo Historical Forecast for historical decision evaluation where weather is part of a candidate method.

Required fields for a leakage-safe snapshot:

- forecast initialization/run time;
- target service time;
- lead time;
- variable(s) actually consumed by the model;
- retrieval/source version;
- proof `available_at <= decision_cutoff_at`.

Never substitute hindsight actual weather or reanalysis for a forecast that would not have been known at the decision point.

### Calendar/menu

Archive the exact public menu/calendar snapshot that existed before the cutoff. If no historical snapshot can be proven, mark the row unavailable rather than reconstructing it from future knowledge.

## 3. External reference datasets

### Genpact Food Demand Forecasting

Class: `REFERENCE_DATASET` / sandbox only.

Useful for:

- forecast-pipeline smoke tests;
- temporal split code;
- baseline/evaluation plumbing;
- feature-contract experiments;
- reproducible examples.

Not usable for:

- Boğaziçi accuracy claims;
- waste-reduction claims;
- PMR;
- campus workflow validation;
- pilot evidence.

## 4. The missing dataset that matters

The decisive dataset remains an **admitted service-level operational truth dataset**, one row per stable `campus × meal period × service date` unit.

Minimum outcome/reconciliation fields:

| Field | Why |
| --- | --- |
| `service_id` | stable join/audit key |
| `campus_id` | allocation/site boundary |
| `meal_period` | comparable service regime |
| `service_date` | temporal ordering |
| `actual_served` | realized accepted demand, once semantics are confirmed |
| `produced_portions` | production action |
| `actual_surplus_portions` and/or accepted `waste_kg` | outcome boundary |
| `waste_stage` | preparation vs unserved surplus vs plate waste vs mixed |
| `shortage_or_early_sellout` | service guardrail |
| `outcome_reconciled` | admission flag |
| `source_record_id` / snapshot IDs | provenance |

Minimum decision-time fields:

| Field | Rule |
| --- | --- |
| `decision_cutoff_at` | all predictive inputs must have existed by this time |
| reservation/intention count | only where a verified workflow exists |
| operator/status-quo estimate | required baseline when available |
| menu snapshot | content-bound + available by cutoff |
| academic calendar snapshot | available by cutoff |
| weather forecast snapshot | archived forecast, not hindsight actual |
| special-event signal | only if known before cutoff |

Minimum decision audit fields:

- baseline/method version;
- recommended quantity/range;
- uncertainty/range semantics;
- operator final action;
- override reason;
- input snapshot IDs;
- final execution/outcome reconciliation status.

## 5. Private-source acquisition map

| Need | Likely source owner to verify | Preferred first request | Privacy default |
| --- | --- | --- | --- |
| produced portions | Food Services / contractor production owner | field dictionary + aggregate export | service-level aggregate |
| served/accepted meals | Food Services / access/payment system owner | aggregate date×campus×meal counts + semantics | no user/card identifiers |
| surplus/unserved | kitchen/contractor operations | existing waste/surplus log schema or prospective weigh sheet | service aggregate |
| plate waste | dining operations / prospective pilot | direct weighing or validated TrayGate protocol | no face/user tracking |
| reservations | workflow owner / IT if present | aggregate active reservation count at cutoff + cancellation semantics | aggregate only |
| contract/payment basis | procurement/administration + contractor finance | relevant clause or owner explanation | no personal data |
| menu ratings/history | Food Services / BUCampus owner | export schema/timestamp semantics | aggregate only |

## 6. Admission gates

A dataset is **not service truth** merely because it is in CSV/JSON or came from a real system. Before benchmark/pilot use, establish:

1. source owner and source-system identity;
2. exact event/field semantics;
3. time of availability relative to decision cutoff;
4. accepted reconciliation to the operational outcome;
5. privacy-safe fields;
6. immutable snapshot/checksum;
7. explicit missingness and exclusion rules;
8. chronological evaluation split;
9. no generated/synthetic rows mixed into measured truth.

## 7. Measurement boundary

For food waste, store stage and method explicitly. Preferred hierarchy is:

existing trustworthy operational record -> simple direct weighing where feasible -> automated sensing only for a specific unresolved burden/gap -> local calibration against physical ground truth.

Monthly total waste is useful context, not a service-level intervention label.
