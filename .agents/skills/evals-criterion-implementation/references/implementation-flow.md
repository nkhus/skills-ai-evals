# Implementation flow

## Goal

Turn the approved design of one criterion into executable datasets and a grader without changing the criterion's meaning.

## Repository inspection

Before writing files, identify:

- the shared `Grade` and execution-artifact contracts;
- how objects are imported from manifest-style paths;
- the repository's Python package roots;
- async conventions;
- Pydantic version and style;
- dependency-injection approach;
- dataset loading and validation conventions;
- lint, type-check, and validation commands;
- existing generic grader implementations.

Prefer adapting to existing compatible framework contracts over introducing parallel abstractions.

## Implementation order

1. Validate prerequisites and criterion identity.
2. Read all three approved design artifacts.
3. Identify the grader family and required artifact fields.
4. Implement dataset groups from the dataset contract.
5. Implement the grader.
6. Add validation fixtures for the grader contract.
7. Run non-production validation.
8. Write the implementation handoff.

## Design authority

The implementation must preserve:

- evaluation question;
- desired and undesired behavior;
- score range and direction;
- record-level scoring semantics;
- dataset-level metric semantics;
- required dataset fields;
- required artifact fields;
- grader family and pattern.

When implementation exposes a missing design decision, ask one focused question. Do not fill a consequential semantic gap with an arbitrary choice.

## Existing files

Preserve valid existing work.

- Update criterion-specific implementation files when the approved design requires it.
- Do not overwrite an existing shared generic runtime unless the user has explicitly approved a migration.
- When rerunning, keep stable record IDs where the scenario meaning has not changed.
- Remove obsolete criterion-specific files only when they conflict with the approved design and the change is evident.

## No component execution

This stage may run:

- imports;
- schema validation;
- grader fixture validation;
- formatting;
- linting;
- type checking;
- deterministic local calculations.

It must not run the component over the evaluation datasets or invoke the LLM judge for production grading.
