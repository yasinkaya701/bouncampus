# Türkiye Catering Software Incumbents — 2026-10-04

**Purpose:** prevent BOUNCAMPUS from claiming novelty for capabilities already sold to Turkish catering operators.  
**Status:** public vendor capability research. Public marketing claims are not independent performance validation.

## Executive conclusion

The Turkish catering-software market already includes products covering substantial parts of:

- menu/recipe management;
- cost calculation;
- inventory;
- procurement;
- daily production planning;
- person/portion scaling;
- multi-location shipment;
- plan-vs-actual / waste-fire tracking;
- invoicing and settlement;
- in some cases, historical-demand forecasting language.

Therefore BOUNCAMPUS must **not** differentiate as:

> `the first digital production-planning system for catering`

or:

> `we replace Excel with an integrated catering ERP.`

The remaining hypothesis is narrower:

> **Does a target operator still lack decision-quality demand intelligence before the quantity freeze, with explicit uncertainty, institution-specific context and recommendation→action→outcome verification?**

That gap must be demonstrated through PMR against the operator's actual incumbent stack.

---

# 1. Deevir — catering / toplu yemek ERP

Public product page describes:

- recipes and production;
- expiration/lot tracking;
- sales/e-documents;
- person-count-based material requirement;
- multi-location shipment;
- menu-level consumption;
- portion cost;
- `fire` rate tracking;
- plan/actual workflow.

Source:
https://www.deevir.com/tr/sektor/catering/

### Implication

Basic production planning and loss reporting are already commodity/ERP capabilities.

---

# 2. YamanSoftSystem Catering ERP

Public page markets a catering-specific ERP with:

- stock;
- recipe costing;
- production planning;
- order management;
- accounting;
- menu planning;
- procurement;
- waste/fire control;
- multi-branch / central-kitchen support.

Source:
https://yamansoftsystem.com/tr/urunlerimiz/catering-erp

### Implication

`single dashboard for stock + recipes + production` is not a defensible BOUNCAMPUS novelty claim.

---

# 3. MutfakPro

Current production-planning page publicly advertises:

- recipe-based production orders;
- daily production planning;
- person-count scaling;
- planned-vs-realized comparison;
- fire/yield tracking;
- batch/lot tracking;
- centralized production use;
- **historical production/demand-based planning language**.

Sources:

- https://mutfakpro.com.tr/yemek-uretim-programi
- https://mutfakpro.com.tr/catering-programi

### Critical implication

Even `uses historical demand to plan production` is not automatically unique.

PMR must ask whether the operator's current ERP already supplies a useful forecast or merely stores/scales the quantity entered by staff.

---

# 4. CateringKolay — explicit manual-plan baseline

CateringKolay publicly describes a daily/weekly production planning table where staff enter planned meal counts, and explicitly states that the product **does not automatically forecast from historical data** in the described production screen.

Source:
https://cateringkolay.com/yemek-uretim-programi

### Why this is useful

This shows an important incumbent archetype:

```text
ERP executes/scales the operator's chosen quantity
BUT does not necessarily solve how the quantity should be chosen
```

That is potentially the exact insertion point for BOUNCAMPUS.

But whether the target operator uses this type of system is unknown.

---

# 5. Çözbim Yemekçi MRP/ERP

Public page describes a long-standing system for:

- production planning;
- purchasing;
- depot/inventory;
- menu;
- costing;
- accounting;
- forms/dispatch documentation;
- role-based access and audit records.

Source:
https://cozbim.com.tr/urun/yemekci-mrp-erp-sistemi/

### Implication

Catering operations can already have mature back-office/process systems. BOUNCAMPUS should prefer integration/adapters over ERP replacement.

---

# 6. Other current products

## MenufyApp

Markets catering production/distribution ERP capabilities including recipe costing, production-planning calendar, shipment and inventory.

Source:
https://www.menufyapp.net/

