# Whole Product & Adoption Burden — 2026-10-04

**Status:** Secondary research + product-design implications. **Not customer validation.**

## Executive conclusion

BOUNCAMPUS cannot be evaluated as `forecast model + dashboard` alone.

Disciplined Entrepreneurship's Full Life Cycle Use Case requires mapping how the customer discovers, acquires, installs, uses, evaluates and renews a product, including barriers around the actual workflow.

Primary methodology sources:

- Life Cycle Use Case — https://www.d-eship.com/step6/
- High-Level Product Specifications — https://www.d-eship.com/step7/
- Customer Acquisition Process — https://www.d-eship.com/step13/

Commercial food-waste incumbents also show that the `whole product` commonly includes hardware/integration, onboarding, coaching, reporting and operational change management rather than analytics alone.

The first BOUNCAMPUS whole product should therefore be the **smallest complete decision-and-verification service** that can fit one real operator workflow.

---

# 1. Current solution is only the core product

Current BOUNCAMPUS core capability:

```text
context inputs
-> demand estimate / production band
-> readiness / uncertainty
-> human review
-> decision record
-> post-service comparison
```

This is the technical core, not necessarily the whole product.

A customer cannot get value unless additional pieces around it work.

---

# 2. Whole-product layers for the first dining pilot

## A. Decision definition

Must establish:

- exact quantity being recommended;
- campus / meal / channel scope;
- decision owner;
- information cutoff;
- freeze point;
- allowed adjustment range;
- food-safety/contract rules.

Without this, a forecast can be technically good and operationally irrelevant.

## B. Data adapter / intake

Minimum required actual sources may include:

- historical served counts;
- planned/produced quantities;
- menu;
- service calendar;
- optional reservation/access aggregate;
- service-regime exceptions.

The initial whole product may need to accept CSV/manual exports rather than require full API integration.

## C. Source reconciliation

Need:

- common service IDs;
- campus/meal definitions;
- timestamp semantics;
- missing-data state;
- source ownership;
- measured vs derived vs model-estimated separation.

This is especially important because Boğaziçi public sources already show incompatible-looking capacities/count semantics across reports.

## D. Operator interface

Needs a narrow workflow:

```text
review tomorrow/next-service recommendation
-> inspect reason/missing signals
-> approve / modify / hold
-> record reason if modified
```

Do not make a generic sustainability dashboard the primary interaction.

## E. Outcome measurement

Minimum:

- served count;
- produced count if available;
- edible surplus or appropriate waste stage;
- early sell-out/service failure;
- operator override.

Optional hardware closes measurement gaps rather than defining the product.

## F. Pilot protocol

Customer needs:

- measurement instructions;
- role ownership;
- inclusion/exclusion rules;
- matched-service logic;
- data-quality review;
- result interpretation.

## G. Onboarding / change management

Need:

- who is trained;
- how long daily use takes;
- who resolves missing data;
- what happens during API/system failure;
- escalation path;
- operator trust-building.

## H. Evidence/reporting output

At the end of a pilot provide:

- individual service records;
- recommendation versus action;
- measured result;
- service guardrails;
- override reasons;
- evidence-quality status;
- clear `PROMISING / FAILED / INCONCLUSIVE` conclusion.

---

# 3. Incumbent benchmark — Winnow

Winnow's current university offering describes:

- AI camera + connected scale for automatic waste measurement;
- pre-consumer and plate-waste variants;
- forecasting/production guidance;
- site/service/category reporting;
- cross-site benchmarking.

Source:
https://www.winnowsolutions.com/industries/universities

Winnow's FAQ states that sites receive a **structured 100-day onboarding programme**, coaching/webinars and ongoing support. It also describes low-installation options and Foresight requiring no kitchen hardware.

Source:
https://www.winnowsolutions.com/faqs

Current Foresight is a pre-service production-planning product accessible on mobile and based on occupancy/past-service data, with a lightweight daily operating workflow.

Source:
https://www.winnowsolutions.com/resources/news/introducing-winnow-foresight-a-new-way-to-prevent-food-waste-and-improve-guest-satisfaction-with-ai-powered-forecasting

### Implication

BOUNCAMPUS cannot differentiate on:

- `AI forecast`;
- `mobile production plan`;
- `camera food recognition`;
- `automatic waste measurement`;
- `university multi-site reporting`.

It must either solve a materially different decision/workflow or deliver a substantially better fit for its selected beachhead.

---

# 4. Incumbent benchmark — Leanpath

Leanpath offers a suite of tracking hardware including high-volume floor-scale/camera systems and emphasizes:

```text
measure
-> analyze/understand
-> optimize
-> team behavior/coaching
```

Sources:

- https://www.leanpath.com/products/food-waste-tracking/
- https://www.leanpath.com/wp-content/uploads/2019/04/leanpath-case-study-university-illinois-en-us.pdf

Recent university case material describes AI-enabled fast logging, photos for root-cause discussion and production adjustment in high-volume service.

Source:
https://blog.leanpath.com/cutting-food-waste-46-how-elior-north-america-turned-data-into-daily-action-at-west-virginia-university

### Implication

