# BOUNCAMPUS Hardware Agent Playbook

## Scope

This playbook governs hardware-specific work owned primarily by **EE — Physical Systems & Measurement Lead**. It supplements `AGENTS.md`, `.agents/FABRIC.md`, `.agents/PLUGIN_POLICY.md`, and the EE role document.

The hardware agent is responsible for turning a measurement need into a testable physical-system architecture without presenting simulations, CAD, or unbuilt designs as field evidence.

## Hardware workstreams

Hardware work should be decomposed into explicit, independently reviewable workstreams when possible:

1. **Measurement Requirement** — what physical variable must be measured, at what accuracy, rate, environment, and operational point.
2. **Sensor / Analog Front End** — sensor technology, excitation, amplification, filtering, ADC/interface, protection, calibration strategy.
3. **Power** — source, conversion, peak/current budget, brownout behavior, protection, thermal margin, battery/runtime if applicable.
4. **Compute / MCU** — controller selection, peripheral budget, timing, memory, watchdog, boot/recovery behavior.
5. **Connectivity** — Wi-Fi/BLE/Ethernet/etc., provisioning, offline buffering, retry/idempotency, security boundary.
6. **Firmware** — drivers, calibration, event state machine, storage, fault handling, observability, update path.
7. **PCB / Interconnect** — schematic, layout constraints, connectors, grounding, analog/digital separation, test points, manufacturability.
8. **Mechanical / Enclosure** — installation, ingress/cleaning constraints, strain relief, mounting, operator interaction, serviceability.
9. **Calibration / Test** — reference method, acceptance criteria, repeatability, drift, failure injection, traceability.
10. **Integration Contract** — event schema, timestamps, quality states, device identity, backend/API behavior.
11. **BOM / Sourcing** — part identity, alternates, lifecycle/availability, unit assumptions, cost provenance.
12. **Pilot Deployment** — installation SOP, safety, staff burden, field failure recovery, evidence collection.

Parallel agents may execute non-overlapping workstreams. Shared interfaces must be written down before independent implementation diverges.

## Hardware branch conventions

Hardware work under the EE role should normally branch from:

`role/ee-physical-systems`

Suggested task lanes:

- `agent/hw-measurement/<task>`
- `agent/hw-sensors/<task>`
- `agent/hw-power/<task>`
- `agent/hw-firmware/<task>`
- `agent/hw-pcb/<task>`
- `agent/hw-mechanical/<task>`
- `agent/hw-calibration/<task>`
- `agent/hw-verification/<task>`

Use the existing `agent/<lane>/<task>` pattern. Do not create overlapping hardware branches that both own the same schematic, board, firmware module, interface contract, or BOM artifact.

## Required design artifacts

A serious hardware proposal should produce the subset of these artifacts relevant to its maturity:

- requirement table with operational rationale;
- block diagram;
- interface/control-flow diagram;
- schematic or schematic-level design notes;
- power tree and power/current budget;
- sensor error/uncertainty budget;
- firmware state machine;
- communication/data contract;
- BOM with exact part numbers where known;
- alternates for single-source or risky parts;
- test-point / debug strategy;
- calibration procedure;
- test plan and acceptance criteria;
- failure-mode table;
- assembly/installation notes;
- DFM/DFT checklist if PCB/manufacturing work exists;
- evidence table separating simulated, bench, field, and assumed values.

Do not create artifacts only for visual completeness. Each artifact must support a decision, implementation, verification, sourcing, or integration need.

## Schematic and PCB requirements

When a custom PCB is justified, agents should verify as applicable:

- input ranges and absolute maximum ratings;
- regulator headroom and transient/peak current;
- decoupling placement intent;
- reverse-polarity / overcurrent / ESD protection where relevant;
- ADC/reference/excitation assumptions;
- grounding and return-current paths;
- analog vs switching/noisy-domain separation;
- connector current/voltage ratings;
- programming/debug interface;
- boot-strapping pins and reset behavior;
- test points for rails and critical signals;
- unused pin treatment;
- pull-up/pull-down requirements;
- external component tolerances;
- thermal dissipation assumptions;
- creepage/clearance where voltage requires it;
- BOM availability and package manufacturability;
- ERC/DRC or equivalent checks when CAD tooling is available.

A rendered PCB image is not a verification artifact by itself.

## Power design gate

Any powered design should have an explicit power budget before it is described as deployable.

At minimum record:

- input source/range;
- nominal and worst-case rail currents;
- startup/peak loads;
- conversion efficiency assumptions;
- regulator thermal assumptions;
- brownout behavior;
- protection strategy;
- expected runtime if battery powered;
- behavior after power loss/restoration.

If these are unknown, label them as assumptions and create tests or calculations to resolve them.

