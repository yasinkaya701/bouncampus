# Boğaziçi Dining Privacy & Data-Minimization Architecture

**Research date:** 2026-10-01  
**Purpose:** Define the smallest privacy-safe data architecture needed to test dining demand/production decisions without turning BUCard, QR, BUBizden or scholarship systems into unnecessary individual tracking pipelines.  
**Status:** Secondary public-source research and technical design guidance. **NOT legal advice. NOT a KVKK compliance certification.**

Related packs:

- [`BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md`](./BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md)
- [`BOGAZICI_CONTRACT_SEMANTICS_EVIDENCE_MAP.md`](./BOGAZICI_CONTRACT_SEMANTICS_EVIDENCE_MAP.md)
- [`BOGAZICI_DINING_INCENTIVE_SUBSIDY_MAP.md`](./BOGAZICI_DINING_INCENTIVE_SUBSIDY_MAP.md)

---

# 0. Executive conclusion

The current product hypothesis does **not** require a student-level surveillance dataset.

The core decision can be tested with aggregate operational quantities such as:

```text
campus × meal × date × service regime
planned / requested quantity
produced quantity
aggregate served/entry count
surplus / waste
shortage event
menu context
```

There is no obvious technical reason to ingest:

- student name;
- student number;
- BUCard identifier;
- QR token;
- exact per-person meal history;
- personal scholarship status;
- individual BUBizden support status;
- device identifier;
- personal contact information.

The preferred architecture is therefore:

```text
SOURCE SYSTEM
(raw BUCard / QR / support data stays with institutional owner)
        ↓
OWNER-CONTROLLED AGGREGATION
        ↓
PRIVACY-SAFE OPERATIONAL COUNTS
        ↓
BOUNCAMPUS DECISION MODEL
```

rather than:

```text
copy raw identifiable logs into BOUNCAMPUS
→ try to anonymize later
```

---

# 1. KVKK general principles directly support minimization

## PRIV-01 — Processing must be purpose-bound, limited and proportionate

`PUBLIC SOURCE`

The Turkish Personal Data Protection Authority (KVKK) summarizes Article 4 principles including:

- lawfulness and fairness;
- accuracy / being kept up to date when necessary;
- processing for specified, explicit and legitimate purposes;
- being **relevant, limited and proportionate** to the processing purpose;
- storage only for the period required by legislation or the processing purpose.

Official source:  
https://www.kvkk.gov.tr/Icerik/6606/General-Principles-in-Processing-of-Personal-Data

The Authority's decision summaries repeatedly explain that data not needed for the defined purpose should not be collected merely for possible future use.

Example source:  
https://www.kvkk.gov.tr/Icerik/7138/2021-799

### Product implication

The dining pilot should first prove that aggregate counts are insufficient **before** asking for person-level records.

The default answer should be `do not ingest identifiers`.

---

# 2. Anonymization is stronger than deleting names

## PRIV-02 — KVKK's anonymization standard requires non-linkability back to a person

`PUBLIC SOURCE`

The Authority states that data are anonymized only when they cannot be associated with an identified or identifiable natural person even through techniques such as reversal or matching with other datasets, taking the relevant environment and activity into account.

Official source:  
https://www.kvkk.gov.tr/Icerik/2038/kisisel-verilerin-silinmesi-yok-edilmesi-veya-anonim-hale-getirilmesi

### Engineering implication

Removing `student_id` from row-level transaction history is not automatically enough.

A row such as:

```text
2026-10-01 12:04:13 | Kandilli | vegan | unique-device-token
```

may still be linkable in context.

Prefer pre-aggregated operational cells over pseudonymous event streams.

---

# 3. The minimum decision dataset does not require identity

## PRIV-03 — Candidate aggregate grain

A first production-demand pilot can use a daily/meal aggregate table:

```text
DATE
CAMPUS
MEAL_CLASS
SERVICE_CHANNEL
SERVICE_REGIME
MENU_ID
INITIAL_REQUEST_QTY
FINAL_REQUEST_QTY
PRODUCED_QTY
AGGREGATE_SERVED_OR_ENTRY_COUNT
CONTRACT_ACCEPTED_QTY        # only if releasable
UNSERVED_SURPLUS_QTY
WASTE_QTY
SHORTAGE_EVENT
```

