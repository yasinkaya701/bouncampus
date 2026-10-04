# EE ↔ EHB Interface Contract Template

Use this contract whenever an EE measurement requirement crosses into EHB electronics/firmware/communications implementation. Fill only fields that are actually known; unknown values remain explicit rather than invented.

## 1. Interface identity

- Interface / subsystem:
- Revision:
- EE owner:
- EHB owner:
- CS1 consumer/reviewer, if applicable:
- Related issue / PR:

## 2. Measurement intent — EE authority

- Physical quantity / event being measured:
- Sensor / measurement principle:
- Required range:
- Required resolution / precision target:
- Sampling requirement:
- Calibration method:
- Calibration version semantics:
- Uncertainty / known limitations:
- Field-validity acceptance evidence:

## 3. Electrical and physical interface — EHB implementation

- Supply rails / nominal voltage:
- Maximum current / power envelope:
- Connector / pinout:
- Logic levels / isolation:
- Protection requirements:
- Mechanical / environmental constraints:
- Power-up / shutdown sequencing:
- Fault-safe behavior:

## 4. Firmware and sampling contract

- Firmware / device software version:
- Sampling cadence / trigger semantics:
- Timestamp source and timezone semantics:
- Calibration metadata persistence:
- Local buffering policy:
- Retry / reconnect behavior:
- Idempotency / duplicate handling:
- Device restart / brownout recovery behavior:

## 5. Communications and schema

- Transport / protocol:
- Device identity field:
- Message / payload schema version:
- Required fields:
- Optional fields:
- Units:
- Null / missing-value semantics:
- Quality states:
- Fault states:
- Ordering / sequence semantics:
- Maximum accepted latency, if validated:

## 6. CS1 consumer review

Required when a change can alter downstream inference, analytics or decisions.

- Downstream CS1 consumer:
- Input fields used by model / decision logic:
- Capture / sampling timing assumptions:
- Calibration identifiers consumed:
- Quality/fault states consumed:
- Representation constraints (resolution, compression, depth encoding, etc.):
- Backward-compatibility requirement:
- CS1 review status / evidence:

EHB must not silently redefine CS1 model/readiness/confidence/decision semantics. CS1 must not silently redefine the physical source or embedded behavior.

## 7. Verification ownership

### EE verifies

- measurement correctness;
- calibration validity;
- uncertainty / limitations;
- field-validity evidence appropriate to the claimed evidence class.

### EHB verifies

- electrical / embedded implementation;
- firmware behavior;
- communications and schema emission;
- buffering / retry / restart behavior;
- device-side fault handling and bring-up.

### Shared system verification

- end-to-end interface compatibility;
- version compatibility;
- schema and units consistency;
- fault propagation;
- safe behavior across disconnect / restart / invalid data cases.

## 8. Evidence and safety gate

- Evidence class: `ASSUMPTION | DATASHEET | CALCULATION | SIMULATION | BENCH_TEST | FIELD_TEST | PRODUCTION_EVIDENCE`
- Physical safety gate required: `YES | NO`
- Safety reviewer / evidence, when required:
- Known blockers:

Do not promote an evidence label merely because documentation, simulation or software tests are complete.

## 9. Change control

Any material change to voltage/pinout, sampling, calibration persistence, protocol/schema, units, quality/fault semantics, timestamp behavior or verification ownership requires review by all affected owners before integration. Device/data-contract changes that affect downstream inference or decisions require CS1 consumer review.
