# KREATE PMR Hypothesis Test Matrix

**Purpose:** Turn the application hypotheses into falsifiable interview work. This file contains **research design**, not interview evidence.

## Core rule

Do not ask interviewees whether BOUNCAMPUS is a good idea. Reconstruct what happened in a recent real service and identify the decision, owner, timing, information, constraints, and consequences.

Recommended source methodology:

- Disciplined Entrepreneurship PMR: https://www.d-eship.com/step1a/
- Key assumptions: https://www.d-eship.com/step20/
- Beachhead: https://www.d-eship.com/step2/
- Persona: https://www.d-eship.com/step5/

---

# H-A — Controllable production decision exists

## Hypothesis

> In large, centrally coordinated university dining operations, an identifiable operational role determines or approves meal-production quantities before actual demand is known, and that quantity remains adjustable until a defined operational freeze point.

## Why this is critical

A high-accuracy forecast has no product value if:

- it arrives after the decision;
- the quantity is fixed contractually;
- the user has no authority to change it;
- changing the quantity is operationally impossible.

## Primary interview roles

1. Food Services Branch / administrative workflow owner
2. contractor local project/production manager
3. central-kitchen production lead / food engineer

## Topics to explore

- normal planning workflow;
- most recent quantity change;
- first proposed quantity;
- who approves it;
- production/batch timeline;
- ingredient commitment;
- cooking start;
- campus allocation timing;
- same-day adjustment rights;
- emergency substitution.

## High-value prompts

- "Walk me through yesterday's lunch from the first expected quantity until service ended."
- "Who first wrote down or communicated the quantity?"
- "When was the last time that number was changed?"
- "What new information caused the change?"
- "At what point would changing the number create waste, delay, or extra cost?"
- "Who has authority to make that change?"

## Supports H-A if

Multiple relevant stakeholders independently describe:

- a named owner;
- a recurring quantity decision;
- a concrete time horizon;
- a non-zero adjustment window;
- a meaningful action that follows the decision.

## Reject / modify H-A if

- quantity is not actively decided;
- quantity is fixed by contract/policy too far in advance;
- the operator cannot modify it;
- only a downstream decision such as campus allocation is adjustable.

## Product consequence if rejected

Move the intervention point to the nearest reachable decision, for example:

- campus allocation;
- batch timing;
- second-batch release;
- package allocation;
- procurement planning;
- post-service waste reduction.

---

# H-B — Demand mismatch materially causes addressable surplus/shortage

## Hypothesis

> Demand uncertainty and the current production-planning process repeatedly create meaningful mismatches between food prepared and food actually needed, producing avoidable edible surplus and/or shortages that can be affected by changing the production decision.

## Why this is critical

The official annual food-waste total does not identify cause. Forecasting is the wrong intervention if the dominant waste is caused by:

- preparation losses;
- portion size;
- menu dissatisfaction/palatability;
- food-safety rules;
- quality failures;
- storage failures;
- plate waste unrelated to production quantity.

## Primary interview roles

1. daily production/kitchen operator
2. Food Services oversight / food engineer
3. waste-measurement / Zero Waste owner

## Incident reconstruction

For the latest mismatch:

```text
expected demand
actual demand
planned portions
produced portions
served portions
unserved edible surplus
plate/prep waste
shortage/substitution
cause assigned by operator
what could have been changed before service
```

## High-value prompts

- "Tell me about the last service with noticeably too much food left."
- "What exactly was left: cooked but unserved food, preparation waste, or food returned on trays?"
- "What caused it?"
- "Would a different production quantity have materially changed that outcome?"
- "Tell me about the last service where food was at risk of running out."
- "What did staff do?"

## Supports H-B if

- repeated concrete incidents tie production mismatch to unserved surplus or shortage;
- the stakeholder can identify a feasible earlier decision that could have changed the outcome;
- the effect is not merely hypothetical.

## Reject / modify H-B if

- addressable surplus is rare/minor;
- most waste occurs downstream on plates;
- quality/menu factors dominate;
- surplus is unavoidable under safety or service constraints.

## Product consequence if rejected

Pivot the food wedge toward the dominant controllable stage, such as:

- portion-size decision;
- menu design;
- plate-waste diagnosis;
- storage/cold-chain;
- batch/preparation process.

---

# H-C — shortage risk creates a safety buffer and asymmetric decision loss

