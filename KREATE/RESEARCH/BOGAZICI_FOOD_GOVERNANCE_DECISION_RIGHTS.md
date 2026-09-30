# Boğaziçi Food Governance & Decision Rights — From Policy Obligation to Daily Operations

**Research date:** 2026-10-01  
**Status:** Secondary/public-source research. Formal governance responsibility does not prove daily production ownership, budget authority or willingness to buy software.

## Executive conclusion

Boğaziçi's own current food-governance material makes the dining problem more structurally credible than a generic sustainability pitch.

The university's Safe and Sustainable Food Management Directive explicitly includes:

- coordinating safe and sustainable food management across units;
- reducing food loss and waste;
- **production planning**;
- determining and recording **produced, consumed and discarded food amounts/types**;
- **monthly reporting** of those quantities;
- strategies for evaluating production surplus;
- recurring evaluation/reporting to Rectorate.

Separately, Boğaziçi has:

- a Food Service Executive Board focused on payment/control governance;
- a Food Services Branch under SKS;
- a formal Dining Hall, Cooking and Food Distribution Control Organisation;
- BUCard / BİD as a digital payment/access system owner;
- a contractor (TEMAŞ) executing the current 2026–2027 service.

This means the likely product workflow is **multi-role and multi-record**, not one cafeteria manager using one dashboard.

The highest-value PMR task is now to resolve the missing arrows between formal responsibilities:

```text
policy / sustainability governance
        ↓
production planning requirement
        ↓
? daily quantity / service-mode decision owner ?
        ↓
contractor execution
        ↓
control / acceptance
        ↓
served / financial records
        ↓
waste measurement + monthly reporting
```

---

# GOV-01 — Current directive explicitly includes production planning and monthly food-flow measurement

`PUBLIC SOURCE`

Boğaziçi's published Safe and Sustainable Food Management Directive assigns the Safe and Sustainable Food Commission responsibility for reducing food loss/waste. The published duties include:

- determining strategies that reduce food loss and waste;
- **production planning**;
- determining the amounts/types of food **produced, consumed and discarded**;
- recording and **monthly reporting** those values;
- identifying strategies for evaluating production surplus.

Primary/current university sources:

- https://kurumsalveri.bogazici.edu.tr/tr/pages/1522-sustainably-farmed-food-on-campus/1958
- https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/48-bogazici-universitesi-guvenli-ve-surdurulebil-20250407-160443.pdf

### Strategic implication

The product does not need to invent a sustainability rationale for production planning. The university's governance framework already connects food-waste reduction to production planning and measurement.

The product must instead prove that it improves a **specific existing planning workflow**.

### What this does not establish

- the frequency/granularity of operational production planning;
- that the monthly reported fields exist at campus × meal level;
- that `produced` and `consumed` quantities are digitally recorded in one system;
- that the monthly sustainability report is used to decide tomorrow's quantity;
- the identity of the daily quantity owner.

---

# GOV-02 — Food governance includes annual evaluation and Rectorate reporting

The same current directive states that food services are evaluated under the governance framework and that yearly evaluation results are reported to Rectorate.

Primary source:
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/48-bogazici-universitesi-guvenli-ve-surdurulebil-20250407-160443.pdf

### Product implication

A verified pilot can potentially create two outputs from the same source data:

```text
operational output:
what should the kitchen/operator do next?

verification/governance output:
what changed, what evidence supports it, and what should be reported?
```

But reporting is **downstream value**, not the first beachhead by itself.

---

# GOV-03 — The Control Organisation is a formal contractor-service oversight layer

`PUBLIC SOURCE`

The university currently lists a **Yemekhane, Yemek Pişirme ve Yemek Dağıtım Kontrol Teşkilatı**. Current sustainability pages describe it as supervising food-service quality, hygiene and compliance with standards/contracts.

Sources:

- https://bogazici.edu.tr/tr/pages/universite-yonetim-kurulu-kurul-ve-komisyonla/246
- https://kurumsalveri.bogazici.edu.tr/tr/pages/234-healthy-and-affordable-food-choices/1314

Current listed principal members include Ayhan Soylu (chair), Barış Pancar, Aygül Demir, Ahmed Musab Taş and Mustafa Tunç.

### Decision-rights implication

The control organisation is a strong candidate owner for **accepted truth / compliance records**, even if it is not the production planner.

Ask it about:

