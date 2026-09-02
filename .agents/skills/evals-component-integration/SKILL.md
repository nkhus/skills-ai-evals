---
name: evals-component-integration
description: Integrates all completed criterion implementations for one component into a runnable component evaluation. Use after criteria discovery, criterion design, and criterion implementation are complete for every approved criterion.
user-invocable: false
---

# Evals Component Integration

Integrate one component at a time.

The caller supplies:

```text
Component: {component}
```

Do not require the caller to summarize earlier decisions. Read repository artifacts directly.

## Goal

Create the shared execution layer and registration artifacts that connect all independently implemented criteria for the component.

The stage owns:

- collecting all criterion implementation handoffs;
- deriving the union of required execution artifact fields;
- implementing one component runner;
- creating the component manifest;
- registering the component in root eval configuration;
- optionally adding baseline execution to an existing local suite;
- validating imports, paths, datasets, grader fixtures, and runner contracts;
- producing an integration report.

The stage does not own:

- component analysis;
- criteria discovery;
- criterion semantic or metric design;
- dataset authoring beyond fixing purely mechanical integration errors;
- criterion grader implementation;
- release thresholds;
- full eval execution;
- judge-model calls.

## Required reading

Read these skill resources before editing files:

1. `references/integration-flow.md`
2. `references/runner-implementation.md`
3. `references/manifest-and-registration.md`
4. `references/integration-validation.md`
5. `references/output-contract.md`

Use the templates in `templates/` as structural targets, adapting them to repository conventions rather than copying them blindly.

## Prerequisites

Require:

```text
evals/config.yaml
evals/components/{component}/README.md
evals/components/{component}/spec/criteria.yaml
```

For every criterion listed in `spec/criteria.yaml`, require:

```text
evals/components/{component}/spec/{criterion_id}.md
evals/components/{component}/datasets/{criterion_id}/README.md
evals/components/{component}/graders/{criterion_id}.md
evals/components/{component}/implementations/{criterion_id}.yaml
```

For LLM prompt graders, also require the shared generic runtime declared by the implementation handoff. The normal expected path is:

```text
evals/shared/graders/prompt_grader.py
```

If a prerequisite is missing, stop with `BLOCKED`. Do not recreate earlier-stage work.

## Workflow

### 1. Resolve the component

Confirm the component name from the task. Locate its component directory and approved criteria list.

### 2. Load the approved criterion list

Read `spec/criteria.yaml`. Preserve its criterion IDs, groups, priorities, names, and intent. Do not add, remove, rename, merge, or reinterpret criteria.

### 3. Load every criterion implementation handoff

Read `implementations/{criterion_id}.yaml` for each approved criterion.

Confirm that each handoff identifies:

- datasets by named group;
- grader family and implementation or definition reference;
- grader version;
- required execution artifact fields;
- validation fixtures and status.

Treat these handoffs as the integration source of truth.

### 4. Build the unified runner contract

Compute the union of all `required_artifact_fields`.

Map every required field to observable data available from the real component. Inspect the component code, factories, dependencies, and repository conventions as needed.

If a required field cannot be produced without changing criterion semantics or production behavior, stop with `NEEDS_USER_INPUT`.

### 5. Implement the component runner

Create or update:

```text
evals/components/{component}/runner/component.py
```

Follow `references/runner-implementation.md`.

The runner must:

- accept a dataset record;
- use only `record["input"]` for component execution;
- receive component dependencies through injection or a repository factory;
- invoke the component once per record;
- normalize output and trace fields required by graders;
- capture execution errors as artifact data;
- never grade;
- never read `record["expected"]`.

### 6. Create a draft manifest

Create:

```text
evals/components/{component}/manifest.draft.yaml
```

Generate it from:

- `spec/criteria.yaml`;
- every `implementations/{criterion_id}.yaml`;
- the runner implementation and factory.

Do not invent dataset paths, grader references, or versions.

### 7. Register the component non-destructively

Update `evals/config.yaml` to reference the component manifest while preserving unrelated configuration.

When an existing local suite is clearly intended for lightweight baseline execution, add the component without replacing existing selections. Do not automatically modify pull-request, release, production, or similarly consequential suites.

### 8. Validate integration

Follow `references/integration-validation.md`.

Use repository-native checks where available. At minimum validate:

- YAML and JSONL syntax;
- unique criterion and record IDs;
- importability of the runner and graders;
- LLM definition and Pydantic schema importability;
- generic prompt grader availability for LLM criteria;
- manifest references and dataset paths;
- grader validation fixtures;
- prompt rendering and grade conversion without a required live judge call;
- runner contract and prohibition on using `expected`;
- preservation of existing root configuration.

Do not run full evaluation datasets unless explicitly requested.

### 9. Publish final artifacts

After required validation succeeds:

1. write `integration-report.md`;
2. publish `manifest.yaml` from the validated draft;
3. remove `manifest.draft.yaml` when safe and consistent with repository conventions.

If an incompatible final manifest already exists, keep the draft and ask the user before replacing it.

## Completion

Completion artifact:

```text
evals/components/{component}/manifest.yaml
```

Return:

```text
COMPLETE

Component: {component}

Produced:
- evals/components/{component}/runner/component.py
- evals/components/{component}/manifest.yaml
- evals/components/{component}/integration-report.md

Updated:
- evals/config.yaml
- evals/suites/local.yaml  # only when applicable
```

## Blocking states

Use `BLOCKED` when prerequisite artifacts or shared framework contracts are missing.

Use `NEEDS_USER_INPUT` when:

- required grader observations cannot be exposed by the component;
- implementation handoffs conflict;
- an existing manifest is incompatible;
- registration would require a consequential suite-policy decision;
- resolving the issue would change an approved criterion design.

Never silently redesign upstream artifacts.
