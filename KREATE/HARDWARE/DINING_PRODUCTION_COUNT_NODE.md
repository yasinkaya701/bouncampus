# Dining Production Count Node — Deterministic Integration Path

Issue: #331  
Parent: #298  
Owner: EHB — Embedded Hardware, Communications & Integration  
Status: design decision only. No access, installation, BENCH_TEST, FIELD_TEST, or production-readiness claim.

## Decision

Do **not** start by adding a camera or free-running sensor to infer how many portions were produced.

Use this priority order:

1. **existing aggregate production record/export** owned by the kitchen/operations system, if it can emit an immutable batch/portion record at the required service horizon;
2. **deterministic machine/control signal** such as an isolated dry contact or pulse from an existing production/dispensing process, but only when the equipment owner and electrical interface are known and safe;
3. **local operator-confirmed batch/portion event** through a minimal dedicated node when no trustworthy system/machine signal exists;
4. new physical inference is a last resort and requires a separate measurement justification.

The node therefore exists as an **integration adapter**, not as a novelty sensor.

## Required output

The merged CS1 consumer contract already expects:

```json
{
  "eventId": "production-2026-10-06-000123",
  "deviceId": "production-count-north-01",
  "stationId": "north-kitchen-production-01",
  "timestamp": "2026-10-06T10:35:00+03:00",
  "measurementType": "PRODUCED_PORTION_DELTA",
  "value": 120,
  "unit": "PORTIONS",
  "quality": "VALID",
  "source": "PHYSICAL_MEASUREMENT",
  "firmwareVersion": "production-node-fw-v1",
  "schemaVersion": "dining-count-event-v1"
}
```

Semantics:

- `value` is a positive **delta**, not a cumulative display value;
- one `eventId` identifies one immutable physical/operational count event;
- retries must reuse the exact same payload under the same `eventId`;
- a changed payload under an existing `eventId` is a conflict, not a correction;
- corrections require a **new event** with explicit operational provenance; do not mutate historical evidence;
- EHB must not emit `actual_served`, surplus, shortage, waste, or savings fields.

## Architecture decision tree

```text
Can Food Services / kitchen system export
a stable aggregate production batch/portion record?
            |
       yes  |  no
            |
            v
   ingest owner-generated
   aggregate record
                       Is there a safe deterministic
                       machine/contact/pulse signal?
                                |
                           yes  |  no
                                |
                                v
                      isolated digital input
                      + EHB event adapter
                                           Can operator confirm
                                           produced batch/portion
                                           with low burden?
                                                |
                                           yes  |  no
                                                |
                                                v
                                     local confirmation node
                                                             stop and
                                                             re-evaluate
                                                             measurement
```

## Path A — existing production export

Preferred when available.

Required fields or deterministic mappings:

- source record ID;
- batch/service timestamp;
- station/kitchen identity;
- produced portion delta or a source-owner-confirmed field that maps to it;
- correction/reversal semantics;
- source-system version/export provenance.

EHB should not fabricate an edge device when this route closes the measurement gap.

This repository currently makes **no claim that such an export is available**.

## Path B — deterministic equipment signal

Use only after the equipment owner confirms the interface and physical-safety boundary.

Example signal classes:

- dry contact;
- opto-isolated digital pulse;
- low-voltage counter output;
- vendor-supported serial/fieldbus counter register.

Do not tap unknown machine/mains wiring autonomously. Equipment modification, energized cabinet work, or an unknown industrial control interface remains a `PHYSICAL_SAFETY` / owner-supervised activity.

### Event conversion

If one equipment pulse does not directly equal one portion, EHB must not silently multiply it by a guessed batch factor.

Allowed mappings require an explicit configuration version, for example:

```text
source pulse -> accepted batch event
accepted batch event + owner-confirmed portions-per-batch configuration
-> PRODUCED_PORTION_DELTA
```

The configuration version and provenance must be retained for later reconciliation.

## Path C — local confirmation node

Fallback when no trustworthy export or machine signal exists.

Operator action should be minimal:

1. finish a production batch;
2. enter/confirm the actual produced portion delta;
3. node validates positive integer input;
4. node creates a new stable anonymous `eventId`;
5. payload enters the persistent EHB edge queue;
6. UI shows queued/sent state without allowing silent history rewrite.

A cancellation or correction creates a traceable new operational record. The first event is not rewritten.

## Reference embedded platform

If a dedicated node is required, **ESP32-S3 class hardware** is a suitable reference architecture, not a frozen procurement choice.

Relevant manufacturer facts:

- 2.4 GHz IEEE 802.11b/g/n Wi-Fi;
- Bluetooth LE 5;
- GPIO plus pulse-count peripheral;
- watchdog/timers and common embedded interfaces;
- 3.0–3.6 V module supply class depending on module.

Sources:

- https://documentation.espressif.com/esp32_s3_datasheet_en.pdf
- https://documentation.espressif.com/esp32-s3-wroom-2_datasheet_en.html

