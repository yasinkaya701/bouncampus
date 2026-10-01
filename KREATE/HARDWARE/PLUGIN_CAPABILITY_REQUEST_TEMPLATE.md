# Hardware Plugin Capability Request Template

Use this only when a missing specialized capability would materially improve or unblock hardware work.

## Capability gap

What engineering capability is missing?

Examples: PCB CAD review, SPICE/circuit simulation, component lifecycle lookup, firmware debug, mechanical CAD, DFM/DFT analysis, signal/power-integrity review, or remote bench measurement.

## Why it matters

State the exact decision, verification step, or acceptance criterion the capability would improve or unlock.

## Work that can continue now

List useful work that does not depend on the plugin/capability. Continue that work instead of blocking unnecessarily.

## What remains unverified without it

Be explicit about evidence maturity. Example:

`The analog-front-end topology can be documented now, but stability/noise behavior remains SIMULATION/ASSUMPTION until an appropriate circuit simulation or bench capability is available.`

## Requested user action

Ask the user to install/connect/enable/authorize a plugin or capability only when needed. Name a specific plugin only if it has actually been discovered and is relevant.

An optional capability request is not a Fabric human gate. Use `BLOCKED` only when the capability is genuinely necessary to meet acceptance criteria and no safe alternate route exists.

Never ask the user to paste passwords, API keys, secrets, or private credentials into chat or repository files when a normal authorization flow exists.
