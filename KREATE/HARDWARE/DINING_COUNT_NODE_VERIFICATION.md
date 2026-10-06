# Dining Count Nodes — Installation and Verification Protocol

Issue: #334  
Parent: #298  
Owner: EHB — Embedded Hardware, Communications & Integration  
Applies to: Production Count Node, Serving Line Counter, Tray Return Counter  
Status: verification protocol only. It does not claim that hardware has been installed or tested.

## Purpose

Define the minimum installation, calibration, reference-count, recovery and evidence procedure before any dining count node may be described as a validated measurement source.

The protocol deliberately separates:

- **software contract correctness**;
- **bench measurement evidence**;
- **field measurement evidence**;
- **reconciled service truth**.

Passing an EHB device test does not automatically promote a signal to `actual_served`, surplus, waste, shortage, or impact evidence.

## Inputs from prior design slices

Production Count design:

- `DINING_PRODUCTION_COUNT_NODE.md`;
- preferred path is existing deterministic aggregate/source integration before new sensing;
- emitted physical semantic is `PRODUCED_PORTION_DELTA / PORTIONS`.

Tray counter design:

- `DINING_TRAY_COUNTERS.md`;
- dual through-beam photoelectric is default for a constrained single-tray lane;
- ToF is fallback when opposite-side mounting is infeasible;
- emitted semantics are `SERVED_TRAY_DELTA / TRAYS` and `RETURNED_TRAY_DELTA / TRAYS`.

Shared runtime:

- persistent immutable queue;
- exact-payload retry;
- changed-payload replay conflict;
- reconnect/backoff and restart recovery;
- CS1 contract regression.

## Installation record

Every physical installation must have one immutable installation record containing at least:

```text
deviceId
stationId
nodeType
installationRevision
physicalLocationDescription
measurementPointDefinition
sensor/controller MPNs
firmwareVersion
schemaVersion
configurationVersion
powerSourceClass
networkPathClass
referenceMethod
installationTimestamp
installer/reviewer role
evidenceClass
knownLimitations
```

Do not store student/person/card identifiers in the installation record.

### Station identity

`stationId` identifies the physical measurement point, not a person, operator, or temporary device session.

Moving a node to a materially different physical measurement point requires a new installation revision and may require a new station identity depending on the service-truth mapping.

## Physical datum

### Production Count

Record the actual source boundary:

- owner-generated system/export;
- deterministic dry contact/pulse/register;
- local operator-confirmed batch/portion event.

Do not describe a source generically as "production count" without stating what creates one event.

### Serving / Return counters

Record:

- tray travel direction;
- lane width;
- sensor A and B positions;
- beam height/reference plane;
- A↔B spacing;
- bypass paths;
- expected tray family;
- expected single/stacked tray behavior;
- sensor window/cleaning access.

If the actual geometry permits unmeasured bypass flow, the station cannot be claimed to measure total service/return flow.

## Electrical and safety pre-check

Before energizing a physical node:

- verify supply type and voltage;
- verify sensor output type (for example NPN/PNP/dry contact);
- verify MCU input conditioning/isolation;
- verify connector polarity and strain relief;
- verify no direct 12/24 V industrial output reaches 3.3 V GPIO;
- verify enclosure/installation does not create an unsafe obstruction;
- keep custom mains work out of the MVP node;
- use the repository `PHYSICAL_SAFETY` gate for energized cabinet work, existing equipment modification or unknown industrial interfaces.

Design review is autonomous; hazardous physical action is not.

## Clock and identity pre-check

Before measurement:

- `deviceId` present and stable;
- `stationId` present and stable;
- firmware/config/schema versions reported;
- time source valid;
- emitted timestamps timezone-aware;
- restart does not create a new device identity;
- queued events retain their original timestamp and identity after reconnect.

If trustworthy time is unavailable, emit/record a fault; do not fabricate plausible timestamps.

## Software contract pre-test

For each node type, verify locally before physical accuracy testing:

- required field set is complete;
- measurement type/unit pair is exact;
- `source = PHYSICAL_MEASUREMENT`;
- normal accepted event uses `quality = VALID`;
- `eventId` is stable and anonymous;
- identical retry remains identical;
- changed payload under the same `eventId` fails closed;
- identity-bearing nested metadata is not accepted downstream;
- network loss leaves the event queued;
- restart recovers pending events;
- ACK only removes the event from pending delivery after exact fingerprint confirmation.

Evidence class: repository software regression, not physical test evidence.

## Manual reference protocol

A human/manual reference count is the default temporary comparison method for tray counters unless a better traceable reference is justified.

### Reference log

For every run record:

```text
runId
stationId
startTimestamp
endTimestamp
testScenario
manualReferenceCount
deviceUniqueEventCount
falsePositiveCount
falseNegativeCount
duplicateEventCount
invalidOrWithheldSequenceCount
restartCount
networkOutageApplied
sensorHealthFaults
notes
rawLogArtifact
reviewer
```

The manual observer must count the same physical measurement definition as the node.

Do not compare "people served" against "trays crossed" and call the difference sensor error.

## Event matching

For each known physical crossing/source event, classify the device result as one of:

- **matched unique event**;
- **false negative** — reference event occurred, no valid device event;
- **false positive** — device event without matching reference event;
- **duplicate** — more than one unique emitted event for one reference event;
- **withheld/invalid** — device explicitly declined to emit a valid count due to state/health rules.

Transport replays with the same stable `eventId` are not duplicate physical measurements; they are retry traffic and must deduplicate downstream.

## Required bench scenarios

### Production Count source

Run the scenarios applicable to the selected source:

- normal source event;
- repeated/bounced contact;
- long/stuck contact;
- source reversal/correction if supported;
- invalid/non-positive local entry;
- rapid sequential source events;
- device restart before enqueue;
- restart after enqueue;
- network disconnect after enqueue;
- server receive followed by lost local ACK.

### Serving / Return beam counters

At minimum:

- normal forward crossing;
- slow crossing;
- fast crossing;
- pause with A blocked;
- pause with A+B blocked;
- reverse crossing;
- partial hand/bag/object interruption;
- two trays with the smallest representative gap;
- stacked trays;
- deliberate blocked/dirty sensor;
- power cycle while clear;
- power cycle around event generation;
- network disconnect/reconnect.

### ToF fallback

Additionally test:

- background-only distance;
- representative tray materials/colors;
- minimum/maximum target distance;
- cover window installed;
- clean vs intentionally contaminated window;
- nearby hands/objects;
- intended ambient-light envelope.

No range threshold from a datasheet may replace measured station calibration.

## Minimum sample structure

Do not select a sample size to manufacture a target percentage.

For initial engineering characterization:

- include every required failure scenario at least once;
- include repeated normal crossings across the expected speed/placement range;
- retain raw event/reference logs;
- continue testing until the main failure regimes are observable and repeatability can be estimated.

A larger sample is required before narrow accuracy claims.

The exact acceptance threshold is a downstream operational requirement and must be set by the measurement/decision owner, not invented by EHB.

## Metrics

Report counts first:

```text
N_reference
N_unique_device
TP_matched
FP
FN
duplicates
withheld_invalid
transport_replays
replay_conflicts
```

Derived rates may be reported only with numerator/denominator:

```text
false_positive_rate = FP / N_unique_device_or_defined_denominator
miss_rate           = FN / N_reference
duplicate_rate      = duplicates / N_reference
withhold_rate       = withheld_invalid / attempted_sequences
```

The denominator definition must be written next to the result.

Do not report only "accuracy = 99.x%" without raw counts and test conditions.

## Network/restart acceptance

For the software/runtime portion, the expected deterministic behavior is:

1. event created once with stable identity;
2. event persisted before delivery;
3. network failure does not delete it;
4. retry uses exact payload;
5. restart reloads pending payload;
6. server-received + local-ACK-lost may cause transport replay;
7. downstream deduplicates identical replay;
8. changed-payload replay conflict fails closed.

Physical storage endurance and true brownout resilience require bench evidence on the selected storage/power hardware.

## Blocked/dirty sensor health

A counter must expose a health fault when the sensor remains in an implausible state longer than the bench-derived allowed interval.

Health fault behavior:

- stop normal count emission when the measurement state is ambiguous;
- retain diagnostics;
- preserve already-created queue items;
- require clear/recovery state before resuming;
- do not silently "estimate" missed trays.

The timeout value is bench-derived per geometry; it is not frozen in this document.

## Cleaning/service verification

For optical devices record:

- sensor/window material;
- cleaning method;
- before-clean check;
- after-clean check;
- visible damage/contamination;
- sensor stability/health result.

A cleanable enclosure concept is not equivalent to an IP or sanitation certification.

## Evidence promotion

### `ASSUMPTION`

Allowed for:

- proposed geometry;
- expected flow;
- unmeasured thresholds;
- anticipated operator behavior.

### `DATASHEET`

Allowed only for manufacturer/source specifications under stated conditions.

### `CALCULATION`

Allowed for traceable derived values with stated inputs.

### `SIMULATION`

Allowed for synthetic state-machine/electrical/mechanical simulation.

### `BENCH_TEST`

Requires:

- physical device or representative prototype;
- recorded setup;
- raw reference/device counts;
- test conditions;
- versioned hardware/firmware/config;
- repeatable procedure.

### `FIELD_TEST`

Requires measurement in the intended or representative operational environment with recorded installation and workflow conditions.

### `PRODUCTION_EVIDENCE`

Requires manufactured/release hardware plus defined production verification.

Never promote evidence because a deadline is close.

## CS1 handoff gate

A node may supply **descriptive physical counts** to CS1 only when:

- software contract tests pass;
- device/station/version metadata are stable;
- timestamp quality is acceptable;
- source measurement definition is explicit;
- physical reference results and known limitations are documented;
- raw event logs are retained for reconciliation;
- no identity-bearing metadata exists.

Even then:

- `SERVED_TRAY_DELTA` remains trays;
- `RETURNED_TRAY_DELTA` remains trays;
- `PRODUCED_PORTION_DELTA` remains the documented source's produced portion delta;
- EHB does not declare `actual_served`, waste, shortage or impact.

## Acceptance decision record

For each node installation produce:

```text
DESIGN_REVIEW: PASS / FAIL
SOFTWARE_CONTRACT: PASS / FAIL
BENCH_EVIDENCE: NOT_RUN / PASS / FAIL / LIMITED
FIELD_EVIDENCE: NOT_RUN / PASS / FAIL / LIMITED
OPERATIONAL_THRESHOLD_OWNER: <role or unresolved>
KNOWN_LIMITATIONS: [...]
CS1_DESCRIPTIVE_HANDOFF: ALLOW / WITHHOLD
RECONCILED_SERVICE_TRUTH: false unless separately admitted by CS1
```

"PASS" must link to the test artifact. "NOT_RUN" must never be rewritten as PASS.

## Exit criterion for #334

This verification slice is complete when:

- installation identity/datum requirements are explicit;
- manual reference protocol is reproducible;
- FP/FN/duplicate/withhold reporting is defined;
- blocked/dirty/restart/network-loss tests are included;
- physical-safety boundary is explicit;
- evidence promotion rules are locked;
- no unsupported accuracy threshold or field result is introduced.
