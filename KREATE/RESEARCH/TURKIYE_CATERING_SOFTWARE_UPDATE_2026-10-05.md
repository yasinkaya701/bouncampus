# Türkiye Catering Software — 2026-10-05 Update

**Purpose:** supplement `TURKIYE_CATERING_SOFTWARE_INCUMBENTS_2026-10-04.md` with additional current vendor capabilities discovered on 2026-10-05.

**Boundary:** vendor pages are marketing claims, not independent validation of customer counts, savings, installed-base share or product quality.

## 1. Edge Bilişim — catering operations framing

Source:
https://edgebilisim.com/catering-yemek-fabrikasi-siparis-yazilimi/

Current vendor guidance explicitly frames catering operations around:
- menu and portion costing;
- production need from person/portion count;
- shipment;
- contractual settlement / invoicing;
- historical consumption coefficients;
- point-level waste/fire measurement.

### Strategic implication

The market already understands the operating problem as:

```text
person-count expectation
→ production quantity
→ recipe/material scaling
→ delivery
→ settlement
```

BOUNCAMPUS should integrate above/beside this stack, not rebuild it.

## 2. MutfakSoft — deeper physical-production integration

Source:
https://mutfaksoft.com.tr/

Vendor claims include:
- plan vs actual production monitoring;
- cauldron/batch-level production tracking;
- tray/container weighing and labeling;
- scale integrations;
- cold-storage monitoring;
- waste/fire analysis;
- logistics/delivery tracking;
- management reporting.

### Strategic implication

Even `hardware + IoT connected kitchen production` is not automatically novel.

TrayGate, Production Count Node or kitchen IoT must therefore justify themselves as **specific missing measurements** rather than a generic connected-kitchen proposition.

## 3. CateringKolay — low-cost operational incumbent

Sources:
- https://cateringkolay.com/
- https://cateringkolay.com/fiyatlandirma

Public pricing/capability pages demonstrate that mature basic catering workflow software may have relatively low monthly software cost and fast/free trials.

Capabilities include:
- menus;
- recipes/costing;
- production plan;
- inventory;
- procurement;
- finance;
- personnel/HACCP;
- logistics;
- multi-branch support.

### Commercial implication

A BOUNCAMPUS buyer may compare integration/pilot burden not only against large global competitors but also against inexpensive local SaaS.

Do not assume willingness to pay merely because institutional meal volumes are large.

## 4. ElzaPro / MenufyApp / YamanSoft / MetasSoft / Deevir / Ycater / Dijimo

Current public pages collectively reinforce that Turkish catering software already covers most back-office and production-execution primitives:
- tender and costing;
- menu/recipe;
- stock;
- production calendars;
- purchase/material requirements;
- shipment;
- accounting/e-invoice;
- multi-location operations;
- person-count / portion scaling.

## 5. Stronger system-boundary rule

Before adding any BOUNCAMPUS module, ask:

> Is this a **decision-intelligence gap**, or are we rebuilding a commodity ERP field/module?

### Commodity / integrate instead
- recipes;
- nutrition tables;
- stock ledger;
- procurement;
- invoice;
- basic production order;
- delivery route record;
- HACCP documentation;
- generic dashboard.

### Candidate intelligence layer
- estimate the demand distribution before the freeze point;
- reconcile university-specific external signals;
- quantify shortage vs surplus risk;
- expose missing/low-quality evidence;
- recommend a bounded action;
- allow human override;
- measure result and learn from override/outcome.

## 6. Critical PMR addition

In every target interview, obtain the actual incumbent stack and ask the interviewee to **show the quantity-entry workflow** if possible.

Key distinction:

```text
Does the system decide the number?
OR
Does a human decide the number and the system simply execute/scale it?
```

The second case is the strongest potential insertion point for BOUNCAMPUS.

## 7. Pricing implication

Some local vendors publicly advertise low-thousands-of-TRY monthly plans, while enterprise/catering-scale products vary upward.

Do **not** use these prices to set BOUNCAMPUS pricing yet.

They are useful only to establish:
- software alternatives can be inexpensive;
- integration friction can outweigh license price;
- value must be tied to a measurable decision outcome, not feature count.

## 8. Final red-team

If BOUNCAMPUS cannot show a measurable improvement over:

```text
experienced operator
+ historical counts
+ existing catering ERP
+ current reservation/card data
```

then it does not have a strong beachhead product merely because the UI/model is more advanced.
