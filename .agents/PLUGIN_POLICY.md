# Agent Plugin and External Capability Policy

## Purpose

BOUNCAMPUS agents are allowed and encouraged to use available plugins, connectors, specialized tools, and external capabilities when they materially improve evidence quality, engineering rigor, speed, or verification.

Plugins are tools, not authorities. Repository truth, measured evidence, official sources, test output, and explicit human decisions remain the source of truth.

## Default behavior

Agents SHOULD proactively use an already available plugin when it is a better tool for the task than generic chat reasoning or ad-hoc manual work.

Examples include:

- GitHub/repository tooling for code, PRs, branches, CI, issues, and review;
- academic/research plugins for literature and technical evidence;
- design/CAD/diagram tools for engineering communication;
- deployment/runtime tools for application verification;
- spreadsheet/data-analysis tools for measurements and BOMs;
- hardware/electronics tools for schematic, PCB, simulation, component, datasheet, firmware, or test workflows when such tools are available;
- meeting/email/calendar/connectors when the task explicitly depends on those records or actions.

An agent must not pretend a plugin was used when it was not, and must not fabricate output from a tool it cannot access.

## Plugin discovery

When a task would benefit materially from a specialized capability, the agent MAY inspect the available plugin/tool catalog before choosing a weaker manual workflow.

The agent should prefer a relevant installed/connected capability over inventing a workaround when the plugin can provide stronger evidence or direct execution.

## Asking the user for a plugin

Agents are explicitly allowed to ask the user to install, enable, connect, or authorize a plugin when all of the following are true:

1. the missing capability would materially improve or unlock the current work;
2. the request is specific about what capability is needed and why;
3. the agent does not falsely claim that a particular plugin exists if it has not been discovered;
4. the requested access is proportionate to the task;
5. the agent continues with useful work that does not depend on the plugin whenever a safe fallback exists.

A plugin request is not automatically a `WAITING_HUMAN` task state. If useful work can continue without it, continue working and treat the plugin as an acceleration/enrichment request.

A task should become blocked on plugin access only when the required capability cannot be reproduced safely or credibly with available tools and the missing access prevents the acceptance criteria from being met.

## Hardware-specific plugin requests

The EE / hardware agent may request specialized capabilities when useful, including categories such as:

- schematic / PCB CAD and review;
- SPICE or circuit simulation;
- BOM sourcing and component lifecycle/availability data;
- datasheet and reference-design retrieval;
- MCU/firmware build and debug tooling;
- mechanical CAD / enclosure design;
- signal/power-integrity analysis;
- laboratory instrument or remote-bench access;
- manufacturing DFM/DFT checks;
- image/diagram generation for hardware communication.

The agent should state the exact capability gap, for example: `I can finish the architecture and firmware contract now; connecting a PCB/SPICE capability would let me verify the analog front end instead of leaving it as an unvalidated design assumption.`

## Security, privacy, and credentials

Agents must use the least privilege needed. They must never ask the user to paste secrets, passwords, API keys, or private credentials into repository files or chat when a normal connection/authorization flow exists.

Plugin output that contains private or sensitive information must not be copied into public artifacts unless the user explicitly intends that disclosure and it is safe to do so.

## Evidence boundary

Plugin output is classified by what it actually represents:

- a datasheet retrieved through a plugin is source evidence;
- a simulator result is simulated evidence, not bench evidence;
- a BOM price is a point-in-time sourcing observation, not a guaranteed procurement price;
- CAD/PCB checks are design verification, not proof of manufactured hardware;
- an AI-generated schematic suggestion is a hypothesis until checked;
- a remote instrument measurement may count as physical evidence only when provenance and test conditions are recorded.

Plugins never authorize agents to convert estimates or simulations into measured claims.

## Reporting

When plugin use materially affects a conclusion, the agent should record:

- capability/tool used;
- input/source context;
- important assumptions;
- output/evidence produced;
- limitations or unresolved validation;
- repository artifact or task affected.

The goal is not to maximize plugin usage. The goal is to use the strongest available capability for the work while keeping the result reproducible and auditable.
