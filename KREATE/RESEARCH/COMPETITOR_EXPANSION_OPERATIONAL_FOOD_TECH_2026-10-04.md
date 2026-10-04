# Competitor Expansion — Operational Food-Tech Red Team — 2026-10-04

**Purpose:** stress-test BOUNCAMPUS differentiation against additional current food-waste and food-operations products beyond Winnow/Leanpath.  
**Status:** public vendor-source research. **Vendor claims are not neutral performance benchmarks and absence from public pages does not prove a missing capability.**

## Executive conclusion

Additional competitor research further narrows what BOUNCAMPUS can credibly claim as differentiation.

The following categories are already commercially offered in overlapping products:

```text
automatic food-waste capture
AI waste classification
university-specific food-waste programs
consumption-trend analysis
menu/portion/overproduction guidance
operator action suggestions
approve/reject action workflow
result tracking
historical-sales demand forecasting
safety-stock configuration
central-kitchen production planning
multi-outlet planning
inventory/procurement automation
role-based operational dashboards
```

Therefore BOUNCAMPUS should not define its moat as a feature checklist.

The remaining product thesis must be tested around **institution-specific decision coordination under contractual/data constraints**, especially:

```text
exact reachable control point
+ university/contractor shared governance
+ decision-time source semantics
+ bounded uncertainty / abstention
+ institution-specific context adapters
+ causal stage measurement
+ auditable recommendation -> approval -> execution -> outcome chain
```

Even several of these elements overlap individually with mature products. The defensibility question is whether the **combined workflow solves a specific unmet institutional job better than existing systems and internal processes**.

---

# 1. KITRO — direct university/campus overlap is stronger than a generic waste tracker

KITRO currently has a dedicated `Universities & Schools` vertical.

Current public page:
https://www.kitro.ch/industries/universities-schools

KITRO publicly names education customers including:

- ETH Zürich;
- EHL Hospitality Business School;
- SHL Schweizerische Hotelfachschule Luzern.

Its university/school messaging explicitly addresses multiple institutional roles.

## Catering Manager

Publicly described jobs include:

- adapt menus from consumption trends;
- reduce waste while maintaining dietary variety;
- improve planning during peak periods, events and semester transitions.

## Procurement Manager

Publicly described jobs include:

- align orders with actual consumption;
- reduce spoilage;
- improve forecasting with kitchen collaboration;
- balance budget efficiency and supplier negotiations.

## Sustainability Officer

Publicly described jobs include:

- track/communicate food-waste reduction;
- use data in sustainability reporting/certification;
- support awareness programs.

KITRO also explicitly markets benefits such as:

- reducing overproduction;
- adapting menus to actual student demand;
- serving appropriate portions;
- aligning procurement to consumption trends.

### Implication

Do **not** claim:

- `university-specific food-waste intelligence is unique`;
- `competitors do not use consumption trends`;
- `competitors only measure bins without operational guidance`;
- `campus semester/peak-period planning is untouched`.

### Important boundary

KITRO's public page does not by itself establish the exact algorithm, timing, reservation integration, contract semantics or decision authority used at each customer.

Use PMR to ask whether KITRO-like systems would solve the target operator's actual decision.

---

# 2. KITRO customer cases show whole-product/value competition, not only technical competition

KITRO's current SHL case study describes:

- one installed TARE device;
- operational food-waste reduction;
- measured time/cost/ROI claims under the vendor's case-study method.

Source:
https://www.kitro.ch/case-studies/shl

KITRO's current EHL case study describes multiple outlets and use of waste data in education/operations.

Source:
https://www.kitro.ch/case-studies/ehl

### Strategic implication

A customer may compare BOUNCAMPUS not only against model accuracy but against a package of:

```text
hardware
installation
analytics
expert support
operational action
sustainability communication
case-study credibility
```

This reinforces `WHOLE_PRODUCT_AND_ADOPTION_BURDEN_2026-10-04.md`.

Vendor case-study savings must **not** be transferred into BOUNCAMPUS expected impact.

---

# 3. Orbisk — action workflow overlaps with human-in-the-loop product language

Orbisk currently markets automatic food-waste capture and an `AI-Powered Actions` layer.

Current sources:

- https://orbisk.com/
- https://orbisk.com/product/orbisk-ai/

Orbisk publicly describes:

```text
waste data
-> AI identifies high-impact actions
-> operator can approve/reject
-> results tracked in Actions tab
```

Its core system automatically captures waste before it is mixed and classifies by food/ingredient, waste stream and serving stage.

### Implication

Do **not** claim:

- `human approve/reject of AI action is unique`;
- `action tracking after an AI recommendation is unique`;
- `automatic stage-aware waste capture is unique`.

### Remaining distinction to test

BOUNCAMPUS may still differ if the job is **pre-service resource commitment under university/contractor governance**, rather than mainly a waste-derived action loop.

But the distinction must be described by the exact decision and workflow, not generic human-in-the-loop language.

---

# 4. Apicbase — demand forecasting + production planning + safety stock are incumbent categories

Apicbase currently offers a broad food-operations stack including:

- demand forecasting;
- production planning;
- central-production-unit workflows;
- inventory management;
- procurement/order suggestions;
- menu planning;
- role-based dashboards;
- traceability.

Sources:

- https://get.apicbase.com/demand-forecasting-software-restaurant/
- https://get.apicbase.com/production-planning/
- https://get.apicbase.com/platform/
- https://support.apicbase.com/help/demand-forecasting

