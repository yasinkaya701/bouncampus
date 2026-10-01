# BOUNCAMPUS Hardware Agent Playbook

## Scope

This playbook governs hardware-specific work across two independent roles:

- **EE — Physical Systems & Measurement Lead:** owns measurement truth, calibration, uncertainty and field validity.
- **EHB — Embedded Hardware, Communications & Integration Lead:** owns embedded electronics, PCB, firmware, communications, bring-up and HW↔SW integration.

It supplements `AGENTS.md`, `.agents/FABRIC.md`, `.agents/PLUGIN_POLICY.md`, and both role documents.

Five execution roles do not imply five humans. The same human may staff more than one role with autonomous agents, but ownership boundaries and review rights remain explicit.

## Ownership model

### EE-owned work

1. **Measurement Requirement** — measurand, operational point, range, accuracy, rate, environment and decision relevance.
2. **Measurement Method / Sensor Selection** — whether the physical method can produce valid evidence.
3. **Calibration / Uncertainty** — reference method, error budget, repeatability, drift, hysteresis and acceptance criteria.
4. **Physical Workflow** — placement, operator burden, service identification and measurement SOP.
5. **Field Measurement Verification** — whether the real measurement remains valid in representative operation.

### EHB-owned work

1. **Compute / MCU** — controller, peripherals, timing, memory, watchdog, boot/recovery.
2. **Power / Interface Electronics** — source, conversion, peak/current budget, protection, brownout, controller-side analog/digital interface implementation.
3. **Connectivity** — Wi-Fi/BLE/Ethernet/USB/RS232/CAN/etc., provisioning, offline buffering, retry/idempotency and security boundary.
4. **Firmware** — drivers, state machine, storage, fault handling, observability and update path.
5. **PCB / Interconnect** — schematic, layout constraints, connectors, grounding, test points, DFM/DFT.
6. **Bring-up / Debug** — board checks, test jigs, firmware/hardware debug and recovery-path testing.
7. **HW↔SW Integration** — device protocol, payload implementation, backend/device compatibility and integration verification.

### Shared work

- **EE↔EHB Interface Contract**
- **System-Level Verification**

Parallel agents may execute non-overlapping workstreams. Shared interfaces must be written down before independent implementation diverges.

## Mandatory EE ↔ EHB interface contract

The relevant subset must define:

- sensor/interface electrical requirements;
- voltage/current limits;
- connector/pinout;
- ADC/interface expectations;
- sampling/timing;
- calibration data ownership and persistence;
- protocol;
- packet/event schema;
- units/scaling;
- quality/status/error flags;
- power budget;
- startup/shutdown behavior;
- offline behavior;
- fault states;
- recovery/retry behavior;
- test points;
- validation method.

Cross-boundary changes require EE+EHB dual review. No silent voltage, pinout, sampling, schema, protocol, calibration-persistence, power-budget or fault-semantic change is permitted.

## Branch conventions

### EE measurement work

Base branch:

`role/ee-physical-systems`

Suggested lanes:

- `agent/hw-measurement/<task>`
- `agent/hw-sensors/<task>`
- `agent/hw-calibration/<task>`
- `agent/hw-field-verification/<task>`

### EHB embedded/integration work

Base branch:

`role/ehb-embedded-integration`

Suggested lanes:

- `agent/ehb-hardware/<task>`
- `agent/ehb-firmware/<task>`
- `agent/ehb-comms/<task>`
- `agent/ehb-integration/<task>`
- `agent/ehb-verification/<task>`

Use the existing `agent/<lane>/<task>` pattern. Do not create overlapping branches that both own the same schematic, board, firmware module, interface contract, measurement SOP or BOM artifact.

## Required design artifacts

A serious hardware proposal should produce only the subset relevant to its maturity/risk:

- measurement requirement table;
- block/interface diagram;
- schematic or schematic-level notes;
- power tree/current budget;
- measurement error/uncertainty budget;
- firmware state machine;
- communication/data contract;
- BOM with exact part numbers where known;
- alternates for risky parts;
- test-point/debug strategy;
- calibration procedure;
- verification plan and acceptance criteria;
- failure-mode table;
- assembly/installation notes;
- DFM/DFT checklist when manufacturing is in scope;
- evidence table separating assumed, simulated, bench and field values.

Do not create artifacts for visual completeness. Each artifact must support a decision, implementation, verification, sourcing or integration need.

## Schematic and PCB requirements — EHB

When a custom PCB is justified, EHB should verify as applicable:

- input ranges and absolute maximum ratings;
- regulator headroom and transient/peak current;
- decoupling placement intent;
- reverse-polarity/overcurrent/ESD protection;
- ADC/reference/excitation assumptions agreed with EE;
- grounding and return-current paths;
- analog vs switching/noisy-domain separation;
- connector current/voltage ratings;
- programming/debug interface;
- boot-strapping pins and reset behavior;
- test points for rails and critical signals;
- unused pin treatment;
- pull-up/pull-down requirements;
- external component tolerances;
- thermal assumptions;
- creepage/clearance where relevant;
- BOM availability/package manufacturability;
- ERC/DRC or equivalent checks when CAD tooling is available.

A rendered PCB image is not a verification artifact by itself.

## Power design gate — EHB

Any powered design should have an explicit power budget before it is described as deployable.

