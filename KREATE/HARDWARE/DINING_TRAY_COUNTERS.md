# Serving Line + Tray Return Counters — Sensor Architecture

Issue: #332  
Parent: #298  
Owner: EHB — Embedded Hardware, Communications & Integration  
Status: design selection only. No installation, BENCH_TEST, FIELD_TEST, or achieved accuracy claim.

## Decision

For a physically constrained **single-tray lane**, use **two through-beam photoelectric channels** as the default sensing architecture.

Use a short-range Time-of-Flight (ToF) sensor as the first fallback when an emitter/receiver cannot be mounted on opposite sides of the tray path.

Do not use camera vision or radar by default. They add complexity without proven incremental value for a binary tray-crossing measurement and increase privacy/integration burden.

The architecture emits physical tray-count deltas only:

- serving line: `SERVED_TRAY_DELTA / TRAYS`;
- return line: `RETURNED_TRAY_DELTA / TRAYS`.

A serving tray is **not** automatically a served portion and is never promoted by EHB to `actual_served`.

## Why through-beam first

A through-beam sensor measures interruption of a known optical path rather than estimating scene content.

Reference industrial sensor class: Omron E3Z through-beam family.

Manufacturer facts for the E3Z family include:

- through-beam models such as E3Z-T61/T81;
- 12–24 VDC supply class;
- 1 ms maximum operate/reset response for standard through-beam models;
- IP67 protection rating in the cited family specification;
- opaque target detection;
- separate emitter + receiver geometry.

Sources:

- https://www.ia.omron.com/products/family/407/specification.html
- https://www.ia.omron.com/products/family/407/lineup.html

Evidence class: `DATASHEET`.

E3Z is a **reference industrial class**, not a frozen procurement choice. Final MPN depends on mounting, output polarity, connector, wash/cleaning environment, local sourcing, and the selected low-voltage interface.

## Dual-beam geometry

Use two beams, A and B, separated along tray travel.

```text
travel direction --->

 emitter A  --->  receiver A
        [ tray path ]
 emitter B  --->  receiver B
```

Mount beams low enough to intersect the intended tray body/edge and high enough to avoid the fixed conveyor/rail.

Exact beam height and A↔B spacing remain `ASSUMPTION` until the real tray path and speed envelope are measured.

### Forward crossing state machine

```text
CLEAR
  |
A blocked
  |
A+B blocked
  |
B blocked
  |
CLEAR
  |
emit +1 tray event
```

Reverse or invalid sequences do not emit a normal count:

```text
B -> A+B -> A -> CLEAR
= reverse / diagnostic

A held too long
= blocked/jam diagnostic

A toggles repeatedly without valid sequence
= bounce/noise diagnostic
```

This sequence makes a count depend on one complete physical crossing rather than one raw edge.

## Serving Line Counter

### Intended measurement point

Place the pair at a constrained tray-exit point after a tray has committed to leaving the serving line.

Requirements:

- one physical lane;
- no alternative bypass path inside the measurement definition;
- detector plane should observe trays, not identify people;
- event timestamp corresponds to completed tray crossing;
- station identity is fixed and versioned.

If the serving process allows multiple side-by-side trays, overlapping objects, staff carrying stacks, or bypass lanes, do not claim the simple beam pair is sufficient. Change the geometry or move to a better measurement point before adding a more complex sensor.

Output example:

```json
{
  "eventId": "served-tray-2026-10-06-000123",
  "deviceId": "serving-counter-north-01",
  "stationId": "north-serving-line-1",
  "timestamp": "2026-10-06T12:10:00+03:00",
  "measurementType": "SERVED_TRAY_DELTA",
  "value": 1,
  "unit": "TRAYS",
  "quality": "VALID",
  "source": "PHYSICAL_MEASUREMENT",
  "firmwareVersion": "tray-counter-fw-v1",
  "schemaVersion": "dining-count-event-v1"
}
```

## Tray Return Counter

The dish-return path is usually the better place for a deterministic beam counter when the tray channel is mechanically constrained.

Use the same dual-beam state machine but a distinct station/device identity.

Output:

- `measurementType = RETURNED_TRAY_DELTA`;
- `unit = TRAYS`;
- value normally 1 per accepted crossing.

Returned trays are a reconciliation/denominator signal. They are not silently converted into `actual_served`.

## ToF fallback

Reference device class: ST VL53L4CX.

Manufacturer facts:

- absolute distance measurement using 940 nm VCSEL;
- 18-degree field of view;
- nominal range up to 6 m under documented conditions;
- multi-object histogram processing;
- I2C interface;
- 2.8 V single supply;
- cover-glass crosstalk handling and smudge compensation are documented features.

Sources:

- https://www.st.com/en/imaging-and-photonics-solutions/VL53L4CX
- https://www.st.com/resource/en/datasheet/vl53l4cx.pdf

Evidence class: `DATASHEET`.

### When ToF is justified

Use ToF only when:

- a receiver cannot be installed opposite an emitter;
- a top-down or side single-ended geometry is mechanically simpler;
- the sensor can be isolated from direct splash/cleaning damage;
- the real tray/background distance bands are separable in bench measurements.

### ToF-specific risks

