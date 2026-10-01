# Campus Decision Surface Atlas — Boğaziçi / KREATE Agent Handoff

**Research date:** 2026-10-01  
**Purpose:** Help all agents choose the next operational decision surface using verified public ownership, data signals, decision cadence and falsifiers instead of feature enthusiasm.  
**Status:** Secondary/public-source synthesis. **NOT PMR. NOT product validation.**

---

# 0. How to use this file

An agent should not ask “what feature can we build?” first. Ask:

```text
1. What real decision exists?
2. Who owns it?
3. When is it made?
4. Which inputs exist before that time?
5. What outcome proves the decision was good or bad?
6. Can the owner actually act on a recommendation?
7. What evidence would kill the module?
```

Every domain below is scored qualitatively from public-source evidence only. `HIGH` does not mean market validation; it means the decision surface is more clearly visible from public sources.

---

# 1. Cross-domain map

| Domain | Public decision owner visibility | Public data/signal visibility | Decision cadence visibility | Direct climate/resource relevance | Current research priority |
| --- | --- | --- | --- | --- | --- |
| Dining production | HIGH | MEDIUM | LOW until PMR | HIGH | **P0 beachhead** |
| Classroom allocation | HIGH | MEDIUM-HIGH | MEDIUM | INDIRECT but operationally strong | **P1 candidate** |
| Shuttle scheduling | MEDIUM | MEDIUM | MEDIUM-HIGH | MEDIUM-HIGH | **P1 candidate** |
| Water management | HIGH | MEDIUM | HIGH | HIGH | P2 unless a sharper operational pain appears |
| Energy/building operations | MEDIUM-HIGH | MEDIUM | MEDIUM | VERY HIGH | P2 because access/control complexity is high |
| Generic sustainability reporting | HIGH | HIGH | MEDIUM | CROSS-DOMAIN | Supporting layer, not standalone wedge |

### Current conclusion

Dining remains the strongest first wedge because its action/outcome loop is short and the problem metric is already public. Classroom allocation and shuttle scheduling are now the strongest **adjacent decision modules** to investigate because public sources expose concrete institutional workflows rather than only sustainability metrics.

---

# 2. Dining production — P0

## Public source anchors

- 48,251 kg food waste reported for 2025.
- central North Campus preparation is publicly described;
- named Food Services technical roles exist;
- a formal dining/cooking/distribution control organization is publicly listed;
- current contractor/procurement is known;
- BUCard/BUCampus are plausible data surfaces.

Read:

- `BOGAZICI_FOOD_OPERATIONS_DEEP_DIVE.md`
- `BOGAZICI_FOOD_PROCUREMENT_CONTRACT.md`
- `BOGAZICI_PMR_PREINTERVIEW_EVIDENCE_PACK.md`

## Decision hypothesis

```text
quantity(date, meal_type, campus, service_channel)
```

## Must learn from PMR

- actual quantity owner;
- production freeze time;
- ordered vs produced vs delivered vs accepted vs served semantics;
- pre-consumer surplus share;
- underproduction consequences;
- data access and granularity.

## Kill condition

No actionable quantity discretion before service, or overproduction is immaterial in measured waste.

---

# 3. Classroom allocation — P1 candidate

## Public source anchors

Boğaziçi Student Affairs states that **general-use classroom scheduling is performed by Kayıt İşleri Şube Müdürlüğü**. The 2025 Facts and Figures inventory lists **161 general-use classrooms**, with 96 in the 26–50 band and heterogeneous larger-room supply.

Sources:

- https://oidb.bogazici.edu.tr/tr/pages/derslikler-hakkinda/4422
- https://sayilarla.bogazici.edu.tr/document

Read: `BOGAZICI_CLASSROOM_ALLOCATION_AND_OCCUPANCY.md`.

## Decision hypothesis

```text
assign(section, time_slot) -> room
```

## Candidate value

- lower capacity mismatch;
- fewer manual revisions;
- less avoidable building/campus movement;
- transparent handling of room type/equipment/accessibility constraints.

