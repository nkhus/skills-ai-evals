---
name: evals-criterion-implementation
description: Implement one approved evaluation criterion, including executable dataset groups, a code-based grader or single-prompt Pydantic LLM grader, validation fixtures, and a machine-readable implementation handoff. Use after evals-criterion-design has produced the criterion specification, dataset contract, and grader design.
user-invocable: false
---

# Evals criterion implementation

Implement exactly one criterion for one component.

The invocation supplies:

```text
Component: <component_name>
Criterion: <criterion_id>
```

Do not rely on conversation history. Read the approved repository artifacts directly.

## Required inputs

Resolve and read:

```text
evals/config.yaml
evals/components/{component}/README.md
evals/components/{component}/spec/criteria.yaml
evals/components/{component}/spec/{criterion_id}.md
evals/components/{component}/datasets/{criterion_id}/README.md
evals/components/{component}/graders/{criterion_id}.md
```

The criterion must be present in `spec/criteria.yaml`.

Treat these design artifacts as authoritative:

- `spec/{criterion_id}.md` — semantic and measurement contract;
- `datasets/{criterion_id}/README.md` — dataset record and coverage contract;
- `graders/{criterion_id}.md` — grader behavior contract.

If they conflict materially, stop with `NEEDS_USER_INPUT`. Do not silently choose one interpretation.

## Read supporting guidance

Before implementation, read:

- `references/implementation-flow.md`
- `references/dataset-implementation.md`
- either `references/code-grader-implementation.md` or `references/llm-prompt-grader-implementation.md`
- `references/grader-validation.md`
- `references/output-contract.md`

Use the templates only as target shapes. Follow the repository's existing language, module layout, imports, typing, formatting, and shared contracts when they differ cosmetically.

## Workflow

1. Resolve the component and criterion.
2. Load the approved design artifacts.
3. Inspect the repository's eval framework, shared Grade contract, dataset loader, import conventions, and dependency-injection patterns.
4. Determine the approved grader family.
5. Implement only the declared dataset groups.
6. Implement the grader:
   - code-based criterion: criterion-specific grader code;
   - LLM-based criterion: one criterion-specific Python definition module plus the shared generic PromptGrader runtime;
   - hybrid criterion: only when explicitly approved by the grader design.
7. Create grader validation fixtures.
8. Run available structural, import, schema, and fixture validation without running the component or paid/production evaluations.
9. Create the implementation handoff only after implementation validation succeeds.

## Dataset record invariant

Every executable dataset record must have exactly these top-level fields:

```json
{
  "id": "stable-record-id",
  "input": {},
  "expected": {}
}
```

Do not add top-level `metadata`, `tags`, `context`, or annotations.

## LLM grader invariant

The default LLM grader architecture is:

```text
one criterion
+ one focused prompt
+ one Pydantic response schema
+ one judge call
+ one structured Grade
```

The criterion-specific module keeps the prompt and Pydantic schema together. It exposes one definition object consumed by a shared generic `PromptGrader`.

The shared runtime receives provider and infrastructure dependencies through injection. Criterion modules must not instantiate provider clients, loggers, telemetry, retry policies, renderers, or model SDKs.

Do not create multi-call, agentic, claim-extraction, chain-of-thought, or composite LLM graders unless the approved grader design explicitly requires one.

## Shared PromptGrader handling

For an LLM-based criterion:

1. Search for an existing compatible generic prompt grader.
2. Reuse it when compatible.
3. If absent, create a shared runtime using `templates/prompt-grader-runtime.py` as the target contract.
4. If an existing runtime is materially incompatible with the approved criterion design, stop and report the incompatibility rather than replacing it.

Do not duplicate the generic runtime per criterion.

## Completion outputs

Create the criterion-specific files required by `references/output-contract.md`.

The completion artifact is:

```text
evals/components/{component}/implementations/{criterion_id}.yaml
```

Write it only after the implementation and local validation are complete.

## Boundaries

Do not:

- alter the approved criterion list;
- redefine score semantics;
- implement another criterion;
- implement or modify the shared component runner;
- create or update the final component manifest;
- register suites or policies;
- add release thresholds;
- execute the component across the evaluation dataset;
- report infrastructure failures as quality score zero;
- invent unverifiable domain truth for dataset expectations.

## Result statuses

Return one of:

```text
COMPLETE
Component: <component>
Criterion: <criterion_id>
Produced:
- <paths>
```

```text
NEEDS_USER_INPUT
Component: <component>
Criterion: <criterion_id>
Question: <one focused question>
```

```text
BLOCKED
Component: <component>
Criterion: <criterion_id>
Missing or incompatible:
- <prerequisite or contract>
```