The incumbent whole product includes **behavioral adoption and operational coaching**, not only measurement technology.

BOUNCAMPUS should test whether operators need:

- software only;
- software + measurement protocol;
- software + hardware;
- software + human onboarding/support.

Do not assume zero-service SaaS is enough.

---

# 5. BOUNCAMPUS whole-product differentiation hypotheses

Potential advantage must be tested around workflow, not feature count.

## Hypothesis WP-01 — existing-data-first installation

A target university can get useful decision support using existing aggregate institutional signals and lightweight service-level measurement without installing full kitchen waste infrastructure first.

Falsifier:

- reliable outcome/decision data cannot be captured without substantial new hardware/process.

## WP-02 — university-context value

Academic calendar, campus/service regime, authorized aggregate movement/access signals and university-specific operational context materially improve decisions beyond generic occupancy/history tools.

Falsifier:

- simple history/occupancy baseline performs equally well in real decision utility.

## WP-03 — provenance/withhold behavior creates trust

Operators value explicit missing-data/readiness states and source traceability enough to change adoption/trust.

Falsifier:

- operators regard these as irrelevant overhead and prioritize simpler workflow.

## WP-04 — decision verification is valuable

Linking recommendation -> operator action -> measured result provides operational/administrative value not already available in current tools.

Falsifier:

- operators do not review decision outcomes or incumbent systems already close the loop sufficiently.

---

# 6. Full life-cycle use case — working hypothesis

## Stage 1 — catalyst

Possible triggers:

- repeated surplus/shortage incident;
- sustainability/waste target;
- contractor performance review;
- procurement renewal;
- new data availability;
- campus service disruption/change.

Must be identified through PMR.

## Stage 2 — discovery

Potential routes:

- peer university referral;
- food-engineering/SKS network;
- sustainability programme;
- contractor/operator network;
- hackathon/pilot introduction.

Word-of-mouth route is currently UNKNOWN.

## Stage 3 — evaluation

Customer likely asks:

- What data are required?
- Will this increase sell-out risk?
- Who sees the recommendation?
- Does it require personal data?
- Does it replace contractor workflow?
- How do we prove savings?
- What does setup require?

## Stage 4 — pilot approval

Potential DMU:

- operations end user/champion;
- Food Services/facilities manager;
- contractor project lead;
- IT/data owner;
- privacy/security;
- procurement/senior administration.

## Stage 5 — install/connect

Preferred first pilot:

```text
existing aggregate export
+ menu/calendar context
+ manual/lightweight outcome capture
```

rather than organization-wide integration.

## Stage 6 — daily use

Target interaction must be very short:

```text
open next service
-> review band/reasons
-> approve/modify/hold
```

Daily burden threshold must be tested.

## Stage 7 — get value

Value is not model accuracy alone.

It is:

```text
better production decision
+ acceptable service level
+ measurable outcome
```

## Stage 8 — evaluate

Pre-agree:

- primary physical KPI;
- service guardrail;
- baseline;
- evidence quality.

## Stage 9 — expand/buy

Only after pilot:

- more halls;
- more campuses;
- deeper integration;
- optional hardware;
- contractor deployment.

## Stage 10 — referral

Test whether operators will introduce peer institutions if the pilot is credible. This is relevant to the DE beachhead word-of-mouth condition.

---

# 7. Minimal whole product for KREATE / first pilot

The first credible package is:

```text
1. workflow discovery + data dictionary
2. historical baseline adapter
3. pre-service production band
4. reason / readiness / WITHHOLD
5. operator approve-modify-hold
6. service-level measurement sheet/import
7. shortage guardrail
8. matched pilot report
9. provenance / claim firewall
10. bounded onboarding + owner responsibilities
```

TrayGate is **optional** unless the pilot's critical measurement cannot otherwise be obtained.

---

# 8. What not to build before PMR

Avoid committing to:

- enterprise ERP replacement;
- student-level tracking;
- mandatory custom sensors at every hall;
- autonomous kitchen actuation;
- generalized digital twin;
- generic sustainability reporting suite;
- complex ML architecture before baseline data;
- cross-domain campus bundle before dining workflow validation.

Each increases whole-product burden without proven customer value.

---

# 9. Adoption questions for interviews

After workflow discovery, ask:

- What would staff need to do differently each day?
- How many minutes of extra work would be unacceptable?
- Who maintains the source data?
- What failure would make you stop trusting the system?
- Would a CSV/manual pilot be acceptable before integration?
- At what point would IT/procurement need to become involved?
- What support would be needed during the first month?
- Who would review pilot results and decide whether to continue?
- Would measurement hardware make adoption easier or harder?

Do not ask merely whether they `like` the product.

---

# 10. Strategic conclusion

The strongest early BOUNCAMPUS strategy is not to out-feature mature waste-tech vendors.

It is to discover a beachhead where a **smaller, existing-data-first, university-workflow-specific whole product** can reach a named decision quickly and prove value with low organizational burden.

If the whole product required to solve the first customer is essentially equivalent to a full Winnow/Leanpath deployment plus university integration, the current differentiation and speed-to-win thesis should be reconsidered.
