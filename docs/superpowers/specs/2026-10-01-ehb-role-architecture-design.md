# EHB Role Architecture Design

Date: 2026-10-01
Status: Proposed / awaiting written-spec approval
Scope: Convert BOUNCAMPUS from a four-role KREATE operating model to a five-role model by adding an independent EHB role.

## Intent

Add a fifth core role, **EHB — Embedded Hardware, Communications & Integration Lead**, that is organizationally independent from EE, owns embedded/electronic implementation and hardware/software communications, and materially reduces EE's hardware workload without weakening coordination.

The role must be a peer of IE, EE, CS1, and CS2, not a sub-role or lane under EE.

## Why this role exists

The current EE role combines two distinct responsibility families:

1. physical measurement strategy and validity;
2. electronics/embedded implementation and integration.

That coupling creates avoidable workload concentration. EHB separates implementation-heavy electronics, firmware, communications, and integration work from measurement-science ownership while retaining a formal EE↔EHB contract.

## Five core roles

1. IE — Customer Discovery & Market Lead
2. EE — Physical Systems & Measurement Lead
3. EHB — Embedded Hardware, Communications & Integration Lead
4. CS1 — Decision Intelligence Lead
5. CS2 — Product Strategy, Evidence Synthesis & Application Lead

## Ownership boundary

### EE final ownership

EE owns the truth of the physical measurement system:

- what physical variable should be measured;
- sensor/measurement strategy;
- required accuracy, repeatability, uncertainty, and calibration;
- physical placement and operational measurement workflow;
- measurement validity and quality semantics;
- pilot measurement SOPs;
- hardware-vs-no-hardware decision at the measurement-system level;
- field constraints that affect measurement correctness.

EE may still design hardware where useful, but it is no longer expected to own all embedded/electronics execution.

### EHB final ownership

EHB owns the embedded/electronic system that makes the physical measurement architecture usable:

- schematic design;
- PCB/module design and layout;
- MCU/SoC/controller selection;
- digital/analog interfaces around the controller;
- power/interface electronics in coordination with EE requirements;
- firmware architecture and implementation;
- UART, I2C, SPI, CAN where applicable, BLE, Wi-Fi, Ethernet, or other device communications;
- device telemetry;
- local buffering and store-and-forward behavior;
- device identity and provisioning interfaces;
- watchdog/recovery behavior;
- board bring-up;
- hardware/firmware debugging;
- test jigs and interface-level verification;
- HW↔firmware↔backend integration;
- device protocol and packet/schema implementation;
- hardware integration documentation.

EHB may independently create hardware designs and prototypes. It is not an EE assistant role.

## Shared EE↔EHB contract

EE and EHB must coordinate through an explicit interface contract when work crosses the measurement/electronics boundary.

At minimum, the contract should define the relevant subset of:

- sensor/interface electrical requirements;
- supply voltage/current limits;
- pinout and connector definitions;
- ADC/interface expectations;
- sampling rate and timing requirements;
- calibration data ownership and persistence;
- communication protocol;
- packet/event schema;
- units and scaling;
- quality/status/error flags;
- power budget;
- startup/shutdown behavior;
- offline behavior;
- fault states;
- recovery/retry behavior;
- test points and validation method.

Changes that alter this contract require cross-role review from both EE and EHB.

## Decision rights

- Measurement correctness dispute → EE has final technical ownership.
- Embedded/comms/interface implementation dispute → EHB has final technical ownership.
- Interface changes affecting both domains → dual review is mandatory.
- Product-direction disputes → follow the existing product/human-gate process.
- Physical-safety issues → existing PHYSICAL_SAFETY gate remains mandatory.

## Branch architecture

EHB receives its own long-lived role integration branch:

`role/ehb-embedded-integration`

Normal EHB task branches follow existing agent branch conventions and may use lanes such as:

- `agent/ehb-hardware/<task>`
- `agent/ehb-firmware/<task>`
- `agent/ehb-comms/<task>`
- `agent/ehb-integration/<task>`
- `agent/ehb-verification/<task>`

These task branches PR into `role/ehb-embedded-integration`, then the role branch integrates to `master` using the same exact-head, latest-master, CI, feature-preservation, and post-merge verification rules used by other roles.

## Fabric changes

`.agents/fabric.json` should be updated to:

- add `ehb: role/ehb-embedded-integration` to `role_branches`;
- change hardware ownership from a single `primary_role: ee` model to an explicit split model;
- keep measurement/calibration-focused lanes associated with EE;
- associate embedded electronics, firmware, communications, PCB, and integration lanes with EHB;
- retain shared physical-safety and evidence rules;
- preserve existing per-role integration limits and merge discipline.

Recommended hardware ownership representation:

- EE: measurement architecture, sensors as measurement devices, calibration, uncertainty, field/pilot verification;
- EHB: embedded electronics, PCB, firmware, communications, power/interface implementation, bring-up, HW-SW integration;
- shared: system-level hardware verification and any interface contract spanning both roles.

## Role-document changes

