# Integration Validation

## Principle

Validate that the assembled eval is structurally runnable without requiring a full evaluation run.

Prefer repository-native validation commands and existing framework contracts. Add small local checks only when the repository has no equivalent.

## Prerequisite validation

Confirm:

- root eval config exists;
- component analysis exists;
- approved criteria list exists;
- every approved criterion has design artifacts;
- every approved criterion has an implementation handoff;
- all paths declared by handoffs exist.

## YAML validation

Parse:

- `evals/config.yaml`;
- `spec/criteria.yaml`;
- every implementation handoff;
- `manifest.draft.yaml`;
- any modified suite file.

Confirm criterion IDs are unique and consistent across files.

## Dataset validation

For every declared JSONL file:

- parse every non-empty line as JSON;
- require top-level keys exactly `id`, `input`, and `expected`, unless the approved framework contract explicitly allows otherwise;
- require non-empty string IDs;
- require `input` and `expected` objects;
- ensure record IDs are unique across all groups for the criterion;
- reject placeholder-only records;
- confirm every dataset group declared in the handoff is represented in the manifest.

Do not reinterpret domain expectations during integration.

## Import validation

Resolve and import:

- component runner implementation;
- runner factory when declared;
- every code grader;
- every LLM criterion definition;
- Pydantic response schemas;
- shared generic prompt grader runtime.

Use repository package/import conventions. Do not mutate production import paths merely to make isolated ad hoc commands succeed.

## Grader fixture validation

For code graders, run declared grader-validation fixtures and compare expected status and score constraints.

For LLM prompt graders, validate without requiring a live judge call:

- definition object exports correctly;
- prompt template renders with fixture variables;
- Pydantic response model validates representative responses;
- result-to-grade conversion works;
- malformed judge responses map to grader errors through the generic runtime;
- required record and artifact fields are documented.

A live judge calibration run is outside this integration stage unless explicitly requested.

## Runner validation

Confirm the runner:

- accepts dataset records;
- uses `input` and not `expected` for execution;
- returns `record_id`, `output`, `trace`, `usage`, `errors`, and `system`, or the repository-approved equivalent;
- produces every required artifact field for representative fixture output;
- converts execution exceptions into artifact errors;
- does not invoke graders or judge models;
- receives external dependencies through injection or a factory.

Static search for `expected` access is useful but not sufficient; inspect the execution path.

## Manifest validation

Confirm:

- component name and runner references are present;
- every approved criterion is present exactly once;
- no unapproved behavioral criterion is present;
- every spec path exists;
- every dataset path exists;
- default dataset groups exist;
- grader family matches the implementation handoff;
- grader references and versions match handoffs;
- LLM criteria declare both generic runtime and criterion definition;
- code criteria declare their grader implementation;
- no release thresholds are embedded unless the repository explicitly defines them as part of manifest schema.

## Registration validation

Confirm:

- root config points to the final component manifest path;
- unrelated component registrations remain unchanged;
- local suite changes reference valid components, priorities, and dataset groups;
- consequential suites were not modified without explicit approval.

## Reporting

Record each performed check and its result in `integration-report.md`.

Do not claim validation that was not actually executed.

## Publication gate

Publish `manifest.yaml` only when all required structural checks pass.

Warnings may remain for optional checks, but they must be listed in the report.
