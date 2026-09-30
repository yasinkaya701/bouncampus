# User Decision Checkpoint Protocol

## Purpose

BOUNCAMPUS agents should be autonomous **inside an accepted work package**, but they must not blindly choose the next strategic direction after that work is complete.

The operating rule is:

> **Finish the current work. Prove what happened. Then pause at the next meaningful branch and help the user choose.**

This protocol exists to avoid two bad extremes:

1. repeatedly asking the user for permission during routine, reversible work; and
2. completing one useful task and then continuing indefinitely into a new product, market, hardware, model, or application direction without giving the user control.

## 1. Do Not Interrupt the Current Work Package

Once an agent accepts a bounded work package, it should execute it end-to-end without asking the user to approve routine implementation details.

The agent should normally decide autonomously within the accepted scope when the choice is:

- reversible,
- low-risk,
- technically routine,
- testable,
- not a material product-direction decision,
- not an external commitment,
- not a real-world evidence attestation,
- not a physical-safety decision.

Examples that should normally **not** trigger a user question:

- file naming,
- refactoring structure,
- which test helper to use,
- minor UI implementation details,
- retry logic,
- bounded model experiments,
- local parameter exploration,
- documentation cleanup,
- reversible branch/PR work,
- ordinary bug fixes inside the accepted task.

The user should receive a finished result, not a stream of permission requests.

## 2. A Decision Checkpoint Happens After Meaningful Completion

Before starting a **new significant workstream**, the agent must create a user decision checkpoint when one or more materially different next directions are available.

Typical checkpoint triggers include:

- the accepted task reached its Definition of Done;
- an experiment produced a decision-relevant result;
- PMR materially changed the problem understanding;
- a feature was validated, rejected, or became ambiguous;
- there are multiple plausible technical architectures;
- hardware versus hardware-free approaches now have meaningful trade-offs;
- the beachhead, persona, buyer, or core workflow could reasonably change;
- a new workstream would consume substantial time before the October 8 deadline;
- the next action changes the application narrative or an important claim;
- the next action creates a new dependency for another team member;
- the next step would move from exploration into a consequential implementation commitment.

At a checkpoint, the agent must **not silently choose a new strategic branch and continue**.

## 3. Required Checkpoint Package

A checkpoint must give the user enough information to make a real decision without having to reconstruct the work themselves.

Use the following structure.

### A. What was completed

State exactly what was finished.

Include concrete artifacts where relevant:

- files,
- commits,
- tests,
- interview count,
- benchmark results,
- calibration data,
- evidence IDs,
- updated assumptions,
- rejected hypotheses,
- application sections affected.

### B. What we learned

Separate:

- facts,
- observed evidence,
- interpretation,
- remaining uncertainty.

Do not convert weak evidence into certainty.

### C. What changed because of the result

Explain whether the result:

- strengthened the current direction,
- weakened it,
- killed an assumption,
- opened a new opportunity,
- created a blocker,
- changed feature priority,
- changed the likely customer,
- changed the technical path,
- changed what should appear in the KREATE application.

### D. Next-step options

Offer **2–4 materially different options** when multiple credible paths exist.

Do not create fake alternatives just to satisfy the format.

For each option include:

1. **Action** — what would be done next;
2. **Why** — why this option is credible now;
3. **Expected result** — what useful outcome or information it should produce;
4. **Cost / effort** — relative time, engineering effort, PMR effort, or coordination cost;
5. **Risk** — what could fail or what opportunity cost it creates;
6. **Dependencies** — people, hardware, data, access, or previous tasks required;
7. **KREATE effect** — how it could affect Top-15 selection probability or application quality.

### E. Recommendation

The agent should **take a position**.

Do not simply say “all options are valid.” State which option the agent recommends and why, based on current evidence and deadline pressure.

A recommendation is advice, not permission to override the user.

### F. Exact user decision needed

End with one concise decision request.

Good examples:

- “Choose A, B, or C for the next workstream.”
- “Do you want us to prioritize more operator PMR or hardware validation next?”
- “Should we keep university dining as the beachhead or spend one bounded cycle testing factory cafeterias first?”

Avoid vague questions such as:

- “What do you want me to do?”
- “Should I continue?”
- “Any thoughts?”

The agent must first provide enough analysis for the user to choose intelligently.

## 4. Decision Table Format

For important branches, prefer a compact table like this:

| Option | What happens next | Expected value | Cost | Main risk | KREATE impact |
|---|---|---|---|---|---|
| A | ... | ... | ... | ... | ... |
| B | ... | ... | ... | ... | ... |
| C | ... | ... | ... | ... | ... |

Then state:

**Recommended:** Option B because ...

**Decision needed:** A / B / C.

## 5. When There Is Only One Obvious Next Step

Do not force the user to choose between artificial options.

If the next action is:

- clearly implied by the existing task,
- low-risk,
- reversible,
- required to satisfy the same acceptance criteria,
- or merely finishing integration / verification,

continue autonomously.

A checkpoint is for a **new meaningful branch**, not every sequential subtask.

## 6. When the Agent Must Stop Before Completion

The agent may need user input before the current work package is complete when the blocker is genuinely human-owned, including:

- real-world evidence attestation,
- irreversible external action,
- physical safety decision,
- purchase or payment,
- final external submission,
- consequential outreach sent on behalf of the team,
- a material product/market pivot with multiple defensible directions.

Even then, the agent should complete all work independent of the decision first and present the same checkpoint package.

## 7. No Blind Continuation

Agents must not use autonomy as a reason to accumulate speculative work.

After finishing a meaningful work package, do not automatically:

- open a new major feature stream,
- pivot the market,
- redesign the architecture,
- start a new hardware concept,
- rewrite the application thesis,
- expand the product into another campus domain,
- spend a full work cycle on polish,
- or launch a large new PMR segment,

without first showing the user the result of the previous work and the available choices.

## 8. No Premature Asking

The opposite failure is also prohibited.

Agents should not stop halfway through routine work and ask the user to make technical decisions that the agent can resolve through:

- repository inspection,
- testing,
- research,
- small experiments,
- comparisons,
- reversible implementation.

The standard is:

> **Resolve what can be resolved. Surface what genuinely requires direction.**

## 9. Relationship to Role Autonomy

Role autonomy remains unchanged.

Any role may:

- investigate outside its nominal lane,
- challenge assumptions,
- propose experiments,
- discover opportunities,
- recommend pivots,
- contribute to another workstream.

The checkpoint protocol only changes **when the next strategic commitment is made**.

Agents are free to discover. The user retains control over meaningful direction changes.

## 10. KREATE-Specific Decision Priority

Until the October 8 application deadline, checkpoint recommendations should explicitly consider:

1. PMR / evidence value;
2. impact on Problem / Beachhead / Persona / PMR rubric quality;
3. time to evidence;
4. risk of unsupported claims;
5. differentiation value;
6. technical feasibility;
7. opportunity cost before the deadline.

A technically exciting option is not automatically the best next step.

## 11. Completion Message Standard

When a work package finishes and a real branch exists, the final response should resemble:

### Completed
- ...

### Evidence / result
- ...

### What this changes
- ...

### Options
| Option | Outcome | Cost | Risk | KREATE impact |
|---|---|---|---|---|
| A | ... | ... | ... | ... |
| B | ... | ... | ... | ... |

### Recommendation
**B**, because ...

### Decision needed
Choose **A or B** for the next workstream.

This is the required default behavior for KREATE agents whenever a completed work package leads to multiple meaningful next directions.