Create a new role document:

`KREATE/ROLES/05_EHB_EMBEDDED_HARDWARE_COMMUNICATIONS_INTEGRATION_LEAD.md`

Update:

- `KREATE/ROLES/00_ROLE_SYSTEM_SUMMARY.md`
- `KREATE/ROLES/README.md`
- `KREATE/ROLES/02_EE_PHYSICAL_SYSTEMS_MEASUREMENT_LEAD.md`
- `AGENTS.md`
- `.agents/WORKSTREAMS.md`
- `.agents/FABRIC.md`
- `.agents/fabric.json`
- any role-count checks, schemas, scripts, or CI validations that currently assume exactly four roles.

## EHB↔CS1 coordination

EHB owns reliable transport and device-side semantics; CS1 owns the decision/model semantics that consume the data.

The two roles must align on:

- event/data schema;
- timestamps and ordering;
- missing/invalid reading representation;
- quality flags;
- device metadata needed for modeling/evaluation;
- duplicate handling;
- offline replay semantics;
- API expectations that affect firmware behavior.

A device payload that reaches the backend but cannot be interpreted reliably is not considered integrated.

## EHB↔CS2 coordination

EHB provides credible implementation evidence for product claims while CS2 controls product/application framing.

EHB must not allow prototype behavior to be described as production-ready without evidence.

## EHB↔IE coordination

IE operational findings should inform provisioning, installation, connectivity, maintenance burden, and operator interaction. EHB should return feasibility constraints that can improve PMR questions.

## Workload-sharing model with EE

EHB should actively reduce EE workload by taking independent execution packages, not by waiting for micro-tasks.

Typical split examples:

### Example A: smart weighing node

EE:
- load-cell choice and measurement requirements;
- calibration plan;
- repeatability/uncertainty criteria;
- physical mounting constraints.

EHB:
- HX711/ADC interface design;
- MCU/controller design;
- PCB/schematic;
- firmware;
- Wi-Fi/BLE path;
- buffering;
- protocol;
- backend integration;
- board-level debug.

### Example B: existing commercial scale integration

EE:
- determine whether the scale's measurements satisfy the operational need;
- define required sampling/quality semantics.

EHB:
- investigate RS232/USB/BLE/network interfaces;
- build the adapter/gateway;
- implement protocol parsing;
- buffer and forward data;
- verify reconnect/error behavior.

## Coordination rules

1. Each cross-role hardware task names one primary owner: EE or EHB.
2. Touched paths remain exclusive under the existing task-claim system.
3. Shared interface changes must list the impacted role and require cross-role review.
4. No silent schema, voltage, pinout, sampling, or protocol changes.
5. EE and EHB may work in parallel when the interface contract is stable.
6. When the interface is not yet stable, create a bounded interface-definition task before deep implementation.
7. Bench/simulation evidence must be labeled under the existing evidence taxonomy and never upgraded beyond what was actually tested.

## Human checkpoint policy

EHB should follow the technical-role default used by EE/CS1: no routine post-work strategic checkpoint unless an existing human gate is triggered.

Recommended checkpoint state:

- IE: ON
- EE: OFF
- EHB: OFF
- CS1: OFF
- CS2: ON

## Anti-slop requirements

EHB must reject:

- fabricated datasheet claims;
- unverified pinouts or voltage compatibility;
- fake bench results;
- simulated behavior presented as physical evidence;
- firmware declared reliable without failure-path tests;
- generic IoT diagrams that are not tied to a real requirement;
- unnecessary custom PCB work where an off-the-shelf path is better;
- production-readiness claims without production evidence.

## Validation requirements for implementation

The role-system migration is complete only when:

1. the five-role documentation is internally consistent;
2. EHB has its own long-lived role branch;
3. fabric/configuration recognizes EHB as a first-class role;
4. hardware ownership is explicitly split between EE and EHB;
5. role-count-dependent scripts/checks pass with five roles;
6. agent-fabric validation passes;
7. KREATE validation passes;
8. feature-preservation checks pass;
9. no existing EE/IE/CS1/CS2 branch flow is broken;
10. a sample EHB task can be represented using the coordination schema;
11. cross-role EE↔EHB ownership/review rules are documented;
12. master is verified after eventual merge.

## Non-goals

This change does not:

- redesign the product itself;
- force the team to build custom hardware;
- move measurement-science ownership away from EE;
- move model ownership away from CS1;
- create a hierarchy where EHB reports to EE;
- weaken evidence, safety, or merge gates;
- require hardware work to block software work when interfaces are stable.

## Recommended implementation approach

Use a focused repository-governance migration:

1. add the EHB role document;
2. update role navigation and collaboration documentation;
3. update `AGENTS.md`, workstreams, and fabric configuration;
4. update role-count assumptions in scripts/CI;
5. create `role/ehb-embedded-integration` from verified master;
6. run repository governance/agent validation;
7. open a governance PR and merge only after exact-head checks pass.

This approach preserves the current role-branch model while adding EHB as an equal fifth integration lane.
