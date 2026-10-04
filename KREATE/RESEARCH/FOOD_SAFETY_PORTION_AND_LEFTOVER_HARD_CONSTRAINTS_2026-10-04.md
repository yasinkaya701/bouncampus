# Food Safety, Portion & Leftover Hard Constraints — 2026-10-04

**Purpose:** identify operational constraints that a dining-production recommendation must respect before it can be considered actionable.  
**Status:** public institutional context. **Exact active contract clauses and daily operating procedures still require PMR/technical-specification confirmation.**

## Executive conclusion

A food-production optimizer cannot treat the university kitchen as an unconstrained inventory problem.

Current Boğaziçi public sources establish several institutional constraints:

- food safety and hygiene are explicit operating requirements;
- university control organizations inspect quality/hygiene/standards;
- published menu items can carry explicit cooked-portion gram weights;
- leftover meals are **not re-served the next day** under normal practice;
- redistribution of leftovers requires special permission/knowledge/approval.

Therefore BOUNCAMPUS must optimize **within food-safety, portion/specification and service rules**, not around them.

---

# 1. Safe and Sustainable Food Management is a formal governance domain

Boğaziçi's published `Güvenli ve Sürdürülebilir Gıda Yönetimi Yönergesi` states that food production/sales/cafeteria/dining services are governed around:

- access to safe food;
- sustainable food management;
- relevant food-hygiene, microbiological and waste-management rules;
- institutional waste-management and ISO 22000 context.

Official public page:
https://impact.bogazici.edu.tr/node/100022576

### Product consequence

A recommendation that increases apparent waste efficiency but violates:

```text
food safety
approved handling
quality standards
contract/specification rules
```

is invalid.

Food safety belongs in the **hard-constraint layer**, not a soft optimization weight.

---

# 2. Leftover meals are not a free inventory carryover

Boğaziçi's current official sustainable-food page states:

- leftover meals are not re-served the next day;
- they are not distributed except with special permission;
- with university knowledge/approval they can be delivered to people in need or animal shelters.

Official source:
https://kurumsalveri.bogazici.edu.tr/tr/pages/234-healthy-and-affordable-food-choices/1314

### Modeling consequence

Do not assume:

```text
surplus_today
-> inventory_tomorrow
```

as a default recovery mechanism.

A production-surplus decision may therefore have real same-service consequences even if some downstream donation/recovery routes exist.

### Measurement consequence

Separate disposition from waste:

```text
unserved_surplus_generated
surplus_donated
surplus_other_approved_use
surplus_discarded
```

A portion not served to a diner is not automatically equivalent to a kilogram of waste if it enters an approved alternative route.

---

# 3. University control organizations are explicit veto/acceptance actors

The same current public page states that campus dining/canteen/cafeteria operations are regularly inspected by university control organizations.

It identifies a `Dining Hall, Cooking and Food Distribution Control Organisation` responsible for quality, hygiene and compliance with standards in food service.

Official source:
https://kurumsalveri.bogazici.edu.tr/tr/pages/234-healthy-and-affordable-food-choices/1314

### Product consequence

Even if the daily production planner likes a recommendation, operational use can still be constrained by a control/acceptance layer.

The pilot approval graph should therefore distinguish:

```text
model recommendation
operator proposal
required control/approval
execution
```

rather than treating one dashboard user as absolute authority.

---

# 4. Portion grammage is an explicit operational dimension

The current Boğaziçi dining site publishes cooked-portion gram weights for some menu items.

Official current dining page:
https://yemekhane.bogazici.edu.tr/

Examples on the public menu include item-level `Pişmiş Porsiyon Gramajı` values.

### What this supports

Portion grammage is not merely a hidden kitchen detail; it is an explicit food-service attribute.

### What remains unknown

- whether every item has a contractually fixed gram standard;
- what tolerance is accepted;
- who can change grammage;
- whether gram changes require contract/menu/control approval;
- whether production quantity is expressed as portions, recipe mass, batches or multiple units operationally.

