# Output contract

## Prerequisites

Required:

```text
evals/config.yaml
evals/components/{component}/README.md
evals/components/{component}/spec/criteria.yaml
evals/components/{component}/spec/{criterion_id}.md
evals/components/{component}/datasets/{criterion_id}/README.md
evals/components/{component}/graders/{criterion_id}.md
```

## Dataset outputs

Create each approved executable group:

```text
evals/components/{component}/datasets/{criterion_id}/{group}.jsonl
```

## Grader output

For a code-based criterion:

```text
evals/components/{component}/graders/{criterion_id}.py
```

For an LLM-based criterion:

```text
evals/components/{component}/graders/{criterion_id}.py
```

The same module path is used, but the module contains the prompt, Pydantic response schema, mapping, conversion, and exported definition object rather than a provider-specific runtime.

When absent and required, create one shared generic runtime at the repository's shared grader location, commonly:

```text
evals/shared/graders/prompt_grader.py
```

## Validation fixtures

```text
evals/components/{component}/grader-validation/{criterion_id}.jsonl
```

## Completion artifact

```text
evals/components/{component}/implementations/{criterion_id}.yaml
```

It must declare:

- component and criterion;
- implementation version;
- dataset group paths;
- grader family;
- grader implementation or definition import path;
- shared runtime import path for LLM graders;
- required execution-artifact fields;
- grader configuration;
- validation fixture path;
- commands or checks run and truthful status.

Use `templates/criterion-implementation.yaml` as the target shape.

## Completion semantics

Write the completion artifact only when:

- all declared dataset files exist and validate structurally;
- the grader implementation imports;
- the criterion identity matches the approved list;
- validation fixtures exist;
- available non-production validation has completed without known failures.

The presence of the completion artifact tells the orchestrator that criterion implementation is complete. The orchestrator does not inspect artifact quality.

## Out of scope outputs

Do not create or edit:

```text
evals/components/{component}/runner/
evals/components/{component}/manifest.yaml
evals/suites/
evals/policies/
```
