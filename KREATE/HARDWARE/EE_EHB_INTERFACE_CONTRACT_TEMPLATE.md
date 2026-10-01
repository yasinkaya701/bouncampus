# EE ↔ EHB Interface Contract Template

Use this template when a hardware workstream crosses the boundary between **EE measurement truth** and **EHB embedded implementation**.

This is a coordination artifact, not bureaucracy. Fill only the sections relevant to the system. The contract should become stable enough that EE and EHB can work in parallel without silently changing each other's assumptions.

## Contract metadata

- Contract ID: `IFACE-EE-EHB-___`
- System / workstream:
- Primary EE task / PR:
- Primary EHB task / PR:
- EE owner/reviewer:
- EHB owner/reviewer:
- CS1 consumer (if data reaches decision/model code):
- Status: `DRAFT | STABLE_FOR_PARALLEL_WORK | CHANGE_PROPOSED | VERIFIED | RETIRED`
- Version:
- Last updated:

## 1. Measurement requirement — EE owner

- Measurand:
- Unit:
- Operational range:
- Required accuracy / uncertainty:
- Required repeatability:
- Sampling / event requirement:
- Calibration/reference method:
- Invalid-reading definition:
- Physical placement / workflow constraints:
- Evidence class currently available:

## 2. Electrical interface — EHB implementation, EE requirement review

| Item | Contract value | Owner | Evidence / source |
|---|---|---|---|
| Sensor/interface type | | | |
| Supply voltage range | | | |
| Maximum/expected current | | | |
| Logic level | | | |
| Connector | | | |
| Pinout | | | |
| ADC/reference/excitation | | | |
| Pull-ups / termination | | | |
| Protection requirements | | | |
| Test points | | | |

## 3. Timing and sampling

- Sampling frequency / trigger:
- Timing tolerance:
- Debounce/filter requirement:
- Warm-up / settling requirement:
- Timestamp source:
- Clock-reset behavior:
- Ordering requirement:

EE confirms these preserve measurement validity. EHB confirms they are implementable and testable.

## 4. Calibration persistence

- Calibration parameters:
- Produced by:
- Stored where:
- Version format:
- Factory/default behavior:
- Update procedure:
- Corruption/missing-value behavior:
- Reset/recovery behavior:

No firmware update may silently replace calibration semantics.

## 5. Device protocol / event contract — EHB owner, CS1 consumer review where applicable

- Transport:
- Protocol/version:
- Device identity:
- Event identity / idempotency key:
- Payload schema/version:
- Units/scaling representation:
- Quality flags:
- Error/status codes:
- Missing/invalid reading representation:
- Duplicate behavior:
- Offline queue behavior:
- Replay behavior:
- Retry/backoff:
- Maximum queue age/depth:

Example payload if useful:

```json
{
  "deviceId": "...",
  "stationId": "...",
  "measurementType": "...",
  "value": null,
  "unit": "...",
  "timestamp": "...",
  "quality": "VALID|INVALID|MISSING",
  "eventId": "...",
  "schemaVersion": "..."
}
```

## 6. Power contract — EHB owner

- Input source/range:
- Nominal power/current:
- Worst-case/peak current:
- Brownout threshold/behavior:
- Startup behavior:
- Shutdown behavior:
- Power-loss recovery:
- Battery/runtime assumptions if applicable:
- Protection strategy:

## 7. Fault and recovery states

| Fault | Detection | Device behavior | Measurement/data consequence | Recovery | Owner |
|---|---|---|---|---|---|
| Sensor disconnected | | | | | |
| Out-of-range reading | | | | | |
| Calibration missing/corrupt | | | | | |
| Network unavailable | | | | | |
| Backend unavailable | | | | | |
| Power interruption | | | | | |
| Device reset/watchdog | | | | | |
| Duplicate/replayed event | | | | | |

## 8. Verification contract

### EE verification

- Reference method:
- Measurement acceptance criteria:
- Repeatability/uncertainty test:
- Field validity check:

### EHB verification

- Electrical bring-up checks:
- Power checks:
- Interface/protocol tests:
- Offline/reconnect/replay tests:
- Fault-injection tests:
- Firmware build/version evidence:

### Shared system verification

- End-to-end scenario:
- Required logs/artifacts:
- Expected data at backend:
- Expected quality/error semantics:
- Evidence maturity target:

## 9. Change control

A proposed change is **cross-boundary** if it changes any of:

- voltage/current;
- pinout/connector;
- ADC/reference/excitation;
- sampling/timing;
- calibration storage/semantics;
- protocol;
- payload/schema;
- units/scaling;
- quality/error flags;
- power budget;
- startup/shutdown;
- offline/retry/replay behavior;
- fault semantics;
- verification method.

For cross-boundary changes:

1. mark status `CHANGE_PROPOSED`;
2. state the reason and affected assumptions;
3. update this contract/version;
4. obtain EE review for measurement correctness;
5. obtain EHB review for implementation correctness;
6. obtain CS1 review if downstream data semantics change;
7. update affected tests before merge;
8. restore status to `STABLE_FOR_PARALLEL_WORK` or `VERIFIED` only after agreement/evidence.

## 10. Review record

### EE review

- Reviewer:
- Version reviewed:
- Measurement correctness: `ACCEPT | REVISE`
- Notes:

### EHB review

- Reviewer:
- Version reviewed:
- Embedded/integration correctness: `ACCEPT | REVISE`
- Notes:

### CS1 review — only when data semantics are affected

- Reviewer:
- Version reviewed:
- Consumer semantics: `ACCEPT | REVISE | NOT_APPLICABLE`
- Notes:

## Core rule

> **EE defines what must be true about the measurement. EHB defines how the embedded system reliably makes that contract real. Neither silently changes the boundary.**