- target coverage and reflectance affect real ranging performance;
- cover glass and contamination require calibration/verification;
- steam, droplets and close foreground objects may change readings;
- a distance threshold copied from another installation is not valid evidence.

Therefore no distance threshold is frozen before bench measurements.

## Why vision is not the default

Vision can solve complex multi-object geometry, but this task is only a tray crossing count.

Vision introduces:

- camera placement and lighting;
- image retention/privacy controls;
- model/version/accuracy lifecycle;
- more compute and power;
- harder field validation.

Use vision only if a constrained deterministic sensor cannot represent the actual physical flow and the added complexity is justified.

If vision is ever introduced, no face/person identification is allowed.

## Why radar is not the default

Radar is useful for presence/motion in many environments but is not selected here because this count needs a crisp mapping from a constrained physical tray crossing to one event.

Before radar promotion, EHB/EE would need evidence that:

- the tray target is separable from people/adjacent motion;
- multipath/reflections do not create ambiguous count states;
- a simpler beam/ToF geometry cannot solve the problem.

No such evidence exists yet.

## Embedded interface

Reference controller class: ESP32-S3.

Relevant manufacturer capabilities include:

- 2.4 GHz Wi-Fi;
- GPIO;
- pulse-count controller peripheral;
- timers/watchdogs;
- common serial buses.

Source:

- https://documentation.espressif.com/esp32_s3_datasheet_en.pdf

Evidence class: `DATASHEET`.

The controller choice is not procurement-frozen.

## Electrical boundary

Industrial photoelectric reference sensors may operate at 12–24 VDC while the MCU is a low-voltage logic device.

Required interface:

```text
approved SELV supply
       |
12/24 V sensor domain
       |
protected / isolated digital interface
       |
3.3 V MCU domain
```

Do not connect a 12/24 V industrial output directly to MCU GPIO.

Final interface design must consider the selected sensor's NPN/PNP output, voltage, connector and cable length.

No custom mains supply is required or justified for the MVP node.

## Firmware event logic

```text
BOOT
 |
load station/device/config
 |
sensor self-check
 |
CLEAR
 |
beam sequence parser
 | valid forward crossing
 v
build immutable eventId
 |
enqueue via EHB persistent queue
 |
delivery/retry runtime
 |
ACK tombstone
```

State timeout, debounce, stuck-beam and invalid-order values are configuration parameters derived from bench testing; they are not invented here.

## Health signals

The device should expose at least:

- sensor A state;
- sensor B state;
- time since last valid transition;
- blocked-beam timeout flag;
- invalid-sequence count;
- unique emitted-event count;
- queue pending/acked/attempt counts;
- network/delivery state;
- firmware/config version;
- clock validity.

Health metadata must not contain student/person/card identifiers.

## Failure modes

| Failure | Behavior |
|---|---|
| tray pauses across one/both beams | do not count until a valid complete sequence; expose blocked duration |
| tray reverses | classify reverse/invalid; do not emit normal forward count |
| hand/bag briefly crosses beam | invalid/partial sequence should not automatically become a tray event |
| two trays with no clear gap | potential undercount; record test failure regime |
| stacked trays | measurement definition may count one crossing rather than physical tray quantity; must be explicitly tested |
| sensor dirty/blocked | health fault; do not continuously generate events |
| steam/water attenuates beam | health/quality fault; verify in bench/field testing |
| network down | queue exact event locally |
| restart after event creation | recover pending immutable event |
| timestamp invalid | withhold/error state rather than fabricate time |
| bypass route exists | measurement point invalid for total flow; fix layout/definition |

## Acceptance test plan

### Bench fixture

Use a representative tray/channel fixture and manually logged ground truth.

Test separately:

- normal single forward crossing;
- slow crossing;
- fast crossing;
- pause while A blocked;
- pause while A+B blocked;
- reverse crossing;
- partial hand/object interruption;
- two trays with minimal gap;
- stacked trays;
- deliberate beam blockage;
- contamination/cleaning-window condition;
- network disconnect/reconnect;
- controller restart around event creation/delivery.

Record raw A/B state transitions and emitted events.

### Accuracy reporting

Do not report one percentage alone.

Record:

- true tray crossings;
- emitted unique events;
- false positives;
- false negatives;
- duplicate events before downstream dedup;
- invalid/withheld sequences;
- test geometry and speed regime.

No minimum percentage is asserted until operations/CS1 define what error level is acceptable for the intended decision.

## Evidence boundary

| Claim | Current status |
|---|---|
| E3Z electrical/response/IP family specs | `DATASHEET` |
| VL53L4CX capabilities | `DATASHEET` |
| dual-beam chosen as default | engineering decision / `ASSUMPTION` until bench |
| actual Boğaziçi lane geometry | unknown |
| sensor cleanliness/steam performance | no `BENCH_TEST` |
| tray-count accuracy | no `BENCH_TEST` |
| real dish-return performance | no `FIELD_TEST` |

## Exit criterion for #332

The design slice is complete when:

- default and fallback sensor architectures are explicit;
- serving/return semantics match the merged CS1 contract;
- privacy boundary is preserved;
- low-voltage interface and failure modes are explicit;
- bench protocol can reveal false positives/negatives/duplicates;
- no `actual_served` or accuracy claim is introduced.
