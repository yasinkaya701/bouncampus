# Boğaziçi Classroom Allocation & Occupancy — Agent Research Pack

**Research date:** 2026-10-01  
**Purpose:** Give IE/CS1/CS2/backend/frontend agents a source-grounded map of the classroom-allocation decision surface, without pretending that public schedules prove a utilization problem.  
**Status:** Secondary/public-source research only. **NOT PMR. NOT internal room-utilization data. NOT measured BOUNCAMPUS impact.**

---

# 0. Agent-critical conclusion

The classroom opportunity is materially more concrete than a generic “smart building” idea because public sources identify:

1. a named institutional owner for general-use classroom scheduling;
2. a published inventory of classroom counts and capacity bands;
3. public course schedule surfaces exposing course time/place assignments;
4. a well-established optimization problem in the academic literature.

But the core pain remains **unverified**. Public data does not establish that Boğaziçi currently suffers from material room-capacity waste, room shortages, excessive inter-campus travel, bad room-type matching or costly rescheduling.

The correct product hypothesis is therefore:

> Can a human-reviewed room-allocation recommender improve capacity fit and movement cost while preserving all academic hard constraints and existing scheduling authority?

Do **not** jump directly to autonomous timetable generation.

---

# 1. Claim firewall

- A public classroom inventory proves capacity supply, not poor utilization.
- A public course schedule proves an assignment exists, not that the assignment is suboptimal.
- A room capacity band is not actual attendance.
- Course quota is not attendance.
- Wi-Fi client count is not automatically occupancy.
- An optimization result from another university is a design reference, not evidence of Boğaziçi savings.
- Do not claim “X% classroom capacity is wasted” without room-level enrollment/attendance and assignment data.
- Do not infer live occupancy from scheduled course presence.

---

# 2. Public decision owner and workflow surface

## CR-S01 — Scheduling owner is publicly identified

**Source:** Boğaziçi University Student Affairs / Registrar — “Derslikler Hakkında”  
https://oidb.bogazici.edu.tr/tr/pages/derslikler-hakkinda/4422

The page states that scheduling of **general-use classrooms** is performed by the **Kayıt İşleri Şube Müdürlüğü** (Registration Branch Directorate). It separately states that reservations of university halls outside course scheduling are managed by the **Corporate Communications Office**.

### What this supports

- classroom/course scheduling is an administratively owned decision surface;
- “course room assignment” and “event/hall reservation” are separate workflows and should not be conflated;
- the Registration Branch is a high-value PMR owner for constraints, timing, overrides and data semantics.

### What remains unknown

- which staff member performs the actual assignment;
- which system/tool is used;
- whether optimization software already exists;
- when rooms are frozen and how often changes occur;
- what constraints are hard vs preference-based;
- whether room type/equipment/accessibility requirements are machine-readable;
- whether historical assignment revisions and exceptions are retained.

### PMR questions

1. Walk through the most recent semester’s room-allocation process from department course request to published schedule.
2. Which constraints are non-negotiable: capacity, room type, campus, equipment, accessibility, instructor availability, student conflicts?
3. Which decisions are still made manually?
4. What causes the most rework after the first schedule is produced?
5. When does room assignment become costly to change?
6. Which objective is hardest today: feasibility, capacity fit, instructor preference, student movement, special room needs, or late changes?
7. Which fields are exportable from BUIS/ÖBİKAS or the course-schedule system?

---

# 3. Public classroom inventory

## CR-S02 — 2025 inventory exposes a highly heterogeneous capacity distribution

**Source:** Boğaziçi University, *Sayılarla Boğaziçi Üniversitesi / Facts and Figures*, Table 81 “Classrooms by Location and Capacity, 2025”  
https://sayilarla.bogazici.edu.tr/document

The table reports **161 general-use classrooms** across the listed buildings, distributed by capacity band as follows:

| Capacity band | General-use classrooms |
| --- | ---: |
| 0–25 | 7 |
| 26–50 | 96 |
| 51–75 | 26 |
| 76–100 | 16 |
| 101–150 | 8 |
| 151–200 | 8 |
| **Total** | **161** |

Selected building-level counts from the same table include:

| Building | Total classrooms | Public capacity structure signal |
| --- | ---: | --- |
| Anadolu Hisarı YADYOK Building | 76 | dominated by 26–50 capacity rooms |
| North Campus New Hall Building | 19 | 13 rooms in 76–100 band, 6 rooms in 151–200 band |
| Education Faculty Building | 18 | mixed 26–50 / 51–75 / 76–100 / 101–150 |
| South Campus Engineering Building | 16 | mostly 51–75 rooms |
| North Park Building | 9 | mostly 26–75 rooms |
| Natuk Birkan Building | 6 | mostly 26–50 rooms |

