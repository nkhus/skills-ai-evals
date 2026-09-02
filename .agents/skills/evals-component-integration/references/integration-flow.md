# Integration Flow

## Purpose

The integration stage assembles independently implemented criteria into one executable component evaluation.

It is a composition stage, not a quality-design stage.

## Inputs

The authoritative inputs are:

```text
component README
criteria.yaml
criterion specification files
criterion dataset contracts
criterion grader design files
criterion implementation handoffs
implemented dataset and grader files
root eval configuration
```

The implementation handoff for each criterion is the primary machine-readable integration input.

## Sequence

1. Load the approved criteria list.
2. Confirm that every approved criterion has an implementation handoff.
3. Read dataset groups and grader references from each handoff.
4. Collect each criterion's required execution artifact fields.
5. Resolve a shared runner contract.
6. Implement the runner using repository conventions and dependency injection.
7. Assemble a draft manifest.
8. Register the component in root configuration.
9. Optionally update an existing local suite.
10. Run structural and fixture validation.
11. Write an integration report.
12. Publish the final manifest.

## Source-of-truth hierarchy

Use this precedence when artifacts overlap:

1. Approved criterion specification for semantic meaning.
2. Criterion implementation handoff for executable paths and versions.
3. Existing implementation files for actual import targets.
4. Root configuration and suite files for registration conventions.

Do not infer a different criterion meaning from implementation details.

## Completeness rule

Every criterion in `spec/criteria.yaml` must be represented in the final manifest.

The final manifest must not contain a behavioral criterion absent from `spec/criteria.yaml`.

Validation checks and operational measurements must remain outside the manifest's behavioral `criteria` map unless the repository has an explicit separate section for them.

## Conflict handling

Stop rather than guessing when:

- two implementation handoffs use the same criterion ID inconsistently;
- a dataset path is declared but missing;
- a grader import target does not exist;
- an LLM criterion lacks the shared generic prompt grader;
- two criteria require incompatible representations of the same artifact field;
- an approved grader needs data that the component cannot expose;
- existing root registration points the component name to another manifest.

State the conflict and the smallest upstream decision required to resolve it.

## Idempotency

A repeated integration run should converge on the same result when inputs have not changed.

Preserve unrelated files and configuration entries. Avoid reformatting whole YAML files when only one mapping entry changes.

## No full eval execution

Structural integration does not require running every dataset record. The stage may run:

- syntax checks;
- import checks;
- fixture-based grader checks;
- prompt rendering checks;
- runner smoke checks using local fixtures or repository-provided fakes.

Do not invoke external judge models or production dependencies by default.
