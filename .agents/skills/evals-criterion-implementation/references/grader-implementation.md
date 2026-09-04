# Grader Implementation Guide

Common implementation rules for all graders. Applies to both `code` and `llm` graders.

Do not repeat grader-design theory such as choosing `code` vs `llm`, inventing labels, or redefining applicability. Those decisions are upstream, in the approved criterion spec.

## Contract

```text
one criterion × one TestCase × one ExecutionArtifact
```

Implement `evals.framework.Grader`:

```python
class Grader(ABC):
    @abstractmethod
    async def grade(
        self,
        case: TestCase,
        artifact: ExecutionArtifact,
    ) -> Grade:
        ...
```

All graders are asynchronous, including deterministic graders.

## Allowed semantic inputs

```text
case.input
case.expected
artifact.output
artifact.trace
artifact.errors
```

- `case.metadata` must not define grading semantics;
- `artifact.metadata` must not define grading semantics.

## Status and value invariants

- for `status: scored`, set `label`, `value`, or both;
- non-scored statuses (`not_applicable`, `error`) must not set `label` or `value`;
- never convert a non-scored status into a quality score of `0`;
- `reasoning` is a concise grader justification, not hidden chain-of-thought;
- `details` holds structured evidence (expected vs observed values, matched/missing items, violated constraints).

## Component failure

A component failure may still be graded when that failure is observable behavior relevant to the approved criterion.

## Boundary

A grader implementation must not:

- aggregate across executions or cases;
- run the component;
- calculate dataset-level metrics;
- persist records;
- require criterion ID, grader version, case/execution IDs, model, timestamps, or run metadata in its interface.

## Location

```text
evals/components/{component}/graders/{criterion_id}.py
```

One criterion produces one grader implementation.
