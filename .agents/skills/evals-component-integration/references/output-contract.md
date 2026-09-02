# Output Contract

## Required final artifacts

```text
evals/components/{component}/runner/component.py
evals/components/{component}/manifest.yaml
evals/components/{component}/integration-report.md
```

## Required configuration update

```text
evals/config.yaml
```

## Optional configuration update

```text
evals/suites/local.yaml
```

Update the local suite only when it exists and its established purpose matches lightweight baseline component evaluation.

## Working artifact

```text
evals/components/{component}/manifest.draft.yaml
```

A draft does not mark the pipeline complete.

## Completion artifact

```text
evals/components/{component}/manifest.yaml
```

The orchestrator may treat its existence as integration completion.

## Integration report contents

The report must identify:

- integrated criteria;
- dataset groups;
- grader families and import targets;
- shared prompt grader usage;
- runner implementation and factory;
- unified required artifact fields;
- root config changes;
- suite changes;
- validation commands or checks actually performed;
- validation results;
- unresolved warnings and limitations.

## Result statuses

### Complete

```text
COMPLETE

Component: {component}

Produced:
- evals/components/{component}/runner/component.py
- evals/components/{component}/manifest.yaml
- evals/components/{component}/integration-report.md

Updated:
- evals/config.yaml
```

Include `evals/suites/local.yaml` only when actually updated.

### Blocked

Use when required prerequisites are absent:

```text
BLOCKED

Component: {component}

Missing:
- evals/components/{component}/implementations/{criterion_id}.yaml
```

### Needs user input

Use when a decision is required:

```text
NEEDS_USER_INPUT

Component: {component}

Question:
The grader requires raw candidate scores, but the component exposes only ordered IDs. Should observability be extended, the grader design be revised, or the criterion be deferred?
```

## Non-goals

This stage must not produce:

- new criterion definitions;
- rewritten criterion metrics;
- new domain expectations;
- full evaluation reports;
- release decisions;
- judge-model calibration results unless explicitly requested.