### Product consequence

Do not propose an `adaptive portion-size` action until PMR identifies the authority and allowable range.

For the initial product, safer action variables may be:

```text
number_of_portions
batch_release
campus_allocation
```

while treating per-portion grammage as fixed unless explicitly validated otherwise.

---

# 5. Menu/service configuration can itself be constrained by food-safety context

Boğaziçi has previously publicly announced menu restrictions during periods when the regular kitchen infrastructure was unavailable, explicitly citing the need to ensure food safety under transported-meal service.

Official source:
https://yemekhane.bogazici.edu.tr/yemek-hizmeti

### Implication

`service_regime` is not merely a demand feature.

It can alter:

- feasible menu;
- transport constraints;
- batch timing;
- food-safety risk;
- production location.

The decision engine should store regime constraints separately from demand signals.

---

# 6. Recommended decision-policy hierarchy

A production recommendation should be generated only after evaluating constraints in this order:

```text
1. service exists / correct regime
2. food-safety constraints satisfied
3. contract/specification/menu/portion constraints satisfied
4. operational capacity / batch constraints satisfied
5. shortage/service guardrail satisfied
6. only then optimize surplus/cost/waste objective
```

This is safer than placing all objectives into one weighted score.

---

# 7. Minimum constraint schema for a pilot

For every service, capture:

```text
service_regime_id
menu_version
recipe_or_spec_version
portion_standard_version
food_safety_constraint_set
production_location
transport_required
batch_structure
latest_safe_adjustment_time
minimum_service_buffer
approved_substitution_options
surplus_disposition_policy
control_approval_required
```

Not every field must exist in software on day one, but the operator interview must identify which constraints are active.

---

# 8. PMR questions added by this research

To Food Services / control organization:

- Which parts of tomorrow's production plan are legally/contractually fixed?
- Can portion grammage change, or only portion count?
- Who approves a recipe/grammage/substitution change?
- At what time does a quantity change create food-safety or logistics risk?
- What happens to unserved cooked food after the service?
- Which surplus can be donated/reused under approval and which must be discarded?
- Is a late second batch operationally safer than one large first batch?
- Which food categories cannot be adjusted late because of cooking/holding constraints?

To contractor/kitchen:

- Which dishes are prepared in one batch versus multiple batches?
- Which ingredients are committed before cooking starts?
- How long can cooked items safely be held?
- What is the last feasible quantity-change point by dish class?
- Does the current ERP distinguish planned portions, produced portions and actual service?

---

# 9. Product-action taxonomy should reflect constraints

Instead of one generic action:

> produce fewer meals

BOUNCAMPUS may need a bounded action taxonomy:

```text
ADJUST_TOTAL_BEFORE_PREP
ADJUST_BATCH_1
HOLD_OR_RELEASE_BATCH_2
REALLOCATE_BETWEEN_CAMPUSES
USE_APPROVED_SUBSTITUTION
NO_ACTION_CONSTRAINT_BOUND
WITHHOLD_INSUFFICIENT_CONTEXT
```

Which actions are actually feasible must be learned from the target workflow.

---

# 10. Claim firewall

Unsafe:

- `leftovers can simply be reused the next day`;
- `the model can freely reduce portion size`;
- `any surplus portion equals waste`;
- `the optimizer may automatically change recipes/menu`;
- `food-safety constraints can be represented only as a cost penalty`.

Safe:

> Recommendations are bounded by existing food-safety, portion, service and approval rules, and the system withholds actions when the feasible operating window is not established.

---

## Current conclusion

The most useful operational forecast may not be the most aggressive one.

The real product objective is:

```text
reduce avoidable production/surplus
subject to
food safety
+ service continuity
+ approved portion/menu rules
+ real kitchen timing
+ human/control approval
```

This makes **freeze-time and batch-structure PMR** even more important than raw predictive accuracy.
