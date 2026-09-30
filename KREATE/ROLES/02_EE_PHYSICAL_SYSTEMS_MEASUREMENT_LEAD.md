# EE — Physical Systems & Measurement Lead

## Mission

Own the persistent `HUMAN-EE` workstream and answer:

> **Can BOUNCAMPUS observe the physical world reliably enough to support better operational decisions, and what is the simplest defensible way to do that?**

The EE role owns physical measurement strategy, instrumentation feasibility, hardware/software boundaries, calibration, data integrity, installation constraints, and pilot measurement design. The right answer may be custom electronics, an existing scale, a software integration, a manual SOP, sensor fusion, or no new hardware.

Detailed hardware execution lives in [`../HARDWARE/HARDWARE_AGENT_PLAYBOOK.md`](../HARDWARE/HARDWARE_AGENT_PLAYBOOK.md). Plugin/tool behavior is defined in [`../../.agents/PLUGIN_POLICY.md`](../../.agents/PLUGIN_POLICY.md).

## Persistent parent, many child agents

The EE human owns one long-lived parent branch:

```text
work/ee/<slug>
```

The parent may fan out into any number of bounded hardware child tasks:

```text
HUMAN-EE
├── agent/hw-measurement/<task>
├── agent/hw-sensors/<task>
├── agent/hw-power/<task>
├── agent/hw-firmware/<task>
├── agent/hw-pcb/<task>
├── agent/hw-mechanical/<task>
├── agent/hw-calibration/<task>
└── agent/hw-verification/<task>
```

There is no artificial agent-count ceiling. Fifty hardware agents are valid if their dependencies and `touched_paths` do not conflict. Agents must not silently co-own the same schematic, PCB, firmware module, BOM, calibration artifact, or interface contract.

Child work integrates into the EE parent branch, never directly into `master`.

## North star

Improve the team's ability to answer:

1. what actually happened physically;
2. whether the measurement is trustworthy;
3. whether data collection is operationally realistic;
4. whether the pilot can produce defensible evidence;
5. whether custom hardware creates enough value to justify complexity;
6. whether the system can scale beyond a one-off demo.

## Core ownership

- measurement requirements and architecture;
- sensors, analog front end, ADC/interface, filtering;
- power architecture and protection;
- MCU/compute/peripheral budgeting;
- firmware state/fault behavior;
- connectivity, buffering, retry and offline behavior;
- PCB/interconnect constraints and test points;
- mechanical/enclosure/serviceability constraints;
- calibration, repeatability, hysteresis, drift and uncertainty;
- BOM/sourcing/lifecycle risk;
- DFM/DFT readiness when manufacturing matters;
- pilot measurement SOP and failure modes;
- hardware API/data-contract coordination with CS1/CS2;
- deciding whether custom hardware should exist at all.

## Hardware child lanes

Use the narrowest lane that makes ownership obvious:

- `hw-measurement` — measurand, range, accuracy/repeatability need, operator workflow;
- `hw-sensors` — sensor technology, AFE, ADC/interface, filtering, calibration inputs;
- `hw-power` — source, rails, peaks, conversion, protection, brownout/thermal behavior;
- `hw-firmware` — drivers, state machine, buffering, retries, watchdog, diagnostics;
- `hw-pcb` — schematic/layout constraints, grounding, connectors, test points, ERC/DRC;
- `hw-mechanical` — mounting, enclosure, cleaning/ingress, strain relief, serviceability;
- `hw-calibration` — references, calibration points, drift/hysteresis/repeatability tests;
- `hw-verification` — acceptance matrix, failure injection, integration and evidence capture.

Other hardware child lanes are allowed when they create a cleaner non-overlapping boundary.

## Evidence maturity

Every hardware claim must retain its real evidence level:

- `ASSUMPTION` — not verified;
- `DATASHEET` — supported by manufacturer/reference documentation;
- `CALCULATION` — engineering calculation with stated inputs;
- `SIMULATION` — simulated only;
- `BENCH_TEST` — physically measured under recorded bench conditions;
- `FIELD_TEST` — measured in intended/representative operating conditions;
- `PRODUCTION_EVIDENCE` — verified on release/manufactured hardware with a defined process.

A CAD render, schematic, firmware build, SPICE result, or datasheet claim is never bench/field evidence by itself.

## Measurement before hardware

Before committing to a device, establish:

- what decision the measurement improves;
- exact measurand and workflow location;
- operator/user and measurement frequency;
- operationally meaningful accuracy/repeatability;
- existing equipment/data sources;
- burden and behavior-change risk;
- service/event association;
- failure, missing-data, power-loss and reconnect behavior;
- whether inference/integration/manual SOP is better than new electronics.

