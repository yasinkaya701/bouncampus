# Boğaziçi Shuttle Operations & Demand — Agent Research Pack

**Research date:** 2026-10-01  
**Purpose:** Give agents a source-grounded view of shuttle scheduling as a possible second decision-intelligence module.  
**Status:** Secondary/public-source research only. **NOT PMR. NOT ridership telemetry. NOT proof of a shuttle optimization problem at Boğaziçi.**

---

# 0. Executive conclusion

Boğaziçi operates a multi-campus shuttle system with public routes/timetables and BUCampus transport access. Public sustainability reporting also gives aggregate capacity/usage indicators. This makes shuttle scheduling a technically plausible optimization surface.

However, the public material does **not** establish departure-level overload, long queues, low occupancy, unreliable travel time, poor route design or avoidable emissions. A product module should therefore start as a **decision hypothesis**, not as a claim that current shuttle operations are inefficient.

Best question:

> Can route/departure recommendations use class-transition demand and observed ridership to reduce crowding or unnecessary runs without harming reliability?

---

# 1. Claim firewall

- Published routes/times prove service structure, not poor scheduling.
- Aggregate 93% occupancy does not describe peak-load distribution by departure.
- Capacity and users from sustainability reporting must not be interpreted as per-trip occupancy without owner confirmation.
- Public course schedules can create a demand prior, not actual ridership.
- App interest/request data is not actual boarding.
- Academic shuttle optimization results are design references, not expected Boğaziçi gains.

---

# 2. Public route and timetable surface

## SH-S01 — Current university page lists seven shuttle route families

**Source:** Boğaziçi University Transportation / Park  
https://bogazici.edu.tr/tr/pages/ulasim-park/138

Routes publicly listed:

1. Güney Meydan – Etiler Kapı
2. Güney Meydan – Etiler Kapı – Hisar Kampüs
3. Etiler Kapı – Anadolu Hisarı Kampüs – Kandilli Kampüs
4. Etiler Kapı – Kilyos Kampüs
5. Kilyos Kampüs – Zekeriyaköy
6. Kilyos Kampüs – Arıköy
7. Kilyos Kampüs – Kilyos Merkez

The same page states that students, faculty and staff use shuttles to move among campuses and access courses, laboratories, dormitories, dining halls and other services.

### Implication

Class schedules and campus destinations are legitimate contextual demand variables, but no public source proves they are sufficient to forecast actual ridership.

---

## SH-S02 — Route-level fixed departure schedules are publicly exposed

**Source example:** Shuttle Information System, South Square departure toward North Campus  
https://mekik.bogazici.edu.tr/route.php?id=12&lang=en

The route page exposes stops and a sequence of scheduled departures. This supports a machine-readable-looking public timetable surface and a fixed-schedule operational baseline.

### PMR/data questions

- Where is the canonical timetable maintained?
- Are actual departure/arrival timestamps stored?
- Are vehicle IDs and capacities stored per run?
- Are boarding/alighting counts measured?
- Are queues or left-behind passengers recorded?
- What triggers adding/removing/re-timing a run?
- Who approves timetable changes?

---

## SH-S03 — BUCampus already exposes transportation information

**Source:** Boğaziçi University IT / BUCampus Transportation page  
https://bilgiislem.bogazici.edu.tr/tr/pages/ulasim/8597

BUCampus exposes inter-campus shuttle route/time information and public transportation guidance.

### Product implication

A student-facing “show me the schedule” feature is not differentiated. If a shuttle module exists, value must come from the **operator decision loop** or from a genuinely new intent signal—not from duplicating timetable display.

---

# 3. Existing aggregate sustainability signal

The university's sustainable-practices reporting has publicly listed:

- campus shuttle services: 7;
- listed service capacity: 1,429;
- users: 1,332;
- occupancy rate: 93%;
- 2026 user target: 1,350.

Existing research source:  
https://kurumsalveri.bogazici.edu.tr/tr/pages/1141-sustainable-practices-targets/1406

### Critical semantic warning

Do not assume:

```text
1332 / 1429 = average per-departure load
```

The published table may use annual/program-level or service-level reporting semantics. The exact denominator and period must be confirmed before optimization claims.

### Research inference

A high aggregate occupancy indicator can coexist with:

- overloaded peaks and empty off-peaks;
- route-specific imbalance;
- reliability problems;
- efficient operations with little room for improvement.

Only departure-level PMR/data can distinguish these cases.

---

# 4. Academic design references

## AR-SH-01 — Class times and historical ridership can inform university shuttle scheduling

**Paper:** A. Mahmoudzadeh, Xiu-Bin Wang (2020), *Transportation Research Record* 2674, 236–248, “Cluster Based Methodology for Scheduling a University Shuttle System.”  
Consensus record: https://consensus.app/papers/cluster-based-methodology-for-scheduling-a-university-mahmoudzadeh-wang/b7343ef3a4815186bb9cae7a144c014b/?utm_source=chatgpt

The study used university ridership data and class-time patterns to identify departure-demand structure and redesign schedules.

