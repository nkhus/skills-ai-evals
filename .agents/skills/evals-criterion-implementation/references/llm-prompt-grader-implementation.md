# LLM prompt grader implementation

## Default architecture

An LLM-based criterion uses:

```text
one criterion-specific Python definition module
+ one shared generic PromptGrader runtime
+ one judge call per dataset record
```

The criterion-specific Python module contains together:

- criterion metadata;
- one focused prompt;
- one Pydantic judge-response schema;
- prompt-variable mapping;
- conversion from the criterion response schema to the shared Grade contract;
- one exported definition object.

## Criterion module path

```text
evals/components/{component}/graders/{criterion_id}.py
```

The module should expose exactly one conventional entry point:

```python
definition
```

## Definition contract

A definition provides:

```text
criterion
version
prompt_template
response_model
build_variables(record, artifact)
to_grade(result)
```

Use `templates/llm-grader-definition.py` as the target shape.

## Prompt rules

The prompt must:

- evaluate exactly one criterion;
- state the evaluation question;
- define what is out of scope;
- provide explicit scoring semantics;
- include only documented variables;
- instruct the judge to return the Pydantic-defined structured response;
- request concise rationale and concrete evidence;
- avoid requesting hidden chain-of-thought;
- define how malformed or absent component output should be treated when relevant.

Do not add adjacent dimensions such as correctness, completeness, tone, grounding, or safety unless they are part of the approved criterion.

## Pydantic response schema

The schema represents the judge's criterion-specific response, not the shared framework Grade.

Use it to validate:

- score range;
- allowed labels;
- required rationale;
- evidence shape;
- optional criterion-specific details such as covered or missing items.

Prompt and schema form one versioned contract. Increment the definition version when either changes semantically.

## Generic PromptGrader

The shared runtime should live in a repository-appropriate shared path, commonly:

```text
evals/shared/graders/prompt_grader.py
```

It is responsible for:

- rendering the definition's prompt;
- invoking a structured-output LLM client;
- validating the Pydantic response;
- converting the result through `to_grade`;
- mapping timeout, parse, and infrastructure failures to `grader_error`;
- recording the criterion and grader version.

It must be generic over the response model.

## Dependency injection

The shared runtime receives infrastructure dependencies externally, such as:

- structured LLM client;
- prompt renderer;
- retry policy;
- model selection or configuration resolver;
- telemetry/tracing;
- logger;
- timeout policy.

Criterion-specific modules must not instantiate provider SDK clients or read provider secrets.

Use `templates/prompt-grader-runtime.py` as the target contract when no compatible shared runtime exists.

## Existing runtime

Search before creating the runtime.

- Reuse a compatible existing implementation.
- Do not create a second generic runtime under another path.
- Do not overwrite an incompatible runtime silently.
- If required capabilities are missing, report the incompatibility for a framework-level decision.

## One-call rule

A normal LLM criterion performs one judge call per record.

Do not implement:

- multi-agent judging;
- separate analysis and scoring calls;
- claim extraction followed by judging;
- majority vote;
- self-consistency loops;
- pairwise tournaments;
- chain-of-thought persistence.

These require an explicit approved grader design.
