---
name: evals-component-analysis
description: Analyze a repository component from technical and functional perspectives and create an approved handoff for downstream LLM evaluation criteria design. Use when the eval pipeline reaches component analysis.
user-invocable: false
---

# Evals Component Analysis

Research one component thoroughly and create an approved description that the
criteria-design stage can use without repeating repository discovery.

## Input

The invoking agent provides:

```text
Component: {component}
```

Read all other context directly from the repository.

Required project prerequisite:

```text
evals/config.yaml
```

When it is absent, stop and report that project initialization is required.

## Artifacts

Working draft:

```text
evals/components/{component}/README.draft.md
```

Completion artifact:

```text
evals/components/{component}/README.md
```

The final `README.md` is pipeline state. Do not create or overwrite it until the
user explicitly approves the component understanding.

If a draft already exists, treat the task as a continuation. Read it before
researching further and preserve confirmed information unless repository
evidence or the user corrects it.

## Scope

Analyze the component from two complementary angles.

### Technical angle

Explain what the component is in code and how it executes:

- code boundary, entry points, and ownership;
- public and internal interfaces;
- accepted inputs and emitted outputs;
- execution lifecycle and major control flow;
- model, prompt, tool, retrieval, or provider interactions;
- dependencies and downstream consumers;
- configuration, feature flags, and environment assumptions;
- state, caching, concurrency, persistence, and side effects;
- errors, retries, fallbacks, timeouts, and partial results;
- observability, traces, logs, events, and intermediate artifacts;
- nondeterministic behavior and external variability;
- existing tests, examples, fixtures, and documentation.

Read `references/technical-research.md` when performing this analysis.

### Functional angle

Explain why the component exists and what correct behavior means in the actual
product or workflow:

- user, business, or system problem being solved;
- callers, consumers, and position in the end-to-end flow;
- primary goal and value delivered by the component;
- important decisions or transformations it owns;
- expected behavior for normal, ambiguous, incomplete, and difficult inputs;
- behavior that is acceptable, unacceptable, or intentionally variable;
- constraints and invariants that must be preserved;
- tradeoffs the component is expected to make;
- consequences of incorrect behavior;
- domain nuances that are not obvious from interfaces alone;
- facts the criteria-design stage must know before proposing evaluations.

Read `references/functional-research.md` when performing this analysis.

## Research method

1. Resolve the concrete repository boundary for the named component.
2. Search broadly before drawing conclusions. Follow callers and consumers, not
   only the component's own directory.
3. Inspect implementation, configuration, prompts, schemas, tests, examples,
   docs, and integration points.
4. Trace at least one representative execution path from input to output.
5. Distinguish code-level mechanics from intended functional behavior.
6. Record repository evidence for material claims using file paths and symbols.
7. Mark each important statement as one of:
   - **Confirmed**: directly supported by repository evidence or user input.
   - **Inferred**: strongly suggested by evidence but not explicitly defined.
   - **Unknown**: important information that cannot be established.
8. Prefer explaining behavior and responsibility over copying code details.
9. Identify contradictions between code, tests, documentation, and naming.
10. Do not invent intended behavior when the repository is ambiguous.

Do not stop after finding the primary class or function. The downstream stage
needs both the implementation boundary and the real functional purpose.

## Boundary rules

You may identify evaluation implications, such as which behaviors are critical,
observable, variable, or currently unobservable.

You must not:

- propose or finalize criterion names;
- select Basic or Quality criteria;
- define metrics or score thresholds;
- choose grader types;
- define dataset records;
- implement evaluation files beyond this stage's analysis artifacts.

Phrase handoff information as expected behavior and evaluation readiness, not as
a criteria proposal.

## Draft creation

Create or update the working draft using:

```text
templates/component-readme.md
```

Follow the complete output contract in:

```text
references/output-contract.md
```

The draft must be useful to a new agent that has not seen the current
conversation. It must contain enough evidence and nuance that criteria design
does not need to repeat the component research.

## User validation

After the draft is complete:

1. Present a concise review containing:
   - the component's primary functional goal;
   - its technical boundary and execution model;
   - the most important expected behaviors;
   - major failure modes and consequences;
   - important unknowns or disputed assumptions.
2. Ask the user to confirm or correct the understanding.
3. When the user provides corrections, update the draft and present the revised
   understanding again.
4. Repeat until the user explicitly approves the understanding.

Do not treat silence, partial agreement, or a request to continue as approval
when unresolved functional questions materially affect expected behavior.

## Finalization

After explicit approval:

1. incorporate all approved corrections into the draft;
2. set the document status to `Approved`;
3. record unresolved but accepted unknowns clearly;
4. write the completed content to:

   ```text
   evals/components/{component}/README.md
   ```

5. rename `README.draft.md` into `README.md` when it is finalized and approved;
6. report the completion artifact path.

Do not create files belonging to criteria, datasets, graders, runners,
manifests, suites, or policies.
