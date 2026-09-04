# Implementation Validation Guide

Defines sufficient evidence for a criterion implementation to be considered complete.

Tests are implementation smoke tests. They do not establish dataset coverage, representativeness, balancing, statistical confidence, or LLM judge calibration.

## Smoke tests

Construct `TestCase` and `ExecutionArtifact` values directly in normal Python tests. Do not introduce a separate fixture-file abstraction unless the repository already needs one.

Test only implementation behavior needed by the approved contract. Typical cases when relevant:

```text
positive
negative
partial / boundary
not_applicable
error
```

## Code graders

Validate:

- grader imports and instantiates;
- expected `Grade` behavior for each relevant case;
- non-scored behavior;
- label/value semantics;
- `details`/`reasoning` when relevant.

## LLM graders

Use an injected fake/stub `LLMClient`. Do not require a real external judge call.

Validate:

- the prompt path executes;
- the criterion-specific Pydantic response model is accepted;
- response → `Grade` mapping;
- label → value mapping, if any;
- provider/runtime failure → `error`;
- `Grade.reasoning` is populated from the response model's `reasoning` field.

## Metrics

Reused shared metrics from `evals.framework.metrics` do not require new tests.

If the implementation adds a new generic metric to the shared framework package:

- add framework-level tests;
- validate the normal case;
- validate no usable scored data (`insufficient_data`);
- validate invalid scored data (`metric_error`);
- validate relevant edge cases (e.g. no positive-label observations for precision/recall).

If a criterion-specific custom metric is implemented, test it the same way the approved metric design specifies, using constructed `GradeRecord`/`TestCase` data.

## Location

Tests live in the repository's global project-level test tree, not inside `evals/components/{component}/`. The exact subpath follows existing repository test conventions.

## Completion

Run the repository's normal relevant test command. Implementation is complete when it passes and covers the cases above that are relevant to the approved design.
