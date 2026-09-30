# KREATE Research Packs

This directory contains secondary/public-source research prepared for KREATE agents. It is a shared **research layer**, not the evidence registry and not PMR.

## Claim boundary

- Nothing in this directory counts as `INTERVIEW EVIDENCE` or customer validation.
- Official university pages and reports may become `PUBLIC_SOURCE` evidence only after a domain owner narrows the claim and promotes it into `../EVIDENCE.md`.
- Academic papers are benchmarks and design references. A result from another university does **not** prove the same mechanism exists at Boğaziçi.
- Apparent inconsistencies in source data are preserved as caveats; agents must not silently repair them.
- Model or scenario implications derived from these sources remain `HYPOTHESIS`, `POLICY_HEURISTIC`, or `MODEL ESTIMATE` until separately validated.

## Available packs

| Pack | Purpose | Machine-readable companion |
| --- | --- | --- |
| [Boğaziçi Sustainability 2025](./BOGAZICI_SUSTAINABILITY_2025.md) | Deep secondary research from Boğaziçi sustainability/SDG sources plus peer-reviewed institutional-dining literature; includes food, water, energy, transport, data-quality caveats, PMR questions and role-specific handoffs. | [`bogazici_sustainability_2025.json`](./bogazici_sustainability_2025.json) |

## How agents should consume a pack

1. Read the **agent-critical takeaways** and **claim firewall** first.
2. Use `fact_id` / `finding_id` references when creating downstream tasks or experiments.
3. Before promoting a number into `../EVIDENCE.md`, reopen the source, verify wording/date/units, and write a claim no broader than the source supports.
4. Route unknown workflow facts to PMR rather than filling them with assumptions.
5. Route quantitative/model implications to reproducible technical tests rather than presenting them as measured campus performance.