### Research implication

The decision is not simply “choose a free room.” Capacity bands and building location create a legitimate **matching** problem.

Candidate decision representation:

```text
assign(section, time_slot) -> room
```

subject to hard constraints and scored by multiple soft objectives.

### Safe candidate objectives

These are **design hypotheses**, not known Boğaziçi priorities:

- minimize seat-capacity slack;
- minimize room-capacity violations;
- minimize room-type mismatch;
- minimize room changes for the same section;
- minimize long student/instructor transitions between consecutive classes;
- minimize inter-campus movement where avoidable;
- preserve accessibility/equipment requirements;
- preserve protected teaching slots and institutional rules.

---

# 4. Public schedule and registration signals

## CR-S03 — Course place/time assignments are publicly surfaced

The Registrar page directs users to the university course-schedule surface for semester course place and time assignments:

http://registration.bogazici.edu.tr/

This supports the existence of a public **assignment output**. It does not prove that all underlying scheduling inputs or constraints are public.

## CR-S04 — Registration systems expose quota/consent concepts, but quota is not occupancy

The 2026 Summer School registration guidance documents course quota states and instructor-consent workflow. It also states that students add approved courses themselves and that course registration remains subject to system deadlines.

Source:  
https://summer.bogazici.edu.tr/?q=tr%2Fnode%2F9164

The 2026 summer course-opening guidance also publishes explicit course slots and warns that splitting slots can affect student numbers.

Source:  
https://summer.bogazici.edu.tr/?q=tr%2Fnode%2F180

### Agent warning

Summer-school rules are useful as a **process precedent**, not proof that regular-semester scheduling uses identical rules.

Do not treat:

```text
quota == enrollment == attendance == occupancy
```

Those are different states.

A robust data contract should keep them separate:

```text
course_quota
registered_students
active_enrollment_at_census
scheduled_capacity
observed_attendance
estimated_occupancy
```

---

# 5. Academic design references

## AR-CR-01 — Multiobjective room allocation is a real operational research problem

**Paper:** Antunes-Batista, Atta, Basto-Fernandes, Yevseyeva & Emmerich (2026), *Multiobjective Optimization Approaches for Room Allocation in University Course Timetabling*.  
Consensus record: https://consensus.app/papers/multiobjective-optimization-approaches-for-room-antunes-batista-atta/c030fabfafb357a797367c6733a37aa3/?utm_source=chatgpt

The study frames room allocation with hard feasibility constraints and multiple objectives including capacity waste, room-type mismatch, student relocation between buildings and room changes.

**Use for:** objective design and baseline selection.  
**Do not use for:** claims about Boğaziçi’s current process or savings.

## AR-CR-02 — Timetables can be evaluated as mobility policies

**Paper:** Keshu Wu, Xinyue Ye, Suphanut Jamonnak, Xin Feng (2025), *Transactions in GIS*, “Human Mobility Reimagined: Digital Twin Intelligence for Adaptive Campus Course Timetabling.”  
Consensus record: https://consensus.app/papers/human-mobility-reimagined-digital-twin-intelligence-for-wu-ye/56c56c329b7d5c02abd2c90f44bd5167/?utm_source=chatgpt

The paper evaluates timetable recommendations using classroom occupancy, travel distance, travel time and vertical transitions.

**Agent implication:** if Boğaziçi PMR confirms room-allocation pain, course scheduling can connect naturally to the shuttle/mobility module through **transition demand**, not through a decorative digital twin.

## AR-CR-03 — Wi-Fi occupancy inference requires calibration

**Paper:** Iresha Pasquel Mohottige, H. Gharakheili, T. Moors, V. Sivaraman (2021), *IEEE Sensors Journal* 22, 9981–9996, “Modeling Classroom Occupancy Using Data of WiFi Infrastructure in a University Campus.”  
Consensus record: https://consensus.app/papers/modeling-classroom-occupancy-using-data-of-wifi-mohottige-gharakheili/22967457baa556c49b5f2fe53fa9ca6e/?utm_source=chatgpt

The paper explicitly warns that raw connected-device counts in dense campuses are polluted by adjoining rooms, outdoor areas and network load balancing; it models occupancy only after mapping/calibration.

### EE / CS1 rule

If Wi-Fi metadata is ever proposed as a low-cost occupancy signal:

- do not equate AP client count with room occupancy;
- document AP-to-room mapping confidence;
- calibrate against a physical/manual ground truth sample;
- aggregate for privacy;
- use `ESTIMATED_OCCUPANCY`, never `MEASURED_ATTENDANCE`, unless the measurement method actually supports that claim.

---

# 6. Minimal data contract for a classroom pilot

The smallest useful table should distinguish assignment, demand and observed use:

```text
term
course_code
section_id
meeting_id
date_or_week_pattern
time_slot
assigned_room
building
campus
room_capacity
room_type_requirements
registered_students
course_quota
instructor_constraints
special_equipment_requirements
accessibility_requirements
assignment_version
assignment_changed_at
change_reason
observed_attendance_optional
occupancy_source_optional
```

For each field record:

```text
owner | source system | availability time | retention | privacy class | known quality issue
```

---

# 7. Baselines before complex optimization

CS1 should not begin with an end-to-end AI scheduler.

Recommended sequence if data access is granted:

1. **Current assignment replay** — reproduce the published assignment without optimization.
2. **Feasibility validator** — detect capacity/time/room-type violations.
3. **Greedy best-fit baseline** — smallest feasible room by capacity.
4. **Integer programming baseline** — hard constraints + one or two transparent objectives.
5. **Multiobjective recommendation** — only after owner weights and trade-offs are learned.
6. **Adaptive/rescheduling layer** — only after late-change incidents are documented.

### Candidate evaluation metrics

```text
hard_constraint_violations
seat_slack
room_type_mismatch_count
cross_building_transition_distance
cross_campus_transition_count
late_reassignment_count
manual_override_rate
scheduler_time_saved
```

Do not optimize “occupancy rate” in isolation; a room can be intentionally underfilled for pedagogy, equipment, accessibility or conflict reasons.

---

# 8. PMR falsifiers

Deprioritize this module if interviews show:

- current room allocation is already near-automatic and low-friction;
- most apparent capacity slack is caused by non-capacity constraints that cannot be encoded/accessed;
- room assignment is not a meaningful operational burden;
- there is no permission to access section-level assignment/enrollment data;
- changing assignments creates unacceptable student/instructor disruption;
- the dominant pain is course-time generation rather than room allocation, requiring a different problem definition.

Strengthen this module if repeated incidents show:

- substantial manual rework;
- repeated room-capacity mismatch;
- frequent late room changes;
- hard-to-manage equipment/accessibility constraints;
- avoidable long transitions between buildings/campuses;
- a clear owner willing to review ranked recommendations.

---

# 9. Agent handoffs

## IE

Interview **Kayıt İşleri Şube Müdürlüğü** before generic students. Ask for the last scheduling cycle, the hardest exception and the real objective hierarchy.

## CS1

Build a constraint model, not a generative chatbot. Start with feasibility + greedy/ILP baselines.

## EE / data

Treat occupancy sensing as optional. First determine whether registration/attendance/room-change data already answer the decision. If sensing is needed, calibrate and preserve measurement semantics.

## CS2

Safe narrative:

> Boğaziçi publicly identifies a central owner for general-use classroom scheduling and publishes a 161-room general-use inventory with heterogeneous capacities. Whether room allocation is sufficiently painful or inefficient to justify a product module remains a PMR question.

## Backend

Keep schedule `version`, `effective_at`, `source`, `owner`, `room_capacity`, `registered_count` and any occupancy estimate provenance separate.

## Frontend

If validated, show **ranked room-assignment alternatives with constraint explanations**, not a generic heatmap. The operator needs “why this room / what trade-off / what breaks if changed.”

---

# 10. Source register

- CR-S01 — Boğaziçi Student Affairs, Classroom Information: https://oidb.bogazici.edu.tr/tr/pages/derslikler-hakkinda/4422
- CR-S02 — Boğaziçi Facts and Figures, Table 81, 2025 classroom inventory: https://sayilarla.bogazici.edu.tr/document
- CR-S03 — Course Schedule surface: http://registration.bogazici.edu.tr/
- CR-S04 — 2026 Summer School registration / quota process: https://summer.bogazici.edu.tr/?q=tr%2Fnode%2F9164
- CR-S05 — 2026 Summer School course-opening / slot guidance: https://summer.bogazici.edu.tr/?q=tr%2Fnode%2F180
- AR-CR-01 — Antunes-Batista et al. (2026), room-allocation multiobjective optimization.
- AR-CR-02 — Wu et al. (2025), adaptive campus timetabling / mobility.
- AR-CR-03 — Mohottige et al. (2021), Wi-Fi classroom occupancy modeling.