**Use for:** feature hypotheses and transparent scheduling baselines.  
**Do not use for:** a claim that Boğaziçi can achieve the paper's reported efficiency improvement.

## AR-SH-02 — Demand-responsive routing is possible but should not be the default starting point

**Paper:** J. Díaz-Ramírez, C. M. Leal-Garza, Carlos Gómez-Acosta (2022), *Computers & Industrial Engineering* 168, 108101, “A smart school routing and scheduling problem for the new normalcy.”  
Consensus record: https://consensus.app/papers/a-smart-school-routing-and-scheduling-problem-for-the-new-díaz-ramírez-leal-garza/767ff4c146d753159a8b834e3e730a20/?utm_source=chatgpt

The research combines routing/scheduling with student demand input in a university context.

**Agent rule:** at Boğaziçi, do not propose dynamic routing before proving that fixed-route timetable adjustment is insufficient and that operator/legal/service constraints permit dynamic operation.

---

# 5. Decision model for agents

Candidate decision:

```text
frequency(route, time_window)
```

or, only if authority/data allow:

```text
select_departure_times(route, service_day)
```

Later-stage decisions might include vehicle assignment or stop strategy, but those should not be assumed available.

### Candidate inputs

- route;
- day type;
- academic-calendar state;
- class transition intensity by origin/destination campus;
- historical ridership by departure;
- vehicle capacity;
- observed travel time;
- weather only if incremental value is demonstrated;
- event/calendar exceptions;
- app intent only if semantics are verified.

### Candidate loss

```text
loss = crowding_or_left_behind_cost
     + waiting_time_cost
     + operating_run_cost
     + reliability_penalty
     + change_disruption_penalty
```

All coefficients remain policy/workflow parameters until an operator supplies them.

---

# 6. Minimal pilot data contract

```text
service_date
route_id
direction
departure_id
scheduled_departure
actual_departure_optional
actual_arrival_optional
vehicle_id_optional
vehicle_capacity
boarded_count
alighted_count_optional
left_behind_count_optional
queue_estimate_optional
origin_campus
destination_campus
class_transition_index
weather_context_optional
special_event_flag
operator_override
```

For every field capture:

```text
source | owner | available_at | granularity | retention | privacy | quality caveat
```

---

# 7. Baselines before ML

1. Current timetable as-is.
2. Historical mean load by route × weekday × departure.
3. Class-transition weighted demand prior.
4. Simple threshold rule for adding/removing/retiming one run.
5. Optimization under fixed fleet/capacity constraints.
6. Only then predictive or demand-responsive models.

Evaluate:

```text
peak_load_factor
left_behind_rate
waiting_time
on_time_rate
runs_per_passenger
seat_km_utilization_if_data_exist
operator_override_rate
```

Do not optimize aggregate occupancy alone.

---

# 8. PMR falsifiers

Deprioritize if:

- no meaningful peak imbalance exists;
- shuttle schedule changes are externally fixed/contractually inaccessible;
- boarding/ridership cannot be measured at useful granularity;
- the reported system already operates near service-quality ceiling;
- timetable changes would create unacceptable reliability/accessibility risk.

Strengthen if:

- repeatable overcrowded departures exist alongside underused adjacent departures;
- class changes clearly drive demand peaks;
- operator currently adjusts schedules manually using informal heuristics;
- route/departure counts are available historically;
- a bounded timetable experiment is operationally acceptable.

---

# 9. Agent handoffs

## IE

Interview the shuttle operations owner, not students first. Ask for the last overloaded or unusually empty run and how the timetable was changed afterward.

## CS1

Build departure-level baselines and a constraint-aware recommender. Course schedules should be a context feature, never a substitute for ridership ground truth.

## EE / EHB

Do not deploy new passenger counters before checking existing operational logs, ticket/access records, manual counts or vehicle telemetry. If sensing is needed, define privacy-safe aggregate counting first.

## CS2

Safe statement:

> Boğaziçi publicly operates a seven-route-family multi-campus shuttle network with published timetables and BUCampus access. Whether there is a material scheduling inefficiency remains unvalidated and requires departure-level operator evidence.

## Backend

Keep `scheduled_time` and `actual_time`, `capacity` and `boarded`, and `observed` versus `estimated` demand separate.

## Frontend

If validated, operator UI should show “which departure to change, why, expected crowding/reliability trade-off, and confidence,” not just a live bus map.

---

# 10. Source register

- SH-S01 — Boğaziçi Transportation / Park: https://bogazici.edu.tr/tr/pages/ulasim-park/138
- SH-S02 — Shuttle Information System example route: https://mekik.bogazici.edu.tr/route.php?id=12&lang=en
- SH-S03 — BUCampus Transportation: https://bilgiislem.bogazici.edu.tr/tr/pages/ulasim/8597
- SH-S04 — Sustainable Practices Targets: https://kurumsalveri.bogazici.edu.tr/tr/pages/1141-sustainable-practices-targets/1406
- AR-SH-01 — Mahmoudzadeh & Wang (2020), university shuttle scheduling.
- AR-SH-02 — Díaz-Ramírez et al. (2022), university/school demand-responsive routing and scheduling.
