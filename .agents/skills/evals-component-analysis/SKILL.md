---
name: evals-component-analysis
description: Understand a repository component and establish the approved behavioral contract used to design its evaluations.
user-invocable: false
---

# Evals Component Analysis

## Purpose

Establish what the component owns, how it behaves, and what parts of its behavior may matter for evaluation.

## Input

```text
Component: {component}
```

## Requires

```text
evals/config.yaml
```

## Workflow

1. Inspect the component implementation and relevant callers, tests, configuration, and documentation.
2. Establish:
   - purpose and responsibility;
   - component boundary;
   - inputs, outputs, state, and important dependencies;
   - expected behavior and important constraints;
   - legitimate variability or nondeterminism;
   - important failure behavior;
   - observable outputs and intermediate actions;
   - behavior that may matter for evaluation;
   - material unknowns or conflicting evidence.
3. Ground material claims in repository evidence.
4. Ask the user when missing or conflicting evidence materially affects the component responsibility or expected behavior.
5. Create or update:

```text
evals/components/{component}/README.md
```

using:

```markdown
# {Component}

Status: Pending approval

## Purpose

## Boundary

## Contract

## Expected Behavior

## Evaluation Surface

## Observability

## Unknowns

## Evidence
```

6. Present the component understanding to the user and apply corrections.
7. After explicit approval, change:

```text
Status: Pending approval
```

to:

```text
Status: Approved
```

## Boundary

`Evaluation Surface` identifies behavior that may be worth evaluating. It does not define evaluation criteria.

Do not design criteria, metrics, datasets, graders, or evaluation implementation.