## Must learn from PMR

- existing scheduling tool;
- manual workload;
- hardest recurring exception;
- hard/soft constraint hierarchy;
- late-change frequency;
- access to assignment/enrollment data.

## Kill condition

Current allocation is already low-friction/near-automated or apparent slack is dominated by legitimate constraints that cannot be represented.

---

# 4. Shuttle scheduling — P1 candidate

## Public source anchors

Boğaziçi publishes seven shuttle route families, route-level departure times and BUCampus transport access. Sustainability reporting also exposes aggregate capacity/usage indicators.

Sources:

- https://bogazici.edu.tr/tr/pages/ulasim-park/138
- https://mekik.bogazici.edu.tr/
- https://bilgiislem.bogazici.edu.tr/tr/pages/ulasim/8597
- https://kurumsalveri.bogazici.edu.tr/tr/pages/1141-sustainable-practices-targets/1406

Read: `BOGAZICI_SHUTTLE_OPERATIONS_AND_DEMAND.md`.

## Decision hypothesis

```text
frequency(route, time_window)
```

or bounded retiming of departures.

## Candidate value

- reduce peak crowding/left-behind passengers;
- reduce underused runs adjacent to peaks;
- align service with class transitions;
- preserve reliability with the same fleet where possible.

## Must learn from PMR

- operator/approver;
- departure-level ridership;
- actual travel-time data;
- fleet/driver constraints;
- current timetable adjustment process;
- contract/service constraints.

## Kill condition

No material peak imbalance or no authority/data to alter schedules.

---

# 5. Water management — governed, but decision gap not yet sharp

## WM-S01 — Formal governance and quarterly cadence are public

Boğaziçi's Water Management Directive defines a **Su Yönetimi Komisyonu** and unit water administrative officers. It states that water consumption/recovery data are to be presented to the commission **every three months**, and that the commission ordinarily meets every three months.

Source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/1541-water-discharge-guidelines-and-standards/1972

The directive also assigns measurement/monitoring responsibilities to unit water administrative officers and includes loss/leak reduction among responsibilities.

### Research implication

This is not an “unmeasured campus” problem. The more credible question is:

> Which water decision is currently delayed, manual or difficult despite quarterly measurement and formal governance?

Candidate decisions to test—not assume:

```text
leak investigation priority
retrofit priority
rainwater/greywater operating intervention
unit-level anomaly escalation
```

### Why not P0

The public source gives strong governance but no concrete high-frequency unresolved decision comparable to dining production.

### PMR owner route

- Water Management Commission;
- Yapı İşleri ve Teknik Daire;
- unit water administrative owner.

### Kill condition

Current monitoring already routes anomalies/actions effectively and no recurring costly decision delay exists.

---

# 6. Energy/buildings — high climate magnitude, high integration burden

## EN-S01 — ISO 50001 management system already exists

Boğaziçi states that its Energy Management System is structured under ISO 50001, energy consumption is regularly measured/analyzed, improvement areas are identified and an **Energy Management Team** coordinates the system.

Source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/724-plan-to-reduce-energy-consumption/1367

The university's climate/energy material also defines an ISO 50001 scope across multiple campuses and energy carriers.

Source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/1332-climate-action-plan-shared/1428

Existing 2025 GHG research shows electricity and natural gas dominate the reported footprint.

### Research implication

A generic energy dashboard is especially weak because monitoring/governance already exist. The unresolved product question is **actionability**:

```text
anomaly -> diagnosis -> accountable action -> verified savings
```

### PMR questions

- What granularity is energy data available at?
- Which anomalies are already alarmed automatically?
- Who receives alarms and what action follows?
- Which recurring energy decision is still manual or delayed?
- Is occupancy/context used in HVAC/lighting decisions?
- Can savings be verified against a defensible baseline?

### Kill condition

Existing BMS/EMS already closes the action loop or data/control access is unavailable for a hackathon-scale intervention.

---

# 7. Why these domains fit one architecture without forcing one product

The reusable architecture is not “one AI model for campus.” It is a contract for decisions:

