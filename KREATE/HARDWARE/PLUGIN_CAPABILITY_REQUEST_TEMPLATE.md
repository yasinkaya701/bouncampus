# Hardware Plugin Capability Request Template

Use this when a missing specialized capability would materially improve hardware work.

## Capability gap

What engineering capability is missing?

Examples: PCB CAD review, SPICE simulation, component lifecycle lookup, firmware debug, mechanical CAD, DFM/DFT analysis, remote bench measurement.

## Why it matters

State the decision, verification, or acceptance criterion that the capability would improve or unlock.

## Work that can continue now

List the useful work that does not depend on the plugin. Continue this work instead of blocking unnecessarily.

## What remains unverified without it

Be explicit. Example: `The analog front-end topology can be documented now, but stability/noise behavior remains SIMULATION/ASSUMPTION until a suitable circuit simulation or bench capability is connected.`

## Requested user action

Ask the user to install/connect/enable/authorize a plugin that provides the required capability. Name a specific plugin only if it has actually been discovered and is relevant.

Never ask the user to paste secrets or credentials into chat/repository files when a normal authorization flow exists.
