# EE — Physical Systems & Measurement Lead

## Mission

Own the question: **Can BOUNCAMPUS observe the physical world reliably enough to support better operational decisions, and what is the most practical way to do that?**

This role is not limited to building a smart scale. The EE lead owns physical measurement strategy, instrumentation feasibility, hardware/software boundaries, sensor selection, installation constraints, data integrity, and pilot measurement design.

The right answer may be a custom device, an existing kitchen scale, a POS integration, a manual measurement protocol, a sensor fusion approach, or no new hardware at all.

The mission is to create the strongest evidence loop with the least unnecessary complexity.

## North Star

Improve the team's ability to answer:

1. what actually happened in the physical operation,
2. whether the data is trustworthy,
3. whether measurement can be deployed without disrupting staff,
4. whether a pilot can produce defensible evidence,
5. whether hardware adds enough value to justify itself,
6. whether the resulting system can scale beyond a one-off prototype.

## Core Ownership

Primary ownership areas include:

- physical measurement architecture,
- waste / surplus measurement strategy,
- sensor and instrumentation experiments,
- calibration and repeatability,
- measurement uncertainty,
- edge-device reliability,
- connectivity and offline behavior,
- installation / power / enclosure feasibility,
- data provenance at the physical layer,
- pilot measurement SOPs,
- physical-system failure modes,
- hardware-vs-software tradeoffs,
- identifying what should be measured versus what can be inferred.

## Current Candidate: Smart Waste Measurement Node

A current candidate architecture is:

`load cell / scale → amplifier / interface → MCU or gateway → network → BOUNCAMPUS measurement API`

Possible implementation components include:

- load cell,
- HX711 or other ADC / scale interface,
- ESP32 or equivalent controller,
- tare / confirmation input,
- local status indication,
- Wi-Fi or other connectivity,
- optional local buffering,
- optional display,
- optional enclosure.

This architecture is **not mandatory**. It should survive comparison with simpler or better approaches.

## Measurement Questions Before Hardware

Before committing to any device, establish:

- What exactly needs to be measured?
- At what point in the workflow?
- By whom?
- How often?
- What accuracy is operationally meaningful?
- What categories matter: edible surplus, preparation waste, plate waste, total waste, produced quantity, served quantity?
- Does an existing device already produce the data?
- Would integration be easier than new hardware?
- What human action would measurement require?
- Would that action change behavior and bias the data?
- What happens when connectivity fails?
- How will measurements be associated with the correct service?

The hardware should follow the measurement requirement, not the other way around.

## Prototype Freedom

The EE lead is free to explore alternative physical-system concepts where they could create more value.

Examples include:

- smart weighing node,
- existing digital-scale integration,
- load-cell platform,
- service throughput sensing,
- portion-counting mechanisms,
- button / NFC / RFID service labeling,
- simple edge display,
- environmental sensing if PMR/model evidence supports it,
- local storage and delayed sync,
- camera-assisted measurement if there is a defensible reason,
- low-tech measurement procedures when they outperform custom electronics,
- integration with existing POS or kitchen systems.

Experiments should be cheap and reversible until evidence supports deeper investment.

## Bench Validation

For any measurement device, establish the relevant performance envelope.

Depending on the device this may include:

- zero stability,
- tare behavior,
- known-reference accuracy,
- repeatability,
- hysteresis,
- drift,
- sensitivity to placement,
- temperature effects,
- power interruption behavior,
- reconnect behavior,
- local buffering,
- invalid-reading detection,
- duplicate-event handling.

Do not use arbitrary engineering thresholds if the operational requirement is unknown. First determine what accuracy or reliability is actually needed for the decision or pilot.

## Data Contract

A useful physical measurement should carry enough context to be auditable. Candidate fields include:

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

The exact schema may change with the measurement architecture. Coordinate with CS1/CS2 rather than optimizing the hardware in isolation.

## Measurement Quality and Provenance

The system should be able to distinguish, where relevant:

- directly measured,
- manually entered,
- estimated,
- derived,
- missing,
- rejected / invalid.

A physical sensor does not automatically create ground truth. Calibration, labeling, operator workflow, and data association matter just as much.

## Pilot Design Contribution

The EE lead should help design a pilot that can actually be executed.

Questions include:

- what will be measured per service,
- which measurements are mandatory,
- who records them,
- how control/intervention services are compared,
- what happens when a reading is missing,
- what constitutes invalid measurement,
- how early sell-out or stockout is observed,
- how operator overrides are captured,
- how measurement burden is minimized.

The role should challenge pilots that look statistically neat but operationally unrealistic.

## Hardware Is Not Automatically a Differentiator

The team should not build hardware merely because an EE member exists.

A custom device is justified when it materially improves one or more of:

- data availability,
- trustworthiness,
- timeliness,
- operator burden,
- intervention loop closure,
- pilotability,
- defensibility,
- scalability.

If a commercial scale + simple data-entry workflow is better for the application stage, say so. If a custom node creates a strong measurable advantage, build it.

## Freedom to Explore

The EE lead may independently initiate small experiments that answer high-value questions without waiting for permission.

Examples:

- test whether a low-cost load cell is stable enough,
- compare manual vs automatic tare,
- benchmark two sensor options,
- prototype offline buffering,
- inspect existing scale interfaces,
- estimate installation burden,
- test whether service identification needs a button/NFC flow,
- prove that a proposed sensor is unnecessary,
- identify a better physical variable than waste mass.

Exploration should produce evidence and a decision, not endless prototyping.

## Collaboration

### With IE

Use PMR to understand measurement reality, operator burden, workflow, and existing equipment.

### With CS1

Define what measurements are needed to evaluate predictions and interventions, and agree on quality/status semantics.

### With CS2

Explain what physical evidence can support product claims, pilot design, differentiation, and application language.

## Anti-AI-Slop Standard

AI can assist with datasheets, firmware drafts, calculations, experiment design, and documentation. It cannot substitute for bench evidence or physical constraints.

Reject:

- hardware specs invented without checking components,
- claimed accuracy without calibration evidence,
- fake sensor readings,
- simulated results presented as measured,
- generic IoT architecture diagrams with no operational need,
- unnecessary sensors added for appearance,
- enclosure / PCB work that consumes time before the measurement question is established,
- climate-impact claims inferred directly from sensor existence.

## Strong Outputs

Useful deliverables may include:

- measurement architecture comparison,
- calibrated prototype,
- experiment CSV,
- photos / bench evidence,
- firmware with clear failure behavior,
- measurement quality model,
- pilot measurement SOP,
- integration contract,
- deployment constraint list,
- decision proving that a proposed hardware component should be removed.

## Application-Stage Success Criteria

By October 8, the physical-systems side should ideally demonstrate:

- a credible measurement strategy,
- understanding of current operational measurement gaps,
- at least one tested technical path where feasible,
- explicit limitations and failure modes,
- a defensible hardware-vs-integration decision,
- a pilot measurement approach that could be run in reality,
- no claim that prototype hardware is production-ready unless evidence supports it.

A polished physical prototype is valuable, but a well-supported decision that a simpler solution is superior is also a success.