## Demand forecasting

Public documentation states sales-based ordering uses:

- POS sales linked to recipes/BOM;
- historical sales patterns;
- day-of-week comparison;
- inventory context;
- configurable safety stock.

It explicitly positions the feature around reducing over-purchase and stockouts.

## Production planning

Public product pages describe:

- recipe/menu production plans;
- automatic scaling to planned portions;
- local or group-wide plans;
- central-kitchen workflows;
- multi-outlet aggregation;
- production tasks and execution tracking;
- BOM-to-purchase-order conversion.

### Implication

Do **not** claim:

- `demand forecasting + safety buffer is unique`;
- `central kitchen production planning is unique`;
- `multi-campus/outlet production aggregation is unique`;
- `forecast -> procurement -> production is an untouched workflow`.

### Critical PMR question

If the target catering operator already uses an ERP/operations platform, ask:

> Which decision remains difficult despite POS/history, inventory, recipe and production-planning tools?

BOUNCAMPUS must earn its place as either:

- an institutional context layer feeding an incumbent;
- a coordination/approval/evidence layer;
- a better decision model for a residual uncertainty source;
- or a different decision product altogether.

---

# 5. Expanded competitive categories

## Category A — automated waste intelligence

Examples:
- Winnow;
- Leanpath;
- KITRO;
- Orbisk.

Compete on:
- measurement quality;
- workflow friction;
- actionability;
- support;
- reporting;
- operational change.

BOUNCAMPUS should integrate rather than duplicate this category when high-quality measurements already exist.

## Category B — foodservice ERP / operations planning

Examples:
- Apicbase;
- Turkish catering ERP incumbents already researched.

Compete on:
- recipes;
- inventory;
- purchasing;
- production execution;
- sales/POS integration;
- forecasting;
- multi-site operations.

BOUNCAMPUS should not become another generic ERP.

## Category C — campus sustainability governance

Example:
- Emissary Campus.

Compete on:
- evidence governance;
- sustainability reporting;
- cross-domain metrics;
- institutional roles/approvals.

BOUNCAMPUS should avoid becoming a generic sustainability reporting system.

## Category D — status quo / expert operator

Often the real incumbent:

```text
experienced planner
+ historical counts
+ Excel/ERP
+ safety buffer
+ contractor/client phone calls
```

This can outperform a new tool on hidden context even with less sophisticated analytics.

---

# 6. What still may be defensible — as hypotheses

## A. Decision-cutoff fidelity

A product explicitly models:

```text
what was knowable before the real freeze point
```

rather than using post-service information or generic forecast windows.

Need PMR to prove the freeze point matters and is not already handled.

## B. Institutional signal adapters

Potentially:

- academic calendar;
- campus/service regime;
- reservation architecture;
- BUCard/turnstile aggregates;
- course/activity context;
- university-specific operational notices;
- contractor settlement/approval rules.

Need measured incremental value; `more features` is not enough.

## C. Shared university–contractor decision governance

Potentially:

```text
recommendation
-> actor-specific review/approval
-> execution
-> override reason
-> contract/source version
-> measured outcome
```

Current Sakarya procurement evidence shows joint decisions exist in the market.

Need PMR to prove the shared evidence/approval workflow is painful enough to buy.

## D. Evidence abstention

`WITHHOLD` when critical source coverage is insufficient.

Could improve institutional trust/safety, but buyers must value it.

## E. Intervention causality / stage-specific verification

Separating:

- unserved edible surplus;
- plate waste;
- prep waste;
- stockout/service guardrails.

This may be valuable because the target intervention should only claim the stage it can affect.

Again, not automatically a moat.

---

# 7. Revised competitor interview script

After reconstructing the current workflow, ask:

- Which software already touches this decision?
- Does your ERP forecast demand, or does it only execute quantities staff enter?
- Where does the initial number come from?
- Does a waste-tracking system influence tomorrow's number?
- Are reservation/card/calendar signals integrated into the same decision?
- Does the tool know the client contract/approval constraints?
- When the system recommendation is wrong, how is the reason learned?
- Can it abstain when data are stale/missing?
- Who sees the recommendation: university, contractor, both?
- Can you trace who changed a quantity and why?
- What part of the workflow still lives in calls, WhatsApp, email or Excel?

The unresolved manual seam may be more valuable than another predictive model.

---

# 8. Claim firewall update

Forbidden without direct comparative evidence:

- `only BOUNCAMPUS closes the action loop`;
- `only BOUNCAMPUS keeps humans in control`;
- `other tools do not track outcomes`;
- `other tools cannot handle universities`;
- `other tools cannot forecast demand`;
- `other tools cannot plan central production`;
- `other tools cannot account for safety stock`;
- `competitors lack role-based workflows`.

Safe:

> Existing food-waste and food-operations platforms already cover many individual capabilities. We are testing whether a university-specific, contract-aware decision-and-verification workflow around a precisely timed operational decision remains underserved.

---

## Current conclusion

The deeper the competitor research goes, the less credible a feature-led moat becomes.

The product must be justified by an unresolved **institutional operating job**, not by the presence of AI, forecasting, cameras, approval buttons or dashboards.

The decisive competitive evidence must now come from PMR:

```text
what current system is used
what decision it changes
what it still cannot resolve
why that gap matters enough to change behavior/pay
```
