# University–Contractor Joint Governance & Veto Structure — 2026-10-04

**Purpose:** test whether institutional dining decisions can be owned jointly by the university and catering contractor rather than by one clean Persona/economic buyer.  
**Status:** public/contract evidence. **Not Boğaziçi workflow validation.**

## Executive conclusion

Current Turkish university food-service evidence shows that the operating Decision-Making Unit can be explicitly **joint**.

In some contracts:

```text
university control organization / food expert
+
contractor project / food expert
```

jointly influence:

- production mix;
- menu/recipe decisions;
- quality/service controls;
- operational records and corrective actions.

This means BOUNCAMPUS should not assume:

```text
one user = one decision owner = one buyer = one approver
```

A more realistic whole-product architecture may need a **shared recommendation, override and evidence trail** visible to both university and contractor stakeholders.

---

# 1. Sakarya University 2026 — explicit joint production-mix decision

Official Public Procurement Board decision:

- Board decision: `2026/UH.I-2163`
- Date: **19.08.2026**
- Procurement: Sakarya University `2026/1002808`, Servise Hazır Yemek Hizmeti Alım İşi
- Scale: **1,250,000 meal units**

Official source:
https://ekap.kik.gov.tr/EKAP/Vatandas/KurulKararGoster.aspx?KararId=992c5efa9fa05688b41bc2a9bf9e09c0927c462208d40fa9af7f78f7e2807899

The reproduced Technical Specification states that the two selectable main dishes are normally produced 50/50, **but the contractor and the University's control organization may jointly decide**, using historical preference data, to produce more of the historically preferred main dish.

### Why this matters

This is direct evidence of a university dining decision where:

```text
historical demand/preference data
        ↓
university control organization + contractor
        ↓
production mix adjustment
```

The control point is not purely a contractor forecast and not purely a university instruction.

### Product implication

A decision-support interface at a site like this may need:

- recommendation visible to both parties;
- source/reason trail;
- explicit university approval / contractor execution state;
- recorded override and actor;
- outcome reconciliation.

---

# 2. Sakarya 2026 — technical food decisions are also joint

The same official decision reproduces a clause for recipes not explicitly defined in the specification: the recipe is to be jointly considered appropriate by the university-side controlling dietitian/food engineer and the contractor's dietitian/food engineer.

The specification also places monthly menu preparation under an institutional Menu Planning Commission with the menu communicated to the contractor by a defined deadline.

### Implication

The institutional dining DMU can include separate authority over:

```text
menu policy / specification
production execution
food-domain technical acceptance
service quality / control
```

Therefore `production quantity decision owner` may itself be only one component of the full adoption unit.

---

# 3. Marmara University — contractor operation under university control organization

Marmara University's current official Food Services page states:

- roughly **10,000 daily students/personnel** use dining services;
- food service across multiple campuses is procured through tender;
- the contractor transports meals to campuses;
- the university's **control organization checks suitability before meals are served**;
- samples are retained and periodically sent for laboratory analysis.

Official source:
https://sks.marmara.edu.tr/hizmetlerimiz/beslenme-hizmetleri/

### Implication

Even where the contractor performs production/logistics, university-side control remains an active operational veto/acceptance layer.

A production recommendation that conflicts with:

- contract standards;
- quality requirements;
- food-safety controls;
- approved menu/portion rules

may be unusable regardless of model quality.

---

# 4. İstanbul Medeniyet University — broad university-side control scope

İstanbul Medeniyet University's current official Food Services page states that catering is provided by experienced food-service firms while the university's control organization performs regular controls across critical points including:

- raw-material sourcing;
- storage conditions;
- kitchen hygiene;
- personnel cleanliness.

Official source:
https://sks.medeniyet.edu.tr/tr/beslenme-hizmetleri-birimi/beslenme-hizmetleri-birimi-hakkinda

### Implication

The university's role can remain substantial even in externally operated catering.

`Outsourced food service` does **not** imply `contractor can unilaterally change operations`.

---

# 5. Çanakkale Onsekiz Mart University — planning/control organization + contractor service

The current ÇOMÜ Food Services page states that its Nutrition Branch manages:

- dining planning and organization;
- food tender, technical specification, control form and contract processes;
- monthly menus under dietitian control;
- control and inspection;
- ÇOMÜ-Kart operations.