## Ycater

Markets supplier invoices, stock, recipe costing, nutrition and basic operational management for catering/toplu-yemek businesses.

Source:
https://ycater.app/

## Qapera

Markets integrated inventory/cost/production visibility for centralized kitchens/catering, including integrations with POS/accounting.

Source:
https://qapera.com/tr

### Research boundary

Marketing pages show advertised capability, not installed-base share, quality, adoption or actual customer outcomes.

---

# 7. ElzaPro — public marketing claims require caution

A current ElzaPro page markets:

- catering-specific SaaS;
- tender/cost engine;
- orders/production;
- daily person notifications;
- menu/stock;
- customer portal;
- various usage/customer and savings claims.

Source:
https://elzapro.com/

### Boundary

Treat self-reported customer counts, live transaction numbers and savings percentages as **vendor marketing claims** unless independently verified.

Do not use competitor self-reported savings as evidence of market performance.

---

# 8. Incumbent-stack taxonomy for PMR

Every interview should classify the current planning stack:

## Type A — spreadsheet/manual

```text
historical judgement
+ Excel/paper
+ manual quantity entry
```

Potential BOUNCAMPUS burden: low integration, but data quality may be weak.

## Type B — operational ERP without predictive decision

```text
operator enters quantity
-> ERP scales recipes/materials/production
```

Potential insertion:

```text
BOUNCAMPUS recommendation
-> existing ERP quantity input
```

This may be the most attractive whole-product fit.

## Type C — ERP with historical planning/forecast features

Need to determine:

- actual forecasting method;
- uncertainty;
- contextual variables;
- whether operator trusts/uses it;
- actual result verification.

BOUNCAMPUS must outperform a real baseline, not a strawman.

## Type D — specialist food-waste/forecast suite

Examples internationally:

- Winnow;
- Leanpath.

This is a harder early customer unless a clear workflow gap exists.

---

# 9. Product boundary

BOUNCAMPUS should avoid rebuilding:

- inventory ledger;
- recipe management;
- standard cost accounting;
- e-invoice;
- procurement ledger;
- shipment tracking;
- generic kitchen MRP.

Those are mature software categories.

Preferred architecture:

```text
ERP / BUCard / service systems
        ↓
BOUNCAMPUS decision context
        ↓
uncertainty-aware recommendation
        ↓
operator action
        ↓
existing production workflow / ERP
        ↓
actual outcome
        ↓
verification
```

---

# 10. PMR questions about incumbent software

Do not ask `Do you use an ERP?` only.

Ask:

- Show me how tomorrow's quantity enters your current system.
- Who types that number?
- Where did that number come from?
- Does the system calculate the number or only scale recipes after someone enters it?
- Does it use historical demand automatically?
- Which context does it use?
- Does it produce a range or one number?
- What happens if data are missing?
- Does it compare recommendation with actual outcome?
- Are override reasons recorded?
- What do staff still do in Excel/WhatsApp/paper outside the ERP?
- What would make switching/integrating another tool unacceptable?

The **workaround outside the ERP** may reveal the true product gap.

---

# 11. Strong differentiation test

BOUNCAMPUS earns differentiation only if PMR/pilot shows a material advantage over the **actual incumbent process** on a named decision.

Candidate test:

```text
current operator/ERP plan
vs
BOUNCAMPUS-assisted plan
```

measure:

- decision loss / surplus;
- shortage/service guardrail;
- operator effort;
- override/trust;
- measurement quality.

Do not benchmark only against a deliberately weak naive method if the site already uses a sophisticated system.

---

# 12. Strategic conclusion

The local software landscape makes BOUNCAMPUS's category clearer:

**not catering ERP**  
**not generic production planning**  
**not generic food-waste dashboard**

The remaining thesis is a **decision-intelligence layer above existing operational systems**, provided PMR proves that those systems do not already solve the pre-service uncertainty problem sufficiently.
