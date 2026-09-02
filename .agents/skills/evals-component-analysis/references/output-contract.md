# Component Analysis Output Contract

The completion artifact is:

```text
evals/components/{component}/README.md
```

It is the authoritative handoff from component analysis to criteria design.

## Required qualities

The document must be:

- self-contained;
- grounded in repository evidence and user-confirmed intent;
- understandable without the analysis conversation;
- explicit about confirmed facts, inferences, and unknowns;
- detailed enough to avoid repeating repository research;
- focused on behavior rather than exhaustive code narration;
- neutral about future criteria and grader implementation.

## Evidence format

For material technical claims, include repository references using paths and,
when useful, symbols:

```text
`src/search/retriever.py::Retriever.retrieve`
```

When behavior is inferred, state why. When evidence conflicts, record the
conflict rather than selecting one interpretation silently.

## Required sections

### 1. Status

Must contain:

```text
Status: Approved
```

Only the final completion artifact may use this status.

### 2. Executive summary

A short description of:

- what the component does;
- why it exists;
- its primary functional goal;
- where it sits in the system.

### 3. Component boundary

Define what is inside and outside the component. Name adjacent components and
ownership boundaries.

### 4. Technical analysis

Cover:

- implementation locations;
- entry points and callers;
- interfaces;
- input semantics;
- execution flow;
- outputs and side effects;
- dependencies and configuration;
- state and concurrency;
- failures, retries, and fallbacks;
- observability;
- nondeterminism;
- existing tests and examples.

### 5. Functional analysis

Cover:

- user or system problem;
- consumers and workflow role;
- primary and secondary goals;
- important decisions;
- expected normal behavior;
- ambiguity and incomplete-data behavior;
- invariants and prohibitions;
- accepted variability;
- quality tradeoffs;
- failure modes and consequences;
- domain-specific nuances.

### 6. Expected behavior handoff

Organize concise statements under:

- **Must do**
- **Must not do**
- **Should optimize for**
- **May legitimately vary**

These are behavioral facts for the next stage, not named criteria.

### 7. Scenario inventory

List representative categories, not full datasets:

- normal scenarios;
- difficult scenarios;
- ambiguous or incomplete scenarios;
- known regression or failure scenarios;
- scenarios outside the component's responsibility.

### 8. Evaluation readiness

Document:

- controllable inputs;
- observable outputs and intermediate signals;
- expected values that can be authored;
- important hidden decisions;
- missing instrumentation;
- environmental dependencies;
- blockers or risks for future evaluation.

### 9. Assumptions and unknowns

Separate:

- accepted assumptions;
- unresolved unknowns;
- conflicts in repository evidence;
- questions intentionally deferred to criteria design.

### 10. Evidence index

Provide a compact list of the most important repository files and what each one
establishes.

### 11. Approval record

Record that the user approved the component understanding. Do not invent a user
name.

## Prohibited content

Do not include:

- finalized criterion names;
- Basic or Quality grouping proposals;
- metric formulas or thresholds;
- grader choices or prompts;
- dataset record definitions;
- implementation plans for the eval framework.
