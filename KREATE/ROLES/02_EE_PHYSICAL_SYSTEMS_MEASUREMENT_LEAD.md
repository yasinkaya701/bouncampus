# EE — Physical Systems & Measurement Lead

## Mission

Turn BOUNCAMPUS from a software-only hypothesis into a credible physical measurement and pilot system. The EE role proves whether the product can observe the real world accurately enough to support a defensible intervention.

The goal is **not** to build hardware for visual impact. Hardware exists only if it closes a measurement gap discovered through PMR or improves pilot credibility.

**Application deadline:** 8 October 2026, 23:59  
**Primary optimization target:** measurement credibility and deployability.

---

## Core question

> Can we measure the operational outcome reliably, cheaply, and with low enough friction that a real institutional kitchen could run a pilot?

---

## Scope

### P0 — Must be completed before application freeze

1. Measurement requirements derived from PMR.
2. Physical measurement architecture.
3. Smart-waste-node feasibility.
4. BOM and component alternatives.
5. Calibration/test methodology.
6. Hardware-to-software data contract with CS1/CS2.
7. Pilot instrumentation plan.
8. Failure modes, safety boundaries, and operational constraints.

### P1 — Allowed experiments

- ESP32 + load cell + HX711 prototype.
- Tare / filtering / local status indication.
- Wi-Fi data transmission.
- Offline buffering.
- OLED or simple operator interaction.
- Portion/service counting experiments.
- ToF/IR sensing.
- NFC/RFID service or operator tagging.
- Environmental sensing if PMR demonstrates relevance.

### Out of scope unless evidence changes priorities

- Custom PCB before breadboard evidence.
- Complex enclosure work before measurement validity.
- Computer vision waste classification merely because it looks advanced.
- Sensors with no validated operational use.
- Claims of production readiness from a bench prototype.

---

## Shared PMR responsibility

EE is expected to lead approximately **4 interviews** as part of the team's target of 16 distinct interviews.

Priority interview targets:

- Food engineers
- Kitchen managers
- Kitchen staff
- Catering technical/operations staff
- Waste-measurement owners
- POS / scale / facilities data owners

Questions should focus on physical reality:

- What is actually weighed today?
- At what point in the workflow?
- By whom?
- How often is measurement skipped?
- What containers are used?
- Is tare known?
- What categories matter?
- What precision is useful operationally?
- Would a scale create hygiene, safety, cleaning, or workflow problems?
- Is Wi-Fi available where measurement occurs?
- What happens during connectivity loss?

Do not pitch the smart node before understanding the current workflow.

---

## Workstreams

### 1. Measurement requirements

Translate PMR into explicit requirements.

Example fields:

- Measurement type
- Range
- Desired resolution
- Desired repeatability
- Measurement frequency
- User interaction
- Cleaning requirement
- Power availability
- Connectivity
- Installation constraints
- Food-safety boundary
- Failure behavior

### Acceptance gate

A requirement must have either:

- PMR evidence,
- technical necessity,
- regulatory/safety necessity,
- or a clearly labeled hypothesis.

Do not invent arbitrary engineering specifications and present them as customer needs.

---

### 2. First hardware hypothesis — Smart Waste Measurement Node

Default experiment:

`load cell -> HX711 -> ESP32 -> Wi-Fi/offline buffer -> BOUNCAMPUS measurement API`

Potential measurement categories:

- Edible surplus
- Preparation waste
- Plate waste
- Other operator-defined category

The exact categories must be reconciled with PMR and pilot design.

### Required data fields

```json
{
  "station_id": "BOUN-NH-01",
  "service_id": "2026-10-03-lunch",
  "measurement_type": "edible_surplus",
  "value": 4.82,
  "unit": "kg",
  "timestamp": "...",
  "quality": "VALID"
}
```

CS1/CS2 may evolve the contract, but hardware firmware must not silently invent missing context.

---

### 3. BOM and fallback design

Document:

- Primary component
- Function
- Why selected
- Expected limitation
- Alternative/fallback
- Whether already available

Initial likely BOM:

- ESP32
- Load cell appropriate to target range
- HX711 or equivalent ADC/amplifier
- Stable power source
- Tare/input button
- Status LED
- Breadboard / wiring

Optional only after core measurement works:

- OLED
- Enclosure
- Local storage
- Second sensor modality

### Acceptance gate

Every optional component must answer:

> What failure, workflow need, or measurement-quality problem does this component solve?

If the answer is mainly "it looks better," defer it.

---

### 4. Calibration protocol

A prototype is not evidence until calibrated.

Minimum test set should cover several known reference masses spanning the useful range.

Record:

- Reference mass
- Measured mass
- Absolute error
- Relative error
- Repeated readings
- Standard deviation or spread
- Drift over time
- Tare behavior

Recommended test sequence:

1. Warm-up / stabilization.
2. Tare.
3. At least 3 distinct reference masses.
4. At least 10 repeated readings at selected masses.
5. Remove/reapply load to test repeatability.
6. Re-tare and repeat.
7. Record environmental/bench conditions relevant to anomalies.

### Acceptance gate

PASS only when:

- Calibration coefficient is documented.
- Repeatability is quantified.
- Known limitations are visible.
- Raw test evidence is retained.

A single successful reading is FAIL.

---

### 5. Firmware behavior

Minimum firmware behavior for a P1 integrated prototype:

- Boot self-state.
- Sensor initialization.
- Tare.
- Stable weight reading.
- Filtering without hiding instability.
- Measurement confirmation.
- Connectivity state.
- API POST.
- Retry/backoff or explicit failure.
- No fabricated successful transmission.

### Failure handling

Explicitly test:

- Sensor disconnected.
- Wi-Fi unavailable.
- Backend unavailable.
- Malformed server response.
- Sudden load changes.
- Negative/invalid reading.
- Reboot during measurement.

The device must expose uncertainty/failure rather than silently report a plausible number.

---

### 6. Pilot instrumentation plan

Work with IE and CS1 to define how a real pilot could capture:

- Produced quantity
- Served quantity
- Edible surplus
- Waste mass
- Early sell-out
- Operator override
- Service context
- Measurement completeness

Not all signals need custom hardware. Manual entry, POS export, or existing scales may be better.

### Acceptance gate

The instrumentation plan must minimize operator burden. A scientifically elegant plan that a kitchen will not follow is FAIL.

---

## Hardware experiment rule

P1 hardware experiments must be time-boxed and falsifiable.

Before starting, create or reference an experiment entry containing:

- Question
- Hypothesis
- Why it matters
- Method
- Success condition
- Failure condition
- Time budget
- Result
- KEEP / MODIFY / KILL

Do not spend multiple days rescuing a low-value hardware feature without new evidence.

---

## Cross-team handoffs

### From IE

Need:

- Measurement workflow.
- Operator constraints.
- Existing tools/scales.
- Required categories.
- Pilot acceptance conditions.

### To CS1

Provide:

- Measurement schema.
- Error characteristics.
- Quality flags.
- Missing-data behavior.
- Calibration evidence.

### To CS2

Provide:

- What hardware proves.
- What remains unproven.
- Deployment constraints.
- Evidence that hardware is or is not necessary.
- Technical feasibility paragraph for application synthesis.

---

## Anti-AI-slop rules

Automatic FAIL if:

- A CAD render is presented as a working prototype.
- A BOM implies purchased/available components that the team does not have.
- Accuracy is claimed without calibration evidence.
- "IoT-enabled" is used as a value proposition by itself.
- A sensor is added with no PMR or technical rationale.
- A simulated payload is presented as physical telemetry.
- A breadboard is described as production-ready.
- Unsupported safety, hygiene, or compliance claims are made.

---

## Definition of Done — 8 October

The EE role is DONE only if:

- [ ] EE led roughly 4 relevant PMR interviews, unless team coverage justified redistribution.
- [ ] Measurement requirements are linked to PMR/technical evidence.
- [ ] Smart-node architecture is documented.
- [ ] BOM and fallbacks are documented.
- [ ] Calibration methodology exists.
- [ ] If hardware is available, real bench evidence is recorded; if unavailable, feasibility is clearly separated from implementation.
- [ ] Hardware/software data contract is agreed with CS1/CS2.
- [ ] Pilot instrumentation plan exists.
- [ ] Major failure modes are documented.
- [ ] Hardware is explicitly KEEP / MODIFY / KILL based on evidence.
- [ ] No prototype capability is overstated in the application.

---

## Success standard

The best outcome is not necessarily "we built a device."

The best outcome is:

> We know exactly what must be measured, why it matters, how reliably we can measure it, how it fits the kitchen workflow, and whether custom hardware is actually justified.