- what record proves the contractor delivered service correctly;
- shortage/service interruption records;
- quantity or distribution deviations;
- whether production/service changes require approval;
- which produced/delivered/served number is trusted;
- where contract-compliance evidence lives.

### Boundary

Do not infer from `control` that this body chooses daily production quantity.

---

# GOV-04 — Food Service Executive Board is explicitly connected to payment/control governance

`PUBLIC SOURCE`

The current Boğaziçi Food Service Executive Board Directive states that the board exists for the payment and control of food services for students, personnel and guests. It defines the Food Services Branch and BUCard Office within the governance/accounting context.

Primary source:
https://mediastore.cc.bogazici.edu.tr/web/upload/sayfalar/275-yemek-hizmetleri-yonergesi-20251103-152153.pdf

A public 2024 implementation decision also shows the board changing personnel meal collection: eligible personnel meal charges are aggregated and deducted from the following month's salary, with transaction detail visible in BUCard/BUCampus.

Source:
https://yemekhane.bogazici.edu.tr/node/225

### Product implication

There are at least two economic ledgers:

1. user contribution / BUCard / payroll accounting;
2. contractor procurement / acceptance / hakediş accounting.

They must not be conflated.

A user transaction may be useful demand evidence without being the contract settlement unit.

---

# GOV-05 — BUCard / BİD is a data-system role, not automatically an operational decision owner

Public food-service material identifies the BUCard Office as an information-technology-linked campus identity/payment function. The dining FAQ shows BUCard and BUCampus QR use at turnstiles.

Sources:

- https://yemekhane.bogazici.edu.tr/sikca-sorulan-sorular-0
- Food Service Executive Board directive above.

### Role boundary

BİD/BUCard may control data availability and export, but it should not be asked to validate kitchen causal assumptions.

Expected interview scope:

```text
what events exist
what timestamps exist
what campus/turnstile attributes exist
retention
aggregate export feasibility
reservation/cancellation tables
privacy/approval requirements
```

Not:

```text
how many meals should be produced
```

---

# GOV-06 — Contractor is execution actor; sector precedents make it a plausible daily decision user

`PUBLIC SOURCE + SECTOR PRECEDENT`

Boğaziçi's 2026–2027 meal-service contractor is TEMAŞ Gıda under a large unit-price service procurement.

Boğaziçi source:
https://ekapveri.com/ihale/ekap-2025-1727143/

Separate Turkish university KİK precedents already documented in `TURKIYE_DINING_CONTRACT_DECISION_PRECEDENTS.md` show cases where contractors estimate daily quantities from historical demand and bear excess/shortage risk.

### What this changes

Do not define the product persona as `university sustainability manager` by default.

Candidate role split:

| Role | Candidate product relationship |
| --- | --- |
| SKS / Food Services | contract/process owner; potential buyer/sponsor |
| TEMAŞ project/kitchen operator | possible daily decision user |
| Control Organisation | verifier/acceptance/compliance stakeholder |
| BİD / BUCard | data-system owner |
| Safe & Sustainable Food Commission | sustainability governance / reporting stakeholder |
| Zero Waste / waste operation | waste measurement owner |
| Students/staff | service beneficiaries / intent signal providers |

PMR must determine which role has **decision + pain + incentive + authority**.

---

# GOV-07 — Current governance source and 2024 draft must be versioned separately

A publicly hosted 2024 draft/version of the Safe and Sustainable Food Management Directive shows a broader proposed/dated commission composition including Corporate Data Management, Asset Management and the Control Organisation Coordinator.

Source:
https://mediastore.cc.bogazici.edu.tr/web/userfiles/files/bogazici_universitesi_guvenli_ve_surdurulebilir_gida_yonetimi_yonergesi_19_07_2024_-taslak.pdf

The currently surfaced directive/impact pages describe a different composition centered on appointed academics, SKS, Food Services, Administrative & Financial Affairs and the Deputy Secretary-General.

### Agent rule

Do not merge these membership lists.

The older/draft version is useful evidence that **cross-unit data/control integration has been contemplated**, but current interview routing must be based on the current organisation or owner confirmation.

---

# GOV-08 — Measurement obligations create a valuable reconciliation question

The current directive asks for produced, consumed and discarded quantities and monthly reporting. Existing public food-waste reporting also contains known generation/collection semantic anomalies documented in `BOGAZICI_SOURCE_RECONCILIATION.md`.

This yields a concrete primary-research question:

> **What exact source systems and definitions are used to produce the monthly `produced`, `consumed`, `discarded` and food-waste reports?**