Evidence class: `DATASHEET`.

The repository does not claim that Wi-Fi coverage exists at the intended installation point. Fixed Ethernet should be preferred where infrastructure and installation constraints justify it.

## Block diagram — dedicated fallback node

```text
owner-approved source
(dry contact / pulse / operator confirm)
              |
      isolation / debounce
              |
        ESP32-S3-class MCU
        |       |       |
 timestamp   local UI   diagnostics
        |
 immutable event builder
        |
 persistent EHB queue
        |
 Wi-Fi / approved network path
        |
 CS1 dining-count admission
```

## Power boundary

Preferred prototype/development boundary:

- SELV low-voltage input only;
- no custom mains conversion;
- powered from an approved external supply;
- equipment-side signal is isolated where the source voltage/domain requires it;
- reverse-polarity / overcurrent / ESD protection is selected once actual interface voltage and connector are known.

If an existing machine exposes 12/24 VDC signals, the MCU must not be connected directly. Use an appropriate isolated/conditioned input stage after interface verification.

Exact regulator, isolator and connector MPNs remain unresolved until the selected source path is known.

## Firmware state machine

```text
BOOT
  |
load identity + config
  |
SELF_CHECK
  |
SOURCE_READY
  |
receive deterministic count
  |
VALIDATE
  | invalid -> reject + diagnostic
  v
BUILD_EVENT
  |
ENQUEUE_IMMUTABLE
  |
DELIVERY_RUNTIME
  | offline -> keep queued + backoff
  | ack     -> retain replay tombstone
  v
SOURCE_READY
```

The delivery layer is owned by #299 and must preserve exact payload identity across retries.

## Timestamp discipline

- device timestamps are timezone-aware;
- UTC storage is preferred internally;
- event payload may use an explicit offset;
- loss of trustworthy time must produce a quality/error state rather than a plausible invented timestamp;
- clock correction must not rewrite already-queued immutable events.

## Duplicate and correction handling

### Duplicate transport retry

Same `eventId` + same payload:

- permitted;
- queued/sent idempotently;
- counted once downstream.

### Reused identity with changed payload

Same `eventId` + different payload:

- fail closed;
- diagnostic: replay conflict;
- do not auto-select either value.

### Operational correction

If an operator/source owner corrects a production record:

- create a new stable source/event record;
- retain the original;
- preserve a reconciliation link if the source system provides one;
- CS1/service-truth reconciliation decides whether/how the correction affects accepted service truth.

## Failure modes

| Failure | Required behavior |
|---|---|
| network unavailable | persist event; retry through #299 runtime |
| restart after enqueue | recover exact pending payload |
| restart after server received event but before local ACK | resend exact payload; downstream deduplicates |
| repeated contact bounce | input debounce/state logic; do not generate uncontrolled events |
| stuck input | health fault; no repeated synthetic counts |
| invalid operator entry | reject locally; no event |
| unknown timestamp | withhold/error state; do not invent time |
| changed payload under old eventId | fail closed |
| source mapping/version unknown | do not emit decision-grade produced portions |
| local storage full/corrupt | explicit health fault; no silent drop |
| device identity missing | refuse event generation |

## Acceptance tests — design and future bench

### Software / deterministic tests

- identical input record produces stable event payload;
- retry preserves byte/JSON-equivalent payload;
- changed-payload identity reuse fails closed;
- queue survives process restart;
- network failure never deletes an unacknowledged event;
- count value must be a positive integer;
- emitted measurement type/unit are exactly `PRODUCED_PORTION_DELTA / PORTIONS`.

### Future bench tests

Only after a real input path is selected:

- exercise at least 100 known source transitions and compare raw source vs emitted unique events;
- test contact bounce / noisy transition handling;
- power-cycle during enqueue and during retry;
- disconnect/reconnect network;
- verify storage-full and clock-invalid behavior;
- measure actual supply/current/thermal conditions;
- record all misses, duplicates and withheld events.

No pass percentage is invented before this test exists.

## Evidence boundary

| Item | Current evidence |
|---|---|
| CS1 event schema | repository contract |
| ESP32-S3 capabilities | `DATASHEET` |
| architecture priority | `ASSUMPTION` / engineering decision |
| exact production source available at Boğaziçi | unknown |
| machine interface voltage/protocol | unknown |
| operator burden | unknown until PMR/operations verification |
| input-count accuracy | no `BENCH_TEST` yet |
| field reliability | no `FIELD_TEST` yet |

## Exit criterion for #331

The design slice is complete when:

- deterministic-source priority is explicit;
- event semantics match the merged CS1 consumer;
- hardware is only introduced when simpler integration cannot close the gap;
- power/safety boundaries are explicit;
- duplicate/correction behavior is fail-closed;
- acceptance tests exist;
- no unsupported production-source or accuracy claim is introduced.