Record as relevant:

- input source/range;
- nominal and worst-case rail currents;
- startup/peak loads;
- conversion-efficiency assumptions;
- regulator thermal assumptions;
- brownout behavior;
- protection strategy;
- expected runtime if battery powered;
- behavior after power loss/restoration.

Unknowns remain `ASSUMPTION` until calculation/test resolves them.

## Firmware quality gate — EHB

Firmware controlling evidence collection should have:

- deterministic state flow;
- explicit invalid/error states;
- watchdog/recovery strategy where relevant;
- calibration values stored/versioned safely according to the EE↔EHB contract;
- offline queue/buffering when network loss is possible;
- idempotent upload/event identity when retries are possible;
- timestamp/order behavior;
- diagnostics for bench/field debugging;
- no silent coercion of invalid sensor data into plausible values;
- reproducible build instructions.

## Communications quality gate — EHB

For connected devices define as applicable:

- provisioning;
- connection-loss behavior;
- queue persistence/depth;
- retry/backoff;
- duplicate/idempotency behavior;
- clock/timestamp source;
- ordering guarantees;
- payload/schema versioning;
- quality/error/status representation;
- restart/power-loss recovery.

A device reaching an API endpoint is not integrated if payload semantics are ambiguous downstream.

## Measurement and calibration gate — EE

No sensor is "accurate" because its datasheet says so.

For measurement-critical hardware, EE defines:

- measurand and unit;
- operational range;
- reference instrument/method;
- calibration points;
- zero/tare procedure;
- repeatability test;
- hysteresis test where relevant;
- drift test where relevant;
- environmental sensitivity where relevant;
- invalid-reading rules;
- acceptance criterion tied to the operational decision.

Raw measurements and test conditions should be retained. Do not report only a final percentage without provenance.

## EHB ↔ CS1 data contract

EHB and CS1 must align on:

- event/data schema;
- timestamps and ordering;
- missing/invalid readings;
- quality flags;
- device metadata;
- duplicate handling;
- offline replay;
- API expectations that affect firmware behavior.

EHB owns reliable transport/device semantics; CS1 owns decision/model semantics.

## Evidence maturity labels

Use these labels in hardware reports and PRs:

- `ASSUMPTION` — not yet verified.
- `DATASHEET` — supported by manufacturer/source documentation.
- `CALCULATION` — engineering calculation with stated inputs.
- `SIMULATION` — circuit/mechanical/software simulation only.
- `BENCH_TEST` — physically measured prototype/board/device under recorded conditions.
- `FIELD_TEST` — measured in intended or representative operation.
- `PRODUCTION_EVIDENCE` — verified on manufactured/release hardware with a defined process.

Never promote a claim to a higher label without corresponding evidence.

## Physical safety and irreversible actions

The repository's `PHYSICAL_SAFETY` and `IRREVERSIBLE_ACTION` human gates remain mandatory.

Agents may autonomously design circuits, write firmware, run simulations, review PCB files, create BOMs, prepare test procedures, calculate power/thermal limits, and design non-energized fixtures.

Human approval/supervision is required before actions that can create real physical risk, including mains/high-voltage energization, unsafe battery handling/charging, high-current fault testing, hazardous actuator motion, destructive testing, or field installation affecting real operations.

## BOM and sourcing discipline — primarily EHB

BOM entries should prefer exact manufacturer part numbers. For material parts record where useful manufacturer, MPN, function, package, critical rating, estimated unit cost/quantity basis, source/date, availability/lifecycle risk, and substitution constraints.

Do not claim a prototype or production cost without stating important excluded items.

## Plugin/tool policy

Use `.agents/PLUGIN_POLICY.md`.

Relevant specialized capabilities include schematic/PCB CAD, SPICE, component/datasheet lookup, BOM sourcing/lifecycle checks, firmware build/debug, mechanical CAD, signal/power-integrity review, remote instruments/bench access, manufacturing/DFM and technical literature.

Optional capability absence does not justify fabricated results. Continue with the strongest safe fallback and record what remains unverified.

## Hardware PR merge checklist

- [ ] Primary owner is correctly identified as EE or EHB.
- [ ] Measurement requirement is stated where the hardware affects measurement.
- [ ] Architecture is compared with simpler alternatives.
- [ ] EE↔EHB interface contract is explicit when both domains are affected.
- [ ] Cross-boundary changes received dual review.
- [ ] Power assumptions are explicit where powered electronics are involved.
- [ ] Safety risks are identified.
- [ ] BOM parts/ratings are not invented.
- [ ] Datasheet-derived claims have provenance.
- [ ] Simulation is not presented as bench evidence.
- [ ] Bench evidence includes setup/test conditions when present.
- [ ] Firmware failure/recovery behavior is defined when relevant.
- [ ] Calibration/invalid-reading handling is defined by EE when measurement-critical.
- [ ] EHB↔CS1 API/data impacts are documented when relevant.
- [ ] Known unverified assumptions are listed.

## Exit criterion

A hardware workstream is complete only when its intended artifact/evidence is merged through the correct EE or EHB role path to verified `master`, or when a genuine hard blocker is recorded.

"Designed", "simulated", "PCB rendered", "firmware compiles", and "BOM drafted" are intermediate states unless they satisfy the explicitly scoped acceptance criteria.