Possible states:

```text
A. already reconciled automatically
   → product should not duplicate it

B. reconciled manually across kitchen/BUCard/waste records
   → provenance/reconciliation may have operational value

C. fields do not exist at decision granularity
   → pilot must create prospective measurement
```

Do not assume B.

---

# 1. Decision-rights matrix to validate

| Decision / record | Likely involved role from public evidence | Validated owner? | Required PMR evidence |
| --- | --- | --- | --- |
| Menu policy | Food Services / relevant boards/food professionals | PARTIAL | recent real menu-change workflow |
| Reservation mechanism | Food Services + BUCard/BİD | PARTIAL | who activates/configures it and why |
| Daily production quantity | Food Services and/or TEMAŞ | **UNKNOWN** | reconstruct a specific service day |
| Campus allocation | central production + local service + contractor | **UNKNOWN** | dispatch/allocation record |
| Package vs dining-hall mode | Food Services / operational governance | historical evidence only | current approval rule |
| Batch/replenishment | TEMAŞ/kitchen | **UNKNOWN** | kitchen process interview |
| Service acceptance/compliance | Control Organisation / Food Services | PLAUSIBLE | accepted record + exception workflow |
| User meal charge | BUCard / Food Service Executive Board/accounting | PARTIAL | transaction/accounting dictionary |
| Contractor hakediş | SKS/procurement/control | **UNKNOWN** | signed contract or hakediş owner |
| Waste measurement | sustainability/Zero Waste/operations | PARTIAL | data dictionary and physical boundary |
| Monthly food-flow reporting | Safe & Sustainable Food governance / unit responsible | policy obligation established | actual reporting owner/system |
| Sustainability strategy | Safe & Sustainable Food Commission | established governance | recent decision example |

---

# 2. PMR sequence after governance research

## Interview A — Food Services Branch

Ask them to draw the real swimlane for yesterday/tomorrow's lunch:

```text
signal
→ who calculates quantity
→ who communicates it
→ contractor action
→ control/acceptance
→ actual service record
→ waste record
→ monthly report
```

Do not ask for generic opinions about AI.

## Interview B — TEMAŞ local operator

Determine the actual direct user and irreversible points:

```text
ingredient commitment
prep start
batch start
campus dispatch
replenishment cutoff
```

## Interview C — Control Organisation

Resolve accepted truth and exception records.

## Interview D — BUCard/BİD

Resolve event schema and aggregate export.

## Interview E — Safe/Sustainable Food or waste-data owner

Resolve monthly `produced / consumed / discarded` definitions and what decisions those reports currently change.

---

# 3. Product architecture implied by governance — if PMR validates it

The strongest long-term object is not a dashboard page; it is a **decision record** connecting multiple institutional roles:

```text
source signals
→ proposed action
→ operator
→ approver / authority
→ execution
→ control/acceptance evidence
→ measured operational outcome
→ waste/sustainability outcome
→ reportable evidence
```

Minimum decision metadata:

```text
decision_owner_role
execution_owner_role
approval_required_by
control_or_acceptance_owner
data_sources
cutoff/freeze_time
recommended_action
operator_action
override_reason
accepted_service_record
physical_outcome
reporting_outcome
```

This provides a defensible differentiation from a generic forecasting notebook or sustainability KPI wall.

---

# 4. Kill / modify conditions from governance research

Modify the product if:

- formal production planning already has an adequate tool and operators report no meaningful unresolved decision;
- monthly produced/consumed/discarded data are already reconciled automatically with no decision friction;
- the production user and economic beneficiary are different actors with no incentive-sharing path;
- any recommendation would require approval too late to affect production;
- the control organisation cannot accept pilot-produced records as meaningful evidence;
- daily decisions are contractually fixed and operator discretion is negligible.

If governance is complex but no decision can be changed, **do not mistake bureaucracy for a software market**.

---

# 5. Safe application language

> `PUBLIC SOURCE` Boğaziçi's Safe and Sustainable Food Management framework explicitly includes production planning and monthly recording of produced, consumed and discarded food quantities as part of reducing food loss and waste. The university also has separate food-service, control, digital payment/access and contractor roles. `HYPOTHESIS` We are testing whether these existing signals and responsibilities leave a time-sensitive production or service-mode decision that can be improved and prospectively verified.

Do not claim that the university has requested BOUNCAMPUS, that governance is fragmented, or that a specific role is the buyer/user until PMR establishes it.