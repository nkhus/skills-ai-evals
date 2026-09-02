# Output Contract

## Invocation inputs

The orchestrator supplies:

- component name;
- criterion ID.

No conversation summary or previous-stage content is required.

## Required repository inputs

The stage requires:

```text
evals/config.yaml
evals/components/{component}/README.md
evals/components/{component}/spec/criteria.yaml
```

The requested criterion ID must exist in `criteria.yaml`.

If a prerequisite is absent, return `BLOCKED` with the missing path or ID. Do
not create the missing artifact.

## Working draft

During discussion, maintain:

```text
evals/components/{component}/criterion-design.{criterion_id}.draft.md
```

The draft may include unresolved alternatives and user decisions. It is not a
completion artifact.

Use `templates/criterion-design-draft.md`.

## Final artifacts

After explicit user approval, create exactly these design artifacts:

```text
evals/components/{component}/spec/{criterion_id}.md
evals/components/{component}/datasets/{criterion_id}/README.md
evals/components/{component}/graders/{criterion_id}.md
```

Use:

- `templates/criterion-spec.md`;
- `templates/dataset-readme.md`;
- `templates/grader-design.md`.

The three artifacts must agree on:

- criterion ID and name;
- evaluation question;
- metric semantics;
- dataset field names;
- required execution-artifact fields;
- grader inputs and outputs;
- not-applicable and invalid-data behavior.

## Completion semantics

The stage is complete only when:

- the user explicitly approved the complete design;
- all three final artifacts exist.

A partial set is incomplete.

Return:

```text
COMPLETE

Component: {component}
Criterion: {criterion_id}

Produced:
- evals/components/{component}/spec/{criterion_id}.md
- evals/components/{component}/datasets/{criterion_id}/README.md
- evals/components/{component}/graders/{criterion_id}.md
```

## User-input result

When a material decision is required, continue the stage conversation and ask
one focused question. When an explicit status is useful, use:

```text
NEEDS_USER_INPUT

Component: {component}
Criterion: {criterion_id}

Question:
{one focused question}
```

Do not write final artifacts before complete approval.

## Blocked result

Use:

```text
BLOCKED

Component: {component}
Criterion: {criterion_id}

Missing or invalid prerequisite:
- {path or criterion ID}
```

## Invalid criterion discovery

If detailed work reveals that the criterion:

- duplicates another criterion;
- combines unrelated quality dimensions;
- belongs to another component;
- cannot be evaluated from observable behavior;
- materially differs from the approved intent;

stop and recommend returning to `evals-criteria-discovery`.

Do not edit `spec/criteria.yaml` yourself.

## Superseding a draft

After writing final artifacts, either delete the working draft or add a clear
header stating:

```text
Superseded by the approved final artifacts on {date}.
```

## Files not produced by this stage

Do not create:

- executable JSONL datasets;
- Python or other grader code;
- runner implementation;
- component manifest;
- root config registration;
- suite or policy changes;
- run artifacts or reports.