## Firmware quality gate

Firmware should be treated as production logic even for prototypes when it controls evidence collection.

Minimum expectations where applicable:

- deterministic measurement/state flow;
- explicit invalid/error states;
- watchdog or recovery strategy for unattended operation;
- debouncing/filtering where relevant;
- calibration values stored/versioned safely;
- offline queue/buffering when network loss is possible;
- idempotent upload/event identity when retries are possible;
- monotonic/event timestamps where ordering matters;
- diagnostics suitable for bench and field debugging;
- no silent coercion of invalid sensor data into plausible values;
- reproducible build instructions.

## Measurement and calibration gate

No sensor is "accurate" because its datasheet says so.

For measurement-critical hardware, define:

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

Report raw measurements and test conditions. Do not report only a final percentage without provenance.

## Evidence maturity labels

Use these labels in hardware reports and PRs:

- `ASSUMPTION` — not yet verified.
- `DATASHEET` — supported by manufacturer/source documentation.
- `CALCULATION` — engineering calculation with stated inputs.
- `SIMULATION` — circuit/mechanical/software simulation only.
- `BENCH_TEST` — physically measured prototype/board/device under recorded conditions.
- `FIELD_TEST` — measured in the intended or representative operating environment.
- `PRODUCTION_EVIDENCE` — verified on manufactured/release hardware with defined test process.

Never promote a claim to a higher label without corresponding evidence.

## Physical safety and irreversible actions

The repository's `PHYSICAL_SAFETY` and `IRREVERSIBLE_ACTION` human gates remain mandatory.

Agents may autonomously:

- design circuits;
- write firmware;
- run simulations;
- review PCB files;
- create BOMs;
- prepare test procedures;
- calculate power/thermal limits;
- design non-energized fixtures.

Human approval/supervision is required before actions that can create real physical risk, including as applicable:

- mains/high-voltage energization;
- unsafe battery handling or charging experiments;
- high-current fault testing;
- actuator motion that can injure people or damage equipment;
- destructive testing;
- field installation affecting real operations;
- hazardous thermal/chemical/mechanical processes.

Do not weaken a safety gate because a deadline is close.

## BOM and sourcing discipline

BOM entries should prefer exact manufacturer part numbers rather than generic descriptions.

For material parts, record where useful:

- manufacturer;
- manufacturer part number;
- function;
- package;
- critical rating;
- estimated unit cost and quantity basis;
- source/date for price observation;
- availability/lifecycle risk;
- approved alternate or substitution constraints.

Do not claim a prototype or production cost without stating excluded items such as PCB fabrication, assembly, enclosure, connectors, shipping, tax, tooling, calibration labor, or test equipment when they are not included.

## Plugin/tool policy for hardware agents

Hardware agents should use `.agents/PLUGIN_POLICY.md`.

They are encouraged to use available specialized plugins or tools for:

- schematic and PCB CAD;
- SPICE/circuit simulation;
- component/datasheet lookup;
- BOM sourcing/lifecycle checks;
- firmware build/debug;
- mechanical CAD;
- signal/power-integrity review;
- remote instruments/bench access;
- manufacturing/DFM checks;
- technical literature.

If a useful specialized capability is not available, the agent may explicitly ask the user to install/connect/authorize an appropriate plugin. The request should name the missing capability rather than inventing a plugin name unless that plugin has actually been discovered.

When a plugin is optional, continue with the best available fallback and record what remains unverified. When the plugin is necessary to satisfy acceptance criteria, document the exact blocker.

## Hardware PR merge checklist

In addition to normal repository CI, a hardware PR should answer the relevant items below:

- [ ] Measurement requirement is stated.
- [ ] Architecture choice is compared against simpler alternatives.
- [ ] Exact interfaces/contracts are documented.
- [ ] Power assumptions are explicit.
- [ ] Safety risks are identified.
- [ ] BOM parts/ratings are not invented.
- [ ] Datasheet-derived claims have source provenance.
- [ ] Simulation is not presented as bench evidence.
- [ ] Bench evidence includes setup/test conditions when present.
- [ ] Firmware failure/recovery behavior is defined.
- [ ] Calibration and invalid-reading handling are defined when measurement-critical.
- [ ] Cross-role API/data impacts are documented.
- [ ] Known unverified assumptions are listed.
- [ ] A missing useful plugin/tool capability is requested from the user when it would materially improve verification.

## Exit criterion

A hardware workstream is complete only when its intended artifact and evidence are merged through the EE role path to verified `master`, or when a genuine hard blocker is recorded.

"Designed", "simulated", "PCB rendered", "firmware compiles", and "BOM drafted" are intermediate states unless they satisfy the explicitly scoped acceptance criteria.
