---
name: evals-criterion-design
description: Design one approved evaluation criterion into an implementation-ready grader, metrics, dataset contract, and observability requirements.
user-invocable: false
---

# Evals Criterion Design

## Purpose

Turn one approved criterion into a complete evaluation design without making implementation decisions.

Implementation should not need to invent semantic evaluation choices.

## Input

```text
Component: {component}
Criterion: {criterion_id}
```

## Requires

```text
evals/components/{component}/README.md
evals/components/{component}/spec/criteria.yaml
```

Require:

- component analysis `Status: Approved`;
- criteria `status: approved`;
- requested criterion exists in `criteria.yaml`.

## Workflow

1. Read the approved component analysis and requested criterion.
2. Preserve the approved criterion `id`, `intent`, and optional `boundary`.
3. Resolve only ambiguities that materially affect evaluation semantics. If the criterion itself must change, return to criteria discovery.
4. Read `references/grader-design.md` and design the case-level grader.
5. Read `references/metric-design.md` and select suitable generic pre-implemented metric(s) from grader outputs. If an appropriate established generic metric is missing, identify the required generic metric semantics for later addition to the shared framework instead of designing a criterion-specific formula.
6. Read `references/dataset-design.md` and define the test-case contract, coverage, and authoring guidance.
7. Derive required observability from the grader execution inputs. Require observable facts only; never hidden reasoning.
8. Create or update:

```text
evals/components/{component}/spec/{criterion_id}.md
```

using:

```markdown
# {Criterion}

Status: Pending approval

## Intent

## Grader

## Metrics

## Dataset

## Required Observability

## Limitations
```

Omit `Limitations` when none are material.

9. Present the complete design to the user and apply corrections.
10. After explicit approval, change:

```text
Status: Pending approval
```

to:

```text
Status: Approved
```

## Boundary

Do not:

- change the approved component analysis or criterion definition;
- design more than one criterion;
- create concrete dataset records;
- implement or execute evaluations;
- make judge-model, provider/runtime, or execution-policy decisions;
- define release or acceptance policy.

The design is complete only when downstream stages do not need to invent semantic evaluation choices: what is judged, what grader outputs mean, which generic metrics aggregate them, what cases must represent, or what execution evidence is required.

Different downstream stages consume different parts of the design:

```text
criterion implementation
→ grader + generic metric support

dataset authoring
→ concrete evaluation cases

future runtime
→ execution / persistence / orchestration
```
