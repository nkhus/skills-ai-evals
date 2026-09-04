---
name: evals-criterion-implementation
description: Implement one approved evaluation criterion as a grader, reusing shared framework code and metrics, without changing evaluation semantics.
user-invocable: false
---

# Evals Criterion Implementation

## Purpose

Consume one approved criterion specification and implement it without changing semantic evaluation decisions.

## Input

```text
Component: {component}
Criterion: {criterion_id}
```

## Requires

```text
evals/components/{component}/spec/{criterion_id}.md
```

Require the criterion spec `Status: Approved`.

## Workflow

Follow these steps and read references docs only when needed.

1. Read the approved criterion spec: grader contract, metrics, dataset contract, and required observability.
2. Ensure the bundled framework is available at `evals/framework/`:
   - create missing framework files from `code/framework/`;
   - preserve compatible existing implementations;
   - do not silently overwrite incompatible existing framework code.
3. Read `references/grader-implementation.md`. If the approved grader `type` is `llm`, also read `references/llm-grader-implementation.md`.
4. Implement the grader at:

```text
evals/components/{component}/graders/{criterion_id}.py
```

5. Select the approved shared metric(s) from `evals.framework.metrics`. Implement a criterion-specific metric only when the approved metric design cannot be represented by the shared metrics package, at:

```text
evals/components/{component}/metrics/{criterion_id}.py
```

If a required generic metric is genuinely missing from the shared package (identified during criterion design), add it to `evals/framework/metrics/` instead of encoding criterion semantics into a metric function.

6. Read `references/implementation-validation.md` and add minimal smoke tests to the repository's global test tree.
7. Run the repository's relevant test command and confirm it passes.

## Bundled framework

```text
code/framework/
├── __init__.py
├── models.py     # TestCase, ExecutionArtifact, Grade, GradeRecord, ExecutionRecord, MetricResult
├── grading.py    # Grader base class
├── llm.py        # LLMClient base class
└── metrics/
    ├── __init__.py
    ├── numeric.py        # mean, median, label_rate, status_rate
    └── classification.py # accuracy, precision, recall, f1
```

This code is the authoritative executable contract. Do not restate its models, base classes, or metric signatures in prose.

## Boundary

Do not:

- change criterion, grader, or metric semantics decided during criterion design;
- generate the full evaluation dataset (concrete case authoring is a separate stage);
- implement the component executor or run components;
- implement inference/grading/metric execution orchestration or persistence;
- calibrate the LLM judge;
- define release thresholds or acceptance policy;
- perform component integration;
- create an implementation-handoff artifact — downstream stages rely on the uniform framework contracts and deterministic repository layout instead.

Validation smoke tests are implementation tests, not the evaluation dataset.