None of those fields inherently requires diner identity.

### Optional higher temporal resolution

If intrameal pacing matters, the data owner can provide aggregated interval counts such as:

```text
DATE | CAMPUS | MEAL | 30_MIN_BUCKET | ENTRY_COUNT
```

Only request finer buckets if they change a named decision, for example whether a second batch can be adjusted during service.

---

# 4. BUCard / QR public evidence should be used only to ask for aggregate export

## PRIV-04 — Public support workflow suggests time/campus/turnstile context exists

`PUBLIC SOURCE`

Boğaziçi's dining FAQ asks users reporting BUCard overcharge issues to supply date, time, campus and turnstile information. The same page states that BUCampus QR can be used for turnstile entry without a physical card.

Source:  
https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0

This suggests that dining-access infrastructure can distinguish operational context.

It does **not** establish:

- retention duration;
- export capability;
- historical completeness;
- one-entry-equals-one-meal semantics;
- legal basis for research use;
- team access.

### Correct PMR/data question

> Can the institutional data owner generate aggregate counts by date × campus × meal/service window from the existing access system, without exposing card/user identifiers?

That is much narrower than asking for raw BUCard logs.

---

# 5. Scholarship/BUBizden identity is unnecessary for the forecasting hypothesis

## PRIV-05 — Access-support systems should become policy-regime context, not personal features

Public sources show:

- in-kind meal scholarships;
- BUBizden free-meal support;
- rights tracked through university systems.

Sources:

- https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096
- https://yemekhane.bogazici.edu.tr/bubizden-uygulamasi

### Forbidden feature design

Do not build features such as:

```text
student_123_is_scholarship_recipient = true
student_456_used_BUBizden_today = true
```

### Safer context

If the operational owner confirms support-policy changes materially alter aggregate demand, use only institutional regime metadata such as:

```text
BUBIZDEN_ACTIVE = true
MEAL_SCHOLARSHIP_POLICY_VERSION = "in_kind_all_meals"
```

Even those should be included only if they improve the named operational decision.

---

# 6. Privacy-by-architecture proposal

## Layer A — institutional source systems

Remain under Boğaziçi control:

- BUCard / QR transaction/access data;
- scholarship/support records;
- payment account details;
- personally attributable complaints;
- personal identity information.

## Layer B — owner-controlled aggregation

Generate only approved operational outputs:

```text
COUNT(entries)
by campus / meal / date / approved interval
```

Potential reconciliation can happen inside the institutional environment before export.

## Layer C — decision dataset

BOUNCAMPUS receives only fields necessary to:

- estimate aggregate demand;
- compare forecast vs actual aggregate;
- evaluate excess/shortage;
- recommend production quantity;
- verify pilot outcomes.

## Layer D — audit/provenance

Store:

- source-system name;
- aggregation rule/version;
- export timestamp;
- measurement unit;
- known limitations;
- no raw personal IDs.

---

# 7. Data contract should declare identity risk explicitly

Each incoming field should have metadata:

```text
field_name
operational_purpose
source_system
aggregation_grain
contains_direct_identifier        # false expected
contains_pseudonymous_identifier  # false expected
reidentification_risk_reviewed
retention_window
owner
correction_policy
```

### Gate

If a proposed field contains a direct or pseudonymous user identifier, the agent must answer:

1. Which decision cannot be made without it?
2. Why does aggregate data fail?
3. Who approved this use?
4. What legal/organizational basis applies?
5. What shorter retention or stronger aggregation can replace it?

Without a clear answer, reject the field from the pilot dataset.

---

# 8. Small-cell and rare-event caution

Even an aggregate table can become identifying when groups are very small or combinations are unique.

Examples:

- tiny campus + rare diet + narrow time bucket;
- single supported user in a narrow cohort;
- unique event/complaint timestamp.

### Internal engineering rule

Do not invent a legal `minimum cell size` and call it KVKK compliance.

Instead:

- identify sparse groups;
- coarsen time/campus/category where necessary;
- have the institutional data owner/privacy function approve the aggregation design;
- document suppression/generalization rules.