## Hypothesis

> Food-service operators intentionally maintain a production safety buffer because shortages create a more immediate operational risk than surplus, and this buffer is determined mainly through historical experience and fragmented information rather than a consistently integrated decision process.

## Why this is critical

The product must optimize operational utility, not only forecast error.

Candidate decision loss:

```text
loss = excess_cost * excess_portions
     + shortage_cost * shortage_or_sellout
     + override_or_operational_friction
```

The coefficients must come from policy/PMR, not team intuition.

## High-value prompts

- "When choosing tomorrow's quantity, how much margin do you add for uncertainty?"
- "What happens if the main dish runs out?"
- "What happens if 100 portions remain?"
- "Which outcome is worse and why?"
- "Who gets the complaint/penalty/cost?"
- "What would make you comfortable reducing the buffer?"

## Supports H-C if

- operator describes a deliberate or implicit safety margin;
- shortage is described as disproportionately costly/visible;
- current margin relies heavily on experience/recent history;
- a confidence/risk range is more usable than a scalar forecast.

## Reject / modify H-C if

- no systematic buffer exists;
- shortage and surplus are symmetric;
- current operational system already gives a well-calibrated range;
- contractual rules dominate the buffer independent of demand uncertainty.

## Product consequence if rejected

Simplify the product policy and re-estimate decision objectives from the actual cost/constraint structure.

---

# Secondary hypothesis — data can be captured with acceptable effort

This remains critical even though it is not one of the three form fields.

## Minimum service-level target

- planned quantity
- produced quantity
- served quantity or validated entry count
- edible unserved surplus
- prep waste
- plate waste
- early sell-out/substitution
- menu/service regime
- measurement method

## Data-owner interviews

- Food Services operations
- contractor records owner
- BUCard/BUCampus / IT owner
- waste-accounting owner

## Safe question

> "Can you export privacy-safe aggregate counts by date x campus x meal/service channel, and what does each count actually mean operationally?"

Never ask for person-level diner data unless a later validated decision question genuinely requires it.

---

# Commercial/incentive hypothesis — buyer captures value

## Key question

> If 100 unnecessary portions are prevented, who saves money or avoids risk?

Possible outcomes:

| Contract structure | Likely primary beneficiary to test |
| --- | --- |
| university pays produced/ordered quantity | university |
| contractor paid served/accepted quantity and bears excess | contractor |
| shared adjustment/penalty model | both / joint workflow |
| no meaningful economic effect | sustainability/service value only; weak commercial route unless another KPI matters |

Do not infer Boğaziçi's structure from other universities' contracts.

---

# Interview order by information value

1. **Boğaziçi Food Services governance owner**
   - identify actual quantity owner, freeze point, contract/approval route;
2. **TEMAŞ local production/project owner**
   - identify actual forecasting heuristic, batch flexibility, excess/shortage consequences;
3. **food engineer / daily operator**
   - validate current workflow, buffer, real incidents, records;
4. **IT / BUCard owner**
   - establish aggregate signal availability and semantics;
5. **waste measurement / sustainability owner**
   - establish waste-stage boundary and authoritative KPI;
6. **same persona at second university**
   - test beachhead repeatability rather than Boğaziçi-specificity.

---

# Evidence capture format per interview

Record:

```text
role
organization/unit
last_concrete_incident
input_signals
quantity_owner
approval_owner
freeze_time
adjustment_rights
current_heuristic
explicit_or_implicit_buffer
excess_consequence
shortage_consequence
settlement_quantity
data_sources
data_granularity
privacy/access_constraint
current_workaround
objection
surprise
hypothesis_supported_or_contradicted
new_follow_up_owner
```

Use `KREATE/PMR/INTERVIEW_TEMPLATE.md` for the actual record. No `E-INT-*` evidence ID should exist until a real interview supports a narrow claim.

---

# Stop/continue decision after first interviews

## KEEP current wedge

Only if evidence shows all of:

- recurring addressable quantity decision;
- meaningful mismatch consequences;
- reachable operator;
- measurable outcome;
- plausible data/measurement path;
- no unacceptable service/safety conflict.

## MODIFY

If the problem exists but the controllable decision is different (allocation, batch, portion, menu, storage).

## KILL food-production wedge

If repeated PMR shows no meaningful controllable decision or no material addressable surplus/shortage mechanism.