It also states the 2026–2027 meal service is performed by a private food company, including production in the contractor's kitchen, transport, service, cleaning and waste management.

Official source:
https://sks.comu.edu.tr/tr/sayfa/beslenme-sube-tanitim-r9.html

### Implication

A common governance split is plausibly:

```text
university
  owns policy/specification/control/card context

contractor
  owns production/logistics/service execution
```

The exact quantity-decision boundary must still be discovered institution by institution.

---

# 6. Shared records can become contractual evidence

Turkish food-service procurement decisions also reproduce specifications where university and contractor food engineers/dietitians perform controls and keep mutual records/forms, with those records treated as evidence for contract enforcement.

This establishes a broader principle:

> operational evidence is not merely analytics; it can become part of contractual accountability.

### BOUNCAMPUS implication

Provenance, actor identity and immutable decision/outcome history may create value beyond forecasting accuracy:

```text
what was recommended
who approved/changed it
what was executed
which source/version was used
what happened
```

This is a **value hypothesis** to test, not a validated buyer priority.

---

# 7. Joint-DMU archetypes

## J0 — university instruction, contractor execution

```text
university sets quantity/policy
contractor executes
```

Likely user/champion:
- university Food Services.

Contractor:
- execution + operational constraint source.

## J1 — contractor forecast, university control/veto

```text
contractor proposes/forecasts
university controls compliance/service
```

Likely end user:
- contractor planner.

Critical veto:
- university Food Services/control organization.

## J2 — explicit joint decision

```text
university + contractor jointly decide
```

Example mechanism:
- Sakarya selectable-main-dish production mix.

Product may need:
- shared view;
- dual actor history;
- joint reason codes;
- role-based approval.

## J3 — contractor central tooling + local client constraints

```text
contractor enterprise system
+
client-specific specification / veto
```

Potentially attractive for enterprise rollout, but only if the same core decision and data contract repeat across projects.

---

# 8. Adoption / veto map to test at Boğaziçi

For each proposed action ask:

| Decision/action | Who proposes? | Who approves? | Who executes? | Who can veto? | Who records outcome? |
| --- | --- | --- | --- | --- | --- |
| total production quantity | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| campus allocation | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| late batch change | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| menu substitution | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| portion/grammage change | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| waste measurement method | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| pilot software use | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| camera/sensor installation | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

The table should be filled through PMR, not inferred from job titles.

---

# 9. PMR questions added by joint-governance evidence

To Food Services:

- Which decisions can TEMAŞ make without university approval?
- Which decisions require Food Services/control-organization approval?
- Can production mix or campus allocation change during the day?
- What records are jointly signed/reconciled?
- Who is blamed when production is excessive or insufficient?
- Which recommendations would you require to review before the contractor acts?

To contractor:

- Which planning decisions can the local project make independently?
- Which require client approval?
- What contract/specification rules prevent following a forecast?
- If the model disagrees with staff/client judgment, whose decision wins?
- Which operational records are shared with the university?

To the economic buyer:

- Would value come from forecast accuracy alone, or also from a shared auditable decision process?

---

# 10. Solution-design consequence

Do **not** architect the first product around autonomous actuation.

A more defensible institutional workflow is:

```text
system generates bounded recommendation
        ↓
role-specific evidence / provenance visible
        ↓
operator proposes action
        ↓
required university/contractor approval state
        ↓
execution recorded
        ↓
outcome + override reason reconciled
```

The exact approval graph should remain configurable because contracts differ.

---

# 11. Beachhead consequence

The DE `same sales process` condition becomes stricter.

Two universities with the same forecasting pain may still be different segments if one has:

```text
university-owned decision
```

and another has:

```text
contractor-owned decision + university veto + central contractor buyer
```

Therefore beachhead validation must compare not just the technical job, but also:

- approval graph;
- contracting party;
- economic beneficiary;
- deployment/pilot permission;
- data owner;
- veto stakeholder.

---

## Current conclusion

Joint university–contractor governance is a **real operating archetype** in Turkish institutional dining.

For BOUNCAMPUS this strengthens the case for:

- human-in-the-loop decisions;
- provenance;
- role-based approval;
- override history;
- measured post-decision verification.

It does **not** prove Boğaziçi uses the same joint quantity-decision mechanism. That remains PMR.
