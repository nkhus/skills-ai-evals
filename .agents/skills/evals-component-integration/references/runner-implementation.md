# Runner Implementation

## Goal

Create one component runner that executes the real component and produces an immutable execution artifact sufficient for all approved criterion graders.

## Location

```text
evals/components/{component}/runner/component.py
```

Follow the repository's Python package structure, naming, async conventions, and dependency-injection patterns.

## Input contract

The runner receives a complete dataset record:

```json
{
  "id": "stable-record-id",
  "input": {},
  "expected": {}
}
```

Execution may use only:

```text
record.id
record.input
```

The runner must not inspect `record.expected`. Expected data belongs exclusively to graders.

## Dependency injection

Do not instantiate provider or production dependencies inside the runner.

Avoid:

```python
client = ProviderClient(...)
database = Database(...)
```

Prefer constructor injection or a repository-defined factory:

```python
runner = ComponentRunner(component=runtime.components.retriever)
```

The manifest may reference both the runner implementation and a factory responsible for assembling dependencies.

## Execution artifact

Use a stable top-level shape unless the repository already defines an equivalent contract:

```json
{
  "record_id": "record-id",
  "output": {},
  "trace": {},
  "usage": {},
  "errors": [],
  "system": {}
}
```

### `record_id`

Must match the dataset record ID.

### `output`

Contains normalized component results used by graders.

### `trace`

Contains observable intermediate decisions required by graders, such as applied filters, tool calls, normalized queries, selected routes, or retrieved candidates.

Do not fabricate hidden reasoning or private chain-of-thought.

### `usage`

May contain observable execution measurements such as latency or token counts. These are operational measurements, not criterion scores.

### `errors`

Contains normalized component execution errors. Do not convert component failures into empty successful output.

### `system`

Contains relevant component and configuration identifiers needed for reproducibility.

## Required field union

Read `required_artifact_fields` from every criterion implementation handoff.

Produce the union using one execution whenever possible.

Example:

```text
retrieval_coverage:
  output.documents[].id

ranking_quality:
  output.documents[].id
  output.documents[].rank
  output.documents[].score

filter_adherence:
  trace.applied_filters
```

Unified runner requirement:

```text
output.documents[].id
output.documents[].rank
output.documents[].score
trace.applied_filters
```

## Error handling

Convert component exceptions into artifact errors using stable fields:

```json
{
  "type": "TimeoutError",
  "message": "Component execution timed out"
}
```

Do not include secrets, credentials, private headers, or full sensitive payloads in errors or trace.

## Single execution principle

Run the component once per record and reuse the resulting artifact for all criterion graders.

Do not execute the component separately for each criterion unless the component contract genuinely requires criterion-specific execution and that requirement is explicitly approved.

## Runner boundaries

The runner must not:

- select or invoke graders;
- calculate scores;
- apply suite or policy thresholds;
- invoke judge models;
- mutate dataset records;
- read expected answers;
- hide execution failures;
- add criterion-specific semantics not represented in the component output.

## Validation

Validate that:

- the runner imports;
- its construction path is resolvable;
- it returns the documented top-level artifact fields;
- required nested artifact fields are present for representative fixture outputs;
- it does not access `expected`;
- exceptions become artifact errors;
- dependencies are injected rather than created from credentials inside the runner.