The hardware follows the measurement requirement, not the other way around.

## Current candidate — not a commitment

A candidate waste-measurement architecture is:

```text
load cell / scale
  -> amplifier / ADC interface
  -> MCU/gateway
  -> network/buffer
  -> BOUNCAMPUS measurement API
```

Potential parts may include a load cell, HX711-class interface, ESP32-class controller, local confirmation/tare input, status indication, buffering and enclosure. These remain candidates until evidence justifies them.

## Electrical design gate

When custom electronics are justified, create the relevant subset of:

- input ranges and absolute-maximum review;
- excitation/reference assumptions;
- sensor/error budget;
- regulator headroom and worst-case power budget;
- decoupling and rail-stability intent;
- reverse-polarity/overcurrent/ESD protection where relevant;
- analog/noisy-domain separation and return paths;
- connector ratings and safe pinout;
- boot/reset/programming behavior;
- test points and debug access;
- tolerance/reference accuracy;
- thermal assumptions;
- creepage/clearance when relevant;
- component availability/package manufacturability;
- ERC/DRC or equivalent tool evidence when available.

Generated Gerbers or a PCB image do not prove these checks passed.

## Firmware gate

Measurement firmware should provide, where relevant:

- deterministic state flow;
- explicit invalid/error states;
- watchdog/recovery behavior;
- documented filtering/debouncing;
- safe calibration storage/versioning;
- local buffering when connectivity fails;
- idempotent event IDs/retries;
- timestamp/order semantics;
- useful diagnostics;
- reproducible build instructions;
- no silent conversion of bad readings into plausible numbers.

## Bench / field validation

Useful physical tests can include:

- zero stability and tare;
- known-reference accuracy;
- repeatability;
- hysteresis and drift;
- placement and temperature sensitivity;
- power interruption/recovery;
- reconnect and offline buffering;
- invalid-reading rejection;
- duplicate-event handling;
- operator workflow burden.

Do not invent arbitrary acceptance thresholds when the operational requirement is unknown. Establish the decision need first.

## Data contract

Physical measurements should carry enough context to audit their origin. Candidate fields include:

```json
{
  "stationId": "...",
  "serviceId": "...",
  "measurementType": "edible_surplus",
  "value": 4.82,
  "unit": "kg",
  "timestamp": "...",
  "quality": "VALID",
  "source": "PHYSICAL_MEASUREMENT"
}
```

Distinguish directly measured, manually entered, estimated, derived, missing, and rejected/invalid values.

## Plugin / specialized-tool behavior

Hardware child agents may proactively use available capabilities for:

- schematic/PCB CAD;
- circuit/SPICE simulation;
- datasheet/component lookup;
- BOM sourcing/lifecycle analysis;
- firmware build/debug;
- mechanical CAD;
- signal/power-integrity analysis;
- DFM/DFT/manufacturing review;
- remote bench/instrument access.

If a useful capability is unavailable, continue all safe independent work and use [`../HARDWARE/PLUGIN_CAPABILITY_REQUEST_TEMPLATE.md`](../HARDWARE/PLUGIN_CAPABILITY_REQUEST_TEMPLATE.md) to describe what remains unverified. Do not invent a plugin name or pretend a tool was used.

## Physical safety

Design, calculations, simulation, CAD, firmware work, and non-energized review are autonomous.

Use `PHYSICAL_SAFETY` before dangerous energization, mains/high-current work, risky battery testing, hazardous actuator motion, destructive physical testing, or consequential field installation.

## Collaboration contracts

### IE

Consume real PMR about workflow, operator burden, existing equipment and measurement gaps.

### CS1

Agree on required signals, quality/status semantics, calibration metadata, and evaluation needs.

### CS2

Provide evidence maturity, limitations, pilotability, and defensible differentiation inputs for application synthesis.

Use Fabric `produces` / `consumes` IDs for durable agent-to-agent handoffs instead of human chat relay.

## Anti-AI-slop standard

Reject:

- invented component specifications;
- fake sensor readings;
- claimed accuracy without calibration evidence;
- simulations presented as measurements;
- generic IoT diagrams without a decision need;
- sensors added for appearance;
- premature enclosure/PCB work before measurement need is clear;
- climate-impact claims inferred merely from having hardware.

## Strong outputs

Good EE child outputs include:

- architecture comparison with a decision;
- exact measurement requirements;
- schematic/PCB constraints with evidence class;
- BOM with exact identities and sourcing notes;
- firmware with failure behavior;
- calibration/repeatability experiment;
- measured CSV with provenance;
- measurement quality model;
- pilot SOP;
- deployment constraint list;
- a defensible decision to remove unnecessary hardware.

The objective is the strongest trustworthy measurement loop, not the largest hardware stack.