```text
OBSERVATION
  source + owner + timestamp + semantics
      ↓
RECONCILIATION
  quality + conflicts + missingness
      ↓
DECISION CONTEXT
  owner + deadline + constraints + allowed actions
      ↓
BASELINE / MODEL
  forecast / score / optimization
      ↓
RECOMMENDATION
  action + confidence + explanation + guardrails
      ↓
HUMAN DECISION
  approve / modify / reject + reason
      ↓
OUTCOME
  service + resource + failure metrics
      ↓
VERIFICATION
  compare against baseline / target / prior state
```

This architecture is justified across dining, rooms and shuttles without claiming all three are validated markets.

---

# 8. Shared data semantics agents must preserve

Never collapse these pairs:

| Concept A | Concept B |
| --- | --- |
| scheduled | observed |
| estimated | measured |
| capacity | demand |
| demand | served/fulfilled |
| recommendation | approved action |
| approved action | executed action |
| event timestamp | reporting period |
| public source | interview evidence |
| model estimate | measured impact |

Cross-domain stable identifiers should include:

```text
decision_id
owner_role
decision_type
context_id
deadline_at
source_snapshot_id
recommendation_version
human_action
executed_at
outcome_window
verification_status
```

---

# 9. Role-specific routing

## IE

P0 dining interviews first. In parallel, perform **one owner interview** each for classroom scheduling and shuttle operations only to determine whether those modules deserve deeper work.

## CS1

Use three baseline-first problem families:

- dining -> probabilistic demand + asymmetric decision loss;
- classrooms -> constraint satisfaction / assignment optimization;
- shuttle -> departure-level demand + schedule optimization.

Do not force the same ML architecture across all three.

## EE

Prioritize measurement semantics and existing data before hardware. Dining waste measurement, classroom occupancy and shuttle counts each have different ground-truth requirements.

## EHB

Only enter when an existing-data audit shows a real sensing gap. Hardware is a means of closing an evidence gap, not the first deliverable.

## CS2

Keep product narrative singular: **decision + verification layer**, with dining as the validated-to-be-tested beachhead and other modules as adjacent expansion hypotheses.

## Backend

Build a reusable provenance/decision ledger, but keep domain payloads explicit rather than flattening all observations into generic telemetry.

## Frontend

Primary UI primitive should be a **decision card** with action, reason, confidence, constraints, approve/override and later outcome. Domain dashboards are secondary.

---

# 10. Next research / PMR sequence

```text
P0 — Dining owner + contractor + BİD + waste semantics
P1a — Registrar classroom-scheduling owner: 1 workflow interview
P1b — Shuttle operations owner: 1 workflow interview
P2a — Water owner: identify one recurring decision after quarterly reporting
P2b — Energy owner: identify one unresolved action loop under ISO 50001
```

Do not deepen a domain merely because more public data exists. Deepen it only when an owner confirms a costly/repeated decision.

---

# 11. Source register

## Classroom
- https://oidb.bogazici.edu.tr/tr/pages/derslikler-hakkinda/4422
- https://sayilarla.bogazici.edu.tr/document

## Shuttle
- https://bogazici.edu.tr/tr/pages/ulasim-park/138
- https://mekik.bogazici.edu.tr/
- https://bilgiislem.bogazici.edu.tr/tr/pages/ulasim/8597
- https://kurumsalveri.bogazici.edu.tr/tr/pages/1141-sustainable-practices-targets/1406

## Water
- https://kurumsalveri.bogazici.edu.tr/tr/pages/1541-water-discharge-guidelines-and-standards/1972
- https://kurumsalveri.bogazici.edu.tr/tr/pages/641-water-reuse-policy/1354

## Energy
- https://kurumsalveri.bogazici.edu.tr/tr/pages/724-plan-to-reduce-energy-consumption/1367
- https://kurumsalveri.bogazici.edu.tr/tr/pages/1332-climate-action-plan-shared/1428

## Dining
See the dedicated dining research packs and source registers in this directory.
