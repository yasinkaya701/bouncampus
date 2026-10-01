# KREATE Hardware

Hardware-specific execution lives here under the persistent `HUMAN-EE` parent workstream.

- [`HARDWARE_AGENT_PLAYBOOK.md`](HARDWARE_AGENT_PLAYBOOK.md) — EE/hardware agent workstreams, evidence maturity, PCB/power/firmware/calibration/BOM/DFM/DFT expectations, safety gates, tool usage, and merge checklist.
- [`PLUGIN_CAPABILITY_REQUEST_TEMPLATE.md`](PLUGIN_CAPABILITY_REQUEST_TEMPLATE.md) — structured request for a missing specialized capability without unnecessarily blocking other work.
- [`../ROLES/02_EE_PHYSICAL_SYSTEMS_MEASUREMENT_LEAD.md`](../ROLES/02_EE_PHYSICAL_SYSTEMS_MEASUREMENT_LEAD.md) — EE role mission and ownership.
- [`../../.agents/PLUGIN_POLICY.md`](../../.agents/PLUGIN_POLICY.md) — repository-wide plugin discovery/use/request policy.
- [`../../.agents/FABRIC.md`](../../.agents/FABRIC.md) — parent/child execution, path leases, critical human gates, and integration rules.

Hardware is justified by measurable operational value and evidence quality, not by demo appearance. Simulations, CAD, calculations, and datasheets must remain explicitly separated from bench, field, and production evidence.

The EE parent may fan out 50+ hardware child agents when tasks have non-overlapping `touched_paths` and clear interfaces. Typical child lanes include measurement, sensors/AFE, power, firmware, PCB, mechanical, calibration, sourcing, and verification. Child hardware work integrates into `work/ee/<slug>`, never directly to `master`.
