# Privacy & Data-Minimization Boundaries — 2026-10-04

**Status:** Product-design research based on public KVKK guidance. **Not legal advice.** Final deployment requires institutional/legal review by the relevant data controller.

---

# 1. Core KVKK design principle

KVKK public guidance on Article 4 lists mandatory principles including:

- lawful and fair processing;
- accurate/up-to-date data;
- specified, explicit and legitimate purposes;
- processing that is **relevant, limited and proportionate** to the purpose;
- retention only for the period required by law or purpose.

Official KVKK source:
https://kvkk.gov.tr/SharedFolderServer/CMSFiles/0517c528-a43d-49f5-b1eb-33dc666cb938.pdf

The Authority's guidance further explains that data not necessary for the stated purpose should not be collected merely for possible future use.

### BOUNCAMPUS implication

The first dining pilot should be designed around **service-level aggregates**, not person-level tracking.

---

# 2. BUCard / turnstile data — minimize upstream

The production decision requires a count, not an identity.

Preferred contract:

```text
date
campus
meal_window
validated_entry_count
source_definition
quality
```

Avoid unless later proven necessary and legally supported:

- student name;
- student number;
- individual dining history;
- demographic profile;
- scholarship identity;
- cross-service behavioral tracking.

If raw event data must be handled by an institutional data owner, aggregation/anonymization should occur as far upstream as feasible before BOUNCAMPUS receives the signal.

### Reason

The decision question is:

> how many people were/are likely to be served?

not:

> which named people ate?

Collecting identity when count suffices increases privacy/security burden without improving the first decision.

---

# 3. TrayGate camera — field of view should be tray-first

A tray-return system does not need to recognize students.

Product-design requirements:

- camera aimed at controlled tray capture area;
- avoid face/head/body field-of-view where technically feasible;
- controlled hood/tunnel can reduce incidental capture and improve lighting consistency;
- do not use facial recognition;
- do not attempt identity linkage between tray and diner in V1;
- process locally where practical;
- retain derived measurement instead of raw images where raw retention is not needed for validation/audit;
- define explicit retention period for temporary calibration images.

### KVKK relevance

KVKK decisions emphasize that collection must be linked to a specified legitimate purpose and be limited/proportionate. A camera system should therefore not capture audio or wider human activity simply because the hardware can.

Official example on camera/audio proportionality principles:
https://www.kvkk.gov.tr/Icerik/6892/2020-212

---

# 4. No biometric shortcut

KVKK has specific decisions concerning university use of biometric data, emphasizing the special sensitivity of biometric processing and proportionality requirements.

Official example:
https://www.kvkk.gov.tr/Icerik/8860/2024-197

### BOUNCAMPUS rule

Do not solve attendance/dining-demand measurement with:

- facial recognition;
- fingerprint;
- biometric re-identification;

when aggregate card/turnstile or anonymous physical counting can answer the operational question.

---

# 5. Anonymous physical counting alternatives

Where existing aggregate digital signals are unavailable, prefer measurements that do not create an identity record:

- IR break-beam;
- ToF;
- radar;
- tray-return counter;
- serving-line counter;
- zone-level occupancy counts.

Even anonymous sensing should still have:

- stated purpose;
- collection boundary;
- quality/uncertainty semantics;
- retention policy where data are stored.

---

# 6. Menu votes / surveys

For demand modeling, individual voter identity is unnecessary in the first design.

Preferred export:

```text
poll_id
candidate
aggregate_vote_count
open_at
close_at
```

Likewise tasting/satisfaction data should initially be requested as aggregate:

```text
service_or_menu_id
question_or_score
aggregate_score
n
questionnaire_version
```

The model needs signal strength/coverage, not who voted.

---

# 7. Operator decision records

Operator identity may be relevant for audit/authorization, but analytical models should generally learn from:

- role;
- override reason;
- timestamp;
- decision/action;

rather than personal performance profiling unless there is a separately justified purpose.

Candidate record:

```text
decision_id
operator_role
created_at
recommendation
operator_action
override_reason
```

Access control can preserve accountability without exposing unnecessary person-level information to model training.

---

# 8. Retention hierarchy

Suggested design principle, subject to institutional policy/legal review:

## Long-term operational record

Retain:

- aggregate measurement;
- service ID;
- provenance;
- decision/output;
- quality metadata;
- derived waste/flow values.

## Short-term validation only

Potentially retain for bounded technical validation:

- TrayGate raw RGB/depth captures;
- calibration frames;
- temporary annotated samples.

Delete/anonymize according to approved validation/retention plan when no longer needed.

### Never default to

> keep all raw data forever in case it becomes useful.

That conflicts with data-minimization/purpose/retention principles.

---

# 9. Pilot privacy checklist

Before a real deployment:

- [ ] named institutional data controller/owner identified;
- [ ] specific purpose documented;
- [ ] legal processing basis reviewed by institution;
- [ ] minimum fields agreed;
- [ ] person-level data excluded unless strictly required;
- [ ] TrayGate field-of-view reviewed;
- [ ] no unnecessary audio capture;
- [ ] raw-image retention period defined;
- [ ] access roles defined;
- [ ] security/storage location defined;
- [ ] aggregate/anonymization approach documented;
- [ ] deletion/retention behavior tested;
- [ ] required privacy/notice process reviewed by institution.

---

# 10. Product advantage of minimization

Data minimization is not only compliance overhead.

A system that can produce useful operational decisions from:

```text
aggregate counts
+ menu/calendar context
+ service-level production/waste data
```

has:

- lower integration friction;
- lower privacy risk;
- simpler security model;
- easier pilot approval;
- better portability to other institutions.

This should be tested as a sales/pilot advantage through PMR, not assumed.