---

# 9. Retention should follow the decision experiment

The KVKK principle of keeping data only as long as necessary supports a bounded pilot dataset.

For KREATE/pilot design:

1. define the historical window needed for baseline/seasonality;
2. define the intervention window;
3. define validation/review period;
4. document deletion/retention responsibility for exported datasets.

Do not create an indefinite copy of dining-access history merely because it may become useful later.

---

# 10. Recommended BİD / data-owner interview questions

## P0

1. Can you export **aggregate** dining entry counts by date × campus × meal window without user/card identifiers?
2. What is the natural time grain of the source system?
3. How do QR and BUCard events differ semantically?
4. Can an entry be reversed/refunded/duplicated?
5. How are guest/second meal/student/staff events distinguished, if at all?
6. What history/retention is available?

## P1

7. Can special service regimes / campus closures be joined to the counts?
8. Can the aggregation run inside Boğaziçi rather than exporting raw logs?
9. Which institutional owner must approve a pilot aggregate extract?
10. Which fields should the team explicitly avoid requesting?

### Desired output

Not a database dump. A one-page source/data dictionary plus an aggregate sample table is enough for feasibility testing.

---

# 11. Model architecture implications

## Use aggregate forecasting first

```text
X_t = calendar + menu + service regime + historical aggregate demand
Y_t = aggregate served-demand proxy
```

No user embedding is required.

## Do not build

- individual attendance prediction;
- personalized meal likelihood;
- scholarship-recipient propensity models;
- individual dietary profiling;
- movement tracking across campuses.

Those are outside the current product need and dramatically increase privacy complexity.

---

# 12. Pilot privacy acceptance criteria

A pilot data design should be rejected unless all are true:

1. every field maps to a named operational decision or evaluation metric;
2. no direct student/staff identifier is exported;
3. pseudonymous transaction IDs are absent by default;
4. support/scholarship identity is not exported;
5. aggregation grain has been reviewed for sparse-cell/re-identification risk;
6. retention window is documented;
7. source owner and correction semantics are documented;
8. model outputs are aggregate recommendations, not person-level classifications;
9. the institutional owner controls any source-system aggregation;
10. known limitations are preserved.

---

# 13. Safe application / jury language

A defensible statement is:

> The proposed pilot does not require individual student tracking. Existing dining-access systems are relevant only as a possible source of privacy-safe aggregate campus/meal counts. Raw BUCard, QR, scholarship and support records can remain with the university; the decision layer can operate on aggregated operational quantities under a data-minimization design.

Do not say:

- `KVKK-compliant` unless the responsible institution/legal process has actually determined compliance;
- `anonymous` merely because names were removed;
- `we have BUCard data` before access exists;
- `we track student meal behavior` as a product feature.

Use `privacy-minimized design` or `aggregate-data architecture` instead.

---

# 14. Sources

1. KVKK — General Principles in Processing of Personal Data:  
   https://www.kvkk.gov.tr/Icerik/6606/General-Principles-in-Processing-of-Personal-Data
2. KVKK — deletion/destruction/anonymization and anonymization definition:  
   https://www.kvkk.gov.tr/Icerik/2038/kisisel-verilerin-silinmesi-yok-edilmesi-veya-anonim-hale-getirilmesi
3. KVKK decision summary explaining purpose limitation / avoiding unnecessary data:  
   https://www.kvkk.gov.tr/Icerik/7138/2021-799
4. Boğaziçi dining FAQ / BUCard + QR operational context:  
   https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0
5. Boğaziçi SKS activity report / meal-support context:  
   https://sks.bogazici.edu.tr/tr/pages/faaliyet-raporu/7096
6. BUBizden support system:  
   https://yemekhane.bogazici.edu.tr/bubizden-uygulamasi

---

# 15. Bottom line

The privacy-safe technical question is not:

```text
How do we get student-level BUCard data?
```

It is:

```text
What is the smallest aggregate signal available before the production freeze point
that materially improves the quantity decision?
```

If `campus × meal × date` aggregate counts are enough, the correct system is simpler, safer and easier to pilot.
